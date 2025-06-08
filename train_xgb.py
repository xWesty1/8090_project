#!/usr/bin/env python3
"""
Train XGBoost model for reimbursement prediction
"""

from model import XGBoostReimbursementModel
import numpy as np

def main():
    print("🚀 Training XGBoost Reimbursement Model")
    print("=" * 50)
    
    # Initialize model
    model = XGBoostReimbursementModel()
    
    # Load data
    print("Loading training data...")
    X, y = model.load_data()
    print(f"✅ Loaded {len(X)} training samples with {len(X[0])} features each")
    
    # Train model
    mae = model.train_model(X, y)
    print(f"✅ Training complete!")
    
    # Save model
    model.save_model()
    print("✅ Model saved to 'xgb_model.pkl'")
    
    # Test on a few examples
    print("\n🧪 Testing predictions:")
    print("-" * 30)
    
    test_cases = [
        (3, 93, 1.42, 364.51),
        (1, 55, 3.6, 126.06),
        (5, 173, 1337.9, 1443.96),
        (8, 795, 1645.99, 644.69),  # Previous high-error case
        (7, 1006, 1181.33, 2279.82)  # Another high-error case
    ]
    
    total_error = 0
    for days, miles, receipts, expected in test_cases:
        pred = model.predict(days, miles, receipts)
        error = abs(pred - expected)
        total_error += error
        
        print(f"Days: {days:2}, Miles: {miles:4}, Receipts: ${receipts:7.2f}")
        print(f"  Expected: ${expected:7.2f}, Predicted: ${pred:7.2f}, Error: ${error:6.2f}")
        print()
    
    avg_error = total_error / len(test_cases)
    print(f"📊 Average error on test cases: ${avg_error:.2f}")
    print(f"📊 Validation MAE: ${mae:.2f}")
    
    print("\n✅ Ready for evaluation!")
    print("Run 'python eval.py' to test on all 1000 cases")

if __name__ == "__main__":
    main() 