"""One C04 development compile; no installation or commit-bound admission."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = 'd7e41b9b60ae7510e5b4cc67eb5d071df21bd73d'
HELPER_BLOB = '518de06530c4c7c56edafdf571e5fb2ef0f808b3'
MODULE = 'P2_C04_SmallPositiveEta'
DEPENDENCIES = (
    ('P2_F1_MainMomentPositivity', '2cc10212d7383a015072e03cbcf7d065117a7be4'),
    ('P2_L2_NormalizedMainMomentComparison', 'cd2a549f4648088e4f5aea04228847b7603caf45'),
    ('P2_L3_TemplateMomentComparison', 'c359075d585f5b66934ad81ae8b29ecba16c9eae'),
    ('P2_D_DeltaMComposition', '6e2bbf2e33efa8a7e36f5d0d4269b96aed5afd56'),
    ('P2_C_MainOnlyCoefficient', '9a73a3e3483dda1a606fde64f792ed457e0fa446'),
    ('P2_C02_ActualCoefficientDecomposition', 'fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c'),
    ('P2_C03_ActualCoefficientAtZero', 'a28d007dd1f84cd8a6e2fc4d03b540eea3ee9ad0'),
)
THEOREMS = ('actualSecondRepairCoefficient_pos_small_positive',)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def run_command(args, **kwargs):
    """Bounded execution boundary; do not mock the stdlib module globally."""
    return subprocess.run(args, **kwargs)


def query(root, args, env):
    result = run_command(args, cwd=root, env=env, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError('IDENTITY_QUERY_FAILED: ' + repr(args))
    return result.stdout


def run(source, nsrw, proof, output, expected_sha, *, expected_dependency_commit=BASE):
    source, nsrw, proof, output = (p.resolve() for p in (source, nsrw, proof, output))
    if (output.exists() or Path(str(output) + '-evidence.zip').exists()
            or output.is_relative_to(source) or output.is_relative_to(nsrw / 'formal')
            or proof.is_relative_to(output)):
        raise RuntimeError('FRESH_SAFE_OUTPUT_REQUIRED')
    output.mkdir(parents=True, exist_ok=False)
    meta = {'kind': 'C04_DEVELOPMENT_COMPILE', 'claim_authority': 'NONE',
            'claim_status': 'UNVERIFIED', 'check_status': 'ERROR[NOT_COMPLETED]',
            'started_utc': datetime.now(timezone.utc).isoformat(), 'stages': {},
            'inputs': {}, 'fresh_artifacts': {},
            'boundary': 'Per-Profile existential epsilon only; no numerical/uniform epsilon or Z.'}
    env = os.environ.copy()
    env['PATH'] = '/root/.elan/bin:' + env['PATH']
    env.pop('LEAN_PATH', None)
    env.pop('LEAN_SRC_PATH', None)

    def save():
        (output / 'run-metadata.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')

    def check(ok, message):
        if not ok:
            raise RuntimeError(message)

    def stage(name, args, stage_env):
        meta['active_stage'] = name
        info = {'command': args, 'exit': None}
        meta['stages'][name] = info
        save()
        start = time.monotonic()
        out, err = output / (name + '.stdout.log'), output / (name + '.stderr.log')
        try:
            with out.open('wb') as stdout, err.open('wb') as stderr:
                result = run_command(args, cwd=source, env=stage_env,
                                     stdout=stdout, stderr=stderr, check=False)
            info['exit'] = result.returncode
        except OSError as exc:
            info['exception'] = repr(exc)
            info['boundary'] = name + '_INVOCATION'
            raise
        finally:
            info['elapsed_seconds'] = time.monotonic() - start
            for label, path in (('stdout', out), ('stderr', err)):
                if path.exists():
                    info[label + '_sha256'] = sha(path)
                    info[label + '_bytes'] = path.stat().st_size
            save()
        preview = out.read_bytes().decode('utf-8', errors='replace')
        print(name, result.returncode, preview[-2000:], flush=True)
        check(result.returncode == 0, 'COMPILE_EXIT: ' + name)
        check(err.stat().st_size == 0, 'STDERR_REQUIRES_REVIEW: ' + name)
        check('sorryAx' not in preview, 'SORRY_AXIOM_OBSERVED')

    save()
    try:
        check(re.fullmatch(r'[0-9a-f]{64}', expected_sha) is not None, 'INVALID_PROOF_SHA')
        check(proof.is_file() and not proof.is_symlink(), 'PROOF_UNAVAILABLE')
        check(sha(proof) == expected_sha, 'C04_INPUT_HASH_MISMATCH')
        actual_base = query(nsrw, ['git', 'rev-parse', 'HEAD'], env).decode().strip()
        check(actual_base == expected_dependency_commit, 'DEPENDENCY_BASE_MISMATCH')
        helper_data = query(nsrw, ['git', 'show', 'HEAD:colab/run-c02-development.py'], env)
        check(blob(helper_data) == HELPER_BLOB, 'HELPER_BLOB_MISMATCH')
        helper = output / 'run-c02-development.py'
        helper.write_bytes(helper_data)
        driver = Path(__file__).resolve()
        shutil.copyfile(driver, output / driver.name)
        meta['runner_sha256'] = sha(driver)
        meta['helper_git_blob'] = HELPER_BLOB
        meta['helper_sha256'] = sha(helper)
        spec = importlib.util.spec_from_file_location('c04_source_helpers', helper)
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        engine.THEOREMS = THEOREMS
        meta['pre_source_identity'] = engine.source_identity(source, env)
        meta['nsrw_pre_observation'] = engine.nsrw_observation(nsrw, env)
        meta['dependency_base'] = actual_base
        inputs, artifacts = output / 'inputs', output / 'artifacts'
        inputs.mkdir()
        artifacts.mkdir()
        for module, expected_blob in DEPENDENCIES:
            relative = 'formal/p2/' + module + '.lean'
            data = query(nsrw, ['git', 'show', 'HEAD:' + relative], env)
            check(blob(data) == expected_blob, 'DEPENDENCY_BLOB_MISMATCH: ' + module)
            path = inputs / (module + '.lean')
            path.write_bytes(data)
            meta['inputs'][module] = {'git_blob': expected_blob, 'sha256': sha(path)}
        copied = inputs / (MODULE + '.lean')
        shutil.copyfile(proof, copied)
        check(sha(copied) == expected_sha, 'COPIED_PROOF_CHANGED')
        meta['inputs'][MODULE] = {'sha256': expected_sha, 'state': 'DEVELOPMENT_BYTES'}
        stage('source', ['lake', 'build', '+NavierStokes.OutgoingProfile'], env)
        target = source / engine.TARGET_ARTIFACT
        meta['target_olean_before_sha256'] = sha(target)
        proof_env = env.copy()
        proof_env['LEAN_PATH'] = str(artifacts)
        for module in [name for name, _ in DEPENDENCIES] + [MODULE]:
            artifact = artifacts / (module + '.olean')
            check(not artifact.exists(), 'ARTIFACT_NOT_FRESH')
            stage(module, ['lake', 'env', 'lean', '-R', str(inputs), '-o', str(artifact),
                           str(inputs / (module + '.lean'))], proof_env)
            check(artifact.is_file() and not artifact.is_symlink(), 'FRESH_ARTIFACT_MISSING')
            meta['fresh_artifacts'][module] = sha(artifact)
        meta['axiom_surface'] = engine.axiom_surface(
            (output / (MODULE + '.stdout.log')).read_bytes().decode('utf-8', errors='replace'))
        meta['post_source_identity'] = engine.source_identity(source, env)
        check(meta['pre_source_identity'] == meta['post_source_identity'], 'SOURCE_IDENTITY_CHANGED')
        meta['nsrw_post_observation'] = engine.nsrw_observation(nsrw, env)
        check(meta['nsrw_pre_observation'] == meta['nsrw_post_observation'], 'NSRW_OBSERVATION_CHANGED')
        meta['target_olean_after_sha256'] = sha(target)
        check(meta['target_olean_before_sha256'] == sha(target), 'SOURCE_TARGET_ARTIFACT_CHANGED')
        for module, expected in meta['fresh_artifacts'].items():
            check(sha(artifacts / (module + '.olean')) == expected, 'FRESH_ARTIFACT_CHANGED')
        for module, identity in meta['inputs'].items():
            check(sha(inputs / (module + '.lean')) == identity['sha256'], 'ARCHIVED_INPUT_CHANGED')
        check(sha(proof) == expected_sha, 'ORIGINAL_PROOF_CHANGED')
        check(sha(driver) == sha(output / driver.name) == meta['runner_sha256'], 'RUNNER_CHANGED')
        check(sha(helper) == meta['helper_sha256'], 'HELPER_CHANGED')
        meta['check_status'] = 'PASS[LOCAL_PROOF_COMPILE:P2_C04]'
    except Exception as exc:
        meta['error'] = repr(exc)
        meta['failure_boundary'] = getattr(exc, 'boundary', meta.get('active_stage', 'INPUT_OR_ENVIRONMENT'))
        meta['check_status'] = 'ERROR[C04_DEVELOPMENT_COMPILE]'
        meta['mathematical_interpretation'] = 'NONE; inspect failure boundary and raw logs'
    finally:
        meta['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        archive = Path(shutil.make_archive(str(output) + '-evidence', 'zip', root_dir=output))
        print('RESULT', meta['check_status'], 'ARCHIVE', archive, 'BYTES', archive.stat().st_size,
              'SHA256', sha(archive), flush=True)
    return 0 if meta['check_status'].startswith('PASS[') else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('source-root', 'nsrw-root', 'proof', 'output-dir'):
        parser.add_argument('--' + arg, type=Path, required=True)
    parser.add_argument('--proof-sha256', required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.source_root, args.nsrw_root, args.proof,
                         args.output_dir, args.proof_sha256))
