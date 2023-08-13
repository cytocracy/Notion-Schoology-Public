from objects import Assignment as ass
import schoology
import notion
import json
import datetime
from os.path import exists




def merge(notion_assignments, school_assignments, exsisting_ids):
    new = 0
    updated = 0
    changed = 0
    for assignment in school_assignments:
        if str(assignment.id) in exsisting_ids:
            curr = notion_assignments[exsisting_ids.index(str(assignment.id))]

            if assignment.last_updated > curr.last_updated:
                notion.update_assignment(assignment, curr.notion_uuid)
                changed += 1
            else :
                updated += 1
        else:
            notion.create_assignment(assignment)
            new+=1

    print("Assignments created: " + str(new))
    sleep(.1)
    print("Assignments confirmed: " + str(updated))
    sleep(.1)
    print("Assignments changed: " + str(changed))


def sync():
    
    print("\nFetching Schoology assignments...", end="")

    school_assignments = schoology.get_assignments()
    print("\u2713", end="")

    print("\nFetching Notion assignments...", end="")
    notion_assignments = notion.get_assignments()[0]
    print("\u2713")
    print()

    exsisting_ids = [x.id for x in notion_assignments]
    # print(exsisting_ids)
    sleep(.1)
    print("Existing assignments: " + str(len(exsisting_ids)))
    #sleep .1 seconds
    sleep(.1)
    merge(notion_assignments, school_assignments, exsisting_ids)

    print()
    notion.update_description(datetime.datetime.now().strftime("%B %d, %Y %I:%M %p"))

    print("\033[1;32mSync complete.")
    print("\033[1;0m")

def sleep(seconds):
    import time
    time.sleep(seconds)




def course_to_page(course_or_page_id):
    courses = {}


    pages = notion.get_courses()
    
    for course in pages:
        courses[course.id] = course.page
        courses[course.page] = course.id
    with open("courses.json", "w") as f:
        json.dump(courses, f)


    return courses[course_or_page_id]


if __name__ == "__main__":
    sync()