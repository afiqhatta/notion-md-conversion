from flask import Flask
import readin as rd
from keys import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    recentStories = 10

    ids, names = rd.getRecentStoryIds(notion_key, database_key, recentStories)
    name_string = ['<ul>{}</ul>'.format(' '.join(string.split('-')[:-1])) for string in names]

    notion_list =  "<p>" + "".join(name_string) + "</p>"
    print(notion_list)
    return notion_list



hello_world()