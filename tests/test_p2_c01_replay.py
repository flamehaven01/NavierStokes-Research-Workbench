"""C01 runner controls; tests never establish the C01 Lean proposition."""

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

RUNNER = Path(__file__).resolve().parents[1] / "scripts/run-p2-c01-replay.py"
SPEC = importlib.util.spec_from_file_location("p2_c01_replay", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class C01ReplayControls(unittest.TestCase):
    def synthetic_replay(self, root, *, fail_stage=None, stderr_stage=None):
        """Mock commands test admission behavior, not any Lean proposition."""
        source, nsrw, output = root / "source", root / "nsrw", root / "run"
        source.mkdir()
        (nsrw / "scripts").mkdir(parents=True)
        (nsrw / "formal/p2").mkdir(parents=True)
        shutil.copyfile(RUNNER, nsrw / runner.RUNNER)
        for _, module, _, _ in runner.MODULES:
            shutil.copyfile(RUNNER.parent.parent / "formal/p2" / (module + ".lean"),
                            nsrw / "formal/p2" / (module + ".lean"))
        (source / "lean-toolchain").write_text(runner.TOOLCHAIN + "\n")
        (source / "lake-manifest.json").write_text('{"packages": []}')
        target = source / ".lake/build/lib/lean/NavierStokes/OutgoingPulseBounds.olean"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"synthetic source cache")
        commit = "a" * 40

        def query(checkout, args, env):
            if args == ["git", "rev-parse", "HEAD"]:
                return runner.SOURCE_COMMIT if checkout == source else commit
            if args[0:2] == ["git", "status"]:
                return ""
            if args == ["lean", "--version"]:
                return "Lean (version 4.34.0-rc2, commit " + runner.LEAN_COMMIT + ")"
            if args == ["lake", "--version"]:
                return "Lake (Lean version 4.34.0-rc2)"
            raise AssertionError(args)

        def committed(checkout, relative, env):
            return {"raw_sha256": runner.digest(checkout / relative),
                    "git_blob_sha1": runner.MANIFEST_BLOB if relative == "lake-manifest.json"
                    else "b" * 40}

        def command(args, **kwargs):
            stage = "source"
            if args[:3] == ["lake", "env", "lean"]:
                module = Path(args[-1]).stem
                stage, _, _, names = next(row for row in runner.MODULES if row[1] == module)
                Path(args[args.index("-o") + 1]).write_bytes(b"synthetic " + stage.encode())
                kwargs["stdout"].write("\n".join(
                    f"'NSRW.P2.{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
                    for name in names).encode())
            if stage == stderr_stage:
                kwargs["stderr"].write(b"synthetic diagnostic requires review")
            return subprocess.CompletedProcess(args, 1 if stage == fail_stage else 0)

        with ExitStack() as stack:
            stack.enter_context(patch.object(runner, "__file__", str(nsrw / runner.RUNNER)))
            stack.enter_context(patch.object(runner, "query", side_effect=query))
            stack.enter_context(patch.object(runner, "committed_input", side_effect=committed))
            stack.enter_context(patch.object(runner, "reject_shadow_inputs"))
            stack.enter_context(patch.object(runner.os, "sysconf", return_value=1, create=True))
            stack.enter_context(patch.object(runner.subprocess, "run", side_effect=command))
            runner.replay(source, nsrw, output, commit)
        return json.loads((output / "metadata.json").read_text())

    def test_successful_execution_never_self_promotes_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            m = self.synthetic_replay(Path(directory))
            self.assertEqual(m["check_status"], "PASS[COMMIT_BOUND_EXTERNAL_P2_C01_REPLAY]")
            self.assertEqual(m["claim_status"], "UNVERIFIED")
            self.assertEqual(len(m["fresh_artifacts"]), 5)
            self.assertEqual(len(m["axiom_surface"]), 12)

    def test_source_or_c01_nonzero_exit_never_admitted(self):
        for stage in ("source", "c01"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                with self.assertRaisesRegex(RuntimeError, "EXECUTION_FAILED: " + stage):
                    self.synthetic_replay(root, fail_stage=stage)
                m = json.loads((root / "run/metadata.json").read_text())
                self.assertEqual(m["check_status"], "ERROR[REPLAY_NOT_ADMITTED]")
                self.assertEqual(m["claim_status"], "UNVERIFIED")
                self.assertEqual(m["stages"][stage]["exit"], 1)

    def test_zero_exit_with_stderr_still_requires_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "STDERR_REQUIRES_REVIEW: c01"):
                self.synthetic_replay(root, stderr_stage="c01")
            m = json.loads((root / "run/metadata.json").read_text())
            self.assertEqual(m["check_status"], "ERROR[REPLAY_NOT_ADMITTED]")
            self.assertEqual(m["claim_status"], "UNVERIFIED")

    def test_module_order_and_real_bytes(self):
        self.assertEqual([row[0] for row in runner.MODULES], ["f1", "l2", "l3", "d", "c01"])
        self.assertEqual(sum(len(row[3]) for row in runner.MODULES), 12)
        for _, module, expected, _ in runner.MODULES:
            path = RUNNER.parent.parent / "formal/p2" / (module + ".lean")
            self.assertEqual(runner.digest(path), expected)

    def test_multiline_axiom_observations(self):
        names = runner.MODULES[-1][3]
        text = "\n".join(f"'NSRW.P2.{name}' depends on axioms: [propext,\n"
                         "Classical.choice,\nQuot.sound]" for name in names)
        self.assertEqual(len(runner.axiom_surface(text, names)), 3)

    def test_bad_axiom_observations_rejected(self):
        name = runner.MODULES[-1][3][-1]
        valid = f"'NSRW.P2.{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for text in ("", valid + valid, valid + "\nsorryAx",
                     valid.replace("Quot.sound", "NewAxiom"),
                     valid.replace("Quot.sound", "Quot.sound, Quot.sound"),
                     valid.replace("Classical.choice, ", "")):
            with self.subTest(text=text), self.assertRaises(RuntimeError):
                runner.axiom_surface(text, [name])

    def test_inherited_search_paths_never_used(self):
        env = {"LEAN_PATH": "old-olean", "LEAN_SRC_PATH": "shadow", "PATH": "unchanged"}
        actual = runner.proof_environment(env, Path("fresh-artifacts"))
        self.assertEqual(actual["LEAN_PATH"], "fresh-artifacts")
        self.assertNotIn("LEAN_SRC_PATH", actual)
        self.assertEqual(actual["PATH"], "unchanged")
        self.assertEqual(env["LEAN_PATH"], "old-olean")

    def test_fresh_dependency_tamper_or_removal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "F1.olean"
            path.write_bytes(b"fresh")
            expected = {path.name: runner.digest(path)}
            runner.unchanged_artifacts(root, expected)
            path.write_bytes(b"modified")
            with self.assertRaisesRegex(RuntimeError, "FRESH_ARTIFACT_CHANGED"):
                runner.unchanged_artifacts(root, expected)
            path.unlink()
            with self.assertRaisesRegex(RuntimeError, "FRESH_ARTIFACT_MISSING"):
                runner.unchanged_artifacts(root, expected)

    def test_existing_output_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_ALREADY_EXISTS"):
                runner.replay(root / "source", root / "nsrw", root, "0" * 40)

    def test_output_inside_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS"):
                runner.replay(root, root / "nsrw", root / "output", "0" * 40)

    def test_full_commit_and_canonical_runner_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "EXPECTED_COMMIT_MUST_BE_FULL"):
                runner.replay(root / "source", root / "nsrw", root / "output", "HEAD")
            with self.assertRaisesRegex(RuntimeError, "RUNNER_OUTSIDE_CANONICAL_PATH"):
                runner.replay(root / "source", root / "nsrw", root / "output", "0" * 40)

    def test_exact_committed_input_and_ignored_shadow(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
            proof = root / "proof.lean"
            proof.write_bytes(b"theorem t : True := by trivial\n")
            subprocess.run(["git", "add", "--", "proof.lean"], cwd=root, check=True)
            subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "commit", "--quiet", "-m", "fixture"], cwd=root, check=True)
            info = runner.committed_input(root, "proof.lean", None)
            self.assertEqual(info["raw_sha256"], runner.digest(proof))
            proof.write_bytes(b"theorem t : False := by trivial\n")
            with self.assertRaisesRegex(RuntimeError, "INPUT_NOT_EXACT_COMMITTED_BYTES"):
                runner.committed_input(root, "proof.lean", None)
            (root / ".gitignore").write_text("*.olean\n")
            (root / "shadow.olean").write_bytes(b"old")
            with self.assertRaisesRegex(RuntimeError, "UNTRACKED_LEAN_INPUT"):
                runner.reject_shadow_inputs(root)


if __name__ == "__main__":
    unittest.main()

