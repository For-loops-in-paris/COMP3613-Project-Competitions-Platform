from App.database import db
from .student_team import *

class Team(db.Model):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', secondary='student_team', overlaps='teams', lazy=True)
    competitions = db.relationship('Competition', secondary='competition_team', overlaps='teams', lazy=True)

    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, stud):
        for s in self.students:
            if s.username == stud.username:
                print(f'{stud.username} is already a member of {self.name}')
                return None
        
        stud_team = StudentTeam(student_id=stud.id, team_id=self.id)
        try:
            self.students.append(stud)
            stud.teams.append(self)
            db.session.commit()
            print(f'{stud.username} was added to {self.name}!')
            return stud_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

    def get_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "students" : [student.username for student in self.students]
        }
    
    def to_Dict(self):
        return {
            "ID" : self.id,
            "Name" : self.name,
            "Students" : [student.username for student in self.students]
        }