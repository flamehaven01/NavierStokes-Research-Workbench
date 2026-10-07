"""One approved Colab C02 development launch, after environment restoration."""
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

source = Path('/content/NavierStokesAndEuler')
nsrw = Path('/content/NavierStokes-Research-Workbench')
runner = Path('/content/run-c02-development.py')
assert hashlib.sha256(runner.read_bytes()).hexdigest() == '540f0aadd7add25bc0cfae2d852009e68c23cb13537ec03c4e5bce1ba085a278'
proof = nsrw / 'formal/p2/P2_C02_ActualCoefficientDecomposition.lean'
blob = subprocess.check_output(['git', 'hash-object', str(proof)], cwd=nsrw).decode().strip()
assert blob == 'fe4c2d1e18c7fbe9db5b9ce36196a9c22184827c'
raw_sha = hashlib.sha256(proof.read_bytes()).hexdigest()
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
output = nsrw / 'colab/evidence/2026-10-07' / ('c02-development-' + stamp)
env = os.environ.copy()
env['PATH'] = '/root/.elan/bin:' + env['PATH']
command = ['python3', str(runner), '--source-root', str(source), '--nsrw-root', str(nsrw), '--proof-sha256', raw_sha, '--output', str(output)]
launcher_dir = Path('/content') / ('nsrw-c02-launch-' + stamp)
launcher_dir.mkdir(exist_ok=False)
print('PROOF_RAW_SHA256', raw_sha, flush=True)
print('RUN_DIR', output, flush=True)
with (launcher_dir / 'launcher.stdout.log').open('wb') as out, (launcher_dir / 'launcher.stderr.log').open('wb') as err:
    result = subprocess.run(command, env=env, stdout=out, stderr=err, check=False)
(launcher_dir / 'launcher.json').write_text(json.dumps({'command': command, 'exit': result.returncode, 'claim_authority': 'NONE'}, indent=2))
for path in launcher_dir.iterdir():
    if output.exists():
        shutil.copyfile(path, output / path.name)
archive_root = output if output.exists() else launcher_dir
archive = Path(shutil.make_archive(str(archive_root) + '-evidence', 'zip', root_dir=archive_root))
print('RUNNER_EXIT', result.returncode, flush=True)
if (output / 'run-metadata.json').exists():
    print((output / 'run-metadata.json').read_text(), flush=True)
print('ARCHIVE', archive, flush=True)
print('ARCHIVE_SHA256', hashlib.sha256(archive.read_bytes()).hexdigest(), flush=True)
raise SystemExit(result.returncode)
