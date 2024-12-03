from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)
    rank_updater = db.Column(db.Integer,db.ForeignKey("rankupdater.id"))
    rank_decay = db.Column(db.Integer,nullable=False)
    past_leaderboard_ranks = db.relationship("Ranking", backref = 'student',lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.rank_decay=0
        self.teams = []
        self.notifications = []

    def add_notification(self, notification):
        if notification:
          try:
            self.notifications.append(notification)
            db.session.commit()
            return notification
          except Exception as e:
            db.session.rollback()
            return None
        return None

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count" : self.comp_count,
            "curr_rank" : self.curr_rank
        }

    def update_stats(self,score):
        self.rating_score =score
        self.comp_count+=1    
        if self.comp_count == 1:
            self.rank_updater=1   
        self.rank_decay = -1
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def update_ranking(self,ranking):
        self.curr_rank = ranking
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
       
    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions" : self.comp_count,
            "Rank" : self.curr_rank
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'