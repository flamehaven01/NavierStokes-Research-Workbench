#!/usr/bin/env bash
# Compile one NSRW P2 module against the pinned OpenAI Lean source environment.
# This script writes run logs only; a dated receipt is completed from those logs.
set -euo pipefail

readonly EXPECTED_SOURCE_COMMIT="8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
readonly EXPECTED_TOOLCHAIN="leanprover/lean4:v4.34.0-rc2"
# Git blob identity is invariant across Windows CRLF and Linux LF checkouts.
# The raw SHA-256 is retained below as execution metadata only.
readonly EXPECTED_MANIFEST_GIT_BLOB_SHA1="f07a8454cb6200d90bcc4371bc9965e9f8f46c7d"
readonly SOURCE_TARGET="+NavierStokes.PulseAmplitude"
readonly EXPECTED_BOOTSTRAP_MANIFEST_NORMALIZATION=$'diff --git a/lake-manifest.json b/lake-manifest.json\nindex f07a845..46cd670 100644\n--- a/lake-manifest.json\n+++ b/lake-manifest.json\n@@ -111,6 +111,6 @@\n    "inputRev": "v4.34.0-rc2",\n    "inherited": true,\n    "configFile": "lakefile.toml"}],\n- "name": "fluidEquations",\n+ "name": "NavierStokesAndEuler",\n  "lakeDir": ".lake",\n  "fixedToolchain": false}'

lean_root=""
proof=""
output_dir=""
bootstrap_dependencies=0
bootstrap_manifest_normalization="not_required"

usage() {
  cat <<'USAGE'
Usage:
  run-p2-lean-colab.sh --lean-root PATH --proof PATH --output-dir PATH
                       [--bootstrap-dependencies]

The source root must be the pinned NavierStokesAndEuler checkout.  The optional
bootstrap flag runs `lake update` only when dependencies are missing. Lake's
known project-name normalization is accepted only when it exactly matches the
pinned diff and is immediately restored from Git; every other tracked change
is rejected. The committed manifest Git blob is the cross-platform admission
identity; the raw SHA-256 is recorded only.
USAGE
}

while (($#)); do
  case "$1" in
    --lean-root) lean_root="${2:?missing value for --lean-root}"; shift 2 ;;
    --proof) proof="${2:?missing value for --proof}"; shift 2 ;;
    --output-dir) output_dir="${2:?missing value for --output-dir}"; shift 2 ;;
    --bootstrap-dependencies) bootstrap_dependencies=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 64 ;;
  esac
done

[[ -n "$lean_root" && -n "$proof" && -n "$output_dir" ]] || {
  usage >&2
  exit 64
}

for command in git lake lean sha256sum; do
  command -v "$command" >/dev/null || {
    printf 'Required command unavailable: %s\n' "$command" >&2
    exit 69
  }
done

[[ -f "$proof" ]] || { printf 'Proof file not found: %s\n' "$proof" >&2; exit 66; }
[[ -f "$lean_root/lean-toolchain" && -f "$lean_root/lake-manifest.json" ]] || {
  printf 'Not a Lean source root: %s\n' "$lean_root" >&2
  exit 66
}

lean_root="$(cd "$lean_root" && pwd -P)"
proof="$(cd "$(dirname "$proof")" && pwd -P)/$(basename "$proof")"
proof_repo="$(git -C "$(dirname "$proof")" rev-parse --show-toplevel 2>/dev/null)" || {
  printf 'Proof file is not inside a Git worktree: %s\n' "$proof" >&2
  exit 65
}
proof_relpath="${proof#"$proof_repo"/}"
git -C "$proof_repo" ls-files --error-unmatch -- "$proof_relpath" >/dev/null || {
  printf 'Proof file is not tracked by its Git worktree: %s\n' "$proof_relpath" >&2
  exit 65
}
git -C "$proof_repo" diff --quiet -- "$proof_relpath" || {
  printf 'Proof file has unstaged changes: %s\n' "$proof_relpath" >&2
  exit 65
}
git -C "$proof_repo" diff --cached --quiet -- "$proof_relpath" || {
  printf 'Proof file has staged changes: %s\n' "$proof_relpath" >&2
  exit 65
}
proof_commit="$(git -C "$proof_repo" rev-parse HEAD)"
runner_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/$(basename "${BASH_SOURCE[0]}")"
runner_repo="$(git -C "$(dirname "$runner_path")" rev-parse --show-toplevel 2>/dev/null)" || {
  printf 'Runner is not inside a Git worktree: %s\n' "$runner_path" >&2
  exit 65
}
[[ "$runner_repo" == "$proof_repo" ]] || {
  printf 'Runner and proof file are not in the same Git worktree.\n' >&2
  exit 65
}
runner_relpath="${runner_path#"$runner_repo"/}"
git -C "$runner_repo" ls-files --error-unmatch -- "$runner_relpath" >/dev/null || {
  printf 'Runner is not tracked by its Git worktree: %s\n' "$runner_relpath" >&2
  exit 65
}
git -C "$runner_repo" diff --quiet -- "$runner_relpath" || {
  printf 'Runner has unstaged changes: %s\n' "$runner_relpath" >&2
  exit 65
}
git -C "$runner_repo" diff --cached --quiet -- "$runner_relpath" || {
  printf 'Runner has staged changes: %s\n' "$runner_relpath" >&2
  exit 65
}

