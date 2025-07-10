#!/usr/bin/env python3
"""
Script to import the converted pincode CSV into the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import PincodeData
from pincode_utils import import_pincode_csv, bulk_import_pincodes

def import_converted_pincodes():
    """Import the converted pincode CSV into the database"""
    with app.app_context():
        csv_file = "converted_indian_pincodes.csv"
        
        if not os.path.exists(csv_file):
            print(f"✗ Converted CSV file not found: {csv_file}")
            return False
        
        print(f"Importing pincodes from {csv_file}...")
        
        try:
            # Import the converted CSV
            pincode_data = import_pincode_csv(csv_file)
            print(f"✓ Loaded {len(pincode_data)} pincode records from CSV")
            
            if pincode_data:
                # Import into database
                success = bulk_import_pincodes(pincode_data)
                if success:
                    print(f"✓ Successfully imported {len(pincode_data)} pincodes to database")
                    
                    # Show some statistics
                    total_pincodes = PincodeData.query.count()
                    serviceable_pincodes = PincodeData.query.filter_by(is_serviceable=True).count()
                    states_count = db.session.query(PincodeData.state_name).distinct().count()
                    
                    print(f"\nDatabase Statistics:")
                    print(f"  - Total pincodes: {total_pincodes}")
                    print(f"  - Serviceable pincodes: {serviceable_pincodes}")
                    print(f"  - States covered: {states_count}")
                    
                    return True
                else:
                    print("✗ Error importing pincodes to database")
                    return False
            else:
                print("✗ No pincode data to import")
                return False
                
        except Exception as e:
            print(f"✗ Error importing pincodes: {e}")
            return False

if __name__ == "__main__":
    print("Importing converted pincode data...")
    success = import_converted_pincodes()
    if success:
        print("✓ Pincode import completed successfully!")
    else:
        print("✗ Pincode import failed!")
        sys.exit(1) 