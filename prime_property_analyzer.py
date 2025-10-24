%%writefile prime_property_analyzer.py
# -*- coding: utf-8 -*-
"""
prime_property_analyzer.py

This script provides the computational verification for the paper:
"A Universal Modular Property of Twin Primes and Asymptotic Failure Rates for Prime Gaps"

It performs several analyses strictly for primes p >= 11, aligning with the
theorems presented in the paper.

1.  Verifies the Δ(N) property for various prime gaps in base 10.
2.  Analyzes the structural reasons for failure rates in gaps divisible by 6,
    breaking down results by mod-6 residue and last-digit patterns.

The script is optimized using Numba for high-performance computation.

Usage:
    python prime_property_analyzer.py --max-prime 1000000 --run-all

Requirements:
    - Python 3.7+
    - numpy
    - numba
"""

import argparse
import time
from typing import Dict, List, Tuple

import numpy as np
from numba import jit

# --- Constants ---
GAPS_TO_ANALYZE = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30]
GAP_NAMES = {
    2: "Twin", 4: "Cousin", 6: "Sexy", 8: "Gap-8", 10: "Gap-10",
    12: "Gap-12", 14: "Gap-14", 16: "Gap-16", 18: "Gap-18",
    20: "Gap-20", 24: "Gap-24", 30: "Gap-30"
}
MOD6_GAPS = [6, 12, 18, 24, 30]

# --- Core Numba-Optimized Functions ---

