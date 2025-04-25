# Term Weight Calculator

This project calculates term weights from document frequency data using the formula:

$w(t_i, d_j) = \frac{freq_{ij}}{max\{\forall t_l \in d_j\} freq_{lj}} * log(\frac{N}{n_i} + 1)$

Where:
- $freq_{ij}$ is the frequency of term $i$ in document $j$
- $max\{\forall t_l \in d_j\} freq_{lj}$ is the maximum frequency of any term in document $j$
- $N$ is the total number of documents
- $n_i$ is the number of documents containing term $i$

## Similarity Calculations

The similarity between a query $Q$ and a document $D_j$ can be calculated using the following formulas:

1. **Dice Similarity:**

   $ frac{2 * \sum_{i=1}^{n} w_{iq} w_{ij}}{\sum_{i=1}^{n} (w_{iq})^2 + \sum_{i=1}^{n} (w_{ij})^2} $

2. **RSV Product:**

   $sum_{i=1}^{n} w_{iq} w_{ij} $

Where:
- $w_{iq}$ is the weight of term $i$ in the query $Q$
- $w_{ij}$ is the weight of term $i$ in the document $D_j$

For example, for a query $Q$ containing the terms: {language, python, java}, the weights can be calculated and used in the above formulas to determine the similarity with each document.

## Setup

1. Install the required dependenciess