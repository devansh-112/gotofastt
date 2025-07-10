#!/usr/bin/env python3
"""
Script to initialize pincode data in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import PincodeData
from pincode_utils import generate_sample_pincode_csv, import_pincode_csv, bulk_import_pincodes

def init_pincode_database():
    """Initialize the database with pincode data"""
    with app.app_context():
        # Create tables
        db.create_all()
        print("✓ Database tables created")
        
        # Check if pincode data already exists
        existing_count = PincodeData.query.count()
        if existing_count > 0:
            print(f"✓ Pincode data already exists ({existing_count} records)")
            return
        
        # Generate and import sample pincode data
        print("Generating sample pincode data...")
        try:
            csv_filename = generate_sample_pincode_csv()
            print(f"✓ Sample CSV file created: {csv_filename}")
            
            # Import the generated CSV
            pincode_data = import_pincode_csv(csv_filename)
            print(f"✓ Loaded {len(pincode_data)} pincode records from CSV")
            
            if pincode_data:
                success = bulk_import_pincodes(pincode_data)
                if success:
                    print(f"✓ Successfully imported {len(pincode_data)} pincodes to database")
                else:
                    print("✗ Error importing pincodes to database")
            else:
                print("✗ No pincode data to import")
                
        except Exception as e:
            print(f"✗ Error initializing pincode data: {e}")
            return False
        
        return True

if __name__ == "__main__":
    print("Initializing pincode database...")
    success = init_pincode_database()
    if success:
        print("✓ Pincode database initialization completed successfully!")
    else:
        print("✗ Pincode database initialization failed!")
        sys.exit(1) 