source_commit="$(git -C "$lean_root" rev-parse HEAD)"
[[ "$source_commit" == "$EXPECTED_SOURCE_COMMIT" ]] || {
  printf 'Pinned source commit mismatch: %s\n' "$source_commit" >&2
  exit 65
}

[[ -z "$(git -C "$lean_root" status --porcelain --untracked-files=no)" ]] || {
  printf 'Pinned source checkout has tracked changes.\n' >&2
  exit 65
}

toolchain="$(tr -d '\r\n' < "$lean_root/lean-toolchain")"
[[ "$toolchain" == "$EXPECTED_TOOLCHAIN" ]] || {
  printf 'Pinned toolchain mismatch: %s\n' "$toolchain" >&2
  exit 65
}

git -C "$lean_root" diff --quiet -- lake-manifest.json || {
  printf 'Pinned manifest has working-tree changes.\n' >&2
  exit 65
}
manifest_git_blob_sha1="$(git -C "$lean_root" rev-parse 'HEAD:lake-manifest.json')"
[[ "$manifest_git_blob_sha1" == "$EXPECTED_MANIFEST_GIT_BLOB_SHA1" ]] || {
  printf 'Pinned manifest Git blob mismatch: %s\n' "$manifest_git_blob_sha1" >&2
  exit 65
}
manifest_runtime_raw_sha256="$(sha256sum "$lean_root/lake-manifest.json" | awk '{print $1}')"

if [[ ! -d "$lean_root/.lake/packages/mathlib" ]]; then
  (( bootstrap_dependencies == 1 )) || {
    printf 'Dependencies are absent. Re-run with --bootstrap-dependencies.\n' >&2
    exit 69
  }
  mkdir -p "$output_dir"
  bootstrap_stdout="$output_dir/bootstrap.stdout.log"
  bootstrap_stderr="$output_dir/bootstrap.stderr.log"
  set +e
  (cd "$lean_root" && lake update && lake exe cache get) >"$bootstrap_stdout" 2>"$bootstrap_stderr"
  bootstrap_exit_code=$?
  set -e
  if (( bootstrap_exit_code != 0 )); then
    printf 'Dependency bootstrap failed; see %s and %s\n' "$bootstrap_stdout" "$bootstrap_stderr" >&2
    exit "$bootstrap_exit_code"
  fi
  bootstrap_manifest_diff="$(git -C "$lean_root" diff --no-ext-diff -- lake-manifest.json)"
  if [[ -n "$bootstrap_manifest_diff" ]]; then
    [[ "$bootstrap_manifest_diff" == "$EXPECTED_BOOTSTRAP_MANIFEST_NORMALIZATION" ]] || {
      printf 'Bootstrap changed lake-manifest.json outside the pinned normalization.\n' >&2
      exit 65
    }
    git -C "$lean_root" checkout -- lake-manifest.json
    bootstrap_manifest_normalization="restored_exact_project_name_normalization"
  fi
  git -C "$lean_root" diff --quiet -- lake-manifest.json || {
    printf 'Bootstrap manifest restoration failed; refusing to compile.\n' >&2
    exit 65
  }
  [[ -z "$(git -C "$lean_root" status --porcelain --untracked-files=no)" ]] || {
    printf 'Pinned source checkout has tracked changes after bootstrap.\n' >&2
    exit 65
  }
  manifest_git_blob_sha1="$(git -C "$lean_root" rev-parse 'HEAD:lake-manifest.json')"
  [[ "$manifest_git_blob_sha1" == "$EXPECTED_MANIFEST_GIT_BLOB_SHA1" ]] || {
    printf 'Pinned manifest Git blob mismatch after bootstrap: %s\n' "$manifest_git_blob_sha1" >&2
    exit 65
  }
  manifest_runtime_raw_sha256="$(sha256sum "$lean_root/lake-manifest.json" | awk '{print $1}')"
