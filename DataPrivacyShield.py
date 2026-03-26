import pandas as pd
import hashlib


class DataPrivacyShield:
    def __init__(self, data):
        """
        Initialize the class with a pandas DataFrame or a CSV file path.
        """
        if isinstance(data, str):
            self.df = pd.read_csv(data)
        elif isinstance(data, pd.DataFrame):
            self.df = data.copy()
        else:
            raise ValueError("Input must be a CSV file path or a pandas DataFrame.")

        self.original_row_count = len(self.df)
        self.processed_columns = set()  # Track columns that have been desensitized

    def encrypt_hash(self, columns):
        """
        Method 1: Hash Encryption (Irreversible).
        Best for unique, direct identifiers like National ID or User ID.
        """
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(
                    lambda x: hashlib.sha256(str(x).encode('utf-8')).hexdigest() if pd.notnull(x) else x
                )
                self.processed_columns.add(col)
        print(f"✅ Hash encryption completed for columns: {columns}")

    def encrypt_mask(self, columns, visible_chars=2):
        """
        Method 2: Masking (Partially visible).
        Best for names or phone numbers (e.g., "John" -> "Jo**").
        """
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(
                    lambda x: str(x)[:visible_chars] + '*' * max(0, len(str(x)) - visible_chars) if pd.notnull(x) else x
                )
                self.processed_columns.add(col)
        print(f"✅ Masking completed for columns: {columns}")

    def generalize_numeric(self, column, bin_size=10):
        """
        Method 3a: Numeric Generalization.
        Groups continuous numerical values into ranges/bins.
        Example: Age 32 with bin_size=10 becomes "30-40".
        """
        if column in self.df.columns:
            def to_bin(val):
                if pd.isnull(val): return val
                try:
                    lower = (int(float(val)) // bin_size) * bin_size
                    upper = lower + bin_size
                    return f"{lower}-{upper}"
                except ValueError:
                    return val  # Return original if conversion fails

            self.df[column] = self.df[column].apply(to_bin)
            self.processed_columns.add(column)
            print(f"✅ Numeric generalization completed for '{column}' (Bin size: {bin_size})")

    def generalize_string(self, column, keep_left=2):
        """
        Method 3b: String Generalization (Hierarchy reduction).
        Replaces specific string details with broader categories using wildcards.
        Example: ZipCode "100086" with keep_left=3 becomes "100***".
        """
        if column in self.df.columns:
            self.df[column] = self.df[column].apply(
                lambda x: str(x)[:keep_left] + '*' * max(0, len(str(x)) - keep_left) if pd.notnull(x) else x
            )
            self.processed_columns.add(column)
            print(f"✅ String generalization completed for '{column}' (Kept left {keep_left} chars)")

    def apply_k_anonymity(self, quasi_identifiers, k):
        """
        Method 4: K-Anonymity (Suppression).
        Ensures every combination of quasi-identifiers appears at least 'k' times.
        Rows that do not meet the 'k' threshold are suppressed (removed).
        NOTE: Apply generalization BEFORE this method to minimize data loss.
        """
        # Count frequencies of each quasi-identifier combination
        counts = self.df.groupby(quasi_identifiers).size().reset_index(name='count')

        # Filter groups that meet the k-anonymity requirement
        valid_groups = counts[counts['count'] >= k]

        # Keep only the rows that belong to valid groups
        self.df = self.df.merge(valid_groups[quasi_identifiers], on=quasi_identifiers, how='inner')
        self.processed_columns.update(quasi_identifiers)

        removed_count = self.original_row_count - len(self.df)
        print(f"✅ {k}-Anonymity applied. Suppressed (removed) {removed_count} records to meet conditions.")

    def calculate_privacy_score(self, quasi_identifiers=None):
        """
        Calculate a privacy score (0-100).
        Evaluates column protection coverage and actual K-anonymity robustness.
        """
        score = 0

        # 1. Coverage Score (50 points max)
        total_cols = len(self.df.columns)
        processed_ratio = len(self.processed_columns) / total_cols if total_cols > 0 else 0
        score += processed_ratio * 50

        # 2. Anonymity Robustness Score (50 points max)
        if quasi_identifiers and not self.df.empty:
            actual_k = self.df.groupby(quasi_identifiers).size().min()
            # Assume k=10 is the gold standard for full 50 points
            k_score = min((actual_k / 10) * 50, 50)
            score += k_score
        else:
            # Baseline score if no quasi-identifiers are defined or dataframe is empty
            score += processed_ratio * 30

        print(f"📊 Current Dataset Privacy Score: {score:.2f} / 100")
        return score

    def export_data(self, output_path):
        """
        Export the processed DataFrame to a CSV file.
        """
        self.df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"💾 Data successfully exported to: {output_path}")