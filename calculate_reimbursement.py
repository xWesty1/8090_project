#!/usr/bin/env python3
import sys
from model import reimbursement

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <trip_duration_days> <miles_traveled> <total_receipts_amount>", file=sys.stderr)
        sys.exit(1)
    
    try:
        days = int(float(sys.argv[1]))  # Handle float days input
        miles = int(float(sys.argv[2]))  # Handle float miles input  
        receipts = float(sys.argv[3])
        
        result = reimbursement(days, miles, receipts)
        print(result)
        
    except ValueError as e:
        print(f"Error: Invalid input - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 