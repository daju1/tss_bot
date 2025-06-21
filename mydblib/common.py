
from typing import List, Dict
import mysql.connector as mysql_connector
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('/app/static'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('tab_template.html')

def get_tss_msg(rendered = True):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tss'
    }
    connection = mysql_connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""SELECT EXTRACT(YEAR FROM date), 
                             EXTRACT(MONTH FROM date),
                             EXTRACT(DAY FROM date),
                             EXTRACT(HOUR FROM date),
                             EXTRACT(MINUTE FROM date),
                             EXTRACT(SECOND FROM date),
                             first_name,
                             msg
                             FROM tss_messages""")
    messages = cursor.fetchall()
    rendered_messages = template.render(messages=messages)

    cursor.close()
    connection.close()

    if rendered:
        return rendered_messages

    return messages


