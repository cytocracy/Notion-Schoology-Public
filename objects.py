class Assignment:
    def __init__(self, title, due_date, description, id, url, last_updated, course_id, uuid=None):
        self.title = title
        self.due_date = due_date
        self.description = description
        self.id = id
        self.url = url
        self.last_updated = last_updated
        self.course_id = course_id
        self.notion_uuid = uuid

    def __str__(self):
        return str(self.id) + " " + self.title


class Course:
    def __init__(self, title, id, page):
        self.title = title
        self.id = id
        self.page = page