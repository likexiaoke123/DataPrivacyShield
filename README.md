# DataPrivacyShield 🛡️

A lightweight and easy-to-use Python utility class designed to help data scientists and engineers apply data desensitization, anonymization, and privacy protection techniques to their datasets. Built on top of `pandas`, it allows you to process sensitive information while retaining the analytical value of your data.

## ✨ Features

* **Hash Encryption:** Irreversible SHA-256 hashing for direct identifiers (e.g., National IDs, User IDs).
* **Data Masking:** Partially hide sensitive strings (e.g., Names, Phone Numbers) by replacing characters with asterisks.
* **Data Generalization:** * *Numeric:* Group continuous numerical values into broader bins (e.g., Exact age `32` -> Age bracket `30-40`).
    * *String:* Reduce the granularity of hierarchical strings (e.g., ZipCode `100086` -> `100***`).
* **K-Anonymity (Suppression):** Ensure that every individual in the dataset cannot be distinguished from at least `k-1` other individuals based on quasi-identifiers.
* **Privacy Scoring:** Automatically calculates a basic privacy score (0-100) based on column protection coverage and the actual K-anonymity robustness.
* **Easy Export:** Instantly export the sanitized pandas DataFrame to a new CSV file.

## 📦 Requirements

* Python 3.6+
* `pandas`
* `numpy`

## 🚀 Quick Start

```python
import pandas as pd
from privacy_shield import DataPrivacyShield  # Assuming you save the class in privacy_shield.py

# 1. Load your dataset (from a CSV path or an existing DataFrame)
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'ID_Card': ['1101', '3101', '4403', '1102'],
    'Age': [32, 35, 41, 38],
    'ZipCode': ['100010', '100020', '300050', '100015']
})

# 2. Initialize the shield
shield = DataPrivacyShield(df)

# 3. Handle Direct Identifiers
shield.encrypt_hash(['ID_Card'])
shield.encrypt_mask(['Name'], visible_chars=1)

# 4. Generalize Quasi-Identifiers (Crucial before K-Anonymity)
shield.generalize_numeric('Age', bin_size=10)
shield.generalize_string('ZipCode', keep_left=3)

# 5. Apply K-Anonymity 
shield.apply_k_anonymity(quasi_identifiers=['Age', 'ZipCode'], k=2)

# 6. Score and Export
shield.calculate_privacy_score(quasi_identifiers=['Age', 'ZipCode'])
shield.export_data('secure_dataset.csv')
