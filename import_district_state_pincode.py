import csv
from app import app, db
from models import PincodeData

CSV_FILE = '5c2f62fe-5afa-4119-a499-fec9d604d5bd.csv'

with app.app_context():
    print('Clearing existing pincode data...')
    PincodeData.query.delete()
    db.session.commit()
    print('✓ Cleared existing data')

    print('Importing district, state, and pincode from CSV...')
    count = 0
    with open(CSV_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pincode = row['pincode'].strip()
            district = row['district'].strip()
            state = row['statename'].strip()
            if not (pincode and district and state):
                continue
            pincode_data = PincodeData(
                pincode=pincode,
                office_name='',
                office_type='',
                delivery_status='',
                division_name='',
                region_name='',
                circle_name='',
                taluk='',
                district_name=district,
                state_name=state,
                is_serviceable=True
            )
            db.session.add(pincode_data)
            count += 1
            if count % 1000 == 0:
                db.session.commit()
                print(f'Imported {count} records...')
        db.session.commit()
    print(f'✓ Successfully imported {count} records.') 