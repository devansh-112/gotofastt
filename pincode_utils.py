import csv
import io
import logging
from models import PincodeData, db
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime

def scrape_indian_pincodes():
    """
    Scrape Indian pincode data from reliable sources
    Returns a list of dictionaries with pincode data
    """
    pincode_data = []
    
    # Source 1: India Post API (if available)
    try:
        # This is a placeholder - you would need to find a reliable API
        # For now, we'll use a sample dataset
        sample_data = [
            {
                'pincode': '302001',
                'office_name': 'Jaipur GPO',
                'office_type': 'Head Post Office',
                'delivery_status': 'Delivery',
                'division_name': 'Jaipur',
                'region_name': 'Jaipur',
                'circle_name': 'Rajasthan',
                'taluk': 'Jaipur',
                'district_name': 'Jaipur',
                'state_name': 'Rajasthan'
            },
            {
                'pincode': '400001',
                'office_name': 'Mumbai GPO',
                'office_type': 'Head Post Office',
                'delivery_status': 'Delivery',
                'division_name': 'Mumbai',
                'region_name': 'Mumbai',
                'circle_name': 'Maharashtra',
                'taluk': 'Mumbai',
                'district_name': 'Mumbai',
                'state_name': 'Maharashtra'
            },
            {
                'pincode': '110001',
                'office_name': 'New Delhi GPO',
                'office_type': 'Head Post Office',
                'delivery_status': 'Delivery',
                'division_name': 'New Delhi',
                'region_name': 'New Delhi',
                'circle_name': 'Delhi',
                'taluk': 'New Delhi',
                'district_name': 'New Delhi',
                'state_name': 'Delhi'
            }
        ]
        pincode_data.extend(sample_data)
        
    except Exception as e:
        logging.error(f"Error scraping pincode data: {e}")
    
    return pincode_data

def import_pincode_csv(file_path):
    """
    Import pincode data from CSV file
    Expected CSV format: pincode,office_name,office_type,delivery_status,division_name,region_name,circle_name,taluk,district_name,state_name
    """
    pincode_data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pincode_data.append({
                    'pincode': row['pincode'].strip(),
                    'office_name': row['office_name'].strip(),
                    'office_type': row['office_type'].strip(),
                    'delivery_status': row['delivery_status'].strip(),
                    'division_name': row['division_name'].strip(),
                    'region_name': row['region_name'].strip(),
                    'circle_name': row['circle_name'].strip(),
                    'taluk': row['taluk'].strip(),
                    'district_name': row['district_name'].strip(),
                    'state_name': row['state_name'].strip()
                })
    except Exception as e:
        logging.error(f"Error importing CSV file: {e}")
        return []
    
    return pincode_data

def bulk_import_pincodes(pincode_list):
    """
    Bulk import pincode data into database
    """
    success_count = 0
    error_count = 0
    
    for pincode_data in pincode_list:
        try:
            # Check if pincode already exists
            existing = PincodeData.get_by_pincode(pincode_data['pincode'])
            if existing:
                # Update existing record
                for key, value in pincode_data.items():
                    setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
            else:
                # Create new record
                new_pincode = PincodeData(**pincode_data)
                db.session.add(new_pincode)
            
            success_count += 1
            
        except IntegrityError as e:
            error_count += 1
            logging.error(f"Integrity error for pincode {pincode_data.get('pincode', 'unknown')}: {e}")
        except Exception as e:
            error_count += 1
            logging.error(f"Error importing pincode {pincode_data.get('pincode', 'unknown')}: {e}")
    
    try:
        db.session.commit()
        logging.info(f"Successfully imported {success_count} pincodes, {error_count} errors")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error committing pincode data: {e}")
        return False
    
    return True

