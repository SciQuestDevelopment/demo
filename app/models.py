from app import db


class User(db.Model):
    __tablename__ = "user"
    email = db.Column(db.String(256), index=True, unique=True)
    u_id = db.Column(db.Integer, index=True, unique=True, primary_key=True, autoincrement=True)
    password = db.Column(db.String(256))
    def __repr__(self):
        return '<User {} {}>'.format(self.email, self.u_id)