fi

if grep -nE '\b(sorry|admit|axiom)\b' "$proof"; then
  printf 'Proof file contains a prohibited placeholder or declaration.\n' >&2
  exit 65
fi

mkdir -p "$output_dir"
source_build_stdout="$output_dir/source-build.stdout.log"
source_build_stderr="$output_dir/source-build.stderr.log"
stdout_log="$output_dir/lean.stdout.log"
stderr_log="$output_dir/lean.stderr.log"
metadata="$output_dir/run-metadata.txt"
started_utc="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
started_seconds="$(date +%s)"

set +e
(cd "$lean_root" && lake build "$SOURCE_TARGET") >"$source_build_stdout" 2>"$source_build_stderr"
source_build_exit_code=$?
if (( source_build_exit_code == 0 )); then
(cd "$lean_root" && lake env lean "$proof") >"$stdout_log" 2>"$stderr_log"
exit_code=$?
else
  exit_code=$source_build_exit_code
  : >"$stdout_log"
  printf 'External module was not compiled because source target build failed.\n' >"$stderr_log"
fi
set -e
finished_seconds="$(date +%s)"

command_version_in_source() {
  if command -v "$1" >/dev/null; then
    (cd "$lean_root" && "$1" --version) | tr '\n' ' '
  else
    printf 'unavailable'
  fi
}

hash_or_not_created() {
  if [[ -f "$1" ]]; then
    sha256sum "$1" | awk '{print $1}'
  else
    printf 'not_created'
  fi
}

{
  printf 'started_utc=%s\n' "$started_utc"
  printf 'source_commit=%s\n' "$source_commit"
  printf 'source_tree_status=clean_tracked\n'
  printf 'toolchain=%s\n' "$toolchain"
  printf 'manifest_git_blob_sha1=%s\n' "$manifest_git_blob_sha1"
  printf 'manifest_runtime_raw_sha256=%s\n' "$manifest_runtime_raw_sha256"
  printf 'bootstrap_manifest_normalization=%s\n' "$bootstrap_manifest_normalization"
  printf 'proof_repository_commit=%s\n' "$proof_commit"
  printf 'proof_repository_path=%s\n' "$proof_relpath"
  printf 'proof_sha256=%s\n' "$(sha256sum "$proof" | awk '{print $1}')"
  printf 'runner_repository_path=%s\n' "$runner_relpath"
  printf 'runner_sha256=%s\n' "$(sha256sum "$runner_path" | awk '{print $1}')"
  printf 'elan_version=%s\n' "$(command_version_in_source elan)"
  printf 'lean_version=%s\n' "$(command_version_in_source lean)"
  printf 'lake_version=%s\n' "$(command_version_in_source lake)"
  printf 'os_kernel=%s\n' "$(uname -a 2>/dev/null || printf unavailable)"
  printf 'cpu_count=%s\n' "$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf unknown)"
  printf 'memory_summary=%s\n' "$(free -h 2>/dev/null | tr '\n' ';' || printf unavailable)"
  printf 'disk_free=%s\n' "$(df -hP "$lean_root" 2>/dev/null | tail -n 1 || printf unavailable)"
  printf 'source_target=%s\n' "$SOURCE_TARGET"
  printf 'source_build_exit_code=%s\n' "$source_build_exit_code"
  printf 'elapsed_seconds=%s\n' "$((finished_seconds - started_seconds))"
  printf 'exit_code=%s\n' "$exit_code"
  printf 'source_build_stdout_sha256=%s\n' "$(hash_or_not_created "$source_build_stdout")"
  printf 'source_build_stderr_sha256=%s\n' "$(hash_or_not_created "$source_build_stderr")"
  printf 'stdout_sha256=%s\n' "$(sha256sum "$stdout_log" | awk '{print $1}')"
  printf 'stderr_sha256=%s\n' "$(sha256sum "$stderr_log" | awk '{print $1}')"
} >"$metadata"

cat "$metadata"
exit "$exit_code"
