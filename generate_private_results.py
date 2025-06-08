#!/usr/bin/env python3
"""
Generate private results for challenge submission on Windows
"""
import json
import subprocess
import sys
import os

def main():
    print("🧾 Black Box Challenge - Generating Private Results")
    print("=" * 52)
    print()
    
    # Check if required files exist
    if not os.path.exists('private_cases.json'):
        print("❌ Error: private_cases.json not found!")
        sys.exit(1)
    
    if not os.path.exists('calculate_reimbursement.py'):
        print("❌ Error: calculate_reimbursement.py not found!")
        sys.exit(1)
    
    # Load private test cases
    print("📊 Loading private test cases...")
    with open('private_cases.json', 'r') as f:
        private_cases = json.load(f)
    
    total_cases = len(private_cases)
    print(f"📝 Processing {total_cases} test cases...")
    print()
    
    # Generate results
    results = []
    errors = 0
    
    for i, case in enumerate(private_cases):
        if i % 1000 == 0 and i > 0:
            print(f"Progress: {i}/{total_cases} cases processed...")
        
        # Extract inputs
        days = case['trip_duration_days']
        miles = case['miles_traveled']
        receipts = case['total_receipts_amount']
        
        try:
            # Run our calculation
            result = subprocess.run([
                sys.executable, 'calculate_reimbursement.py',
                str(days), str(miles), str(receipts)
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = float(result.stdout.strip())
                results.append(f"{output:.2f}")
            else:
                print(f"Error on case {i+1}: {result.stderr.strip()}")
                results.append("ERROR")
                errors += 1
                
        except Exception as e:
            print(f"Error on case {i+1}: {e}")
            results.append("ERROR")
            errors += 1
    
    # Write results to file
    with open('private_results.txt', 'w') as f:
        for result in results:
            f.write(f"{result}\n")
    
    print()
    print("✅ Results generated successfully!")
    print(f"📄 Output saved to private_results.txt")
    print(f"📊 {total_cases} cases processed")
    if errors > 0:
        print(f"⚠️  {errors} errors encountered")
    else:
        print("🎉 No errors!")
    
    print()
    print("🎯 Next steps:")
    print("  1. Check private_results.txt - it contains one result per line")
    print("  2. Each line corresponds to the same-numbered test case in private_cases.json")
    print("  3. Submit your private_results.txt file via the challenge form!")
    
    # Show sample results
    print(f"\n📈 Sample results (first 5):")
    for i in range(min(5, len(results))):
        days = private_cases[i]['trip_duration_days']
        miles = private_cases[i]['miles_traveled']
        receipts = private_cases[i]['total_receipts_amount']
        print(f"  Case {i+1}: {days} days, {miles} miles, ${receipts} → ${results[i]}")

if __name__ == "__main__":
    main() 