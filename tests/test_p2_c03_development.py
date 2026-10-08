"""Runner input controls only: these tests do not establish Lean proof evidence."""
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    'c03_development', Path(__file__).parents[1] / 'colab/run-c03-development.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_bad_proof_hash_preserves_failure_without_invoking_tools(tmp_path, monkeypatch):
    proof = tmp_path / 'proof.lean'
    proof.write_text('example : True := True.intro')
    output = tmp_path / 'run'

    def forbidden(*args, **kwargs):
        pytest.fail('Input rejection must precede subprocess execution')

    monkeypatch.setattr(runner.subprocess, 'check_output', forbidden)
    code = runner.run(tmp_path / 'source', tmp_path / 'nsrw', proof, output, '0' * 64)
    metadata = json.loads((output / 'run-metadata.json').read_text())
    assert code == 1
    assert metadata['check_status'] == 'ERROR[C03_DEVELOPMENT_COMPILE]'
    assert 'C03_INPUT_HASH_MISMATCH' in metadata['error']
    assert metadata['claim_authority'] == 'NONE'
    assert metadata['claim_status'] == 'UNVERIFIED'
    assert metadata['stages'] == {}
    assert Path(str(output) + '-evidence.zip').exists()


def test_existing_output_is_not_overwritten(tmp_path):
    output = tmp_path / 'run'
    output.mkdir()
    sentinel = output / 'original.log'
    sentinel.write_bytes(b'preserve')
    with pytest.raises(RuntimeError, match='FRESH_EXTERNAL_OUTPUT_REQUIRED'):
        runner.run(tmp_path / 'source', tmp_path / 'nsrw', tmp_path / 'proof', output, '0' * 64)
    assert sentinel.read_bytes() == b'preserve'


def test_path_alias_cannot_place_run_inside_source(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    output = source / '..' / 'source' / 'run'
    with pytest.raises(RuntimeError, match='FRESH_EXTERNAL_OUTPUT_REQUIRED'):
        runner.run(source, tmp_path / 'nsrw', tmp_path / 'proof', output, '0' * 64)
    assert not output.exists()
