# Notation and Construct Coverage

MATH is human-written natural-language mathematics. Its worked solutions are **not** promoted into verified transitions — they are unverified prose and `D-008` keeps that boundary. They answer a coverage question the formal corpus cannot answer about itself: which mathematical constructs does a representation search over 608 Lean transitions never see?

**The correspondence below is lexical.** A construct counts as covered when the corpus mentions a Mathlib constant whose *name* contains a matching fragment. That is not autoformalization and is not a claim that the corpus proves anything about the construct.

Read 12,000 MATH problems and their solutions; 3,663 distinct Mathlib constants appear in the corpus.

**25 of 25 constructs** have a matching constant family in the corpus, so a binary coverage table says almost nothing. The informative number is the **intensity ratio**: how much more often humans reach for a construct (per 1,000 MATH problems) than the corpus mentions it (per transition). A large ratio marks a construct that is nominally covered and effectively unexercised.

**11 constructs are under-exercised** by at least 100x: `square root`, `trigonometry`, `vector / inner product`, `factorial`, `binomial coefficient`, `logarithm / exponential`, `fraction`, `congruence / modular`, `matrix`, `finite sum`, `implication`.

| Construct | LaTeX | MATH per 1k problems | Corpus per transition | Intensity ratio |
|---|---|---:|---:|---:|
| square root | `\sqrt` | 1,016.58 | 0.01 | **101,658x** |
| trigonometry | `\sin \cos \tan` | 914.67 | 0.05 | **18,293x** |
| vector / inner product | `\vec \cdot` | 1,138.08 | 0.16 | **7,113x** |
| factorial | `!` | 221.67 | 0.05 | **4,433x** |
| binomial coefficient | `\binom \choose` | 110.83 | 0.05 | **2,217x** |
| logarithm / exponential | `\log \ln \exp` | 98.83 | 0.12 | **824x** |
| fraction | `\frac \dfrac \tfrac` | 3,153.58 | 3.89 | **811x** |
| congruence / modular | `\pmod \equiv` | 254.25 | 0.93 | **273x** |
| matrix | `\begin{pmatrix} \det` | 240.0 | 1.04 | **231x** |
| finite sum | `\sum` | 47.75 | 0.21 | **227x** |
| implication | `\implies \Rightarrow \to` | 101.33 | 0.83 | **122x** |
| finite product | `\prod` | 3.67 | 0.19 | 19.30x |
| set membership | `\in \notin` | 18.33 | 3.01 | 6.10x |
| union / intersection | `\cup \cap` | 11.42 | 1.89 | 6.00x |
| infinity | `\infty` | 37.33 | 9.83 | 3.80x |
| limit | `\lim` | 0.17 | 0.24 | 0.70x |
| integral | `\int` | 0.08 | 0.31 | 0.30x |
| subset | `\subset \subseteq` | 0.25 | 0.78 | 0.30x |
| absolute value | `\abs \lvert` | 0.58 | 8.58 | 0.10x |
| real / complex numbers | `\mathbb{R} \mathbb{C}` | 4.58 | 30.86 | 0.10x |
| derivative | `\frac{d} \partial` | 0.0 | 0.08 | 0.00x |
| universal quantifier | `\forall` | 0.0 | 0.66 | 0.00x |
| existential quantifier | `\exists` | 0.0 | 0.99 | 0.00x |
| probability | `\Pr \mathbb{P}` | 0.0 | 3.77 | 0.00x |
| integers / naturals | `\mathbb{Z} \mathbb{N}` | 0.58 | 54.43 | 0.00x |

## MATH subject distribution

| Subject | Problems |
|---|---:|
| Algebra | 2,807 |
| Intermediate Algebra | 2,101 |
| Prealgebra | 1,994 |
| Number Theory | 1,347 |
| Geometry | 1,309 |
| Precalculus | 1,235 |
| Counting & Probability | 1,207 |

## What this does and does not license

- It **does** identify constructs the search never exercises, which bounds any claim that a finalist representation is good for mathematics in general.
- It **does not** license translating a MATH solution into a canonical transition. Doing that would need a verifier, and an unverified translation entering the corpus is precisely the contamination `D-008` exists to prevent.
