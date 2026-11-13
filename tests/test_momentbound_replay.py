"""Replay binding and log parsing checks using synthetic execution output."""

import importlib.util
import json
import re
import subprocess
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'momentbound_replay', ROOT / 'scripts/run-momentbound-replay.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_pins_and_dependency_order():
    assert len(runner.MODULES) == 9
    assert len(runner.INPUTS) == 11
    assert [len(names) for names in runner.SURFACES.values()] == [8, 6]
    modules = set(runner.MODULES)
    seen = set()
    for name in runner.MODULES:
        path = f'formal/p2/{name}.lean'
        data = (ROOT / path).read_bytes()
        blob = subprocess.check_output(
            ['git', 'hash-object', '--stdin', '--no-filters'], input=data,
        ).decode().strip()
        assert blob == runner.PINS[path]
        text = data.decode()
        assert (set(re.findall(r'^import (\w+)$', text, re.M)) & modules) <= seen
        if name in runner.SURFACES:
            names = runner.SURFACES[name]
            assert tuple(re.findall(r'^#check NSRW\.P2\.(\w+)$', text, re.M)) == names
            assert tuple(re.findall(r'^#print axioms NSRW\.P2\.(\w+)$', text, re.M)) == names
        seen.add(name)


@pytest.mark.parametrize('failure', [None, 'missing_statement', 'extra_axiom', 'source_drift'])
def test_replay_captures_statements_warnings_and_failures(tmp_path, monkeypatch, failure):
    source, nsrw, output = (tmp_path / name for name in ('source', 'nsrw', 'run'))
    source.mkdir()
    nsrw.mkdir()
    bindings = {}
    for relative in runner.INPUTS:
        path = nsrw / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(relative.encode())
        bindings[relative] = {'raw_sha256': runner.digest(path)}
    expected_commit = 'a' * 40
    identity = {'commit': expected_commit, 'tracked_clean': True, 'inputs': bindings}
    target = source / 'target.olean'
    target.write_bytes(b'source artifact')
    helper = SimpleNamespace(
        TARGET_ARTIFACT=target.name, reject_shadow_inputs=lambda *_: None,
        source_identity=lambda *_: {'source': 'pinned'},
    )
    monkeypatch.setattr(runner, '__file__', str(nsrw / runner.RUNNER))
    monkeypatch.setattr(runner, 'identity', lambda *_: identity)
    monkeypatch.setattr(runner, 'load_helper', lambda *_: helper)
    commands = []

    def compile_stage(args, **kwargs):
        name = 'source' if args[1] == 'build' else Path(args[-1]).stem
        commands.append(name)
        if name != 'source':
            Path(args[args.index('-o') + 1]).write_bytes(name.encode())
        lines = []
        for short in runner.SURFACES.get(name, ()):
            qualified = f'NSRW.P2.{short}'
            affected = short == 'mb_fixed_coarse_eq'
            if not (affected and failure == 'missing_statement'):
                lines.append(f'{qualified} (c : Parameters) : True')
            axioms = 'propext, Classical.choice, Quot.sound'
            if affected and failure == 'extra_axiom':
                axioms += ', extraAx'
            lines.append(f"'{qualified}' depends on axioms: [{axioms}]")
        if name == 'P2_CoefficientSourceBounds':
            lines.append('test.lean:10:2: warning: redundant tactic')
            if failure == 'source_drift':
                target.write_bytes(b'drifted artifact')
        kwargs['stdout'].write('\n'.join(lines).encode())
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(runner, 'run_command', compile_stage)
    result = runner.replay(source, nsrw, output, expected_commit)
    assert commands == ['source', *runner.MODULES]
    assert (result['claim_authority'], result['claim_status']) == ('NONE', 'UNVERIFIED')
    assert len(result['fresh_artifacts']) == 9
    if failure is None:
        assert result['check_status'] == runner.PASS
        assert len(result['axiom_surfaces']) == 14
        assert len(result['warnings']['P2_CoefficientSourceBounds']) == 1
    else:
        assert result['check_status'] != runner.PASS
        assert result['error'].startswith({
            'missing_statement': 'STATEMENT_OUTPUT_MISSING_OR_DUPLICATED:',
            'extra_axiom': 'AXIOM_SURFACE_UNEXPECTED:',
            'source_drift': 'SOURCE_TARGET_DRIFT',
        }[failure])
    with zipfile.ZipFile(str(output) + '-replay-evidence.zip') as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read('replay-metadata.json')) == result
