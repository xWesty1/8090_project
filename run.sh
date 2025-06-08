#!/bin/bash
<<<<<<< HEAD

# Black Box Challenge - Your Implementation
# This script should take three parameters and output the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Example implementations (choose one and modify):

# Example 1: Python implementation
# python3 calculate_reimbursement.py "$1" "$2" "$3"

# Example 2: Node.js implementation
# node calculate_reimbursement.js "$1" "$2" "$3"

# Example 3: Direct bash calculation (for simple logic)
# echo "scale=2; $1 * 100 + $2 * 0.5 + $3" | bc

# Python implementation using our optimized model
python3 calculate_reimbursement.py "$1" "$2" "$3" 
=======
# Simple reimbursement calculation implementation
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

python3 - "$1" "$2" "$3" <<'PY'
import sys
DAYS = float(sys.argv[1])
MILES = float(sys.argv[2])
RECEIPTS = float(sys.argv[3])
mpd = MILES / DAYS
rpd = RECEIPTS / DAYS
coef_days = -5.29162828
coef_mpd = 0.42850268
coef_rpd = 0.48292152
intercept = 121.00623854
per_day = intercept + coef_days * DAYS + coef_mpd * mpd + coef_rpd * rpd
result = per_day * DAYS
print(f"{result:.2f}")
PY
>>>>>>> 1f0bd29bcce8e279602380130ef73924d2c83951
