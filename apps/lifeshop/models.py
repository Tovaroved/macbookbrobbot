from utils.extensions import db

class Lifeshop(db.Model):
    __tablename__ = 'lifeshop'
    
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer, db.ForeignKey('customer.id'))
    title = db.Column(db.String(100))
    weight = db.Column(db.Float, nullable=True)
    track_number = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    link_to_ms = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.Date, nullable=True)
    updated_date = db.Column(db.Date, nullable=True)
    coming_date = db.Column(db.Date, nullable=True)

    def __str__(self) -> str:
        return self.title