def generate_sample_pincode_csv():
    """
    Generate a sample CSV file with Indian pincode data
    This is a comprehensive sample dataset
    """
    sample_data = [
        # Rajasthan
        {'pincode': '302001', 'office_name': 'Jaipur GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jaipur', 'region_name': 'Jaipur', 'circle_name': 'Rajasthan', 'taluk': 'Jaipur', 'district_name': 'Jaipur', 'state_name': 'Rajasthan'},
        {'pincode': '302002', 'office_name': 'Jaipur Collectorate', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jaipur', 'region_name': 'Jaipur', 'circle_name': 'Rajasthan', 'taluk': 'Jaipur', 'district_name': 'Jaipur', 'state_name': 'Rajasthan'},
        {'pincode': '302003', 'office_name': 'Jaipur University', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jaipur', 'region_name': 'Jaipur', 'circle_name': 'Rajasthan', 'taluk': 'Jaipur', 'district_name': 'Jaipur', 'state_name': 'Rajasthan'},
        {'pincode': '302004', 'office_name': 'Jaipur Medical College', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jaipur', 'region_name': 'Jaipur', 'circle_name': 'Rajasthan', 'taluk': 'Jaipur', 'district_name': 'Jaipur', 'state_name': 'Rajasthan'},
        {'pincode': '302005', 'office_name': 'Jaipur Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jaipur', 'region_name': 'Jaipur', 'circle_name': 'Rajasthan', 'taluk': 'Jaipur', 'district_name': 'Jaipur', 'state_name': 'Rajasthan'},
        
        # Delhi
        {'pincode': '110001', 'office_name': 'New Delhi GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'New Delhi', 'region_name': 'New Delhi', 'circle_name': 'Delhi', 'taluk': 'New Delhi', 'district_name': 'New Delhi', 'state_name': 'Delhi'},
        {'pincode': '110002', 'office_name': 'New Delhi Parliament House', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'New Delhi', 'region_name': 'New Delhi', 'circle_name': 'Delhi', 'taluk': 'New Delhi', 'district_name': 'New Delhi', 'state_name': 'Delhi'},
        {'pincode': '110003', 'office_name': 'New Delhi Supreme Court', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'New Delhi', 'region_name': 'New Delhi', 'circle_name': 'Delhi', 'taluk': 'New Delhi', 'district_name': 'New Delhi', 'state_name': 'Delhi'},
        
        # Maharashtra
        {'pincode': '400001', 'office_name': 'Mumbai GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Mumbai', 'region_name': 'Mumbai', 'circle_name': 'Maharashtra', 'taluk': 'Mumbai', 'district_name': 'Mumbai', 'state_name': 'Maharashtra'},
        {'pincode': '400002', 'office_name': 'Mumbai Fort', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Mumbai', 'region_name': 'Mumbai', 'circle_name': 'Maharashtra', 'taluk': 'Mumbai', 'district_name': 'Mumbai', 'state_name': 'Maharashtra'},
        {'pincode': '400003', 'office_name': 'Mumbai Ballard Estate', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Mumbai', 'region_name': 'Mumbai', 'circle_name': 'Maharashtra', 'taluk': 'Mumbai', 'district_name': 'Mumbai', 'state_name': 'Maharashtra'},
        
        # Karnataka
        {'pincode': '560001', 'office_name': 'Bangalore GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Bangalore', 'region_name': 'Bangalore', 'circle_name': 'Karnataka', 'taluk': 'Bangalore', 'district_name': 'Bangalore', 'state_name': 'Karnataka'},
        {'pincode': '560002', 'office_name': 'Bangalore Cantonment', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Bangalore', 'region_name': 'Bangalore', 'circle_name': 'Karnataka', 'taluk': 'Bangalore', 'district_name': 'Bangalore', 'state_name': 'Karnataka'},
        
        # Tamil Nadu
        {'pincode': '600001', 'office_name': 'Chennai GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Chennai', 'region_name': 'Chennai', 'circle_name': 'Tamil Nadu', 'taluk': 'Chennai', 'district_name': 'Chennai', 'state_name': 'Tamil Nadu'},
        {'pincode': '600002', 'office_name': 'Chennai Fort', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Chennai', 'region_name': 'Chennai', 'circle_name': 'Tamil Nadu', 'taluk': 'Chennai', 'district_name': 'Chennai', 'state_name': 'Tamil Nadu'},
        
        # West Bengal
        {'pincode': '700001', 'office_name': 'Kolkata GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kolkata', 'region_name': 'Kolkata', 'circle_name': 'West Bengal', 'taluk': 'Kolkata', 'district_name': 'Kolkata', 'state_name': 'West Bengal'},
        {'pincode': '700002', 'office_name': 'Kolkata Dalhousie', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kolkata', 'region_name': 'Kolkata', 'circle_name': 'West Bengal', 'taluk': 'Kolkata', 'district_name': 'Kolkata', 'state_name': 'West Bengal'},
        
        # Gujarat
        {'pincode': '380001', 'office_name': 'Ahmedabad GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ahmedabad', 'region_name': 'Ahmedabad', 'circle_name': 'Gujarat', 'taluk': 'Ahmedabad', 'district_name': 'Ahmedabad', 'state_name': 'Gujarat'},
        {'pincode': '380002', 'office_name': 'Ahmedabad Ellis Bridge', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ahmedabad', 'region_name': 'Ahmedabad', 'circle_name': 'Gujarat', 'taluk': 'Ahmedabad', 'district_name': 'Ahmedabad', 'state_name': 'Gujarat'},
        
        # Uttar Pradesh
        {'pincode': '226001', 'office_name': 'Lucknow GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Lucknow', 'region_name': 'Lucknow', 'circle_name': 'Uttar Pradesh', 'taluk': 'Lucknow', 'district_name': 'Lucknow', 'state_name': 'Uttar Pradesh'},
        {'pincode': '226002', 'office_name': 'Lucknow Hazratganj', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Lucknow', 'region_name': 'Lucknow', 'circle_name': 'Uttar Pradesh', 'taluk': 'Lucknow', 'district_name': 'Lucknow', 'state_name': 'Uttar Pradesh'},
        
        # Andhra Pradesh
        {'pincode': '500001', 'office_name': 'Hyderabad GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Hyderabad', 'region_name': 'Hyderabad', 'circle_name': 'Andhra Pradesh', 'taluk': 'Hyderabad', 'district_name': 'Hyderabad', 'state_name': 'Andhra Pradesh'},
        {'pincode': '500002', 'office_name': 'Hyderabad Abids', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Hyderabad', 'region_name': 'Hyderabad', 'circle_name': 'Andhra Pradesh', 'taluk': 'Hyderabad', 'district_name': 'Hyderabad', 'state_name': 'Andhra Pradesh'},
        
        # Kerala
        {'pincode': '682001', 'office_name': 'Kochi GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kochi', 'region_name': 'Kochi', 'circle_name': 'Kerala', 'taluk': 'Kochi', 'district_name': 'Kochi', 'state_name': 'Kerala'},
        {'pincode': '682002', 'office_name': 'Kochi Fort', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kochi', 'region_name': 'Kochi', 'circle_name': 'Kerala', 'taluk': 'Kochi', 'district_name': 'Kochi', 'state_name': 'Kerala'},
        
        # Punjab
        {'pincode': '141001', 'office_name': 'Ludhiana GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ludhiana', 'region_name': 'Ludhiana', 'circle_name': 'Punjab', 'taluk': 'Ludhiana', 'district_name': 'Ludhiana', 'state_name': 'Punjab'},
        {'pincode': '141002', 'office_name': 'Ludhiana Civil Lines', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ludhiana', 'region_name': 'Ludhiana', 'circle_name': 'Punjab', 'taluk': 'Ludhiana', 'district_name': 'Ludhiana', 'state_name': 'Punjab'},
        
        # Haryana
        {'pincode': '122001', 'office_name': 'Gurgaon GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Gurgaon', 'region_name': 'Gurgaon', 'circle_name': 'Haryana', 'taluk': 'Gurgaon', 'district_name': 'Gurgaon', 'state_name': 'Haryana'},
        {'pincode': '122002', 'office_name': 'Gurgaon Civil Lines', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Gurgaon', 'region_name': 'Gurgaon', 'circle_name': 'Haryana', 'taluk': 'Gurgaon', 'district_name': 'Gurgaon', 'state_name': 'Haryana'},
        
        # Madhya Pradesh
        {'pincode': '452001', 'office_name': 'Indore GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Indore', 'region_name': 'Indore', 'circle_name': 'Madhya Pradesh', 'taluk': 'Indore', 'district_name': 'Indore', 'state_name': 'Madhya Pradesh'},
        {'pincode': '452002', 'office_name': 'Indore Central', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Indore', 'region_name': 'Indore', 'circle_name': 'Madhya Pradesh', 'taluk': 'Indore', 'district_name': 'Indore', 'state_name': 'Madhya Pradesh'},
        
        # Bihar
        {'pincode': '800001', 'office_name': 'Patna GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Patna', 'region_name': 'Patna', 'circle_name': 'Bihar', 'taluk': 'Patna', 'district_name': 'Patna', 'state_name': 'Bihar'},
        {'pincode': '800002', 'office_name': 'Patna Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Patna', 'region_name': 'Patna', 'circle_name': 'Bihar', 'taluk': 'Patna', 'district_name': 'Patna', 'state_name': 'Bihar'},
        
        # Odisha
        {'pincode': '751001', 'office_name': 'Bhubaneswar GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Bhubaneswar', 'region_name': 'Bhubaneswar', 'circle_name': 'Odisha', 'taluk': 'Bhubaneswar', 'district_name': 'Bhubaneswar', 'state_name': 'Odisha'},
        {'pincode': '751002', 'office_name': 'Bhubaneswar Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Bhubaneswar', 'region_name': 'Bhubaneswar', 'circle_name': 'Odisha', 'taluk': 'Bhubaneswar', 'district_name': 'Bhubaneswar', 'state_name': 'Odisha'},
        
        # Assam
        {'pincode': '781001', 'office_name': 'Guwahati GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Guwahati', 'region_name': 'Guwahati', 'circle_name': 'Assam', 'taluk': 'Guwahati', 'district_name': 'Guwahati', 'state_name': 'Assam'},
        {'pincode': '781002', 'office_name': 'Guwahati Fancy Bazar', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Guwahati', 'region_name': 'Guwahati', 'circle_name': 'Assam', 'taluk': 'Guwahati', 'district_name': 'Guwahati', 'state_name': 'Assam'},
        
        # Jharkhand
        {'pincode': '834001', 'office_name': 'Ranchi GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ranchi', 'region_name': 'Ranchi', 'circle_name': 'Jharkhand', 'taluk': 'Ranchi', 'district_name': 'Ranchi', 'state_name': 'Jharkhand'},
        {'pincode': '834002', 'office_name': 'Ranchi Civil Lines', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Ranchi', 'region_name': 'Ranchi', 'circle_name': 'Jharkhand', 'taluk': 'Ranchi', 'district_name': 'Ranchi', 'state_name': 'Jharkhand'},
        
        # Chhattisgarh
        {'pincode': '492001', 'office_name': 'Raipur GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Raipur', 'region_name': 'Raipur', 'circle_name': 'Chhattisgarh', 'taluk': 'Raipur', 'district_name': 'Raipur', 'state_name': 'Chhattisgarh'},
        {'pincode': '492002', 'office_name': 'Raipur Civil Lines', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Raipur', 'region_name': 'Raipur', 'circle_name': 'Chhattisgarh', 'taluk': 'Raipur', 'district_name': 'Raipur', 'state_name': 'Chhattisgarh'},
        
        # Uttarakhand
        {'pincode': '248001', 'office_name': 'Dehradun GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Dehradun', 'region_name': 'Dehradun', 'circle_name': 'Uttarakhand', 'taluk': 'Dehradun', 'district_name': 'Dehradun', 'state_name': 'Uttarakhand'},
        {'pincode': '248002', 'office_name': 'Dehradun Civil Lines', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Dehradun', 'region_name': 'Dehradun', 'circle_name': 'Uttarakhand', 'taluk': 'Dehradun', 'district_name': 'Dehradun', 'state_name': 'Uttarakhand'},
        
        # Himachal Pradesh
        {'pincode': '171001', 'office_name': 'Shimla GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Shimla', 'region_name': 'Shimla', 'circle_name': 'Himachal Pradesh', 'taluk': 'Shimla', 'district_name': 'Shimla', 'state_name': 'Himachal Pradesh'},
        {'pincode': '171002', 'office_name': 'Shimla Mall Road', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Shimla', 'region_name': 'Shimla', 'circle_name': 'Himachal Pradesh', 'taluk': 'Shimla', 'district_name': 'Shimla', 'state_name': 'Himachal Pradesh'},
        
        # Goa
        {'pincode': '403001', 'office_name': 'Panaji GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Panaji', 'region_name': 'Panaji', 'circle_name': 'Goa', 'taluk': 'Panaji', 'district_name': 'Panaji', 'state_name': 'Goa'},
        {'pincode': '403002', 'office_name': 'Panaji Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Panaji', 'region_name': 'Panaji', 'circle_name': 'Goa', 'taluk': 'Panaji', 'district_name': 'Panaji', 'state_name': 'Goa'},
        
        # Manipur
        {'pincode': '795001', 'office_name': 'Imphal GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Imphal', 'region_name': 'Imphal', 'circle_name': 'Manipur', 'taluk': 'Imphal', 'district_name': 'Imphal', 'state_name': 'Manipur'},
        {'pincode': '795002', 'office_name': 'Imphal Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Imphal', 'region_name': 'Imphal', 'circle_name': 'Manipur', 'taluk': 'Imphal', 'district_name': 'Imphal', 'state_name': 'Manipur'},
        
        # Meghalaya
        {'pincode': '793001', 'office_name': 'Shillong GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Shillong', 'region_name': 'Shillong', 'circle_name': 'Meghalaya', 'taluk': 'Shillong', 'district_name': 'Shillong', 'state_name': 'Meghalaya'},
        {'pincode': '793002', 'office_name': 'Shillong Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Shillong', 'region_name': 'Shillong', 'circle_name': 'Meghalaya', 'taluk': 'Shillong', 'district_name': 'Shillong', 'state_name': 'Meghalaya'},
        
        # Nagaland
        {'pincode': '797001', 'office_name': 'Kohima GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kohima', 'region_name': 'Kohima', 'circle_name': 'Nagaland', 'taluk': 'Kohima', 'district_name': 'Kohima', 'state_name': 'Nagaland'},
        {'pincode': '797002', 'office_name': 'Kohima Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kohima', 'region_name': 'Kohima', 'circle_name': 'Nagaland', 'taluk': 'Kohima', 'district_name': 'Kohima', 'state_name': 'Nagaland'},
        
        # Tripura
        {'pincode': '799001', 'office_name': 'Agartala GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Agartala', 'region_name': 'Agartala', 'circle_name': 'Tripura', 'taluk': 'Agartala', 'district_name': 'Agartala', 'state_name': 'Tripura'},
        {'pincode': '799002', 'office_name': 'Agartala Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Agartala', 'region_name': 'Agartala', 'circle_name': 'Tripura', 'taluk': 'Agartala', 'district_name': 'Agartala', 'state_name': 'Tripura'},
        
        # Mizoram
        {'pincode': '796001', 'office_name': 'Aizawl GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Aizawl', 'region_name': 'Aizawl', 'circle_name': 'Mizoram', 'taluk': 'Aizawl', 'district_name': 'Aizawl', 'state_name': 'Mizoram'},
        {'pincode': '796002', 'office_name': 'Aizawl Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Aizawl', 'region_name': 'Aizawl', 'circle_name': 'Mizoram', 'taluk': 'Aizawl', 'district_name': 'Aizawl', 'state_name': 'Mizoram'},
        
        # Arunachal Pradesh
        {'pincode': '791001', 'office_name': 'Itanagar GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Itanagar', 'region_name': 'Itanagar', 'circle_name': 'Arunachal Pradesh', 'taluk': 'Itanagar', 'district_name': 'Itanagar', 'state_name': 'Arunachal Pradesh'},
        {'pincode': '791002', 'office_name': 'Itanagar Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Itanagar', 'region_name': 'Itanagar', 'circle_name': 'Arunachal Pradesh', 'taluk': 'Itanagar', 'district_name': 'Itanagar', 'state_name': 'Arunachal Pradesh'},
        
        # Sikkim
        {'pincode': '737101', 'office_name': 'Gangtok GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Gangtok', 'region_name': 'Gangtok', 'circle_name': 'Sikkim', 'taluk': 'Gangtok', 'district_name': 'Gangtok', 'state_name': 'Sikkim'},
        {'pincode': '737102', 'office_name': 'Gangtok Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Gangtok', 'region_name': 'Gangtok', 'circle_name': 'Sikkim', 'taluk': 'Gangtok', 'district_name': 'Gangtok', 'state_name': 'Sikkim'},
        
        # Telangana
        {'pincode': '500001', 'office_name': 'Hyderabad GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Hyderabad', 'region_name': 'Hyderabad', 'circle_name': 'Telangana', 'taluk': 'Hyderabad', 'district_name': 'Hyderabad', 'state_name': 'Telangana'},
        {'pincode': '500002', 'office_name': 'Hyderabad Abids', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Hyderabad', 'region_name': 'Hyderabad', 'circle_name': 'Telangana', 'taluk': 'Hyderabad', 'district_name': 'Hyderabad', 'state_name': 'Telangana'},
        
        # Jammu and Kashmir
        {'pincode': '180001', 'office_name': 'Jammu GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jammu', 'region_name': 'Jammu', 'circle_name': 'Jammu and Kashmir', 'taluk': 'Jammu', 'district_name': 'Jammu', 'state_name': 'Jammu and Kashmir'},
        {'pincode': '180002', 'office_name': 'Jammu Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Jammu', 'region_name': 'Jammu', 'circle_name': 'Jammu and Kashmir', 'taluk': 'Jammu', 'district_name': 'Jammu', 'state_name': 'Jammu and Kashmir'},
        
        # Ladakh
        {'pincode': '194101', 'office_name': 'Leh GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Leh', 'region_name': 'Leh', 'circle_name': 'Ladakh', 'taluk': 'Leh', 'district_name': 'Leh', 'state_name': 'Ladakh'},
        {'pincode': '194102', 'office_name': 'Leh Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Leh', 'region_name': 'Leh', 'circle_name': 'Ladakh', 'taluk': 'Leh', 'district_name': 'Leh', 'state_name': 'Ladakh'},
        
        # Andaman and Nicobar Islands
        {'pincode': '744101', 'office_name': 'Port Blair GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Port Blair', 'region_name': 'Port Blair', 'circle_name': 'Andaman and Nicobar Islands', 'taluk': 'Port Blair', 'district_name': 'Port Blair', 'state_name': 'Andaman and Nicobar Islands'},
        {'pincode': '744102', 'office_name': 'Port Blair Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Port Blair', 'region_name': 'Port Blair', 'circle_name': 'Andaman and Nicobar Islands', 'taluk': 'Port Blair', 'district_name': 'Port Blair', 'state_name': 'Andaman and Nicobar Islands'},
        
        # Dadra and Nagar Haveli and Daman and Diu
        {'pincode': '396001', 'office_name': 'Silvassa GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Silvassa', 'region_name': 'Silvassa', 'circle_name': 'Dadra and Nagar Haveli and Daman and Diu', 'taluk': 'Silvassa', 'district_name': 'Silvassa', 'state_name': 'Dadra and Nagar Haveli and Daman and Diu'},
        {'pincode': '396002', 'office_name': 'Silvassa Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Silvassa', 'region_name': 'Silvassa', 'circle_name': 'Dadra and Nagar Haveli and Daman and Diu', 'taluk': 'Silvassa', 'district_name': 'Silvassa', 'state_name': 'Dadra and Nagar Haveli and Daman and Diu'},
        
        # Lakshadweep
        {'pincode': '682551', 'office_name': 'Kavaratti GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kavaratti', 'region_name': 'Kavaratti', 'circle_name': 'Lakshadweep', 'taluk': 'Kavaratti', 'district_name': 'Kavaratti', 'state_name': 'Lakshadweep'},
        {'pincode': '682552', 'office_name': 'Kavaratti Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Kavaratti', 'region_name': 'Kavaratti', 'circle_name': 'Lakshadweep', 'taluk': 'Kavaratti', 'district_name': 'Kavaratti', 'state_name': 'Lakshadweep'},
        
        # Puducherry
        {'pincode': '605001', 'office_name': 'Puducherry GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Puducherry', 'region_name': 'Puducherry', 'circle_name': 'Puducherry', 'taluk': 'Puducherry', 'district_name': 'Puducherry', 'state_name': 'Puducherry'},
        {'pincode': '605002', 'office_name': 'Puducherry Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Puducherry', 'region_name': 'Puducherry', 'circle_name': 'Puducherry', 'taluk': 'Puducherry', 'district_name': 'Puducherry', 'state_name': 'Puducherry'},
        
        # Chandigarh
        {'pincode': '160001', 'office_name': 'Chandigarh GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'Chandigarh', 'region_name': 'Chandigarh', 'circle_name': 'Chandigarh', 'taluk': 'Chandigarh', 'district_name': 'Chandigarh', 'state_name': 'Chandigarh'},
        {'pincode': '160002', 'office_name': 'Chandigarh Secretariat', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'Chandigarh', 'region_name': 'Chandigarh', 'circle_name': 'Chandigarh', 'taluk': 'Chandigarh', 'district_name': 'Chandigarh', 'state_name': 'Chandigarh'},
        
        # NCT of Delhi
        {'pincode': '110001', 'office_name': 'New Delhi GPO', 'office_type': 'Head Post Office', 'delivery_status': 'Delivery', 'division_name': 'New Delhi', 'region_name': 'New Delhi', 'circle_name': 'NCT of Delhi', 'taluk': 'New Delhi', 'district_name': 'New Delhi', 'state_name': 'NCT of Delhi'},
        {'pincode': '110002', 'office_name': 'New Delhi Parliament House', 'office_type': 'Sub Post Office', 'delivery_status': 'Delivery', 'division_name': 'New Delhi', 'region_name': 'New Delhi', 'circle_name': 'NCT of Delhi', 'taluk': 'New Delhi', 'district_name': 'New Delhi', 'state_name': 'NCT of Delhi'}
    ]
    
    # Create CSV file
    csv_filename = 'indian_pincodes_sample.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['pincode', 'office_name', 'office_type', 'delivery_status', 'division_name', 'region_name', 'circle_name', 'taluk', 'district_name', 'state_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in sample_data:
            writer.writerow(data)
    
    print(f"Sample CSV file created: {csv_filename}")
    return csv_filename

def validate_pincode_format(pincode):
    """
    Validate pincode format (6 digits)
    """
    if not pincode:
        return False
    return len(str(pincode)) == 6 and str(pincode).isdigit()

def get_pincode_info(pincode):
    """
    Get pincode information from database
    """
    if not validate_pincode_format(pincode):
        return None
    
    pincode_data = PincodeData.get_by_pincode(str(pincode))
    if pincode_data:
        return pincode_data.to_dict()
    return None

def search_pincodes_by_district(district_name):
    """
    Search pincodes by district name
    """
    pincodes = PincodeData.search_by_district(district_name)
    return [pincode.to_dict() for pincode in pincodes]

def search_pincodes_by_state(state_name):
    """
    Search pincodes by state name
    """
    pincodes = PincodeData.search_by_state(state_name)
    return [pincode.to_dict() for pincode in pincodes]

def get_all_states():
    """
    Get all unique states from database
    """
    states = db.session.query(PincodeData.state_name).distinct().all()
    return [state[0] for state in states if state[0]]

def get_districts_by_state(state_name):
    """
    Get all districts for a given state
    """
    districts = db.session.query(PincodeData.district_name).filter(
        PincodeData.state_name == state_name
    ).distinct().all()
    return [district[0] for district in districts if district[0]] 