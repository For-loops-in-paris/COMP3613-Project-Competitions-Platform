from App.database import db
from App.models import Student

class RankUpdater(db.Model):

    __tablename__ = 'rankupdater'

    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship("Student",backref = "updater",lazy=True)

    def get_json(self):
        return {
            "comp_id": self.comp_id,
            "leaderboard_id":self.leaderboard_id

        }
    
    def get_students(self):
        return RankUpdater.query.get(1).students
    
   

        

