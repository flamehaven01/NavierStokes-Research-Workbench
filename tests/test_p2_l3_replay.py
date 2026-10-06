"""L3 runner controls only; these tests do not establish any Lean proposition."""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "scripts/run-p2-l3-replay.py"
SPEC = importlib.util.spec_from_file_location("p2_l3_replay", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class L3ReplayControls(unittest.TestCase):
    def test_named_axiom_surface(self):
        text = f"'{runner.THEOREM}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        self.assertEqual(runner.axiom_surface(text), sorted(runner.AXIOMS))

    def test_missing_duplicate_unexpected_or_sorry_rejected(self):
        valid = f"'{runner.THEOREM}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for text in ("", valid + valid, valid.replace("Quot.sound", "NewAxiom"),
                     valid + "\nsorryAx", valid.replace("Quot.sound", "Quot.sound, Quot.sound")):
            with self.subTest(text=text), self.assertRaises(RuntimeError):
                runner.axiom_surface(text)

    def test_output_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_ALREADY_EXISTS"):
                runner.replay(root / "source", root / "nsrw", root, "0" * 40)

    def test_output_inside_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS"):
                runner.replay(root, root / "nsrw", root / "output", "0" * 40)

    def test_full_expected_commit_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "EXPECTED_COMMIT_MUST_BE_FULL"):
                runner.replay(root / "source", root / "nsrw", root / "output", "HEAD")

    def test_exact_committed_bytes_and_tamper(self):
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

    def test_ignored_shadow_olean_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / ".gitignore").write_text("*.olean\n")
            (root / "shadow.olean").write_bytes(b"unadmitted")
            with self.assertRaisesRegex(RuntimeError, "UNTRACKED_LEAN_INPUT"):
                runner.reject_shadow_inputs(root)


if __name__ == "__main__":
    unittest.main()
