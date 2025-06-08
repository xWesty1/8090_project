#!/usr/bin/env python3
"""
Black Box Challenge Evaluation Script (Python version)
This script tests your reimbursement calculation implementation against 1,000 historical cases
"""

import json
import subprocess
import sys
import os
from statistics import mean

def run_reimbursement(days, miles, receipts):
    """Run the reimbursement calculation using the command line interface"""
    try:
        # Try Python directly first
        result = subprocess.run([
            sys.executable, 'calculate_reimbursement.py', 
            str(days), str(miles), str(receipts)
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            raise RuntimeError(f"Script failed: {result.stderr}")
            
    except Exception as e:
        raise RuntimeError(f"Error running calculation: {e}")

def main():
    print("🧾 Black Box Challenge - Reimbursement System Evaluation")
    print("=======================================================")
    print()
    
    # Check if required files exist
    if not os.path.exists('calculate_reimbursement.py'):
        print("❌ Error: calculate_reimbursement.py not found!")
        sys.exit(1)
        
    if not os.path.exists('public_cases.json'):
        print("❌ Error: public_cases.json not found!")
        sys.exit(1)
    
    print("📊 Running evaluation against 1,000 test cases...")
    print()
    
    # Load test cases
    with open('public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    # Initialize counters
    successful_runs = 0
    exact_matches = 0
    close_matches = 0
    errors = []
    results = []
    
    num_cases = len(test_cases)
    
    # Process each test case
    for i, case in enumerate(test_cases):
        if i % 100 == 0:
            print(f"Progress: {i}/{num_cases} cases processed...")
        
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        try:
            actual = run_reimbursement(days, miles, receipts)
            error = abs(actual - expected)
            
            results.append({
                'case': i + 1,
                'expected': expected,
                'actual': actual,
                'error': error,
                'days': days,
                'miles': miles,
                'receipts': receipts
            })
            
            successful_runs += 1
            
            # Check for exact match (within $0.01)
            if error < 0.01:
                exact_matches += 1
            
            # Check for close match (within $1.00)
            if error < 1.0:
                close_matches += 1
                
        except Exception as e:
            errors.append(f"Case {i+1}: {e}")
    
    # Calculate and display results
    if successful_runs == 0:
        print("❌ No successful test cases!")
        print("\nYour script either:")
        print("  - Failed to run properly")
        print("  - Produced invalid output format")
        print("  - Timed out on all cases")
        return
    
    # Calculate statistics
    avg_error = mean(result['error'] for result in results)
    max_error_result = max(results, key=lambda r: r['error'])
    
    exact_pct = (exact_matches / successful_runs) * 100
    close_pct = (close_matches / successful_runs) * 100
    
    print("\n✅ Evaluation Complete!")
    print()
    print("📈 Results Summary:")
    print(f"  Total test cases: {num_cases}")
    print(f"  Successful runs: {successful_runs}")
    print(f"  Exact matches (±$0.01): {exact_matches} ({exact_pct:.1f}%)")
    print(f"  Close matches (±$1.00): {close_matches} ({close_pct:.1f}%)")
    print(f"  Average error: ${avg_error:.2f}")
    print(f"  Maximum error: ${max_error_result['error']:.2f}")
    print()
    
    # Calculate score (lower is better)
    score = avg_error * 100 + (num_cases - exact_matches) * 0.1
    print(f"🎯 Your Score: {score:.2f} (lower is better)")
    print()
    
    # Provide feedback
    if exact_matches == num_cases:
        print("🏆 PERFECT SCORE! You have reverse-engineered the system completely!")
    elif exact_matches > 950:
        print("🥇 Excellent! You are very close to the perfect solution.")
    elif exact_matches > 800:
        print("🥈 Great work! You have captured most of the system behavior.")
    elif exact_matches > 500:
        print("🥉 Good progress! You understand some key patterns.")
    else:
        print("📚 Keep analyzing the patterns in the interviews and test cases.")
    
    # Show high-error cases
    if exact_matches < num_cases:
        print("\n💡 Tips for improvement:")
        print("  Check these high-error cases:")
        
        # Sort by error and show top 5
        high_error_cases = sorted(results, key=lambda r: r['error'], reverse=True)[:5]
        for result in high_error_cases:
            print(f"    Case {result['case']}: {result['days']} days, {result['miles']} miles, ${result['receipts']} receipts")
            print(f"      Expected: ${result['expected']:.2f}, Got: ${result['actual']:.2f}, Error: ${result['error']:.2f}")
    
    # Show errors if any
    if errors:
        print("\n⚠️  Errors encountered:")
        for error in errors[:10]:
            print(f"  {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

if __name__ == "__main__":
    main() 