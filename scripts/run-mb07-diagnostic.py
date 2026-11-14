"""Run the frozen MB-07 ratio comparison and record all decisions and costs."""

import argparse
import hashlib
import json
import math
import platform
import statistics
import subprocess
import sys
import time
import tracemalloc
from fractions import Fraction
from pathlib import Path

import mpmath

from nsrw.math_kernel.p2_coefficient_verify import _rational
from nsrw.math_kernel.p2_core_scalars import expm1_bounds
from nsrw.math_kernel.p2_normalized_j_factors import BITS, COARSE_B, LAM

CALIBRATION = tuple(map(Fraction, ('1/16', '1/1048576', '1/1000000000000', '1/1099511627776')))
HELD_OUT = tuple(Fraction(1, 2**power) for power in (7, 10, 52, 60, 120, 160, 400, 520))
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'docs/momentbound/MB07_DIAGNOSTIC_BENCHMARK_CONTRACT_2026-11-13.md'
BACKEND = ROOT / 'src/nsrw/math_kernel/p2_core_scalars.py'
METHODS = ('float_exp', 'float_expm1', 'analytic', 'fraction')
WARMUPS, TRIALS, TIMEOUT = 3, 20, 120


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest():
    return {
        'contract_sha256': sha(CONTRACT), 'runner_sha256': sha(Path(__file__)),
        'backend_sha256': sha(BACKEND), 'python': sys.version, 'mpmath': mpmath.__version__,
        'platform': platform.platform(), 'processor': platform.processor(),
        'methods': list(METHODS), 'warmups': WARMUPS, 'trials': TRIALS,
        'timeout_per_case_seconds': TIMEOUT, 'reference_bits': [768, 1024],
        'fractional_bits': list(BITS),
        'calibration': list(map(str, CALIBRATION)), 'held_out': list(map(str, HELD_OUT)),
        'reference_role': 'empirical comparison', 'review': 'internal operator',
        'upstream': '8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538',
        'mb06_execution': '40e0cfe7c2defeeeee871f1923552c352f28ee5c',
    }


def parse_input(raw):
    value = _rational(raw)
    if not 0 < value < Fraction(1, 10):
        raise ArithmeticError('REJECT[OUT_OF_DOMAIN]')
    return value


def interval_decisions(bounds, thresholds):
    if bounds is None:
        return ['UNRESOLVED'] * len(thresholds)
    lower, upper = bounds
    return ['BELOW' if upper < t else 'ABOVE' if lower > t else 'UNRESOLVED'
            for t in thresholds]


def thresholds_for(lam):
    return (Fraction(17, 20) - 13 * lam / 100, Fraction(17, 20) - lam / 8)


def evaluate(method, lam, thresholds):
    a, b = 17 * lam / 10, 2 * lam
    if method in ('float_exp', 'float_expm1'):
        binary_lam = float(lam)
        args = (17 * binary_lam / 10, 2 * binary_lam)
        if method == 'float_exp':
            numerator, denominator = (math.exp(x) - 1 for x in args)
        else:
            numerator, denominator = map(math.expm1, args)
        result = {
            'lambda_conversion_error': str(Fraction.from_float(binary_lam) - lam),
            'denominator': denominator,
        }
        if denominator == 0:
            return {**result, 'status': 'ZERO_DENOMINATOR', 'estimates': ['UNRESOLVED'] * 2}
        estimate = numerator / denominator
        return {**result, 'status': 'ESTIMATE', 'estimate': estimate,
                'estimates': ['BELOW' if estimate < float(t) else
                              'ABOVE' if estimate > float(t) else 'UNRESOLVED'
                              for t in thresholds],
                'rounded_threshold_tie': [estimate == float(t) for t in thresholds]}
    if method == 'analytic':
        bounds = (Fraction(17, 20) * (1 - b), Fraction(17, 20) / (1 - a))
        return {'bounds': bounds, 'decisions': interval_decisions(bounds, thresholds)}
    attempts = []
    bounds = None
    for bits in BITS:
        nlo, nhi = expm1_bounds(a, bits)
        dlo, dhi = expm1_bounds(b, bits)
        if dlo == 0:
            attempts.append({'bits': bits, 'status': 'ZERO_LOWER_DENOMINATOR'})
            continue
        bounds = (nlo / dhi, nhi / dlo)
        decisions = interval_decisions(bounds, thresholds)
        attempts.append({'bits': bits, 'decisions': decisions, 'bounds': bounds})
        if 'UNRESOLVED' not in decisions:
            break
    return {'bounds': bounds, 'decisions': interval_decisions(bounds, thresholds), 'attempts': attempts}


