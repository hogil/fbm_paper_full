# Internal Reviewer Rubric

Apply this after the format gate. If the format gate fails, the decision is reject regardless of numeric quality.

## Format gate

Fail if any item is materially wrong:

- Not 4 to 10 pages including references.
- Missing title, Abstract, body, conclusion, or references.
- Wrong A4 margins, two-column body, font sizes, header/footer, figure/table caption rules, or citation style.
- Abstract has paragraphs or exceeds 15 lines.
- Title exceeds 2 lines.

## Primary Samsung Numeric Score

Use this official scoring first after the format gate:

| Category | Points |
|---|---:|
| Technical excellence | 30 |
| Originality | 30 |
| Impact | 10 |
| Paper quality | 30 |

Scoring interpretation:

- Technical excellence: assess whether the paper presents a technology direction beyond ordinary model application. Do not reward unsupported world-first or source-technology wording.
- Originality: assess differentiation from prior wafer/bin map classification, clustering, and inspection work.
- Impact: assess product applicability, field issue resolution, operational contribution, and future value within the evidence boundary.
- Paper quality: assess whether conclusions are derived from clear evidence and whether field, generated, internal engineering measurement, and future-work scopes are separated.

## Diagnostic Score

Score harshly. The reviewer should behave like a skeptical internal committee member who is trying to find submission-exclusion risk, overclaiming, weak evidence, and operational ambiguity before giving credit.

| Category | Points |
|---|---:|
| Internal usefulness | 25 |
| Technical depth | 25 |
| Evidence rigor | 20 |
| Paper clarity | 15 |
| Reproducibility | 10 |
| Future work | 5 |

## Decision bands

- `90-100`: Strong accept if format gate passes and claims are well sourced.
- `80-89`: Accept with minor risks.
- `70-79`: Weak accept; improve evidence or clarity.
- `<70`: Reject or major rewrite.

## Strict score caps

- Maximum `89` if any important metric lacks a source path, split definition, or scope label.
- Maximum `84` if operational evidence and generated/synthetic benchmark evidence could be confused.
- Maximum `79` if the work is technically valid but the manufacturing usefulness is not concrete.
- Maximum `74` if a key figure or table is decorative rather than needed for a claim.
- Reject regardless of score if the template, page range, citations, abstract, or title rules materially fail.

## Cold-review checks

- Under the 30/30/10/30 rubric, where does the paper lose points?
- Does the paper show a defensible new technical direction without unsupported world-first language?
- Is the originality explicit enough, or does it read like a standard model application?
- Is the impact tied to product/application/issue-resolution evidence rather than broad claims?
- Would a Samsung manufacturing reviewer understand how this helps real work?
- Is the AI method more than applying a standard model to a convenient dataset?
- Are operational evidence, synthetic benchmark evidence, and future work clearly separated?
- Are baselines and ablations described honestly?
- Does any sentence sound like unsupported promotion?
- Can each metric be traced to a source path?

## Required output

```text
Score: NN/100
Decision:
Format gate:
Most serious issue:
Top 3 required fixes:
Evidence still needed:
```
