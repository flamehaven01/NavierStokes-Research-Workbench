"""Exercise actual containment and contract failures of the second backend."""
import copy
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("scalar_crosscheck", ROOT / "scripts/check-core-scalars-mpmath.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


@pytest.mark.parametrize("bits", [128, 256, 512])
def test_retained_intervals_contain_second_backend(bits):
    raw = (ROOT / f"examples/p2-core-scalars/core-scalars-{bits}.json").read_bytes()
    report = CHECKER.check(raw)
    assert report["status"] == "PASS"
    assert len(report["checks"]) == 5
    assert report["working_precision_bits"] == bits + 192
    assert report["independent_operator"] is False


@pytest.mark.parametrize("quantity", CHECKER.FIELDS)
def test_shifted_interval_is_rejected(quantity):
    record = json.loads((ROOT / "examples/p2-core-scalars/core-scalars-128.json").read_bytes())
    # Valid positive dyadic syntax; change only the numeric claim.
    record[quantity] = {key: str(Fraction(value) + 1) for key, value in record[quantity].items()}
    with pytest.raises(ValueError, match="not contained"):
        CHECKER.check(json.dumps(record).encode())


@pytest.mark.parametrize("mutation", ["scope", "unresolved", "inputs", "formal_basis", "i01_lower_bound", "extra", "width"])
def test_changed_contract_rejected(mutation):
    record = json.loads((ROOT / "examples/p2-core-scalars/core-scalars-128.json").read_bytes())
    changed = copy.deepcopy(record)
    if mutation == "extra":
        changed["numerical_J_certificate"] = True
    elif mutation == "width":
        changed["weight_gap"]["upper"] = changed["weight_gap"]["lower"]
    else:
        changed[mutation] = {} if isinstance(changed[mutation], dict) else "PROMOTED"
    with pytest.raises(ValueError):
        CHECKER.check(json.dumps(changed).encode())


def test_duplicate_key_and_cli_failure(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"scope":1,"scope":2}')
    target = tmp_path / "report.json"
    assert CHECKER.main([str(bad), "--output", str(target)]) == 1
    assert not target.exists()
    assert "Duplicate" in capsys.readouterr().err


def test_cli_success(tmp_path):
    target = tmp_path / "report.json"
    assert CHECKER.main([str(ROOT / "examples/p2-core-scalars/core-scalars-128.json"), "--output", str(target)]) == 0
    assert json.loads(target.read_text())["records"][0]["status"] == "PASS"


def test_no_producer_import():
    import ast
    tree = ast.parse((ROOT / "scripts/check-core-scalars-mpmath.py").read_text())
    imports = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
    imports += [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names]
    assert not any(name.startswith("nsrw") or "p2_core_scalars" in name for name in imports)


def test_lf_identity_is_portable_and_raw_identity_is_observed():
    raw = (ROOT / "examples/p2-core-scalars/core-scalars-128.json").read_bytes().replace(b"\r\n", b"\n")
    lf, crlf = CHECKER.check(raw), CHECKER.check(raw.replace(b"\n", b"\r\n"))
    assert lf["input_sha256"] != crlf["input_sha256"]
    assert lf["input_lf_sha256"] == crlf["input_lf_sha256"]
