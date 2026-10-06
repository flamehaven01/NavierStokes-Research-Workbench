"""D runner controls; tests never establish the D Lean proposition."""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "scripts/run-p2-d-replay.py"
SPEC = importlib.util.spec_from_file_location("p2_d_replay", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class DReplayControls(unittest.TestCase):
    def test_module_order_and_real_bytes(self):
        self.assertEqual([row[0] for row in runner.MODULES], ["f1", "l2", "l3", "d"])
        self.assertEqual(sum(len(row[3]) for row in runner.MODULES), 9)
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
