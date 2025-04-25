import pandas as pd
import numpy as np
import math
import os

class TermWeightCalculator:
    def __init__(self, csv_file):
        """Initialize with the path to the CSV file containing term frequencies."""
        self.df = pd.read_csv(csv_file)
        self.terms = self.df['term'].tolist()
        self.documents = self.df.columns[1:].tolist()
        self.N = len(self.documents)  # Total number of documents
        
        # Calculate document frequency (n_i) for each term
        self.doc_freq = {}
        for term in self.terms:
            term_row = self.df[self.df['term'] == term].iloc[0, 1:].tolist()
            self.doc_freq[term] = sum(1 for freq in term_row if freq > 0)
        
        # Calculate max frequency for each document
        self.max_freq = {}
        for doc in self.documents:
            self.max_freq[doc] = self.df[doc].max()
    
    def calculate_weight(self, term, document):
        """Calculate the weight of a term in a document using the given formula."""
        term_idx = self.df[self.df['term'] == term].index[0]
        freq_ij = self.df.at[term_idx, document]
        max_freq_j = self.max_freq[document]
        n_i = self.doc_freq[term]
        
        # Handle division by zero
        if max_freq_j == 0:
            normalized_freq = 0
        else:
            normalized_freq = freq_ij / max_freq_j
        
        # Calculate the weight using log base 2 instead of log base 10
        log_term = math.log2(self.N / n_i + 1)
        weight = normalized_freq * log_term
        
        return weight, freq_ij, max_freq_j, n_i, normalized_freq, log_term
    
    def calculate_query_weights(self, query_terms):
        """Calculate weights for query terms."""
        # Create a dictionary to store query term frequencies
        query_freq = {term: 0 for term in self.terms}
        
        # Count frequency of each term in the query
        for term in query_terms:
            if term in query_freq:
                query_freq[term] += 1
        
        # Find max frequency in query
        max_freq_q = max(query_freq.values()) if any(query_freq.values()) else 1
        
        # Calculate weights for each term
        query_weights = {}
        for term in self.terms:
            freq_iq = query_freq[term]
            n_i = self.doc_freq[term]
            
            # Handle division by zero
            if max_freq_q == 0:
                normalized_freq = 0
            else:
                normalized_freq = freq_iq / max_freq_q
            
            # Calculate the weight using log base 2
            log_term = math.log2(self.N / n_i + 1)
            weight = normalized_freq * log_term
            
            query_weights[term] = weight
        
        return query_weights
    
    def save_weights_to_csv(self, output_file="term_weights.csv", query_terms=None):
        """Save the calculated term weights to a CSV file."""
        # Create a DataFrame to store the weights
        weights_df = pd.DataFrame(index=self.terms)
        
        # Calculate weights for each term and document
        for doc in self.documents:
            weights_df[doc] = [self.calculate_weight(term, doc)[0] for term in self.terms]
        
        # Add query weights if provided
        if query_terms:
            query_weights = self.calculate_query_weights(query_terms)
            weights_df['Q'] = [query_weights[term] for term in self.terms]
        
        # Save to CSV
        weights_df.to_csv(output_file)
        print(f"Term weights saved to: {output_file}")
        return output_file
    
    def generate_latex_report(self, output_file="term_weights.tex", query_terms=None):
        """Generate a LaTeX report with calculation steps."""
        with open(output_file, 'w') as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage[utf8]{inputenc}\n")
            f.write("\\usepackage[T1]{fontenc}\n")
            f.write("\\usepackage{amsmath}\n")
            f.write("\\usepackage{booktabs}\n")
            f.write("\\usepackage{array}\n")
            f.write("\\usepackage[margin=1in]{geometry}\n")
            f.write("\\begin{document}\n\n")
            
            # Title
            f.write("\\title{Term Weight Calculation Report}\n")
            f.write("\\author{Term Weight Calculator}\n")
            f.write("\\maketitle\n\n")
            
            # Formula explanation
            f.write("\\section{Formula Used}\n")
            f.write("\\begin{equation}\n")
            f.write("w(t_i, d_j) = \\frac{freq_{ij}}{\\max\\{\\forall t_l \\in d_j\\} freq_{lj}} \\times \\log_{2}\\left(\\frac{N}{n_i} + 1\\right)\n")
            f.write("\\end{equation}\n\n")
            
            # Input data
            f.write("\\section{Input Term Frequencies}\n")
            f.write("\\begin{table}[h]\n")
            f.write("\\centering\n")
            f.write("\\begin{tabular}{l" + "c" * (len(self.documents) + 1) + "}\n")
            f.write("\\toprule\n")
            f.write("Term & " + " & ".join(self.documents) + " & Total \\\\\n")
            f.write("\\midrule\n")
            
            for term in self.terms:
                term_row = self.df[self.df['term'] == term].iloc[0, 1:].tolist()
                total_freq = sum(term_row)
                # Fix accented characters for LaTeX
                term_fixed = term.replace("utilisé", "utilis\\'{e}")
                f.write(f"{term_fixed} & " + " & ".join(str(freq) for freq in term_row) + f" & {total_freq} \\\\\n")
            
            f.write("\\bottomrule\n")
            f.write("\\end{tabular}\n")
            f.write("\\caption{Term frequencies in each document}\n")
            f.write("\\end{table}\n\n")
            
            # Query information if provided
            if query_terms:
                f.write("\\section{Query Information}\n")
                f.write(f"Query: \\{{{', '.join(query_terms)}\\}}\n\n")
                
                # Create a table for query term frequencies
                query_freq = {term: 0 for term in self.terms}
                for term in query_terms:
                    if term in query_freq:
                        query_freq[term] += 1
                
                f.write("\\begin{table}[h]\n")
                f.write("\\centering\n")
                f.write("\\begin{tabular}{lc}\n")
                f.write("\\toprule\n")
                f.write("Term & Frequency in Query \\\\\n")
                f.write("\\midrule\n")
                
                for term in self.terms:
                    term_fixed = term.replace("utilisé", "utilis\\'{e}")
                    f.write(f"{term_fixed} & {query_freq[term]} \\\\\n")
                
                f.write("\\bottomrule\n")
                f.write("\\end{tabular}\n")
                f.write("\\caption{Term frequencies in query}\n")
                f.write("\\end{table}\n\n")
            
            # Calculation steps for each term and document
            f.write("\\section{Term Weight Calculations}\n")
            
            for term in self.terms:
                # Fix accented characters for LaTeX
                term_fixed = term.replace("utilisé", "utilis\\'{e}")
                f.write(f"\\subsection{{Term: {term_fixed}}}\n")
                
                for doc in self.documents:
                    weight, freq_ij, max_freq_j, n_i, normalized_freq, log_term = self.calculate_weight(term, doc)
                    
                    f.write(f"\\subsubsection*{{For document {doc}}}\n")
                    
                    # Write the full equation with substituted values
                    f.write("\\begin{align}\n")
                    f.write(f"w({term_fixed}, {doc}) &= \\frac{{{freq_ij}}}{{{max_freq_j}}} \\times \\log_{{2}}\\left(\\frac{{{self.N}}}{{{n_i}}} + 1\\right) \\\\\n")
                    f.write(f"&= {normalized_freq:.3f} \\times {log_term:.3f} \\\\\n")
                    f.write(f"&= {weight:.3f}\n")
                    f.write("\\end{align}\n\n")
                
                # Add query weight calculation if query terms are provided
                if query_terms:
                    query_freq = {term: 0 for term in self.terms}
                    for qt in query_terms:
                        if qt in query_freq:
                            query_freq[qt] += 1
                    
                    max_freq_q = max(query_freq.values()) if any(query_freq.values()) else 1
                    freq_iq = query_freq[term]
                    n_i = self.doc_freq[term]
                    
                    if max_freq_q == 0:
                        normalized_freq = 0
                    else:
                        normalized_freq = freq_iq / max_freq_q
                    
                    log_term = math.log2(self.N / n_i + 1)
                    weight = normalized_freq * log_term
                    
                    f.write(f"\\subsubsection*{{For query Q}}\n")
                    f.write("\\begin{align}\n")
                    f.write(f"w({term_fixed}, Q) &= \\frac{{{freq_iq}}}{{{max_freq_q}}} \\times \\log_{{2}}\\left(\\frac{{{self.N}}}{{{n_i}}} + 1\\right) \\\\\n")
                    f.write(f"&= {normalized_freq:.3f} \\times {log_term:.3f} \\\\\n")
                    f.write(f"&= {weight:.3f}\n")
                    f.write("\\end{align}\n\n")
            
            # Final weights table
            f.write("\\section{Final Term Weights}\n")
            f.write("\\begin{table}[h]\n")
            f.write("\\centering\n")
            
            # Add Q to the table header if query terms are provided
            if query_terms:
                f.write("\\begin{tabular}{l" + "c" * (len(self.documents) + 1) + "}\n")
                f.write("\\toprule\n")
                f.write("Term & " + " & ".join(self.documents) + " & Q \\\\\n")
            else:
                f.write("\\begin{tabular}{l" + "c" * len(self.documents) + "}\n")
                f.write("\\toprule\n")
                f.write("Term & " + " & ".join(self.documents) + " \\\\\n")
            
            f.write("\\midrule\n")
            
            for term in self.terms:
                row = [term]
                for doc in self.documents:
                    weight, _, _, _, _, _ = self.calculate_weight(term, doc)
                    row.append(f"{weight:.3f}")
                
                # Add query weight if query terms are provided
                if query_terms:
                    query_freq = {term: 0 for term in self.terms}
                    for qt in query_terms:
                        if qt in query_freq:
                            query_freq[qt] += 1
                    
                    max_freq_q = max(query_freq.values()) if any(query_freq.values()) else 1
                    freq_iq = query_freq[term]
                    n_i = self.doc_freq[term]
                    
                    if max_freq_q == 0:
                        normalized_freq = 0
                    else:
                        normalized_freq = freq_iq / max_freq_q
                    
                    log_term = math.log2(self.N / n_i + 1)
                    weight = normalized_freq * log_term
                    row.append(f"{weight:.3f}")
                
                # Fix accented characters for LaTeX
                term_fixed = term.replace("utilisé", "utilis\\'{e}")
                f.write(" & ".join([term_fixed] + row[1:]) + " \\\\\n")
            
            f.write("\\bottomrule\n")
            f.write("\\end{tabular}\n")
            f.write("\\caption{Final term weights}\n")
            f.write("\\end{table}\n\n")
            
            f.write("\\end{document}\n")
        
        print(f"LaTeX report generated: {output_file}")
        return output_file

# Main execution
if __name__ == "__main__":
    calculator = TermWeightCalculator('term_frequencies.csv')
    
    # Define query terms
    query_terms = ['langage', 'python', 'java']
    
    # Save weights to CSV with query weights
    csv_file = calculator.save_weights_to_csv(query_terms=query_terms)
    
    # Generate LaTeX report with query information
    tex_file = calculator.generate_latex_report(query_terms=query_terms)
    
    print(f"LaTeX file created: {tex_file}")
    print(f"CSV file created: {csv_file}")
    print("To convert to PDF, run: pdflatex term_weights.tex")