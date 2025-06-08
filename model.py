# Optimized reimbursement calculation using XGBoost
import json
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

class XGBoostReimbursementModel:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def load_data(self, filepath='public_cases.json'):
        """Load and preprocess the training data"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        features = []
        targets = []
        
        for case in data:
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            target = case['expected_output']
            
            feature_vec = self.create_features(days, miles, receipts)
            features.append(feature_vec)
            targets.append(target)
        
        return np.array(features), np.array(targets)
    
    def create_features(self, days, miles, receipts):
        """Create comprehensive feature set optimized for XGBoost"""
        # Basic features
        features = [days, miles, receipts]
        
        # Derived features
        miles_per_day = miles / max(days, 1)
        receipts_per_day = receipts / max(days, 1)
        
        # Interaction features
        days_miles = days * miles
        days_receipts = days * receipts
        miles_receipts = miles * receipts
        
        # Polynomial features
        days_sq = days ** 2
        miles_sq = miles ** 2
        receipts_sq = receipts ** 2
        
        # Log features (XGBoost can handle these well)
        log_days = np.log(max(days, 1))
        log_miles = np.log(max(miles, 1))
        log_receipts = np.log(max(receipts, 1))
        
        # Sqrt features
        sqrt_days = np.sqrt(days)
        sqrt_miles = np.sqrt(miles)
        sqrt_receipts = np.sqrt(receipts)
        
        # Categorical features (XGBoost handles these naturally)
        trip_length_cat = 0 if days <= 2 else (1 if days <= 5 else (2 if days <= 8 else 3))
        miles_cat = 0 if miles <= 100 else (1 if miles <= 500 else (2 if miles <= 1000 else 3))
        receipts_cat = 0 if receipts <= 50 else (1 if receipts <= 500 else (2 if receipts <= 1500 else 3))
        
        # Business rule approximations as features
        per_diem_est = days * 100
        mileage_est = miles * 0.5
        
        # Efficiency metrics
        efficiency_score = miles_per_day if miles_per_day <= 300 else 300  # Cap extreme values
        spending_intensity = receipts_per_day if receipts_per_day <= 500 else 500
        
        # Special pattern features
        high_mileage_trip = 1 if miles > 800 else 0
        high_spending_trip = 1 if receipts > 1500 else 0
        weekend_trip = 1 if days == 2 else 0
        week_trip = 1 if days == 5 else 0
        long_trip = 1 if days >= 10 else 0
        
        # Receipt patterns (from winning solution insights)
        receipts_ends_49 = 1 if f"{receipts:.2f}".endswith('.49') else 0
        receipts_ends_99 = 1 if f"{receipts:.2f}".endswith('.99') else 0
        
        # Combine all features
        all_features = [
            days, miles, receipts,  # Basic
            miles_per_day, receipts_per_day,  # Ratios
            days_miles, days_receipts, miles_receipts,  # Interactions
            days_sq, miles_sq, receipts_sq,  # Polynomials
            log_days, log_miles, log_receipts,  # Logs
            sqrt_days, sqrt_miles, sqrt_receipts,  # Square roots
            trip_length_cat, miles_cat, receipts_cat,  # Categories
            per_diem_est, mileage_est,  # Business rules
            efficiency_score, spending_intensity,  # Efficiency
            high_mileage_trip, high_spending_trip, weekend_trip, week_trip, long_trip,  # Patterns
            receipts_ends_49, receipts_ends_99  # Special receipt patterns
        ]
        
        return all_features
    
    def train_model(self, X, y):
        """Train XGBoost model with optimal parameters"""
        print("Training XGBoost model...")
        
        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # XGBoost parameters optimized for this problem
        params = {
            'objective': 'reg:squarederror',
            'max_depth': 8,
            'learning_rate': 0.1,
            'subsample': 0.9,
            'colsample_bytree': 0.9,
            'min_child_weight': 3,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
            'random_state': 42,
            'n_jobs': -1
        }
        
        # Create DMatrix for XGBoost
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)
        
        # Train with early stopping
        evals = [(dtrain, 'train'), (dval, 'eval')]
        self.model = xgb.train(
            params,
            dtrain,
            num_boost_round=1000,
            evals=evals,
            early_stopping_rounds=50,
            verbose_eval=False
        )
        
        # Validate performance
        val_pred = self.model.predict(dval)
        mae = mean_absolute_error(y_val, val_pred)
        print(f"XGBoost validation MAE: {mae:.2f}")
        
        self.is_trained = True
        return mae
    
    def predict(self, days, miles, receipts):
        """Fast prediction using XGBoost"""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        features = np.array(self.create_features(days, miles, receipts)).reshape(1, -1)
        dtest = xgb.DMatrix(features)
        prediction = self.model.predict(dtest)[0]
        return max(0, prediction)
    
    def save_model(self, filepath='xgb_model.pkl'):
        """Save the trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'is_trained': self.is_trained
            }, f)
    
    def load_model(self, filepath='xgb_model.pkl'):
        """Load a trained model"""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            self.model = data['model']
            self.is_trained = data['is_trained']
            return True
        except:
            return False

# Global model instance
xgb_model = XGBoostReimbursementModel()

def reimbursement(days: int, miles: int, receipts: float) -> float:
    """XGBoost-powered prediction function"""
    global xgb_model
    
    # Load model only once on first call
    if not xgb_model.is_trained:
        if not xgb_model.load_model():
            # Train new model if no saved model exists
            X, y = xgb_model.load_data()
            xgb_model.train_model(X, y)
            xgb_model.save_model()
    
    # Make prediction
    prediction = xgb_model.predict(days, miles, receipts)
    return round(prediction, 2) 