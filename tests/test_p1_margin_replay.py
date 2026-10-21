"""Synthetic custody controls only; these tests do not constitute Lean evidence."""

import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

SPEC = importlib.util.spec_from_file_location(
    'p1_margin_replay', Path(__file__).parents[1] / 'scripts/run-p1-margin-replay.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
LAST = tuple(runner.MODULES)[-1]


def synthetic(root, monkeypatch, failure=None):
    source, nsrw, output = ((root / n).resolve() for n in ('source', 'nsrw', 'run'))
    source.mkdir()
    nsrw.mkdir()
    binding = {'commit': 'a' * 40, 'tracked_clean': True, 'inputs': {}}
    for relative in runner.INPUTS:
        p = nsrw / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(relative.encode())
        binding['inputs'][relative] = {'raw_sha256': runner.digest(p), 'git_blob_sha1': 'b' * 40}
    target = source / 'target.olean'
    target.write_bytes(b'pinned source artifact')
    original_run = subprocess.run
    observed_envs = []

    def command(args, **kwargs):
        assert subprocess.run is original_run
        observed_envs.append(kwargs['env'])
        assert 'LEAN_SRC_PATH' not in kwargs['env']
        name = 'source' if args[1] == 'build' else Path(args[-1]).stem
        if failure == 'invocation':
            raise FileNotFoundError('missing lake executable')
        if name != 'source' and failure != 'missing_artifact':
            Path(args[args.index('-o') + 1]).write_bytes(b'fresh artifact:' + name.encode())
        if name == 'source' and failure == 'not_fresh':
            (output / 'artifacts' / (next(iter(runner.MODULES)) + '.olean')).write_bytes(b'stale')
        text = '\n'.join('NSRW.P2.' + short + ' (c : Parameters) : True\n' +
                         "'NSRW.P2." + short +
                         "' depends on axioms: [propext, Classical.choice, Quot.sound]"
                         for short in runner.SURFACES.get(name, ()))
        if name == LAST:
            if failure == 'sorry':
                text += '\nsorryAx'
            elif failure == 'missing_axioms':
                text = text.replace('depends on axioms:', 'missing axiom output:')
            elif failure == 'missing_statement':
                text = '\n'.join(line for line in text.splitlines() if not line.startswith('NSRW.'))
            elif failure == 'extra_axiom':
                text = text.replace('Quot.sound]', 'Quot.sound, extraAx]')
            elif failure == 'duplicate_axioms':
                text += '\n' + text
            elif failure == 'printed_promotion':
                text += '\nclaim_authority=INDEPENDENT; claim_status=CONFIRMED'
        kwargs['stdout'].write(text.encode())
        kwargs['stderr'].write(b'warning' if failure == 'stderr:' + name else b'')
        return SimpleNamespace(returncode=1 if failure == 'exit:' + name else 0)

    monkeypatch.setattr(runner, 'run_command', command)
    monkeypatch.setattr(runner, '__file__', str(nsrw / runner.RUNNER) +
                        ('.outside' if failure == 'canonical' else ''))
    bindings = iter([binding, {**binding, 'commit': 'c' * 40} if failure == 'head' else binding])
    monkeypatch.setattr(runner, 'identity', lambda *_: next(bindings))
    source_calls = []

    def source_identity(*_):
        source_calls.append(1)
        return {'pin': 'changed' if failure == 'source_identity' and len(source_calls) > 1 else 'same'}

    def shadow(*_):
        if failure == 'shadow':
            raise RuntimeError('UNTRACKED_LEAN_SHADOW_INPUT')

    helper = SimpleNamespace(source_identity=source_identity, reject_shadow_inputs=shadow,
                             TARGET_ARTIFACT='target.olean')
    monkeypatch.setattr(runner, 'load_helper', lambda *_: helper)
    inspect = runner.inspect_axioms

    def inspect_and_mutate(text, names):
        result = inspect(text, names)
        if names == runner.SURFACES[LAST]:
            if failure == 'target':
                target.write_bytes(b'changed')
            elif failure == 'input':
                (output / 'inputs' / (LAST + '.lean')).write_bytes(b'changed')
            elif failure == 'runner':
                (output / 'inputs' / Path(runner.RUNNER).name).write_bytes(b'changed')
            elif failure == 'artifact':
                (output / 'artifacts' / (LAST + '.olean')).write_bytes(b'changed')
            elif failure == 'log':
                (output / (LAST + '.stdout.log')).write_bytes(b'changed')
            elif failure == 'extra_input':
                (output / 'inputs' / 'shadow.lean').write_bytes(b'extra')
            elif failure == 'extra_artifact':
                (output / 'artifacts' / 'shadow.olean').write_bytes(b'extra')
        return result

    monkeypatch.setattr(runner, 'inspect_axioms', inspect_and_mutate)
    report = runner.replay(source, nsrw, output, 'a' * 40)
    assert subprocess.run is original_run
    if observed_envs:
        assert 'LEAN_PATH' not in observed_envs[0]
        assert all(e.get('LEAN_PATH') == str(output / 'artifacts') for e in observed_envs[1:])
    return report, output


@pytest.mark.parametrize('printed', [None, 'printed_promotion'])
def test_success_has_ten_surfaces_and_never_self_promotes(tmp_path, monkeypatch, printed):
    monkeypatch.setenv('LEAN_PATH', 'untrusted old external artifacts')
    monkeypatch.setenv('LEAN_SRC_PATH', 'untrusted source path')
    report, output = synthetic(tmp_path, monkeypatch, printed)
    assert report['check_status'] == runner.PASS
    assert report['claim_authority'] == 'NONE' and report['claim_status'] == 'UNVERIFIED'
    assert len(report['axiom_surfaces']) == 10 and len(report['fresh_artifacts']) == 5
    assert len(report['inputs']) == 7 and len(report['stages']) == 6
    assert report['pre_identity'] == report['post_identity']
    assert json.loads((output / 'replay-metadata.json').read_text()) == report
    with zipfile.ZipFile(str(output) + '-replay-evidence.zip') as z:
        assert z.testzip() is None
        assert z.read('inputs/' + Path(runner.RUNNER).name)
        assert json.loads(z.read('replay-metadata.json')) == report


@pytest.mark.parametrize('failure', [
    *('exit:' + name for name in ['source', *runner.MODULES]),
    'stderr:source', 'stderr:' + LAST, 'invocation', 'missing_artifact', 'not_fresh',
    'sorry', 'missing_axioms', 'missing_statement', 'extra_axiom', 'duplicate_axioms',
    'source_identity', 'head', 'shadow', 'canonical', 'input', 'runner', 'artifact',
    'log', 'target', 'extra_input', 'extra_artifact',
])
def test_failure_preserves_archive_without_admission(tmp_path, monkeypatch, failure):
    report, output = synthetic(tmp_path, monkeypatch, failure)
    assert report['check_status'] == 'ERROR[REPLAY_NOT_ADMITTED]'
    assert report['claim_authority'] == 'NONE' and report['claim_status'] == 'UNVERIFIED'
    assert report['error']
    assert (output / 'replay-metadata.json').is_file()
    with zipfile.ZipFile(str(output) + '-replay-evidence.zip') as z:
        assert z.testzip() is None
        assert json.loads(z.read('replay-metadata.json')) == report


@pytest.mark.parametrize('failure', ['head', 'dirty', 'bytes', 'blob', 'missing'])
def test_identity_binds_real_inputs_to_expected_commit(tmp_path, monkeypatch, failure):
    path = tmp_path / runner.INPUTS[0]
    path.parent.mkdir(parents=True)
    if failure != 'missing':
        path.write_bytes(b'candidate')

    def git(_, args, env):
        if args[0] == 'rev-parse':
            return ('b' * 40 if failure == 'head' else 'a' * 40).encode()
        if args[0] == 'status':
            return b' M tracked-file' if failure == 'dirty' else b''
        return b'different' if failure == 'bytes' else b'candidate'

    monkeypatch.setattr(runner, 'git', git)
    with pytest.raises(RuntimeError):
        runner.identity(tmp_path, 'a' * 40, {})


@pytest.mark.parametrize('protected', ['output', 'archive', 'source', 'nsrw', 'commit'])
def test_preconditions_do_not_overwrite_or_write_inside_checkouts(tmp_path, protected):
    source, nsrw, output = (tmp_path / n for n in ('source', 'nsrw', 'run'))
    source.mkdir()
    nsrw.mkdir()
    commit = 'a' * 40
    if protected == 'output':
        output.mkdir()
    elif protected == 'archive':
        Path(str(output) + '-replay-evidence.zip').write_bytes(b'preserve')
    elif protected in {'source', 'nsrw'}:
        output = (source if protected == 'source' else nsrw) / 'nested'
    else:
        commit = 'not-a-commit'
    with pytest.raises(RuntimeError):
        runner.replay(source, nsrw, output, commit)


def test_portable_blob_pins_and_minimal_dependency_surface():
    root = Path(__file__).parents[1]
    assert len(runner.MODULES) == 5 and len(runner.INPUTS) == 7
    assert sum(map(len, runner.SURFACES.values())) == 10
    for relative, pin in runner.PINS.items():
        data = (root / relative).read_bytes().replace(b'\r\n', b'\n')
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == pin
    assert all(not any(word in p for word in ('docs/', 'observe', 'preserve', 'development'))
               for p in runner.INPUTS if p != runner.HELPER)
    assert not any(name.startswith(('P2_F1', 'P2_L2', 'P2_L3', 'P2_C')) for name in runner.MODULES)
