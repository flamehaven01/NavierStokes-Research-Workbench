"""Bounded D: review of one Z replay ZIP; no extraction or claim admission."""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(archive, expected_sha, expected_size, root, checkpoint):
    assert __debug__, "DO_NOT_RUN_VERIFIER_WITH_OPTIMIZATION"
    bounded = load(root / "colab/check-zplus-development-archive.py", "zip_checks")
    wrapper = load(root / "scripts/run-p2-z-replay.py", "replay_surface")
    result = bounded.check(archive, expected_sha, expected_size)
    with zipfile.ZipFile(archive) as bundle:
        execution_raw = bundle.read("run-metadata.json")
        execution = json.loads(execution_raw)
        replay = json.loads(bundle.read("replay-metadata.json"))
        assert replay["check_status"] == wrapper.PASS
        assert replay["claim_authority"] == "NONE" and replay["claim_status"] == "UNVERIFIED"
        assert replay["expected_nsrw_commit"] == checkpoint
        assert replay["pre_identity"] == replay["post_identity"]
        assert replay["pre_identity"]["commit"] == checkpoint
        assert replay["pre_identity"]["tracked_clean"] is True
        assert replay["pre_base_identity"] == replay["post_base_identity"]
        assert replay["pre_base_identity"] == {"commit": wrapper.BASE, "tracked_clean": True}
        assert hashlib.sha256(execution_raw).hexdigest() == replay["execution_metadata_sha256"]
        inputs = replay["pre_identity"]["inputs"]
        assert set(inputs) == set(wrapper.INPUTS)
        for relative, identity in inputs.items():
            data = subprocess.run(["git", "show", checkpoint + ":" + relative],
                                  cwd=root, capture_output=True, check=True).stdout
            member = Path(relative).name
            raw = bundle.read(member if relative == wrapper.RUNNER else "inputs/" + member)
            assert raw == data, "COMMITTED_ARCHIVE_INPUT_MISMATCH: " + relative
            assert hashlib.sha256(raw).hexdigest() == identity["raw_sha256"]
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            assert blob == identity["git_blob_sha1"]
            assert relative not in wrapper.PINS or blob == wrapper.PINS[relative]
        names = {*wrapper.COMMITTED, *wrapper.Z_BLOBS}
        assert set(execution["stages"]) == {"source", *names}
        assert set(execution["fresh_artifacts"]) == {n + ".olean" for n in names}
        assert execution["nsrw_pre_observation"] == execution["nsrw_post_observation"]
        assert execution["nsrw_pre_observation"]["head"] == wrapper.BASE
        surfaces = {}
        for module, names in wrapper.SURFACES.items():
            surfaces.update(wrapper.inspect_axioms(bundle.read(module + ".stdout.log").decode("utf-8"), names))
        assert surfaces == replay["axiom_surfaces"] and len(surfaces) == 19
        source = execution["pre_source_identity"]
        assert source["commit"] == "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
        assert source["manifest_blob"] == "f07a8454cb6200d90bcc4371bc9965e9f8f46c7d"
        assert source["toolchain_file"] == "leanprover/lean4:v4.34.0-rc2"
        assert source["tracked_status"] == ""
    result.update({"check_status": "PASS[LOCAL_ARCHIVE_CROSSCHECK:Z_PHASE_REPLAY]",
                   "execution_check_status": replay["check_status"], "committed_inputs": len(inputs),
                   "checkpoint": checkpoint, "axiom_surfaces": len(surfaces)})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--bytes", required=True, type=int)
    parser.add_argument("--checkpoint", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(check(args.archive, args.sha256, args.bytes, root, args.checkpoint), indent=2))
