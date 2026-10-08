"""C03 development compile with fresh actual dependencies; never claim admission."""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

BASE = '01d2deae3534cba5a035e87ac1cbe37faac470ca'
MODULE = 'P2_C03_ActualCoefficientAtZero'
DEPENDENCIES = (
    ('P2_F1_MainMomentPositivity', '2cc10212d7383a015072e03cbcf7d065117a7be4'),
    ('P2_L2_NormalizedMainMomentComparison', 'cd2a549f4648088e4f5aea04228847b7603caf45'),
    ('P2_L3_TemplateMomentComparison', 'c359075d585f5b66934ad81ae8b29ecba16c9eae'),
    ('P2_D_DeltaMComposition', '6e2bbf2e33efa8a7e36f5d0d4269b96aed5afd56'),
    ('P2_C_MainOnlyCoefficient', '9a73a3e3483dda1a606fde64f792ed457e0fa446'),
    ('P2_C02_ActualCoefficientDecomposition', 'fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c'),
)
THEOREMS = (
    'actualSecondRepairCoefficient_zero_eq',
    'actualSecondRepairCoefficient_zero_pos',
    'actualSecondRepairCoefficient_continuous',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, nsrw, proof, output, expected_sha, *, expected_dependency_commit=BASE):
    source, nsrw, proof, output = (p.resolve() for p in (source, nsrw, proof, output))
    if output.exists() or output.is_relative_to(source) or output.is_relative_to(nsrw):
        raise RuntimeError('FRESH_EXTERNAL_OUTPUT_REQUIRED')
    output.mkdir(parents=True)
    meta = {'kind': 'C03_DEVELOPMENT_COMPILE', 'claim_authority': 'NONE',
            'claim_status': 'UNVERIFIED', 'check_status': 'ERROR[NOT_COMPLETED]',
            'started_utc': datetime.now(timezone.utc).isoformat(), 'stages': {},
            'inputs': {}, 'fresh_artifacts': {},
            'boundary': 'Development evidence only; no C04 epsilon or mass zero.'}
    env = os.environ.copy()
    env['PATH'] = '/root/.elan/bin:' + env['PATH']
    env.pop('LEAN_PATH', None)
    env.pop('LEAN_SRC_PATH', None)

    def save():
        (output / 'run-metadata.json').write_text(json.dumps(meta, indent=2) + '\n')

    def check(ok, message):
        if not ok:
            raise RuntimeError(message)

    def stage(name, args, stage_env):
        meta['active_stage'] = name
        save()
        start = time.monotonic()
        out, err = output / (name + '.stdout.log'), output / (name + '.stderr.log')
        with out.open('wb') as o, err.open('wb') as e:
            try:
                result = subprocess.run(args, cwd=source, env=stage_env, stdout=o, stderr=e)
            except OSError as exc:
                meta['stages'][name] = {'command': args, 'exception': repr(exc),
                                        'boundary': 'INVOCATION'}
                raise
        meta['stages'][name] = {'command': args, 'exit': result.returncode,
                               'elapsed_seconds': time.monotonic() - start,
                               'stdout_sha256': sha(out), 'stderr_sha256': sha(err),
                               'stdout_bytes': out.stat().st_size,
                               'stderr_bytes': err.stat().st_size}
        save()
        print(name, result.returncode, out.read_text(errors='replace')[-3000:], flush=True)
        check(result.returncode == 0, 'COMPILE_EXIT: ' + name)
        check(err.stat().st_size == 0, 'STDERR_REQUIRES_REVIEW: ' + name)
        check('sorryAx' not in out.read_text(errors='replace'), 'SORRY_AXIOM_OBSERVED')

    try:
        check(sha(proof) == expected_sha, 'C03_INPUT_HASH_MISMATCH')
        actual_base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=nsrw).decode().strip()
        check(actual_base == expected_dependency_commit, 'DEPENDENCY_BASE_MISMATCH')
        helper = nsrw / 'colab/run-c02-development.py'
        helper_blob = subprocess.check_output(['git', 'hash-object', str(helper)], cwd=nsrw).decode().strip()
        check(helper_blob == '518de06530c4c7c56edafdf571e5fb2ef0f808b3', 'HELPER_BLOB_MISMATCH')
        spec = importlib.util.spec_from_file_location('c02_identity_helpers', helper)
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        meta['pre_source_identity'] = engine.source_identity(source, env)
        meta['nsrw_observation'] = engine.nsrw_observation(nsrw, env)
        meta['dependency_base'] = actual_base
        shutil.copyfile(helper, output / helper.name)
        shutil.copyfile(Path(__file__), output / Path(__file__).name)
        inputs, artifacts = output / 'inputs', output / 'artifacts'
        inputs.mkdir()
        artifacts.mkdir()
        for module, blob in DEPENDENCIES:
            relative = 'formal/p2/' + module + '.lean'
            actual = subprocess.check_output(['git', 'rev-parse', 'HEAD:' + relative], cwd=nsrw).decode().strip()
            check(actual == blob, 'DEPENDENCY_BLOB_MISMATCH: ' + module)
            data = subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=nsrw)
            check(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blob,
                  'DEPENDENCY_BYTES_MISMATCH')
            (inputs / (module + '.lean')).write_bytes(data)
            meta['inputs'][module] = {'git_blob': blob, 'sha256': sha(inputs / (module + '.lean'))}
        shutil.copyfile(proof, inputs / (MODULE + '.lean'))
        meta['inputs'][MODULE] = {'sha256': expected_sha, 'state': 'UNCOMMITTED_DEVELOPMENT_BYTES'}
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
            check(artifact.is_file(), 'FRESH_ARTIFACT_MISSING')
            meta['fresh_artifacts'][module] = sha(artifact)
        # The existing exact-surface checker is reused only for the three C03 names.
        engine.THEOREMS = THEOREMS
        meta['axiom_surface'] = engine.axiom_surface((output / (MODULE + '.stdout.log')).read_text())
        meta['post_source_identity'] = engine.source_identity(source, env)
        check(meta['pre_source_identity'] == meta['post_source_identity'], 'SOURCE_IDENTITY_CHANGED')
        meta['target_olean_after_sha256'] = sha(target)
        check(meta['target_olean_before_sha256'] == sha(target), 'SOURCE_TARGET_ARTIFACT_CHANGED')
        for module, expected in meta['fresh_artifacts'].items():
            check(sha(artifacts / (module + '.olean')) == expected, 'FRESH_ARTIFACT_CHANGED')
        for module, identity in meta['inputs'].items():
            check(sha(inputs / (module + '.lean')) == identity['sha256'], 'ARCHIVED_INPUT_CHANGED')
        meta['check_status'] = 'PASS[LOCAL_PROOF_COMPILE:P2_C03]'
    except Exception as exc:
        meta['error'] = repr(exc)
        meta['check_status'] = 'ERROR[C03_DEVELOPMENT_COMPILE]'
    finally:
        meta['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        archive = Path(shutil.make_archive(str(output) + '-evidence', 'zip', root_dir=output))
        print('RESULT', meta['check_status'], 'ARCHIVE', archive, 'BYTES', archive.stat().st_size,
              'SHA256', sha(archive), flush=True)
    return 0 if meta['check_status'].startswith('PASS[') else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for arg in ('source-root', 'nsrw-root', 'proof', 'output-dir'):
        parser.add_argument('--' + arg, type=Path, required=True)
    parser.add_argument('--proof-sha256', required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.source_root, args.nsrw_root, args.proof,
                         args.output_dir, args.proof_sha256))
