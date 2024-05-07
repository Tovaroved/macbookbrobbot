from utils.extensions import db

class Shipper(db.Model):
    __tablename__ = 'shipper'
    
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer, db.ForeignKey('customer.id'))
    title = db.Column(db.String(100))
    weight = db.Column(db.Float)
    track_number = db.Column(db.String(150))
    status = db.Column(db.String(50), nullable=False)
    is_recieved = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.Date)
    coming_date = db.Column(db.Date, nullable=True)

    def __str__(self) -> str:
        return self.title