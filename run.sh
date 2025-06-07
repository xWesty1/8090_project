#!/bin/bash
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
