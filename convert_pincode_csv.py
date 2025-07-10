#!/usr/bin/env python3
"""
Script to convert the uploaded All India Pincode CSV to our required format
"""

import csv
import sys
import os
import re

def extract_district_from_office_name(office_name, state):
    """
    Extract district name from office name using various patterns
    """
    office_name = office_name.upper()
    state = state.upper()
    
    # Common patterns for district extraction
    patterns = [
        # Pattern: "OFFICE_NAME (DISTRICT_NAME)"
        r'\(([^)]+)\)',
        # Pattern: "DISTRICT_NAME OFFICE"
        r'^([A-Z\s]+?)\s+(?:POST\s+OFFICE|GPO|HO|SO)',
        # Pattern: "OFFICE DISTRICT_NAME"
        r'(?:POST\s+OFFICE|GPO|HO|SO)\s+([A-Z\s]+)',
        # Pattern: "OFFICE_NAME, DISTRICT_NAME"
        r',\s*([A-Z\s]+)$',
        # Pattern: "DISTRICT_NAME ROAD"
        r'^([A-Z\s]+?)\s+ROAD',
        # Pattern: "ROAD DISTRICT_NAME"
        r'ROAD\s+([A-Z\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, office_name)
        if match:
            district = match.group(1).strip()
            # Clean up district name
            district = re.sub(r'\s+', ' ', district)  # Remove extra spaces
            district = district.replace('(', '').replace(')', '')  # Remove parentheses
            
            # Skip if district is same as state or too short
            if district != state and len(district) > 2:
                return district
    
    # If no pattern matches, try to extract from common keywords
    keywords = ['NAGAR', 'PUR', 'GARH', 'ABAD', 'PURAM', 'NAGAR', 'VIHAR', 'COLONY']
    words = office_name.split()
    
    for word in words:
        if any(keyword in word for keyword in keywords):
            # Check if this word is not the state name
            if word != state and len(word) > 2:
                return word
    
    # If still no match, try to extract the first meaningful word
    words = office_name.split()
    for word in words:
        # Skip common words that are not district names
        skip_words = ['POST', 'OFFICE', 'GPO', 'HO', 'SO', 'ROAD', 'STREET', 'NAGAR', 'PUR', 'GARH']
        if word not in skip_words and len(word) > 2:
            return word
    
    # Last resort: return a default based on state
    return f"{state}_DISTRICT"

def convert_pincode_csv(input_file, output_file):
    """
    Convert the uploaded CSV format to our required format
    """
    converted_data = []
    
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row_num, row in enumerate(reader, 1):
            # Skip header rows and empty rows
            if row_num <= 2 or not row or all(cell.strip() == '' for cell in row):
                continue
            
            # Extract data from the row
            # Format: POST_OFFICE_NAME, PIN_CODE, STATE
            if len(row) >= 2:
                # Find pincode and state in the row
                pincode = None
                state = None
                office_name = ""
                
                for i, cell in enumerate(row):
                    cell = cell.strip()
                    if not cell:
                        continue
                    
                    # Check if this is a 6-digit pincode
                    if cell.isdigit() and len(cell) == 6:
                        pincode = cell
                        # State should be in the next column or nearby
                        if i + 1 < len(row) and row[i + 1].strip():
                            state = row[i + 1].strip()
                        elif i + 2 < len(row) and row[i + 2].strip():
                            state = row[i + 2].strip()
                        break
                
                # If we found a pincode, process the row
                if pincode and state:
                    # Extract office name (everything before the pincode)
                    office_parts = []
                    for i, cell in enumerate(row):
                        cell = cell.strip()
                        if cell.isdigit() and len(cell) == 6:
                            break
                        if cell:
                            office_parts.append(cell)
                    
                    office_name = ' '.join(office_parts).strip()
                    
                    # Clean up state name (remove extra spaces and special characters)
                    state = state.replace(',', '').strip()
                    
                    # Extract district name from office name
                    district = extract_district_from_office_name(office_name, state)
                    
                    # Create the converted record
                    converted_record = {
                        'pincode': pincode,
                        'office_name': office_name or f"Post Office {pincode}",
                        'office_type': 'Sub Post Office',  # Default type
                        'delivery_status': 'Delivery',
                        'division_name': state,
                        'region_name': state,
                        'circle_name': state,
                        'taluk': state,
                        'district_name': district,
                        'state_name': state
                    }
                    
                    converted_data.append(converted_record)
    
    # Write the converted data to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['pincode', 'office_name', 'office_type', 'delivery_status', 
                     'division_name', 'region_name', 'circle_name', 'taluk', 
                     'district_name', 'state_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(converted_data)
    
    return len(converted_data)

def validate_pincodes(converted_file):
    """
    Validate the converted pincode data
    """
    valid_count = 0
    invalid_count = 0
    errors = []
    
    with open(converted_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):  # Start from 2 to account for header
            pincode = row['pincode']
            state = row['state_name']
            office_name = row['office_name']
            
            # Validate pincode format
            if not pincode.isdigit() or len(pincode) != 6:
                invalid_count += 1
                errors.append(f"Row {row_num}: Invalid pincode format '{pincode}'")
                continue
            
            # Validate required fields
            if not state or not office_name:
                invalid_count += 1
                errors.append(f"Row {row_num}: Missing state or office name")
                continue
            
            valid_count += 1
    
    return valid_count, invalid_count, errors

if __name__ == "__main__":
    input_file = "/Users/devanshgupta/Downloads/458185243.csv"
    output_file = "converted_indian_pincodes.csv"
    
    print("Converting pincode CSV format...")
    try:
        converted_count = convert_pincode_csv(input_file, output_file)
        print(f"✓ Converted {converted_count} pincode records")
        
        # Validate the converted data
        print("\nValidating converted data...")
        valid_count, invalid_count, errors = validate_pincodes(output_file)
        
        print(f"✓ Valid records: {valid_count}")
        if invalid_count > 0:
            print(f"✗ Invalid records: {invalid_count}")
            print("\nErrors found:")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        print(f"\nConverted file saved as: {output_file}")
        print("You can now import this file using the admin panel.")
        
    except Exception as e:
        print(f"✗ Error converting file: {e}")
        sys.exit(1) 