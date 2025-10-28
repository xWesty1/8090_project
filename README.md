# Reimbursement Calculator - XGBoost

This repository contains an XGBoost-based machine learning solution for predicting travel reimbursement amounts based on trip duration, miles traveled, and receipts.

## Public cases

- **Average Error**: $19.72
- **Validation MAE**: $64.42
- **Exact Matches**: 4/1000 (0.4%)
- **Close Matches** (±$1): 68/1000 (6.8%)
- **Score**: 2071.20 (lower is better)

## Project Structure

### Core Files
- `model.py` - Main XGBoost model implementation
- `train_xgb.py` - Training script for the XGBoost model
- `xgb_model.pkl` - Pre-trained XGBoost model (521KB)
- `calculate_reimbursement.py` - Interface script for individual calculations

### Data Files
- `public_cases.json` - Training data (1,000 cases)
- `private_cases.json` - Additional test data (25,000 cases)

### Evaluation
- `eval.py` - Evaluation script for testing model performance
- `eval.sh` - Shell script for batch evaluation
- `generate_results.sh` - Results generation script

### Documentation
- `PRD.md` - Product Requirements Document
- `INTERVIEWS.md` - Interview transcripts and insights
- `README.md` - This file

## Usage

### Quick Start
```bash
# Evaluate the pre-trained model
python eval.py

# Train a new model (optional)
python train_xgb.py

# Calculate individual reimbursement
python calculate_reimbursement.py [days] [miles] [receipts]
```

### Example Usage
```python
from model import reimbursement

# Calculate reimbursement for a 5-day trip
amount = reimbursement(days=5, miles=850, receipts=750.50)
print(f"Reimbursement: ${amount:.2f}")
```

### XGBoost Features
The model uses 29 engineered features including:
- **Basic inputs**: days, miles, receipts
- **Derived ratios**: miles_per_day, receipts_per_day
- **Interactions**: days×miles, days×receipts, miles×receipts
- **Transformations**: polynomial, logarithmic, square root
- **Categories**: trip length, mileage, spending levels
- **Patterns**: special receipt endings (.49, .99), efficiency scores
- **Business rules**: per diem estimates, mileage estimates

### Model Configuration
```python
params = {
    'objective': 'reg:squarederror',
    'max_depth': 8,
    'learning_rate': 0.1,
    'subsample': 0.9,
    'colsample_bytree': 0.9,
    'min_child_weight': 3,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'n_jobs': -1
}
```

## Model Performance

### Key Improvements
- **Speed**: Evaluation completes in seconds (vs. minutes with ensemble)
- **Accuracy**: 81% reduction in average error vs. rule-based approach
- **Robustness**: Handles edge cases better than manual rules

### Challenging Cases
The model still struggles with some extreme cases:
- Very short trips (1 day) with high mileage/receipts
- Long trips (10+ days) with unusual spending patterns
- Cases with receipt amounts ending in .49 or .99 (legacy system bug)

## Requirements

```bash
pip install xgboost scikit-learn numpy pandas
```
---

**Note**: Below are the original instructions for the challenge
=======
# Top Coder Challenge: Black Box Legacy Reimbursement System

**Reverse-engineer a 60-year-old travel reimbursement system using only historical data and employee interviews.**

ACME Corp's legacy reimbursement system has been running for 60 years. No one knows how it works, but it's still used daily.

8090 has built them a new system, but ACME Corp is confused by the differences in results. Your mission is to figure out the original business logic so we can explain why ours is different and better.

Your job: create a perfect replica of the legacy system by reverse-engineering its behavior from 1,000 historical input/output examples and employee interviews.

## What You Have

### Input Parameters

The system takes three inputs:

- `trip_duration_days` - Number of days spent traveling (integer)
- `miles_traveled` - Total miles traveled (integer)
- `total_receipts_amount` - Total dollar amount of receipts (float)

## Documentation

- A PRD (Product Requirements Document)
- Employee interviews with system hints

### Output

- Single numeric reimbursement amount (float, rounded to 2 decimal places)

### Historical Data

- `public_cases.json` - 1,000 historical input/output examples

## Getting Started

1. **Analyze the data**: 
   - Look at `public_cases.json` to understand patterns
   - Look at `PRD.md` to understand the business problem
   - Look at `INTERVIEWS.md` to understand the business logic
2. **Create your implementation**:
   - Copy `run.sh.template` to `run.sh`
   - Implement your calculation logic
   - Make sure it outputs just the reimbursement amount
3. **Test your solution**: 
   - Run `./eval.sh` to see how you're doing
   - Use the feedback to improve your algorithm
4. **Submit**:
   - Run `./generate_results.sh` to get your final results.
   - Add `arjun-krishna1` to your repo.
   - Complete [the submission form](https://forms.gle/sKFBV2sFo2ADMcRt8).

## Implementation Requirements

Your `run.sh` script must:

- Take exactly 3 parameters: `trip_duration_days`, `miles_traveled`, `total_receipts_amount`
- Output a single number (the reimbursement amount)
- Run in under 5 seconds per test case
- Work without external dependencies (no network calls, databases, etc.)

Example:

```bash
./run.sh 5 250 150.75
# Should output something like: 487.25
```

## Evaluation

Run `./eval.sh` to test your solution against all 1,000 cases. The script will show:

- **Exact matches**: Cases within ±$0.01 of the expected output
- **Close matches**: Cases within ±$1.00 of the expected output
- **Average error**: Mean absolute difference from expected outputs
- **Score**: Lower is better (combines accuracy and precision)

Your submission will be tested against `private_cases.json` which does not include the outputs.

## Submission

When you're ready to submit:

1. Push your solution to a GitHub repository
2. Add `arjun-krishna1` to your repository
3. Submit via the [submission form](https://forms.gle/sKFBV2sFo2ADMcRt8).
4. When you submit the form you will submit your `private_results.txt` which will be used for your final score.

---

**Good luck and Bon Voyage!**
>>>>>>> 1f0bd29bcce8e279602380130ef73924d2c83951
