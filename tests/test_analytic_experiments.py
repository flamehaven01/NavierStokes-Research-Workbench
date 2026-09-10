from __future__ import annotations

import json

from nsrw.analytic_cli import main
from nsrw.math_kernel.analytic_experiments import run_analytic_spine_check


def test_analytic_spine_receipt_passes_without_claim_inflation() -> None:
    receipt = run_analytic_spine_check()
    assert receipt["check_status"] == "PASS"
    assert receipt["claim_status"] == "UNVERIFIED"
    assert receipt["authority"]["source_paper_profiles"] == "NOT_INSTANTIATED"
    assert receipt["authority"]["global_navier_stokes_claim"] == "NOT_ESTABLISHED"
    assert set(receipt["checks"].values()) == {"PASS"}
    assert receipt["residual_order_samples"][1]["check_status"] == "FAIL"


def test_analytic_cli_is_deterministic(tmp_path, capsys) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    assert main(["--output", str(first)]) == 0
    capsys.readouterr()
    assert main(["--output", str(second)]) == 0
    rendered = capsys.readouterr().out
    assert first.read_bytes() == second.read_bytes()
    assert json.loads(rendered)["check_status"] == "PASS"
