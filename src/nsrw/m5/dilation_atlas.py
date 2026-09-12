"""A bounded scaling atlas for selected OutgoingDilation declarations.

The atlas is intentionally a fixed ten-law research surface.  It binds those
declarations to one pinned raw Lean export and performs exact exponent algebra;
it is not a general theorem-ingestion or proof-verification system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping

from nsrw.m5.lean_export import NORMALIZED_SCHEMA_ID, SourceBinding
from nsrw.schema_admission import validate_document
from nsrw.strict_json import canonical_json_bytes, load_strict_json

MODULE = "NavierStokes.OutgoingDilation"
SOURCE_IDENTITY = {
    "repository_commit": "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538",
    "module": MODULE,
    "source_file_sha256": "be46401810940d1021c2f2ccf0ce00bdffef82d413f2146742564d15c5516438",
    "source_manifest_sha256": "d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f",
    "lean_toolchain": "leanprover/lean4:v4.34.0-rc2",
}
EXPORTER_IDENTITY = {
    "exporter_commit": "cacf989bd75f608700820f6afc595f32e7a99a4d",
    "exporter_binary_sha256": "a638952892fede28e6b530243dc4f15a5d0fddd988f3f2494ded812249315234",
}


@dataclass(frozen=True)
class ScalingLaw:
    """The source-bound metadata needed for one selected scaling law."""

    declaration: str
    quantity: str
    exponent: Fraction
    coordinate_action: str
    hypotheses: tuple[str, ...]
    representation: str

    def as_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["exponent"] = _fraction_text(self.exponent)
        value["hypotheses"] = list(self.hypotheses)
        return value


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _law(
    suffix: str,
    quantity: str,
    exponent: Fraction,
    coordinate_action: str,
    hypotheses: tuple[str, ...],
    representation: str,
) -> ScalingLaw:
    return ScalingLaw(
        declaration=f"{MODULE}.{suffix}",
        quantity=quantity,
        exponent=exponent,
        coordinate_action=coordinate_action,
        hypotheses=hypotheses,
        representation=representation,
    )


SCALING_LAWS = (
    _law("H_scaling", "H", Fraction(1, 2), "p.1 -> p.1 / XR", ("0 < XR",), "pointwise"),
    _law(
        "powerH_scaling", "powerH", Fraction(1, 2), "X -> X / XR", ("0 < XR",), "pointwise"
    ),
    _law(
        "energyDensity_scaling", "energyDensity", Fraction(0), "X -> X / XR", (), "pointwise"
    ),
    _law(
        "canonicalKernel_scaling",
        "canonicalKernel",
        Fraction(-1),
        "X -> X / XR",
        ("0 < XR",),
        "pointwise",
    ),
    _law("M_scaling", "M", Fraction(1), "X -> X / XR", ("0 < XR",), "integral_ioc"),
    _law(
        "I_scaling", "I", Fraction(3, 2), "X -> X / XR", ("0 < XR",), "integral_ioc_expanded"
    ),
    _law("J_scaling", "J", Fraction(3, 2), "X -> X / XR", ("0 < XR",), "integral_ioc"),
    _law("S_scaling", "S", Fraction(1), "X -> X / XR", ("0 < XR",), "integral_ioc_expanded"),
    _law(
        "totalS_scaling", "totalS", Fraction(1), "u -> u / XR", ("0 < XR",), "integral_ioi"
    ),
    _law(
        "renormalizedI_scaling",
        "renormalizedI",
        Fraction(3, 2),
        "u -> u / XR",
        ("0 < XR",),
        "integral_ioi_expanded",
    ),
)

_EXPECTED_LAWS = {law.declaration: law for law in SCALING_LAWS}
PILOT_DECLARATIONS = (
    f"{MODULE}.H_scaling",
    f"{MODULE}.canonicalKernel_scaling",
    f"{MODULE}.M_scaling",
    f"{MODULE}.J_scaling",
)

# This value is deliberately unset until one complete, reviewed ten-law export
# has produced a committed ledger.  A digest generated from caller-provided
# normalized records is diagnostic material, never atlas admission authority.
ATLAS_DIGEST_LEDGER_PATH = (
    Path(__file__).resolve().parents[3] / "fixtures/m5/outgoing_dilation_atlas_digests.json"
)
PINNED_ATLAS_DIGEST_LEDGER_SHA256: str | None = None
ATLAS_DIGEST_LEDGER_SCHEMA_ID = "flamehaven.nsrw-outgoing-dilation-atlas-digest-ledger.v1"


class AtlasLedgerNotPinnedError(ValueError):
    """Raised while the atlas lacks independently pinned digest authority."""


def source_bindings(laws: Iterable[ScalingLaw] = SCALING_LAWS) -> tuple[SourceBinding, ...]:
    """Return bindings for an exact selected subset of the fixed law family."""

    selected = tuple(laws)
    if not selected:
        raise ValueError("at least one dilation atlas law is required")
    for law in selected:
        if _EXPECTED_LAWS.get(law.declaration) != law:
            raise ValueError(f"dilation atlas law binding mismatch: {law.declaration}")

    return tuple(
        SourceBinding(
            declaration=law.declaration,
            exporter_commit=EXPORTER_IDENTITY["exporter_commit"],
            exporter_binary_sha256=EXPORTER_IDENTITY["exporter_binary_sha256"],
            **SOURCE_IDENTITY,
        )
        for law in selected
    )


def validate_law_set(laws: Iterable[ScalingLaw]) -> tuple[ScalingLaw, ...]:
    """Reject law additions, omissions, or source-metadata mutations."""

    observed = tuple(laws)
    by_declaration = {law.declaration: law for law in observed}
    if len(by_declaration) != len(observed) or set(by_declaration) != set(_EXPECTED_LAWS):
        raise ValueError("dilation atlas law set does not match the fixed ten-law contract")
    for declaration, expected in _EXPECTED_LAWS.items():
        if by_declaration[declaration] != expected:
            raise ValueError(f"dilation atlas law binding mismatch: {declaration}")
    return observed


def compute_semantic_digests(normalized: Mapping[str, Mapping[str, object]]) -> dict[str, str]:
    """Return candidate record digests for review; never admission authority."""

    return {
        declaration: sha256(canonical_json_bytes(record)).hexdigest()
        for declaration, record in normalized.items()
    }


def load_pinned_digest_ledger() -> dict[str, object]:
    """Load the separately reviewed ledger after its file hash is source-pinned."""

    if PINNED_ATLAS_DIGEST_LEDGER_SHA256 is None:
        raise AtlasLedgerNotPinnedError(
            "HELD[LEDGER_NOT_INDEPENDENTLY_PINNED]: no reviewed ten-law digest ledger is pinned"
        )
    try:
        ledger, raw = load_strict_json(ATLAS_DIGEST_LEDGER_PATH)
    except (OSError, ValueError) as exc:
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger is unavailable or invalid") from exc
    if sha256(raw).hexdigest() != PINNED_ATLAS_DIGEST_LEDGER_SHA256:
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger file hash mismatches")
    if not isinstance(ledger, dict) or ledger.get("schema_id") != ATLAS_DIGEST_LEDGER_SCHEMA_ID:
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger schema mismatches")
    if not isinstance(ledger.get("raw_sha256"), str):
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger lacks raw_sha256")
    digests = ledger.get("semantic_digests")
    if not isinstance(digests, dict) or set(digests) != set(_EXPECTED_LAWS):
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger law set mismatches")
    if not all(isinstance(value, str) and len(value) == 64 for value in digests.values()):
        raise AtlasLedgerNotPinnedError("pinned atlas digest ledger contains invalid semantic digests")
    return ledger


def validate_atlas_bindings(
    normalized: Mapping[str, Mapping[str, object]], pinned_ledger: Mapping[str, object]
) -> None:
    """Bind all ten law records to one raw export and reviewed semantic digests."""

    if set(normalized) != set(_EXPECTED_LAWS):
        raise ValueError("normalized declarations do not match the fixed ten-law atlas")
    expected_semantic_digests = pinned_ledger.get("semantic_digests")
    expected_raw_sha256 = pinned_ledger.get("raw_sha256")
    if not isinstance(expected_semantic_digests, Mapping) or set(expected_semantic_digests) != set(
        _EXPECTED_LAWS
    ):
        raise ValueError("atlas semantic digest ledger does not match the fixed ten-law atlas")
    if not isinstance(expected_raw_sha256, str):
        raise ValueError("atlas semantic digest ledger raw hash is missing")
    raw_hashes: set[str] = set()
    for law in SCALING_LAWS:
        record = normalized[law.declaration]
        try:
            validate_document(dict(record), NORMALIZED_SCHEMA_ID)
        except ValueError as exc:
            raise ValueError(f"atlas declaration fails schema admission: {law.declaration}") from exc
        source = record.get("source")
        export = record.get("export")
        declaration = record.get("declaration")
        if not all(isinstance(item, dict) for item in (source, export, declaration)):
            raise ValueError(f"atlas declaration sections are malformed: {law.declaration}")
        for field, expected in SOURCE_IDENTITY.items():
            if source.get(field) != expected:
                raise ValueError(f"atlas source binding mismatch: {law.declaration}.{field}")
        if source.get("declaration") != law.declaration:
            raise ValueError(f"atlas source declaration mismatch: {law.declaration}")
        for field, expected in EXPORTER_IDENTITY.items():
            if export.get(field) != expected:
                raise ValueError(f"atlas exporter binding mismatch: {law.declaration}.{field}")
        if declaration.get("kind") != "thm" or declaration.get("name") != law.declaration:
            raise ValueError(f"atlas theorem binding mismatch: {law.declaration}")
        if record.get("normalization_status") != "PASS" or record.get("losses") != []:
            raise ValueError(f"atlas declaration is not loss-free: {law.declaration}")
        actual_digest = sha256(canonical_json_bytes(record)).hexdigest()
        if expected_semantic_digests[law.declaration] != actual_digest:
            raise ValueError(f"atlas semantic binding mismatch: {law.declaration}")
        raw_hash = export.get("raw_sha256")
        if not isinstance(raw_hash, str):
            raise ValueError(f"atlas raw hash is missing: {law.declaration}")
        raw_hashes.add(raw_hash)
    if len(raw_hashes) != 1:
        raise ValueError("atlas declarations are not bound to one raw export")
    if raw_hashes.pop() != expected_raw_sha256:
        raise ValueError("atlas raw export does not match the pinned digest ledger")


def scale_degree(terms: Mapping[str, int], laws: Iterable[ScalingLaw] = SCALING_LAWS) -> Fraction:
    """Compute an exact XR degree from a named product or ratio expression."""

    by_quantity = {law.quantity: law for law in validate_law_set(laws)}
    degree = Fraction(0)
    for quantity, multiplicity in terms.items():
        if isinstance(multiplicity, bool) or not isinstance(multiplicity, int):
            raise ValueError(f"scale multiplicity must be an integer: {quantity}")
        try:
            degree += multiplicity * by_quantity[quantity].exponent
        except KeyError as exc:
            raise ValueError(f"unknown scaling quantity: {quantity}") from exc
    return degree


_CANDIDATE_EXPRESSIONS = (
    (
        "J_over_M_times_H",
        {"J": 1, "M": -1, "H": -1},
        "At a common positive radial coordinate where M and H are nonzero.",
    ),
    (
        "I_over_M_times_H",
        {"I": 1, "M": -1, "H": -1},
        "At a common positive radial coordinate where M and H are nonzero.",
    ),
    (
        "M_over_S",
        {"M": 1, "S": -1},
        "Only a scale-degree comparison; the two source integrands differ.",
    ),
)


def degree_zero_candidates() -> list[dict[str, object]]:
    """Return bounded algebraic candidates, never universal invariance claims."""

    result: list[dict[str, object]] = []
    for identifier, terms, condition in _CANDIDATE_EXPRESSIONS:
        degree = scale_degree(terms)
        if degree == 0:
            result.append(
                {
                    "identifier": identifier,
                    "terms": dict(terms),
                    "xr_degree": _fraction_text(degree),
                    "status": "FORMAL_SCALE_DEGREE_ZERO_CANDIDATE",
                    "condition": condition,
                }
            )
    result.append(
        {
            "identifier": "XR_times_canonicalKernel",
            "terms": {"scale_parameter_XR": 1, "canonicalKernel": 1},
            "xr_degree": "0",
            "status": "FORMAL_SCALE_DEGREE_ZERO_CANDIDATE",
            "condition": "At the corresponding scaled radial coordinate; no nonzero denominator is required.",
        }
    )
    return result


def build_static_scaling_analysis() -> dict[str, object]:
    """Return reviewed static metadata and exact algebra, without source admission."""

    validate_law_set(SCALING_LAWS)
    return {
        "artifact_kind": "m5-outgoing-dilation-static-analysis-v1",
        "claim_status": "UNVERIFIED",
        "check_status": "PASS[LOCAL]",
        "evidence_class": "REVIEWED_STATIC_SCALING_METADATA_AND_EXACT_EXPONENT_ALGEBRA",
        "laws": [law.as_dict() for law in SCALING_LAWS],
        "degree_zero_candidates": degree_zero_candidates(),
        "p2_question": (
            "For J/(M*H) at a common scaled radial coordinate, do support, zero-set, "
            "or cone and moment conditions prevent this degree-zero candidate from "
            "becoming a useful bound?"
        ),
        "non_claim": (
            "The exponents are reviewed static metadata, not automatically derived from Lean "
            "theorem bodies. Degree zero records scaling algebra only; it does not establish "
            "a global invariant, a cone estimate, or a Navier--Stokes theorem."
        ),
    }


def build_dilation_atlas(normalized: Mapping[str, Mapping[str, object]]) -> dict[str, object]:
    """Build the bounded P1 output after all selected records are bound."""

    pinned_ledger = load_pinned_digest_ledger()
    validate_atlas_bindings(normalized, pinned_ledger)
    atlas = build_static_scaling_analysis()
    return {
        "artifact_kind": "m5-outgoing-dilation-atlas-v1",
        "claim_status": atlas["claim_status"],
        "check_status": "PASS[PINNED_SAME_RAW]",
        "evidence_class": "SOURCE_BOUND_SCALING_METADATA_AND_EXACT_EXPONENT_ALGEBRA",
        "laws": atlas["laws"],
        "degree_zero_candidates": atlas["degree_zero_candidates"],
        "p2_question": atlas["p2_question"],
        "non_claim": atlas["non_claim"],
    }
