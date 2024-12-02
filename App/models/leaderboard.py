from App.database import db
from datetime import datetime

class Leaderboard(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.now())
    user =  db.relationship("Student",secondary="ranking")

    def get_json(self):
        
        return {
            "id": self.id,
            "date":self.date.strftime("%d %b %Y")
        }
    