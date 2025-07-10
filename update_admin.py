from app import app, db
from models import Admin

NEW_USERNAME = 'superadmin'
NEW_PASSWORD = 'SuperSecure@2024'
NEW_EMAIL = 'superadmin@example.com'

with app.app_context():
    admin = Admin.query.filter_by(username=NEW_USERNAME).first()
    if admin:
        admin.set_password(NEW_PASSWORD)
        db.session.commit()
        print(f"Password reset! Username: {NEW_USERNAME}, Password: {NEW_PASSWORD}")
    else:
        new_admin = Admin(username=NEW_USERNAME, email=NEW_EMAIL, full_name='Super Admin', is_super_admin=True)
        new_admin.set_password(NEW_PASSWORD)
        db.session.add(new_admin)
        db.session.commit()
        print(f"New admin created! Username: {NEW_USERNAME}, Password: {NEW_PASSWORD}") 