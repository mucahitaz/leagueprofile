from app import db

class Summoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    server = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "Summoner('{},{}')".format(self.name,self.server)