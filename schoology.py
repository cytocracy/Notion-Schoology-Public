import schoolopy 
import datetime
from objects import Assignment
from objects import Class
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("SCHOOLOGY_KEY")
secret = os.getenv("SCHOOLOGY_SECRET")
sc = schoolopy.Schoology(schoolopy.Auth(key, secret, domain="https://schoology.shschools.org"))

def get_courses():
    courses = sc.get_user_sections(sc.get_me().uid)
    result = []
    for course in courses:
        c = Class(course['course_title'], course['id'])
        result.append(c)
    return result

def get_assignments():
    courses = sc.get_user_sections(sc.get_me().uid)
    result = []
    for course in courses:
        if course['id'] == "5948029489":
            continue
        assignments = sc.get_assignments(course['id'])
        for assignment in assignments:
            if assignment['due'] == None or assignment['due'] == "":
                continue
            test = datetime.datetime.strptime(assignment['due'], "%Y-%m-%d %H:%M:%S")
            if test > datetime.datetime.now():
                url = "https://schoology.shschools.org/assignment/" + str(assignment['id'])
                new = Assignment(assignment['title'], assignment['due'], assignment['description'], assignment['id'], url, assignment['last_updated'], course['id'])
                result.append(new)
    return result

if __name__ == "__main__":
    for a in get_courses():
        print(a.title)
