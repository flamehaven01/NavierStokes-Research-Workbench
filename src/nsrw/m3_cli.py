"""Command line for the M3 profile-closure diagnostic."""

from __future__ import annotations

import sys

from nsrw.math_kernel.profile_closure import render_m3_receipt, run_m3_self_check


def main() -> int:
    receipt = run_m3_self_check()
    sys.stdout.write(render_m3_receipt(receipt))
    return 0 if receipt["check_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
