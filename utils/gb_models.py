from .extensions import db


class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    company = db.Column(db.String(50), default="lifeshop")
    password = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=True)
    cookie = db.Column(db.Text, nullable=True)
    tarif = db.Column(db.Integer, nullable=False)
    sh_packs = db.relationship('Shipper', backref='customer_shipper',
                                lazy='dynamic')
    # ls_packs = db.relationship('Lifeshop', backref='customer_lifeshop',
    #                             lazy='dynamic')

    def __str__(self):
        return self.full_name