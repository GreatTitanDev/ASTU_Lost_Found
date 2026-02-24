from app import db

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeigKey('items.id'), nullable=False)
    claimed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullabele=False)
    proof_decription = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.now())
