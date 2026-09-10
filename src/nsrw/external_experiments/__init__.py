"""Independent numerical experiment surfaces.

These modules audit bounded external artifacts.  They are not theorem or Lean
proof authority.
"""

from nsrw.external_experiments.fno_dataset_audit import (
    ExternalSource,
    audit_vorticity_trajectory,
    reconstruct_velocity,
)

__all__ = ["ExternalSource", "audit_vorticity_trajectory", "reconstruct_velocity"]
