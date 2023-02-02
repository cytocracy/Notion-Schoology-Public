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


#update the description of a dtabase
def update_description(description):
    response = notion.databases.update(
        database_id=database,
        description=[{
            "type": "text",
            "text": {
                "content": "Homework - " + description
            },
            
        }]
    )
    return response["description"]


# def update_description(description):
#     response = notion.databases.update(
#         database_id=database,
#         description=[
#             {
#                 "type": "text",
#                 "text": {
#                     "content": "Homework - " + description
#                 },
#                 "plain_text": "Homework - " + description
#             }
#         ]
#     )
#     return response["description"]


if __name__ == "__main__":
    response = update_description(datetime.datetime.now().strftime("%B %d, %Y %I:%M %p"))
    print(response)