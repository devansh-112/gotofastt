from datetime import datetime, timedelta
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
import random
import string

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"admin_{self.id}"

class DeliveryPartner(UserMixin, db.Model):
    __tablename__ = 'delivery_partners'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return f"partner_{self.id}"

class Zone(db.Model):
    __tablename__ = 'zones'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    base_rate = db.Column(db.Float, nullable=False)  # Base rate per kg
    delivery_days = db.Column(db.Integer, nullable=False)  # Standard delivery days
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PricingSettings(db.Model):
    __tablename__ = 'pricing_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    admin = db.relationship('Admin', backref='pricing_updates')

class GlobalPricingConfig(db.Model):
    __tablename__ = 'global_pricing_config'
    
    id = db.Column(db.Integer, primary_key=True)
    gst_rate = db.Column(db.Float, default=0.18)
    pickup_charge_jaipur = db.Column(db.Float, default=100)
    pickup_charge_oda_jaipur = db.Column(db.Float, default=300)
    delivery_charge_jaipur_0_5 = db.Column(db.Float, default=300)
    delivery_charge_jaipur_5_15 = db.Column(db.Float, default=500)
    delivery_charge_rajasthan_base = db.Column(db.Float, default=800)
    delivery_charge_rajasthan_per_kg = db.Column(db.Float, default=20)
    delivery_charge_india_base = db.Column(db.Float, default=1500)
    delivery_charge_india_per_kg = db.Column(db.Float, default=30)
    oda_charge = db.Column(db.Float, default=300)
    min_weight = db.Column(db.Float, default=15)
    volume_rate = db.Column(db.Float, default=50)  # per cubic meter
    # New fields for weight categories and cancellation charge
    weight_cat_0_5 = db.Column(db.Float, default=0)
    weight_cat_5_15 = db.Column(db.Float, default=0)
    weight_cat_15_plus = db.Column(db.Float, default=0)
    cancellation_charge = db.Column(db.Float, default=300)
    # Add more fields as needed
    
    # Remove or comment out the admin relationship that has no ForeignKey
    # admin = db.relationship('Admin', backref='global_pricing_updates')

class StateConfig(db.Model):
    __tablename__ = 'state_config'
    
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(100), unique=True, nullable=False)
    state_code = db.Column(db.String(10), unique=True, nullable=False)
    is_serviceable = db.Column(db.Boolean, default=True)
    base_pickup_rate = db.Column(db.Float, nullable=False, default=100.0)  # ₹
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    admin = db.relationship('Admin', backref='state_configs')

class InvoiceTemplate(db.Model):
    __tablename__ = 'invoice_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100), unique=True, nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    company_address = db.Column(db.Text, nullable=False)
    company_phone = db.Column(db.String(20), nullable=False)
    company_email = db.Column(db.String(120), nullable=False)
    gst_number = db.Column(db.String(15), nullable=False)
    logo_url = db.Column(db.String(500))
    terms_conditions = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    admin = db.relationship('Admin', backref='invoice_templates')

class DeliveryEvent(db.Model):
    __tablename__ = 'delivery_events'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # picked_up, in_transit, delivered, etc.
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(50))  # partner_username or admin
    
    order = db.relationship('Order', backref='delivery_events')

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Customer details
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    
    # Package details
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    package_type = db.Column(db.String(50), nullable=False)  # electronics, home, clothing, etc.
    weight = db.Column(db.Float, nullable=False)  # in kg
    length = db.Column(db.Float, nullable=False)  # in cm
    width = db.Column(db.Float, nullable=False)   # in cm
    height = db.Column(db.Float, nullable=False)  # in cm
    quantity = db.Column(db.Integer, nullable=False, default=1)  # number of packages
    package_description = db.Column(db.Text)
    
    # Recipient details
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_phone = db.Column(db.String(20), nullable=False)
    
    # Payment details
    payment_mode = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, unpaid, failed
    
    # Detailed pricing breakdown
    base_amount = db.Column(db.Float, nullable=False, default=0.0)  # Base shipping cost
    pickup_charge = db.Column(db.Float, nullable=False, default=0.0)  # Pickup fee
    extra_weight_charge = db.Column(db.Float, nullable=False, default=0.0)  # Extra weight fee
    payment_fee = db.Column(db.Float, nullable=False, default=0.0)  # COD/Card fee
    subtotal = db.Column(db.Float, nullable=False, default=0.0)  # Before tax
    gst_amount = db.Column(db.Float, nullable=False, default=0.0)  # GST
    total_amount = db.Column(db.Float, nullable=False)
    
    # Invoice details
    invoice_number = db.Column(db.String(20), unique=True)
    invoice_date = db.Column(db.DateTime)
    invoice_generated = db.Column(db.Boolean, default=False)
    
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    
    # Delivery details
    delivery_status = db.Column(db.String(20), default='pending')  # pending, picked_up, in_transit, delivered, cancelled
    estimated_delivery = db.Column(db.DateTime, nullable=False)
    actual_delivery = db.Column(db.DateTime)
    
    gst_bill_filename = db.Column(db.String(255), nullable=True)  # Path to uploaded GST bill
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    zone = db.relationship('Zone', backref='orders')
    partner = db.relationship('DeliveryPartner', backref='orders')
    partner_id = db.Column(db.Integer, db.ForeignKey('delivery_partners.id'), nullable=True)
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
    
    @staticmethod
    def generate_reference_number(order_id=None):
        # abcdDDMMYYab1234: abcd=random words, DD=day, MM=month, YY=year, ab=random letters, 1234=random code
        rand_words = ''.join(random.choices(string.ascii_uppercase, k=4))
        now = datetime.now()
        date_part = now.strftime('%d%m%y')
        rand_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        random_code = f'{random.randint(1000,9999)}'
        return f"{rand_words}{date_part}{rand_letters}{random_code}"
    
    def calculate_total_amount(self):
        """Calculate total amount using advanced pricing configuration"""
        if not self.zone:
            return 0.0
        
        # Use a fallback base rate if zone.base_rate is 0 or None
        base_rate = self.zone.base_rate if self.zone.base_rate and self.zone.base_rate > 0 else 100.0
        
        # Get global pricing configuration
        config = GlobalPricingConfig.query.first()
        if not config:
            # Fallback to basic calculation if no config
            return round(base_rate * self.weight * self.quantity, 2)
        
        # Calculate billable weight (minimum weight or actual weight, whichever is higher)
        billable_weight = max(self.weight, config.min_weight)
        
        # Base amount calculation
        self.base_amount = base_rate * billable_weight * self.quantity
        
        # Pickup charge (using a default value since base_pickup_charge doesn't exist)
        self.pickup_charge = 100.0  # Default pickup charge
        
        # Extra weight charge if weight exceeds minimum weight
        if self.weight > config.min_weight:
            extra_weight = self.weight - config.min_weight
            self.extra_weight_charge = extra_weight * 20.0  # Default extra charge per kg
        else:
            self.extra_weight_charge = 0.0
        
        # Volume calculation for size-based pricing (if specified in settings)
        volume = (self.length * self.width * self.height) / 1000000  # Convert cm³ to m³
        volume_rate = PricingSettings.query.filter_by(setting_name='volume_rate_per_cubic_meter').first()
        if volume_rate:
            volume_cost = volume * volume_rate.setting_value
            # Use higher of weight-based or volume-based pricing for base amount
            self.base_amount = max(self.base_amount, volume_cost)
        
        # Payment processing fees
        subtotal_for_fees = self.base_amount + self.pickup_charge + self.extra_weight_charge
        
        if self.payment_mode == 'cod':
            self.payment_fee = subtotal_for_fees * 0.02  # 2% COD fee
        elif self.payment_mode == 'card':
            self.payment_fee = subtotal_for_fees * 0.015  # 1.5% card fee
        else:
            self.payment_fee = 0.0
        
        # Calculate subtotal before tax
        self.subtotal = (self.base_amount + self.pickup_charge + self.extra_weight_charge + 
                        self.payment_fee)
        
        # Calculate GST
        self.gst_amount = self.subtotal * config.gst_rate
        
        # Calculate total amount
        total = self.subtotal + self.gst_amount
        
        return round(total, 2)
    
    def get_delivery_timeline(self):
        """Get delivery timeline with status updates"""
        timeline = []
        
        if self.delivery_status in ['pending', 'picked_up', 'in_transit', 'delivered', 'cancelled']:
            timeline.append({
                'status': 'Order Placed',
                'timestamp': self.created_at,
                'completed': True,
                'description': 'Your order has been placed successfully'
            })
        
        if self.delivery_status in ['picked_up', 'in_transit', 'delivered']:
            timeline.append({
                'status': 'Package Picked Up',
                'timestamp': self.created_at + timedelta(hours=2),  # Simulated
                'completed': True,
                'description': 'Package has been picked up from origin'
            })
        
        if self.delivery_status in ['in_transit', 'delivered']:
            timeline.append({
                'status': 'In Transit',
                'timestamp': self.created_at + timedelta(days=1),  # Simulated
                'completed': True,
                'description': 'Package is on the way to destination'
            })
        
        if self.delivery_status == 'delivered':
            timeline.append({
                'status': 'Delivered',
                'timestamp': self.actual_delivery or self.estimated_delivery,
                'completed': True,
                'description': 'Package has been delivered successfully'
            })
        elif self.delivery_status == 'cancelled':
            timeline.append({
                'status': 'Cancelled',
                'timestamp': self.updated_at,
                'completed': True,
                'description': 'Order has been cancelled'
            })
        else:
            timeline.append({
                'status': 'Delivered',
                'timestamp': self.estimated_delivery,
                'completed': False,
                'description': f'Expected delivery by {self.estimated_delivery.strftime("%B %d, %Y at %I:%M %p")}'
            })
        
        return timeline

