"""Approved one-off Colab environment restoration; no proof compile or admission."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

source = Path('/content/NavierStokesAndEuler')
nsrw = Path('/content/NavierStokes-Research-Workbench')
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
logs = Path('/content') / ('nsrw-c02-bootstrap-' + stamp)
logs.mkdir(exist_ok=False)
env = os.environ.copy()
env['PATH'] = '/root/.elan/bin:' + env['PATH']
metadata = {'started_utc': stamp, 'kind': 'ENVIRONMENT_RESTORATION', 'claim_authority': 'NONE', 'stages': {}}

def save():
    (logs / 'bootstrap-metadata.json').write_text(json.dumps(metadata, indent=2))

def run(label, command, cwd=None):
    print(label, flush=True)
    with (logs / (label + '.stdout.log')).open('wb') as out, (logs / (label + '.stderr.log')).open('wb') as err:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=out, stderr=err, check=False)
    metadata['stages'][label] = {'command': command, 'exit': result.returncode}
    save()
    if result.returncode:
        raise RuntimeError(label + ': inspect preserved logs')

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root).decode().strip()

try:
    for label, root, url, revision in (
        ('source', source, 'https://github.com/openai/NavierStokesAndEuler.git', '8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538'),
        ('nsrw', nsrw, 'https://github.com/flamehaven01/NavierStokes-Research-Workbench.git', '9f39e82f9cc57b2d43e3d08bb7294920bdb74c0c'),
    ):
        if not root.exists():
            run(label + '-clone', ['git', 'clone', url, str(root)])
        run(label + '-checkout', ['git', 'checkout', '--detach', revision], root)
        assert git(root, 'rev-parse', 'HEAD') == revision
        assert not git(root, 'status', '--porcelain', '--untracked-files=no')
    assert git(source, 'rev-parse', 'HEAD:lake-manifest.json') == 'f07a8454cb6200d90bcc4371bc9965e9f8f46c7d'
    manifest = source / 'lake-manifest.json'
    original = manifest.read_bytes()
    (logs / 'manifest-before.json').write_bytes(original)
    installer = logs / 'elan-init.sh'
    run('installer-download', ['curl', '--fail', '--location', '--output', str(installer), 'https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh'])
    metadata['installer_sha256'] = hashlib.sha256(installer.read_bytes()).hexdigest()
    run('elan-install', ['sh', str(installer), '-y', '--default-toolchain', 'none'])
    run('toolchain-install', ['elan', 'toolchain', 'install', 'leanprover/lean4:v4.34.0-rc2'])
    run('toolchain-observation', ['lean', '--version'], source)
    run('dependencies', ['lake', 'env', 'true'], source)
    changed = manifest.read_bytes()
    (logs / 'manifest-after-bootstrap.json').write_bytes(changed)
    (logs / 'manifest.diff').write_bytes(subprocess.check_output(['git', 'diff', '--', 'lake-manifest.json'], cwd=source))
    if changed != original:
        before, after = json.loads(original), json.loads(changed)
        old_name, new_name = before.pop('name'), after.pop('name')
        metadata['observed_name_normalization'] = [old_name, new_name]
        assert before == after and old_name == 'fluidEquations' and new_name == 'NavierStokesAndEuler', 'UNEXPECTED_MANIFEST_CHANGE'
        manifest.write_bytes(original)
    assert manifest.read_bytes() == original
    assert not git(source, 'status', '--porcelain', '--untracked-files=no')
    for package in json.loads(original)['packages']:
        root = source / '.lake/packages' / package['name']
        assert git(root, 'rev-parse', 'HEAD') == package['rev']
        assert not git(root, 'status', '--porcelain', '--untracked-files=no')
    run('cache', ['lake', 'exe', 'cache', 'get'], source)
    assert manifest.read_bytes() == original
    assert not git(source, 'status', '--porcelain', '--untracked-files=no')
    metadata['status'] = 'PASS[PINNED_ENVIRONMENT_RESTORATION]'
except Exception as exc:
    metadata['status'] = 'ERROR[ENVIRONMENT_RESTORATION]'
    metadata['error'] = str(exc)
    raise
finally:
    metadata['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    print('BOOTSTRAP_LOGS', logs, flush=True)
    print(metadata.get('status'), flush=True)
