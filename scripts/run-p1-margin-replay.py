#!/usr/bin/env python3
"""One commit-bound P1 margin/normalization replay; no install or claim admission."""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

RUNNER = 'scripts/run-p1-margin-replay.py'
HELPER = 'colab/run-c02-development.py'
MODULES = {
    'P2_Z01_LocalMassIdentities': '9d6a9a2196b8383fc17b38585e39a80188e3bfcd',
    'P2_Z02_BoundaryMassSigns': 'a4681a313cbebcbacbf49962484725cbafe896a2',
    'P2_ZPLUS_J_FirstRepairAngularMoment': '11ccd687f7157c7a1bb5529843344ce04373d7af',
    'P2_ZPLUS_J_QuantitativeMargin': '16e0f2d48f0205db7a7d3bca9c1ab9262e7b925a',
    'P2_ZPLUS_J_MarginNormalization': 'b3d8d48f9cd808a101540fff91f4314f921f6a0e',
}
SURFACES = {
    'P2_ZPLUS_J_QuantitativeMargin': (
        'secondBump_massTail_eq_full', 'firstRepair_weightGap_pos',
        'angularMoment_ge_firstRepair_margin', 'firstRepair_margin_pos'),
    'P2_ZPLUS_J_MarginNormalization': (
        'firstRepair_weightGap_exp_eq', 'normalizedSecondBumpMoment_eq_interval',
        'secondBumpWeightedMoment_eq_normalized', 'normalizedSecondBumpMoment_eq_rowMoment',
        'normalizedSecondBumpMoment_ge_plateau', 'angularMoment_ge_plateau_margin'),
}
PINS = {'formal/p2/' + name + '.lean': pin for name, pin in MODULES.items()}
PINS[HELPER] = '518de06530c4c7c56edafdf571e5fb2ef0f808b3'
INPUTS = (*PINS, RUNNER)
PASS = 'PASS[COMMIT_BOUND_EXTERNAL_P1_MARGIN_REPLAY]'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args, **kwargs):
    """Mock only this command boundary, never the shared subprocess module."""
    return subprocess.run(args, **kwargs)


def git(root, args, env):
    return run_command(['git', *args], cwd=root, env=env,
                       capture_output=True, check=True).stdout


def identity(root, expected_commit, env):
    require(git(root, ['rev-parse', 'HEAD'], env).decode().strip() == expected_commit,
            'NSRW_COMMIT_MISMATCH')
    require(not git(root, ['status', '--porcelain', '--untracked-files=no'], env).strip(),
            'NSRW_TRACKED_TREE_DIRTY')
    inputs = {}
    for relative in INPUTS:
        path = root / relative
        require(path.is_file() and not path.is_symlink(), 'INPUT_UNAVAILABLE:' + relative)
        committed = git(root, ['show', 'HEAD:' + relative], env)
        require(path.read_bytes() == committed, 'INPUT_NOT_EXACT_COMMITTED_BYTES:' + relative)
        blob = hashlib.sha1(b'blob ' + str(len(committed)).encode() + b'\0' + committed).hexdigest()
        require(relative not in PINS or blob == PINS[relative], 'INPUT_BLOB_MISMATCH:' + relative)
        inputs[relative] = {'raw_sha256': digest(path), 'git_blob_sha1': blob}
    return {'commit': expected_commit, 'tracked_clean': True, 'inputs': inputs}


