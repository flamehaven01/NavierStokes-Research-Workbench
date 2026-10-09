"""Input/failure controls only; these tests are not Lean compilation evidence."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    'c04_development', Path(__file__).parents[1] / 'colab/run-c04-development.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


@pytest.mark.parametrize('digest,error', [('0' * 64, 'C04_INPUT_HASH_MISMATCH'),
                                         ('not-a-sha', 'INVALID_PROOF_SHA')])
def test_input_rejection_preserves_failure_without_tools(tmp_path, monkeypatch, digest, error):
    proof = tmp_path / 'proof.lean'
    proof.write_bytes(b'example : True := True.intro\n')
    output = tmp_path / 'run'

    def forbidden(*args, **kwargs):
        pytest.fail('Input rejection must precede subprocess execution')

    monkeypatch.setattr(runner, 'run_command', forbidden)
    assert runner.run(tmp_path / 'source', tmp_path / 'nsrw', proof, output, digest) == 1
    meta = json.loads((output / 'run-metadata.json').read_text(encoding='utf-8'))
    assert error in meta['error']
    assert meta['check_status'] == 'ERROR[C04_DEVELOPMENT_COMPILE]'
    assert meta['claim_authority'] == 'NONE'
    assert meta['claim_status'] == 'UNVERIFIED'
    assert meta['stages'] == {}
    assert Path(str(output) + '-evidence.zip').exists()


def test_existing_archive_is_not_overwritten(tmp_path):
    output = tmp_path / 'run'
    archive = Path(str(output) + '-evidence.zip')
    archive.write_bytes(b'preserve')
    with pytest.raises(RuntimeError, match='FRESH_SAFE_OUTPUT_REQUIRED'):
        runner.run(tmp_path / 'source', tmp_path / 'nsrw', tmp_path / 'proof', output, '0' * 64)
    assert archive.read_bytes() == b'preserve'
    assert not output.exists()


@pytest.mark.parametrize('inside', ['source', 'nsrw/formal'])
def test_path_alias_cannot_place_output_inside_protected_inputs(tmp_path, inside):
    source, nsrw = tmp_path / 'source', tmp_path / 'nsrw'
    root = tmp_path / inside
    root.mkdir(parents=True)
    output = root / '..' / root.name / 'run'
    with pytest.raises(RuntimeError, match='FRESH_SAFE_OUTPUT_REQUIRED'):
        runner.run(source, nsrw, tmp_path / 'proof', output, '0' * 64)
    assert not output.exists()


def test_dependency_base_is_immutable_and_includes_c03():
    assert runner.BASE == 'd7e41b9b60ae7510e5b4cc67eb5d071df21bd73d'
    assert runner.DEPENDENCIES[-1] == (
        'P2_C03_ActualCoefficientAtZero', 'a28d007dd1f84cd8a6e2fc4d03b540eea3ee9ad0')
    assert len(runner.DEPENDENCIES) == 7
    assert runner.THEOREMS == ('actualSecondRepairCoefficient_pos_small_positive',)


@pytest.mark.parametrize('failure', ['invocation', 'wrong-base'])
def test_environment_failure_is_not_mathematical_admission(tmp_path, monkeypatch, failure):
    proof = tmp_path / 'proof.lean'
    proof.write_bytes(b'example : True := True.intro\n')
    output = tmp_path / 'run'

    def command(*args, **kwargs):
        if failure == 'invocation':
            raise FileNotFoundError('git executable unavailable')
        return SimpleNamespace(returncode=0, stdout=b'wrong-base\n', stderr=b'')

    monkeypatch.setattr(runner, 'run_command', command)
    assert runner.run(tmp_path / 'source', tmp_path / 'nsrw', proof,
                      output, runner.sha(proof)) == 1
    meta = json.loads((output / 'run-metadata.json').read_text(encoding='utf-8'))
    assert meta['check_status'] == 'ERROR[C04_DEVELOPMENT_COMPILE]'
    assert meta['claim_authority'] == 'NONE'
    assert meta['claim_status'] == 'UNVERIFIED'
    assert meta['mathematical_interpretation'].startswith('NONE;')
    assert meta['stages'] == {}
    assert Path(str(output) + '-evidence.zip').exists()


def test_replay_commit_override_keeps_fixed_dependency_blob_checks(tmp_path, monkeypatch):
    proof = tmp_path / 'proof.lean'
    proof.write_bytes(b'example : True := True.intro\n')
    output = tmp_path / 'run'
    checkpoint = 'a' * 40

    def query(root, args, env):
        if args == ['git', 'rev-parse', 'HEAD']:
            return checkpoint.encode()
        assert args == ['git', 'show', 'HEAD:colab/run-c02-development.py']
        return b'wrong helper bytes'

    monkeypatch.setattr(runner, 'query', query)
    assert runner.run(tmp_path / 'source', tmp_path / 'nsrw', proof, output,
                      runner.sha(proof), expected_dependency_commit=checkpoint) == 1
    meta = json.loads((output / 'run-metadata.json').read_text())
    assert 'HELPER_BLOB_MISMATCH' in meta['error']
    assert meta['claim_status'] == 'UNVERIFIED' and meta['claim_authority'] == 'NONE'
