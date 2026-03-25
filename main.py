import subprocess
import sys

print("=" * 50)
print("Fraud Detection Pipeline")
print("=" * 50)

steps = [
    ("Validating data...",    "src/validate_data.py"),
    ("Training model...",     "src/train_model.py"),
    ("Evaluating model...",   "src/evaluate_model.py"),
    ("Generating predictions...", "src/predict.py"),
]

for message, script in steps:
    print(f"\n{message}")
    result = subprocess.run([sys.executable, script], check=True)

print("\n Pipeline complete!")