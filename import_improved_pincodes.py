#!/usr/bin/env python3
"""
Script to import improved pincode data with better district names
"""

import csv
from app import app, db
from models import PincodeData

def import_improved_pincodes():
    """Import improved pincode data with better district names"""
    
    with app.app_context():
        # Clear existing pincode data
        print("Clearing existing pincode data...")
        PincodeData.query.delete()
        db.session.commit()
        print("✓ Cleared existing data")
        
        # Import new data
        print("Importing improved pincode data...")
        count = 0
        
        with open('converted_indian_pincodes.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Convert string values to appropriate types
                pincode_data = PincodeData(
                    pincode=row['pincode'],
                    office_name=row['office_name'],
                    office_type=row['office_type'],
                    delivery_status=row['delivery_status'],
                    division_name=row['division_name'],
                    region_name=row['region_name'],
                    circle_name=row['circle_name'],
                    taluk=row['taluk'],
                    district_name=row['district_name'],
                    state_name=row['state_name'],
                    is_serviceable=True  # Default to serviceable
                )
                
                db.session.add(pincode_data)
                count += 1
                
                # Commit in batches to avoid memory issues
                if count % 1000 == 0:
                    db.session.commit()
                    print(f"Imported {count} records...")
        
        # Final commit
        db.session.commit()
        print(f"✓ Successfully imported {count} pincode records")
        
        # Verify some sample records
        print("\nSample records:")
        sample_records = PincodeData.query.limit(5).all()
        for record in sample_records:
            print(f"Pincode: {record.pincode}, Office: {record.office_name}, District: {record.district_name}, State: {record.state_name}")

if __name__ == "__main__":
    import_improved_pincodes() 