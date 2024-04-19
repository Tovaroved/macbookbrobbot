from utils.extensions import db

class Shipper(db.Model):
    __tablename__ = 'shipper'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    track_number = db.Column(db.String(150))
    created_date = db.Column(db.Date, )
    coming_date = db.Column(db.Date, nullable=True)


