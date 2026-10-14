"""Bounded local ZIP cross-check; no extraction and no claim admission."""

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


def check(path, expected_sha, expected_size):
    raw = path.read_bytes()
    assert len(raw) == expected_size, "ARCHIVE_SIZE_MISMATCH"
    assert hashlib.sha256(raw).hexdigest() == expected_sha, "ARCHIVE_SHA_MISMATCH"
    with zipfile.ZipFile(path) as bundle:
        names = bundle.namelist()
        assert len(names) == len(set(names)), "DUPLICATE_ARCHIVE_MEMBER"
        for item in bundle.infolist():
            member = PurePosixPath(item.filename)
            assert not member.is_absolute() and ".." not in member.parts, "UNSAFE_MEMBER"
            assert "\\" not in item.filename and ":" not in item.filename, "UNSAFE_MEMBER"
            assert (item.external_attr >> 16) & 0o170000 != 0o120000, "SYMLINK_MEMBER"
        assert bundle.testzip() is None, "ZIP_CRC_FAILURE"
        meta = json.loads(bundle.read("run-metadata.json"))
        assert meta["claim_authority"] == "NONE" and meta["claim_status"] == "UNVERIFIED"
        assert meta["check_status"].startswith("PASS[LOCAL_PROOF_COMPILE:")
        checked = 0

        def match(name, digest):
            nonlocal checked
            assert hashlib.sha256(bundle.read(name)).hexdigest() == digest, name
            checked += 1

        for name, digest in meta["inputs"].items():
            match("inputs/" + name, digest)
        for name, digest in meta["fresh_artifacts"].items():
            match("artifacts/" + name, digest)
        for name, stage in meta["stages"].items():
            assert stage["exit"] == 0 and stage["stderr_bytes"] == 0, name
            for stream in ("stdout", "stderr"):
                member = name + "." + stream + ".log"
                match(member, stage[stream + "_sha256"])
                assert len(bundle.read(member)) == stage[stream + "_bytes"]
            assert b"sorryAx" not in bundle.read(name + ".stdout.log"), name
        expected_axioms = {"propext", "Classical.choice", "Quot.sound"}
        for name, values in meta["axiom_surfaces"].items():
            assert len(values) == 3 and set(values) == expected_axioms, name
            matches = []
            for member in names:
                if member.endswith(".stdout.log"):
                    matches.extend(re.findall(
                        r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]",
                        bundle.read(member).decode("utf-8", errors="replace")))
            assert len(matches) == 1, name
            assert {s.strip() for s in matches[0].split(",")} == expected_axioms, name
        assert meta["pre_source_identity"] == meta["post_source_identity"]
        assert meta["nsrw_pre_observation"] == meta["nsrw_post_observation"]
        assert meta["target_olean_before_sha256"] == meta["target_olean_after_sha256"]
    return {
        "check_status": "PASS[LOCAL_ARCHIVE_CROSSCHECK:ZPLUS_DEVELOPMENT]",
        "execution_check_status": meta["check_status"],
        "archive_sha256": expected_sha, "archive_bytes": expected_size,
        "checked_member_hashes": checked, "stages": len(meta["stages"]),
        "fresh_artifacts": len(meta["fresh_artifacts"]),
        "axiom_surfaces": len(meta["axiom_surfaces"]),
        "claim_authority": "NONE", "claim_status": "UNVERIFIED",
        "independent_attestation": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--bytes", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.archive, args.sha256, args.bytes), indent=2))