def load_helper(path):
    spec = importlib.util.spec_from_file_location('p1_committed_source_identity', path)
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def inspect_axioms(text, names):
    require('sorryAx' not in text, 'SORRY_AXIOM_OBSERVED')
    result = {}
    for short in names:
        name = 'NSRW.P2.' + short
        require(len(re.findall(r'^' + re.escape(name) + r'(?=\s|\()', text, re.M)) == 1,
                'STATEMENT_OUTPUT_MISSING_OR_DUPLICATED:' + name)
        found = re.findall("'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
        require(len(found) == 1, 'AXIOM_OUTPUT_MISSING_OR_DUPLICATED:' + name)
        values = [v.strip() for v in found[0].split(',') if v.strip()]
        require(len(values) == 3 and set(values) == STANDARD, 'AXIOM_SURFACE_UNEXPECTED:' + name)
        result[name] = sorted(values)
    return result


def replay(source, nsrw, output, expected_commit):
    source, nsrw, output = (p.resolve() for p in (source, nsrw, output))
    archive = Path(str(output) + '-replay-evidence.zip')
    require(re.fullmatch('[0-9a-f]{40}', expected_commit) is not None, 'EXPECTED_COMMIT_FORMAT')
    require(not output.exists() and not archive.exists(), 'OUTPUT_OR_ARCHIVE_ALREADY_EXISTS')
    require(not output.is_relative_to(source) and not output.is_relative_to(nsrw),
            'OUTPUT_MUST_BE_OUTSIDE_CHECKOUTS')
    output.mkdir(parents=True, exist_ok=False)
    inputs, artifacts = output / 'inputs', output / 'artifacts'
    inputs.mkdir()
    artifacts.mkdir()
    env = os.environ.copy()
    env['PATH'] = '/root/.elan/bin:' + env.get('PATH', '')
    env.pop('LEAN_PATH', None)
    env.pop('LEAN_SRC_PATH', None)
    meta = {'kind': 'COMMIT_BOUND_P1_MARGIN_REPLAY', 'claim_authority': 'NONE',
            'claim_status': 'UNVERIFIED', 'check_status': 'ERROR[REPLAY_NOT_ADMITTED]',
            'expected_nsrw_commit': expected_commit,
            'started_utc': datetime.now(timezone.utc).isoformat(), 'stages': {},
            'fresh_artifacts': {},
            'cache_policy': 'REUSED_PINNED_SOURCE_CACHE; FRESH_FIVE_EXTERNAL_MODULES',
            'shared_trust_domain': True,
            'scope': 'Ten named conditional margin/normalization propositions only; '
                     'no numerical q, explicit Profile, root finder, performance or automatic admission'}

    def save():
        (output / 'replay-metadata.json').write_text(json.dumps(meta, indent=2) + '\n',
                                                  encoding='utf-8')

    def stage(name, command, stage_env):
        info = {'command': command, 'exit': None}
        meta['stages'][name] = info
        meta['active_stage'] = name
        save()
        start = time.monotonic()
        try:
            with (output / (name + '.stdout.log')).open('xb') as out, \
                    (output / (name + '.stderr.log')).open('xb') as err:
                info['exit'] = run_command(command, cwd=source, env=stage_env,
                                           stdout=out, stderr=err, check=False).returncode
        except OSError as exc:
            info['invocation_exception'] = repr(exc)
            raise RuntimeError(name + '_INVOCATION') from exc
        finally:
            info['elapsed_seconds'] = time.monotonic() - start
            for stream in ('stdout', 'stderr'):
                path = output / (name + '.' + stream + '.log')
                if path.exists():
                    info[stream + '_sha256'] = digest(path)
                    info[stream + '_bytes'] = path.stat().st_size
            save()
        print('STAGE', name, info['exit'], flush=True)
        require(info['exit'] == 0, name + '_NONZERO_EXIT')
        require(info['stderr_bytes'] == 0, name + '_STDERR_REVIEW')
        require(b'sorryAx' not in (output / (name + '.stdout.log')).read_bytes(),
                'SORRY_AXIOM_OBSERVED')

    save()
    try:
        require(Path(__file__).resolve() == nsrw / RUNNER, 'RUNNER_OUTSIDE_CANONICAL_PATH')
        meta['pre_identity'] = identity(nsrw, expected_commit, env)
        for relative in INPUTS:
            shutil.copyfile(nsrw / relative, inputs / Path(relative).name)
        meta['inputs'] = {Path(p).name: v['raw_sha256']
                          for p, v in meta['pre_identity']['inputs'].items()}
        helper = load_helper(inputs / Path(HELPER).name)
        helper.reject_shadow_inputs(nsrw, env)
        meta['pre_source_identity'] = helper.source_identity(source, env)
        stage('source', ['lake', 'build', '+NavierStokes.OutgoingProfile'], env)
        target = source / helper.TARGET_ARTIFACT
        meta['target_olean_before_sha256'] = digest(target)
        lean_env = {**env, 'LEAN_PATH': str(artifacts)}
        for module in MODULES:
            fresh = artifacts / (module + '.olean')
            require(not fresh.exists(), 'ARTIFACT_NOT_FRESH:' + module)
            stage(module, ['lake', 'env', 'lean', '-R', str(inputs), '-o', str(fresh),
                           str(inputs / (module + '.lean'))], lean_env)
            require(fresh.is_file() and not fresh.is_symlink(), 'FRESH_ARTIFACT_MISSING:' + module)
            meta['fresh_artifacts'][fresh.name] = digest(fresh)
        meta['axiom_surfaces'] = {}
        for module, surface in SURFACES.items():
            meta['axiom_surfaces'].update(inspect_axioms(
                (output / (module + '.stdout.log')).read_text(encoding='utf-8'), surface))
        meta['post_source_identity'] = helper.source_identity(source, env)
        meta['target_olean_after_sha256'] = digest(target)
        require(meta['pre_source_identity'] == meta['post_source_identity'], 'SOURCE_IDENTITY_DRIFT')
        require(meta['target_olean_before_sha256'] == meta['target_olean_after_sha256'],
                'SOURCE_TARGET_DRIFT')
        helper.reject_shadow_inputs(nsrw, env)
        meta['post_identity'] = identity(nsrw, expected_commit, env)
        require(meta['pre_identity'] == meta['post_identity'], 'NSRW_IDENTITY_DRIFT')
        require({p.name for p in inputs.iterdir()} == set(meta['inputs']), 'ARCHIVED_INPUT_SET_DRIFT')
        require({p.name for p in artifacts.iterdir()} == set(meta['fresh_artifacts']),
                'ARTIFACT_SET_DRIFT')
        for folder, values in ((inputs, meta['inputs']), (artifacts, meta['fresh_artifacts'])):
            for name, pin in values.items():
                path = folder / name
                require(path.is_file() and not path.is_symlink() and digest(path) == pin,
                        'ARCHIVED_FILE_DRIFT:' + name)
        for name, info in meta['stages'].items():
            for stream in ('stdout', 'stderr'):
                path = output / (name + '.' + stream + '.log')
                require(path.is_file() and not path.is_symlink()
                        and digest(path) == info[stream + '_sha256']
                        and path.stat().st_size == info[stream + '_bytes'], 'LOG_DRIFT:' + name)
        require(meta['claim_authority'] == 'NONE' and meta['claim_status'] == 'UNVERIFIED',
                'CLAIM_SELF_PROMOTION')
        meta['check_status'] = PASS
    except Exception as exc:
        meta['error'] = str(exc)
        meta['failure_boundary'] = getattr(exc, 'boundary', str(exc))
        meta['error_type'] = type(exc).__name__
        meta['mathematical_interpretation'] = 'NONE; inspect preserved raw logs'
    finally:
        meta['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as bundle:
            for path in output.rglob('*'):
                if path.is_file():
                    bundle.write(path, path.relative_to(output).as_posix())
        print('RESULT', meta['check_status'], 'claim_authority=NONE', flush=True)
        print('ARCHIVE', archive, 'BYTES', archive.stat().st_size,
              'SHA256', digest(archive), flush=True)
    return meta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ('source-root', 'nsrw-root', 'output-dir'):
        parser.add_argument('--' + argument, type=Path, required=True)
    parser.add_argument('--expected-nsrw-commit', required=True)
    args = parser.parse_args()
    result = replay(args.source_root, args.nsrw_root, args.output_dir, args.expected_nsrw_commit)
    raise SystemExit(0 if result['check_status'] == PASS else 1)
