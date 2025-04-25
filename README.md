# Term Weight Calculator

This project calculates term weights from document frequency data using the formula:

$w(t_i, d_j) = \frac{freq_{ij}}{max\{\forall t_l \in d_j\} freq_{lj}} * log(\frac{N}{n_i} + 1)$

Where:
- $freq_{ij}$ is the frequency of term $i$ in document $j$
- $max\{\forall t_l \in d_j\} freq_{lj}$ is the maximum frequency of any term in document $j$
- $N$ is the total number of documents
- $n_i$ is the number of documents containing term $i$

## Setup

1. Install the required dependencies: