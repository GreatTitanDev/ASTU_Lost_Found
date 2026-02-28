from datetime import datetime
from app import db


class Item(db.Model):
    """Item model for lost and found items."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_lost_found = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='lost')  # 'lost', 'found', 'claimed', 'resolved'
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    claims = db.relationship('Claim', backref='item', lazy='dynamic', cascade='all, delete-orphan')

    # Categories
    CATEGORIES = [
        'ID Cards',
        'Electronics',
        'Keys',
        'Books',
        'Calculators',
        'USB Drives',
        'Lab Coats',
        'Bags',
        'Clothing',
        'Other'
    ]

    def __repr__(self):
        return f'<Item {self.title}>'
