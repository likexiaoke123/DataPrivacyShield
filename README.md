---

# DataPrivacyShield 🛡️

A lightweight and easy-to-use Python utility class designed to help users assess and improve the privacy of sensitive datasets while also making governance and compliance considerations more explicit. Built on top of `pandas`, it allows you to process sensitive information while retaining the analytical value of your data.

## ✨ Features

* **Hash Encryption:** Irreversible SHA-256 hashing for direct identifiers (e.g., National IDs, User IDs).
* **Data Masking:** Partially hide sensitive strings (e.g., Names, Phone Numbers) by replacing characters with asterisks.
* **Data Generalization:**
* *Numeric:* Group continuous numerical values into broader bins (e.g., Exact age `32` -> Age bracket `30-40`).
* *String:* Reduce the granularity of hierarchical strings (e.g., ZipCode `100086` -> `100***`).


* **K-Anonymity (Suppression):** Ensure that every individual in the dataset cannot be distinguished from at least `k-1` other individuals based on quasi-identifiers.
* **L-Diversity (Suppression):** An extension of K-Anonymity that ensures every group of quasi-identifiers contains at least `l` distinct values for a sensitive attribute, protecting against homogeneity attacks.
* **Privacy Scoring:** Automatically calculates a basic privacy score (0-100) based on column protection coverage and the actual K-anonymity robustness.
* **Easy Export:** Instantly export the sanitized pandas DataFrame to a new CSV file.

## 📦 Requirements

* Python 3.6+
* `pandas`
* `numpy`

## 🚀 Quick Start

```python
import pandas as pd
from privacy_shield import DataPrivacyShield  # Assuming you have downloaded privacy_shield.py

# 1. Load your dataset
# Included a 'Disease' column to act as our Sensitive Attribute for L-Diversity
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'ID_Card': ['1101', '3101', '4403', '1102', '5101', '6102'],
    'Age': [32, 35, 31, 38, 41, 44],
    'ZipCode': ['100010', '100020', '100030', '100015', '300050', '300055'],
    'Disease': ['Flu', 'Asthma', 'Cancer', 'Flu', 'Heart Disease', 'Diabetes']
})

# 2. Initialize the shield
shield = DataPrivacyShield(df)

# 3. Handle Direct Identifiers
shield.encrypt_hash(['ID_Card'])
shield.encrypt_mask(['Name'], visible_chars=1)

# 4. Generalize Quasi-Identifiers (Crucial before K-Anonymity)
shield.generalize_numeric('Age', bin_size=10)
shield.generalize_string('ZipCode', keep_left=3)

# Define columns for advanced privacy models
qi = ['Age', 'ZipCode']
sensitive_col = 'Disease'

# 5. Apply K-Anonymity 
# Ensures at least 2 people share the same Age bracket and ZipCode prefix
shield.apply_k_anonymity(quasi_identifiers=qi, k=2)

# 6. Apply L-Diversity
# Ensures each K-Anonymous group has at least 2 different types of diseases
shield.apply_l_diversity(quasi_identifiers=qi, sensitive_column=sensitive_col, l=2)

# 7. Score and Export
shield.calculate_privacy_score(quasi_identifiers=qi)
shield.export_data('secure_dataset.csv')

```
