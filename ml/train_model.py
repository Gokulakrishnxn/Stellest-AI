#!/usr/bin/env python3
"""
Train a lightweight logistic regression model for Stellest AI and export to JSON.
- Input CSV columns should map to the API's PatientData fields or a superset.
- Output JSON contains feature order, standardization params, coefficients, and intercept.

Usage:
  python ml/train_model.py --csv data/processed_myopia_data.csv --target will_benefit --out models/model.json

Dependencies (install locally, not on serverless):
  pip install pandas scikit-learn
"""

import argparse
import json
import os
from typing import List

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score

# Define the feature order we expect at inference time
FEATURES: List[str] = [
    'age',
    'age_myopia_diagnosis',
    'gender',
    'family_history_myopia',
    'outdoor_time',
    'screen_time',
    'previous_myopia_control',  # 0=None, 1=Drops, 2=VT, 3=Both
    'right_eye_spherical',      # Spherical power OD (D)
    'right_eye_cylinder',       # Cylinder power OD (D)  
    'left_eye_spherical',       # Spherical power OS (D)
    'left_eye_cylinder',        # Cylinder power OS (D)
    'right_eye_axial_length',   # Axial length OD (mm)
    'left_eye_axial_length',    # Axial length OS (mm)
    'keratometry_k1_re',        # Keratometry K1 right eye (diopters)
    'keratometry_k2_re',        # Keratometry K2 right eye (diopters)
    'keratometry_k1_le',        # Keratometry K1 left eye (diopters)
    'keratometry_k2_le',        # Keratometry K2 left eye (diopters)
    'new_stellest_lenses',      # 0=No, 1=Yes (considering new Stellest lenses)
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True, help='Path to input CSV with patient records')
    parser.add_argument('--target', default='will_benefit', help='Target column (0/1)')
    parser.add_argument('--out', default='models/model.json', help='Output JSON model path')
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    # Filter to known features; coerce numeric
    X = pd.DataFrame()
    for col in FEATURES:
        if col in df.columns:
            X[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            # If missing, fill with reasonable default
            X[col] = 0
    # Simple cleaning: drop rows with missing target
    y = pd.to_numeric(df[args.target], errors='coerce')
    keep_mask = y.notna() & X.notna().all(axis=1)
    X = X[keep_mask]
    y = y[keep_mask].astype(int)

    if len(X) < 10:
        raise RuntimeError('Not enough valid rows to train')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = LogisticRegression(max_iter=200, solver='lbfgs')
    clf.fit(X_train_scaled, y_train)

    # Metrics
    y_prob = clf.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)
    auc = float(roc_auc_score(y_test, y_prob))
    acc = float(accuracy_score(y_test, y_pred))

    # Export JSON model
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    model_json = {
        'feature_order': FEATURES,
        'scaler_mean': scaler.mean_.tolist(),
        'scaler_scale': scaler.scale_.tolist(),
        'coefficients': clf.coef_[0].tolist(),
        'intercept': float(clf.intercept_[0]),
        'metrics': {'auc': auc, 'accuracy': acc},
        'version': '1.0.0'
    }
    with open(args.out, 'w') as f:
        json.dump(model_json, f)

    print(f'Model saved to {args.out}')
    print(f'Holdout AUC={auc:.3f} ACC={acc:.3f}')


if __name__ == '__main__':
    main()
