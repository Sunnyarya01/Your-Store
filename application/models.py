from application.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    password= db.Column(db.String)
    role = db.Column(db.String)
    city = db.Column(db.String)
    mobile_no = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String, unique=False)
    product_name = db.Column(db.String, unique=False)
    quantity = db.Column(db.String, unique=False)
    price = db.Column(db.Integer , unique=False)
    unit_price = db.Column(db.Integer, unique=False)
    description = db.Column(db.String, unique=False)
    image = db.Column(db.BLOB, unique=False)
