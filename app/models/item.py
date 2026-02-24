from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_lost_found = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='lost')
    image_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())
