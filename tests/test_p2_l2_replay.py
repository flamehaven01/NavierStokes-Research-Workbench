"""Negative controls for the bounded replay launcher; no Lean authority claims."""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "scripts/run-p2-l2-replay.py"
SPEC = importlib.util.spec_from_file_location("p2_l2_replay", RUNNER)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class ReplayControls(unittest.TestCase):
    def test_expected_axiom_surface(self):
        runner.axiom_surface(
            "'NSRW.P2.t' depends on axioms: [propext, Classical.choice, Quot.sound]",
            ["NSRW.P2.t"],
        )

    def test_missing_or_extra_axiom_rejected(self):
        for text in (
            "",
            "'NSRW.P2.t' depends on axioms: [propext, Classical.choice, Quot.sound, sorryAx]",
            "'NSRW.P2.t' depends on axioms: [propext, Classical.choice, Quot.sound, NewAxiom]",
        ):
            with self.subTest(text=text), self.assertRaises(RuntimeError):
                runner.axiom_surface(text, ["NSRW.P2.t"])

    def test_shadow_lean_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / "shadow.lean").write_text("theorem bogus : True := by trivial\n")
            with self.assertRaisesRegex(RuntimeError, "UNTRACKED_LEAN_INPUT"):
                runner.reject_shadow_inputs(root)

    def test_ignored_shadow_still_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / ".gitignore").write_text("*.olean\n")
            (root / "shadow.olean").write_bytes(b"not admitted")
            with self.assertRaisesRegex(RuntimeError, "UNTRACKED_LEAN_INPUT"):
                runner.reject_shadow_inputs(root)

    def test_existing_output_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "output"
            output.mkdir()
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_ALREADY_EXISTS"):
                runner.replay(root / "source", root / "nsrw", output, "not-used")

    def test_output_inside_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, nsrw = root / "source", root / "nsrw"
            with self.assertRaisesRegex(RuntimeError, "OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS"):
                runner.replay(source, nsrw, source / "output", "not-used")


if __name__ == "__main__":
    unittest.main()