class ContactSettings(db.Model):
    __tablename__ = 'contact_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False, default='GotoFast Logistics')
    company_address = db.Column(db.Text, nullable=False, default='123 Logistics Street, City, State 12345')
    company_phone = db.Column(db.String(20), nullable=False, default='+91 98765 43210')
    company_email = db.Column(db.String(120), nullable=False, default='info@gotofast.com')
    company_website = db.Column(db.String(200), nullable=False, default='https://gotofast.com')
    support_phone = db.Column(db.String(20), nullable=False, default='+91 98765 43211')
    support_email = db.Column(db.String(120), nullable=False, default='support@gotofast.com')
    business_hours = db.Column(db.String(100), nullable=False, default='Monday - Friday: 9:00 AM - 6:00 PM')
    facebook_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))
    updated_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    admin = db.relationship('Admin', backref='contact_updates')
    
    @classmethod
    def get_settings(cls):
        """Get the current contact settings, creating default if none exist"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings



class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    category = db.Column(db.String(50), default='general')  # general, technical, billing, delivery
    assigned_to = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    admin = db.relationship('Admin', backref='assigned_tickets')
    
    def __init__(self, **kwargs):
        super(SupportTicket, self).__init__(**kwargs)
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
    
    @staticmethod
    def generate_ticket_number():
        """Generate a unique ticket number: TKT-YYYYMMDD-XXXX"""
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"TKT-{date_part}-{random_part}"

class PincodeData(db.Model):
    __tablename__ = 'pincode_data'
    
    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(6), nullable=False, index=True)
    office_name = db.Column(db.String(200), nullable=False)
    office_type = db.Column(db.String(50), nullable=False)
    delivery_status = db.Column(db.String(50), nullable=False)
    division_name = db.Column(db.String(100), nullable=False)
    region_name = db.Column(db.String(100), nullable=False)
    circle_name = db.Column(db.String(100), nullable=False)
    taluk = db.Column(db.String(100), nullable=False)
    district_name = db.Column(db.String(100), nullable=False)
    state_name = db.Column(db.String(100), nullable=False)
    is_serviceable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PincodeData {self.pincode}: {self.district_name}, {self.state_name}>'
    
    @classmethod
    def get_by_pincode(cls, pincode):
        """Get pincode data by pincode number"""
        return cls.query.filter_by(pincode=pincode).first()
    
    @classmethod
    def search_by_district(cls, district_name):
        """Search pincodes by district name"""
        return cls.query.filter(
            cls.district_name.ilike(f'%{district_name}%')
        ).all()
    
    @classmethod
    def search_by_state(cls, state_name):
        """Search pincodes by state name"""
        return cls.query.filter(
            cls.state_name.ilike(f'%{state_name}%')
        ).all()
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'pincode': self.pincode,
            'office_name': self.office_name,
            'office_type': self.office_type,
            'delivery_status': self.delivery_status,
            'division_name': self.division_name,
            'region_name': self.region_name,
            'circle_name': self.circle_name,
            'taluk': self.taluk,
            'district_name': self.district_name,
            'state_name': self.state_name,
            'is_serviceable': self.is_serviceable
        }

class DeliveryServiceablePincode(db.Model):
    __tablename__ = 'delivery_serviceable_pincodes'
    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(6), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DeliveryServiceablePincode {self.pincode}>'

class PickupServiceablePincode(db.Model):
    __tablename__ = 'pickup_serviceable_pincodes'
    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.String(6), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PickupServiceablePincode {self.pincode}>'


class VariablePricingRule(db.Model):
    __tablename__ = 'variable_pricing_rules'
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=True)  # Null = applies to all zones
    min_weight = db.Column(db.Float, nullable=False, default=0.0)
    max_weight = db.Column(db.Float, nullable=True)  # Null = no upper limit
    service_type = db.Column(db.String(50), nullable=True)  # e.g., express, standard
    rate_per_kg = db.Column(db.Float, nullable=False)
    flat_rate = db.Column(db.Float, nullable=True)  # Optional flat rate
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    zone = db.relationship('Zone', backref='variable_pricing_rules')