@jit(nopython=True)
def is_prime(n: int) -> bool:
    """Fast primality test for integers."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

@jit(nopython=True)
def generate_primes_array(max_n: int) -> np.ndarray:
    """Generates a numpy array of all prime numbers up to max_n."""
    primes = []
    for n in range(2, max_n + 1):
        if is_prime(n):
            primes.append(n)
    return np.array(primes, dtype=np.int64)

@jit(nopython=True)
def compute_delta(n: int) -> int:
    """Computes the Δ(n) = X² + Y² - n property for a number n in base 10."""
    if n < 10:
        return -1
    x = n // 10
    y = n % 10
    return x * x + y * y - n

@jit(nopython=True)
def _collect_base10_data(
    primes: np.ndarray, gap: int, modulus: int
) -> Tuple[int, int, List[Tuple[int, int]]]:
    """Numba-optimized core logic to collect data for base-10 analysis for p >= 11."""
    total_pairs = 0
    successful_pairs = 0
    counterexamples = []
    prime_set = set(primes)

    for p1 in primes:
        # **MODIFICATION**: Strictly enforce p >= 11 as per the paper's theorems.
        if p1 < 11:
            continue

        p2 = p1 + gap
        if p2 > primes[-1]:
            break
        
        if p2 in prime_set:
            total_pairs += 1
            delta1 = compute_delta(p1)
            delta2 = compute_delta(p2)
            mod1 = delta1 % modulus
            mod2 = delta2 % modulus
            
            if mod1 == 0 or mod2 == 0:
                successful_pairs += 1
            else:
                if len(counterexamples) < 10:
                    counterexamples.append((p1, p2))
    
    return total_pairs, successful_pairs, counterexamples

@jit(nopython=True)
def _collect_mod6_data(
    max_prime: int, gap: int
) -> Tuple[List[Tuple], List[Tuple]]:
    """Numba-optimized core logic for mod-6 structural analysis for p >= 11."""
    mod6_results = []
    digit_pattern_results = []

    # Loop starts at 11, so p1 is always >= 11.
    for p1 in range(11, max_prime - gap + 1):
        if is_prime(p1):
            p2 = p1 + gap
            if is_prime(p2):
                x1, y1 = p1 // 10, p1 % 10
                x2, y2 = p2 // 10, p2 % 10
                delta1 = x1 * x1 + y1 * y1 - p1
                delta2 = x2 * x2 + y2 * y2 - p2
                has_property = (delta1 % 3 == 0) or (delta2 % 3 == 0)
                
                mod6_results.append((p1 % 6, has_property))
                digit_pattern_results.append((
                    y1, y2, has_property, p1, p2, x1 % 3, x2 % 3
                ))
    
    return mod6_results, digit_pattern_results

# --- Analysis and Presentation Functions ---

def run_base10_analysis(primes: np.ndarray):
    """Runs and prints the analysis for various prime gaps in base 10, mod 3."""
    print("=" * 70)
    print("ANALYSIS 1: PROPERTY SUCCESS RATE FOR VARIOUS PRIME GAPS (p >= 11)")
    print("=" * 70)
    print("\nVerifying the property for prime pairs (p, p+k) where p >= 11.\n")
    
    print(f"{'Gap (k)':<8} | {'Name':<9} | {'Total Pairs':>12} | {'Success':>10} | {'Rate (%)':>9} | {'Status'}")
    print("-" * 70)
    
    for gap in GAPS_TO_ANALYZE:
        total, success, counterex = _collect_base10_data(primes, gap, 3)
        
        if total > 0:
            rate = (success / total) * 100
            is_proven_universal = gap in [2, 4, 8, 10, 12, 18] # Gaps with 100% success rate
            
            if is_proven_universal and abs(rate - 100.0) < 1e-9:
                status = "100% (Universal)"
            else:
                status = f"{rate:.2f}"

            name = GAP_NAMES.get(gap, f"Gap-{gap}")
            
            print(f"{gap:<8} | {name:<9} | {total:>12,d} | {success:>10,d} | {rate:>8.2f}% | {status}")
            
            if counterex:
                ex_str = ", ".join([f"({p1},{p2})" for p1, p2 in counterex[:3]])
                print(f"{'':11}└─ Counterexamples: {ex_str}, ...")
    print("\n")

def run_mod6_analysis(max_prime: int):
    """Runs and prints the detailed mod-6 structural analysis for p >= 11."""
    print("=" * 70)
    print("ANALYSIS 2: STRUCTURAL ANALYSIS OF GAPS DIVISIBLE BY 6 (p >= 11)")
    print("=" * 70)
    print("\nInvestigating failure rates for gaps k ≡ 0 (mod 6).\n")

    for gap in MOD6_GAPS:
        mod6_data, digit_data = _collect_mod6_data(max_prime, gap)

        print("-" * 70)
        print(f"Analysis for Gap {gap}")
        print("-" * 70)

        # ... (The rest of the printing logic remains the same)
        print("\n(A) Breakdown by p (mod 6) residue class:")
        stats_mod6 = {1: [0, 0], 5: [0, 0]}
        for p_mod6, has_property in mod6_data:
            stats_mod6[p_mod6][0] += 1
            if has_property:
                stats_mod6[p_mod6][1] += 1
        
        for res in sorted(stats_mod6.keys()):
            total, success = stats_mod6[res]
            if total > 0:
                rate = (success / total) * 100
                print(f"  p ≡ {res} (mod 6): {success:,d}/{total:,d} pairs = {rate:.2f}% success")

        print("\n(B) Breakdown by last digit pattern (Y₁ → Y₂):")
        stats_digit: Dict[str, List[int]] = {}
        failing_examples: Dict[str, Tuple] = {}

        for y1, y2, has_property, p1, p2, x1_mod3, x2_mod3 in digit_data:
            pattern = f"{y1}→{y2}"
            if pattern not in stats_digit:
                stats_digit[pattern] = [0, 0]
            
            stats_digit[pattern][0] += 1
            if has_property:
                stats_digit[pattern][1] += 1
            elif pattern not in failing_examples:
                failing_examples[pattern] = (p1, p2, x1_mod3, x2_mod3)

        for pattern in sorted(stats_digit.keys()):
            total, success = stats_digit[pattern]
            rate = (success / total) * 100
            status = "✓" if abs(rate - 100.0) < 1e-9 else "✗"
            print(f"  {pattern:^5s}: {success:5,d}/{total:5,d} pairs = {rate:6.2f}% {status}")

        if failing_examples:
            print("\n(C) Details on first counterexample for failing patterns:")
            for pattern, (p1, p2, x1, x2) in sorted(failing_examples.items()):
                 print(f"  - Pattern {pattern}: e.g., ({p1},{p2}).")
                 print(f"    (X₁≡{x1}, X₂≡{x2} mod 3 cause failure)")
        
        print("\n")


def main():
    """Main function to parse arguments and run the requested analyses."""
    parser = argparse.ArgumentParser(
        description='Computational verification for the prime digit-square property paper.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-n', '--max-prime',
        type=int,
        default=1000000,
        help='Set the upper limit for prime generation (default: 1,000,000).'
    )
    parser.add_argument(
        '-b', '--run-base10',
        action='store_true',
        help='Run Analysis 1: General success rates for various gaps.'
    )
    parser.add_argument(
        '-m', '--run-mod6',
        action='store_true',
        help='Run Analysis 2: Detailed mod-6 structural breakdown.'
    )
    parser.add_argument(
        '--run-all',
        action='store_true',
        help='Run all available analyses (default if no other run flag is set).'
    )
    
    args = parser.parse_args()

    run_all = args.run_all or not (args.run_base10 or args.run_mod6)

    print("=" * 70)
    print("Prime Digit-Square Property Analyzer")
    print("=" * 70)
    print(f"\nSettings: Maximum prime = {args.max_prime:,d}\n")
    
    if run_all or args.run_base10:
        print("Generating primes for Analysis 1...")
        start_time = time.time()
        primes = generate_primes_array(args.max_prime)
        end_time = time.time()
        print(f"Found {len(primes):,d} primes in {end_time - start_time:.3f} seconds.\n")
        run_base10_analysis(primes)
        
    if run_all or args.run_mod6:
        run_mod6_analysis(args.max_prime)

    print("=" * 70)
    print("Analysis Complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
