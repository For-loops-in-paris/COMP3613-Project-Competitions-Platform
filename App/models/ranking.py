from App.database import db

class Ranking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    leaderboard_id =  db.Column(db.Integer, db.ForeignKey('leaderboard.id'), nullable=False)

    def get_json(self):
        return {
            "comp_id": self.comp_id,
            "leaderboard_id":self.leaderboard_id

        }
    