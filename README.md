# Prime Digit-Square Property Analyzer

This repository contains the Python code used for the computational verification in the paper: *"A Universal Modular Property of Twin Primes and Asymptotic Failure Rates for Prime Gaps"*.

### Pre-print (Zenodo) : [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17162937.svg)](https://doi.org/10.5281/zenodo.17438456)
* **DOI** - 10.5281/zenodo.17438456
* **URL** - https://doi.org/10.5281/zenodo.17438456

## Abstract

We prove that for any twin prime pair $(p, p+2)$ with $p \ge 11$ in base 10, at least one member satisfies the modular property $\Delta(N) = X^2 + Y^2 - N \equiv 0 \pmod{3}$, where $N = 10X+Y$ is the decimal representation of the prime. The proof uses elementary modular arithmetic and is completely rigorous.

Additionally, we present extensive computational evidence suggesting that for prime pairs $(p, p+k)$ with the gap $k$ divisible by 6, the proportion of pairs satisfying this property approaches specific rational limits. A heuristic argument based on residue classes modulo 30 is provided to explain these observed rates ($5/6$ for gaps $k \equiv 6, 24 \pmod{30}$ and $3/4$ for gaps $k \equiv 0 \pmod{30}$). These conjectures, conditional on the Hardy-Littlewood prime k-tuple conjecture, reveal a novel structural regularity in the distribution of prime constellations.

## Code Summary
The script analyzes an elementary modular property of prime pairs $(p, p+k)$ related to their decimal digits. The property is defined by the function $\Delta(N) = X^2 + Y^2 - N$, where $N = 10X + Y$. We test when at least one member of a prime pair satisfies $\Delta(N) \equiv 0 \pmod{3}$.

**Note:** All analyses in the script are performed strictly for primes `p >= 11`, in direct correspondence with the theorems and conjectures presented in the paper.


## Repository Contents
- `prime_property_analyzer.py`: A Numba-optimized Python script used to perform all computational verifications presented in the paper. The script is configurable to test the property for various prime gaps up to a user-defined limit.
- `README.md`: Provides detailed instructions on how to set up the environment and run the analysis code to reproduce the paper's results.
- `requirements.txt`: Specifies the exact Python library versions (numpy==2.0.2, numba==0.60.0) used to ensure perfect reproducibility.
- `results.txt`: Provides the output generated from executing the python code.

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

## Citation

If you use this work, please cite the paper using the Zenodo archive.

@misc{naladiga_venkat_2025_17438456,
  author       = {Naladiga Venkat, Arvind},
  title        = {A Universal Modular Property of Twin Primes and
                   Asymptotic Failure Rates for Prime Gaps
                  },
  month        = oct,
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17438456},
  url          = {https://doi.org/10.5281/zenodo.17438456},
}

---

## License

The content of this repository is dual-licensed:

- **MIT License** for `prime_property_analyzer.py` See the [LICENSE](LICENSE) file for details.
- **CC BY 4.0** (Creative Commons Attribution 4.0 International) for all other content (results.txt, README, etc.)

