#!/usr/bin/env python3
"""Run the nine-module MomentBound coefficient replay at an exact NSRW commit."""

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

RUNNER = 'scripts/run-momentbound-replay.py'
HELPER = 'colab/run-c02-development.py'
MODULES = {
    'P2_F1_MainMomentPositivity': '2cc10212d7383a015072e03cbcf7d065117a7be4',
    'P2_L2_NormalizedMainMomentComparison': 'cd2a549f4648088e4f5aea04228847b7603caf45',
    'P2_L3_TemplateMomentComparison': 'c359075d585f5b66934ad81ae8b29ecba16c9eae',
    'P2_D_DeltaMComposition': '6e2bbf2e33efa8a7e36f5d0d4269b96aed5afd56',
    'P2_C_MainOnlyCoefficient': '9a73a3e3483dda1a606fde64f792ed457e0fa446',
    'P2_C02_ActualCoefficientDecomposition': 'fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c',
    'P2_C03_ActualCoefficientAtZero': 'a28d007dd1f84cd8a6e2fc4d03b540eea3ee9ad0',
    'P2_CoefficientScaledBounds': '5af9c1ddc8ea5757f6a7e76fd80f416d47abe029',
    'P2_CoefficientSourceBounds': 'b26fbb1214a79702e3fdd04f7802374ffea1d6f8',
}
SURFACES = {
    'P2_CoefficientScaledBounds': (
        'mb_normalizedMainMoment_zero_le_decay_one', 'mb_prefix_one_eq_row_difference',
        'mbCommonScale_pos', 'mb_actualSecondRepairCoefficient_eq',
        'mb_actualSecondRepairCoefficient_gt_qStar', 'mb_qStar_ge_scaled_coarse',
        'mb_actualSecondRepairCoefficient_gt_scaled_coarse',
        'mb_actualSecondRepairCoefficient_pos_of_scaled_coarse',
    ),
    'P2_CoefficientSourceBounds': (
        'mb_main_one_ge_coarse', 'mb_prefix_one_abs_le_coarse',
        'mb_qStar_ge_source_coarse', 'mb_fixed_coarse_eq', 'mb_fixed_coarse_pos',
        'mb_actualSecondRepairCoefficient_fixed_pos',
    ),
}
PINS = {'formal/p2/' + name + '.lean': pin for name, pin in MODULES.items()}
PINS[HELPER] = '518de06530c4c7c56edafdf571e5fb2ef0f808b3'
INPUTS = (*PINS, RUNNER)
PASS = 'PASS[COMMIT_BOUND_EXTERNAL_MOMENTBOUND_REPLAY]'
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
    spec = importlib.util.spec_from_file_location('momentbound_committed_source_identity', path)
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
        found = re.findall(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", text)
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
    meta = {'kind': 'COMMIT_BOUND_MOMENTBOUND_REPLAY', 'claim_authority': 'NONE',
            'claim_status': 'UNVERIFIED', 'check_status': 'ERROR[REPLAY_NOT_ADMITTED]',
            'expected_nsrw_commit': expected_commit,
            'started_utc': datetime.now(timezone.utc).isoformat(), 'stages': {},
            'fresh_artifacts': {},
            'cache_policy': 'REUSED_PINNED_SOURCE_CACHE; FRESH_NINE_EXTERNAL_MODULES',
            'shared_trust_domain': True,
            'scope': 'Fourteen named coefficient propositions, with the source Profile '
                     'and amplitude conditions shown in the printed statements.'}

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
        for name, pin in meta['inputs'].items():
            require(digest(inputs / name) == pin, 'INPUT_COPY_MISMATCH:' + name)
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
        meta['warnings'] = {}
        for module in MODULES:
            stdout = (output / (module + '.stdout.log')).read_text(encoding='utf-8')
            if module in SURFACES:
                meta['axiom_surfaces'].update(inspect_axioms(stdout, SURFACES[module]))
            warnings = [line for line in stdout.splitlines() if ': warning:' in line]
            if warnings:
                meta['warnings'][module] = warnings
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
