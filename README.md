# Prime Digit-Square Property Analyzer

This repository contains the Python code used for the computational verification in the paper: *"A Universal Modular Property of Twin Primes and Asymptotic Failure Rates for Prime Gaps"*.

The script analyzes an elementary modular property of prime pairs $(p, p+k)$ related to their decimal digits. The property is defined by the function $\Delta(N) = X^2 + Y^2 - N$, where $N = 10X + Y$. We test when at least one member of a prime pair satisfies $\Delta(N) \equiv 0 \pmod{3}$.

**Note:** All analyses in the script are performed strictly for primes `p >= 11`, in direct correspondence with the theorems and conjectures presented in the paper.

## Requirements

The computational results in the paper were generated using a specific set of library versions to ensure reproducibility.

### Environment

The code requires **Python 3.7+**. The primary development and testing were performed using **Python 3.12.12**.

### Dependencies
The following packages are required. The exact versions used for generating the paper's results are specified in the `requirements.txt` file.

- `numpy==2.0.2`
- `numba==0.60.0`

### Installation

To create the exact environment, navigate to the repository's directory and run:
```
pip install -r requirements.txt
```

## How to Run the Code

The script `prime_property_analyzer.py` is controlled via the command line.

### Basic Usage

To run all analyses with the default maximum prime of 1,000,000:
```
python prime_property_analyzer.py --run-all
```
*or more simply:*
```
python prime_property_analyzer.py
```

### Running Specific Analyses

You can choose to run only one of the two main analyses for faster results.

**1. Run only the Base-10 Gap Analysis (Analysis 1):**
This will check the success rates for various prime gaps.
```
python prime_property_analyzer.py --run-base10 --max-prime 10000000
```

**2. Run only the Mod-6 Structural Analysis (Analysis 2):**
This provides the detailed breakdown for gaps divisible by 6.
```
python prime_property_analyzer.py --run-mod6 --max-prime 5000000
```

### Adjusting the Limit

The `--max-prime` (or `-n`) argument controls the upper bound for the prime search. Higher numbers will yield more accurate percentages but will take significantly longer to run.

Example for a deep analysis up to 10 million:
```
python prime_property_analyzer.py -n 10000000
```

## Example Output

Running the script will produce formatted tables summarizing the results directly in your console, similar to the tables presented in the paper.

```
======================================================================
ANALYSIS 1: PROPERTY SUCCESS RATE FOR VARIOUS PRIME GAPS (p >= 11)
======================================================================

Verifying the property for prime pairs (p, p+k) where p >= 11.

Gap (k)  | Name      |  Total Pairs |    Success |  Rate (%) | Status
----------------------------------------------------------------------
2        | Twin      |        8,167 |      8,167 |   100.00% | 100% (Universal)
4        | Cousin    |        8,142 |      8,142 |   100.00% | 100% (Universal)
6        | Sexy      |       16,384 |     13,657 |    83.36% | 83.36
           └─ Counterexamples: (23,29), (53,59), (83,89), ...
...
```
```
