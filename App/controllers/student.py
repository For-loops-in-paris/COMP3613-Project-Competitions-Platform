from App.database import db
from App.models import Student, Competition, Notification, CompetitionTeam, Leaderboard, Ranking

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
        print(f'New Student: {username} created!')
        return newStudent
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_decayed_students():
    return Student.query.filter_by(rank_decay=3)

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

#todo:  change so that student rank is also in info
def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        competitions = []
        
        for team in student.teams:
            team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()
            for comp_team in team_comps:
                comp = Competition.query.filter_by(id=comp_team.comp_id).first()
                competitions.append(comp.name)

        profile_info = {
            "profile" : student.get_json(),
            "competitions" : competitions
        }

        return profile_info

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_Dict() for notification in student.notifications]}

def update_rankings():
    students = get_all_students()
    
    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1
    
    curr_high = students[0].rating_score
    curr_rank = 1

    
    for student in students:
        if student.rank_decay<3:
            student.rank_decay+=1

        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            ranking = Ranking(student.id,Leaderboard.query.count(),count,student.rating_score)
            count += 1
        
            
        
            notification = Notification(student.id, create_notification(student.comp_count,student.curr_rank,curr_rank))
            student.curr_rank = curr_rank
            try:
                db.session.add(student)
                db.session.add(notification)
                db.session.add(ranking)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return leaderboard


def create_notification(comp_count,current_rank,rank):
    message = f'RANK : {rank}. '
    if comp_count == 1:
        message += 'Congratulations on your first rank!'
    elif current_rank == rank:
        message +=' Well done! You retained your rank.'
    elif current_rank > rank:
        message += 'Congratulations! Your rank has went up.'
    else:
        message += 'Oh no! Your rank has went down.'
    return message


def display_rankings():
    students = get_all_students()

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    leaderboard = []
    count = 1
    curr_high = students[0].rating_score
    curr_rank = 1
        
    for student in students:
        if curr_high != student.rating_score:
            curr_rank = count
            curr_high = student.rating_score

        if student.comp_count != 0:
            leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
            count += 1

    print("Rank\tStudent\tRating Score")

    for position in leaderboard:
        print(f'{position["placement"]}\t{position["student"]}\t{position["rating score"]}')
    
    return leaderboard