def measure(method, lam, thresholds):
    for _ in range(WARMUPS):
        evaluate(method, lam, thresholds)
    samples = []
    for _ in range(TRIALS):
        start = time.perf_counter_ns()
        result = evaluate(method, lam, thresholds)
        samples.append(time.perf_counter_ns() - start)
    tracemalloc.start()
    evaluate(method, lam, thresholds)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {**result, 'time_ns_samples': samples, 'median_ns': statistics.median(samples),
            'p95_ns': sorted(samples)[math.ceil(.95 * TRIALS) - 1], 'traced_peak_bytes': peak}


def reference(lam, thresholds, bits):
    with mpmath.workprec(bits):
        def mp(value):
            return mpmath.mpf(value.numerator) / value.denominator
        x = mp(lam)
        value = mpmath.expm1(17*x/10) / mpmath.expm1(2*x)
        decisions = ['BELOW' if value < mp(t) else 'ABOVE' if value > mp(t) else 'UNRESOLVED'
                     for t in thresholds]
        return value, decisions


def review(case, result, value, reference_decisions):
    observed = result.get('decisions', result.get('estimates', ['UNRESOLVED'] * 2))
    result['contradictions'] = sum(a != 'UNRESOLVED' and a != b
                                   for a, b in zip(observed, reference_decisions, strict=True))
    bounds = result.get('bounds')
    if bounds is not None:
        lo, hi = map(Fraction, bounds)
        assert 0 <= lo <= hi
        with mpmath.workprec(1024):
            result['reference_inside'] = (
                mpmath.mpf(lo.numerator) / lo.denominator <= value <=
                mpmath.mpf(hi.numerator) / hi.denominator)
        result['width'] = str(hi - lo)
        if case == LAM:
            result['fixed_B_times_R_bounds'] = [str(COARSE_B * x) for x in (lo, hi)]
    if 'estimate' in result:
        with mpmath.workprec(1024):
            result['absolute_error'] = mpmath.nstr(abs(result['estimate'] - value), 18)


def run_case(lam):
    thresholds = thresholds_for(lam)
    _, first = reference(lam, thresholds, 768)
    value, second = reference(lam, thresholds, 1024)
    assert first == second and 'UNRESOLVED' not in second
    try:
        process = subprocess.run(
            [sys.executable, __file__, '--worker', str(lam)], capture_output=True, text=True,
            encoding='utf-8', check=True, timeout=TIMEOUT)
        results = json.loads(process.stdout)
    except subprocess.TimeoutExpired:
        results = {method: {'status': 'UNRESOLVED[TIMEOUT]'} for method in METHODS}
    for result in results.values():
        review(lam, result, value, second)
    return {'lambda': str(lam), 'thresholds': list(map(str, thresholds)),
            'reference': mpmath.nstr(value, 185), 'reference_decisions': second,
            'methods': results}


def rejection_controls():
    observed = []
    for raw in ('0', '-1/1000000000000', '1/10', 0.01, True, '2/32'):
        try:
            parse_input(raw)
        except ValueError:
            status = 'REJECT[MALFORMED]'
        except ArithmeticError:
            status = 'REJECT[OUT_OF_DOMAIN]'
        else:
            status = 'ACCEPTED'
        observed.append({'input': raw, 'status': status})
    from nsrw.math_kernel.p2_normalized_j_factors import bound_normalized_ratio
    from nsrw.math_kernel.p2_normalized_j_verify import verify_normalized_ratio
    record = bound_normalized_ratio()
    record['input']['lambda'] = '1/1000000000001'
    try:
        verify_normalized_ratio(record)
    except ValueError:
        status = 'REJECT[INPUT_BINDING]'
    else:
        status = 'ACCEPTED'
    return [*observed, {'input': 'fixed MB-06 record with changed lambda', 'status': status}]


def write_json(path, data):
    with path.open('x', encoding='utf-8') as target:
        json.dump(data, target, indent=2)
        target.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--freeze', type=Path)
    mode.add_argument('--manifest', type=Path)
    mode.add_argument('--worker')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker:
        lam = parse_input(args.worker)
        thresholds = thresholds_for(lam)
        print(json.dumps({method: measure(method, lam, thresholds) for method in METHODS},
                         default=str))
    elif args.freeze:
        write_json(args.freeze, manifest())
    else:
        if args.output is None or args.output.exists():
            parser.error('provide a new --output file')
        frozen = json.loads(args.manifest.read_text(encoding='utf-8'))
        if frozen != manifest():
            parser.error('frozen manifest differs from the runtime or source bytes')
        write_json(args.output, {'manifest_sha256': sha(args.manifest),
                                 'calibration': [run_case(x) for x in CALIBRATION],
                                 'held_out': [run_case(x) for x in HELD_OUT],
                                 'controls': rejection_controls()})


if __name__ == '__main__':
    main()
