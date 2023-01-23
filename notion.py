import os
from notion_client import Client
from objects import Assignment
from objects import Course
import json
import datetime
import sync
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("NOTION_DATABASE")
gallery = os.getenv("NOTION_GALLERY")
token = os.getenv("NOTION_TOKEN")

notion = Client(auth=token)

def get_properties(assignment):
    return {
        "title": {
            "title": [
                {
                    "text": {
                        "content": assignment.title
                    } 
                }
            ]
        },
        "Due date": {
            "date": {
                "start": assignment.due_date
            }
        },
        "Course": {
            "relation": [
                {
                    "id": sync.course_to_page(assignment.course_id)
                }
            ],
            "has_more": False
        },
        "Status":{
            "select": {
                "name": "Not started",
                "color": "red"
            }
        },
        "URL": {
            "url": assignment.url
        },
        "Assignment ID": {
            "rich_text": [
                {
                    "text": {
                        "content": str(assignment.id)
                    }
                }
            ]
        },
        "Course ID": {
            "rich_text": [
                {
                    "text": {
                        "content": assignment.course_id
                    }
                }
            ]
        },
        "Last updated": {
            "rich_text": [
                {
                    "text": {
                        "content": str(assignment.last_updated)
                    }
                }
            ]
        }
    }

def get_children(assignment):
    return [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": assignment.description
                            }
                        }
                    ]
                }
            }
        ]

def create_assignment(assignment):
    response = notion.pages.create(
        parent={"type": "database_id", "database_id": database},
        properties=get_properties(assignment),
        children=get_children(assignment)
    )

def get_courses():
    response = notion.databases.query(
        database_id=gallery
    )
    result = []
    # print(response['results'])
    for x in response['results']:
        title = x['properties']['Course name']['title'][0]['plain_text']
        id = x['properties']['URL']['url'].split("/")[-2]
        page = x['id']
        new = Course(title, id, page)
        result.append(new)
    return result

def update_assignment(new_assignment, uuid):
    id = uuid
    response = notion.pages.update(
        page_id=id,
        properties=get_properties(new_assignment),
        children=get_children(new_assignment)
    )



def get_assignments():
    response = notion.databases.query(
        database_id=database
    )
    result = []
    for x in response['results']:
        title = x['properties']['Name']['title'][0]['plain_text']
        due_date = x['properties']['Due date']['date']['start']
        id = x['properties']['Assignment ID']['rich_text'][0]['text']['content']
        url = x['properties']['URL']['url']
        last_updated = x['properties']['Last updated']['rich_text'][0]['text']['content']
        course_id = x['properties']['Course ID']['rich_text'][0]['text']['content']
        uuid = x['id']

        description = notion.blocks.children.list(x['id'])
        description = description['results'][0]['paragraph']['rich_text']
        description = description[0]['text']['content']

        new = Assignment(title, due_date, description, id, url, last_updated, course_id, uuid)
        result.append(new)
    return result


if __name__ == "__main__":
    assignments = get_assignments()
    for x in assignments:
        print(x)
        print(x.notion_uuid)
