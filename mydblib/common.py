
from typing import List, Dict
import mysql.connector as mysql_connector
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('/app/comon'),
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
    sql = """SELECT EXTRACT(YEAR FROM date), 
                             EXTRACT(MONTH FROM date),
                             EXTRACT(DAY FROM date),
                             EXTRACT(HOUR FROM date),
                             EXTRACT(MINUTE FROM date),
                             EXTRACT(SECOND FROM date),
                             first_name,
                             msg
                             FROM tss_messages"""

    sql = """SELECT date,
                    first_name,
                    msg
                    FROM tss_messages"""

    sql = """SELECT
                    DATE(date),
                    TIME(date),
                    first_name,
                    msg
                    FROM tss_messages"""

    cursor.execute(sql)
    messages = cursor.fetchall()
    print("messages = ", messages, flush=True)

    rendered_messages = template.render(messages=messages)
    print("rendered_messages = ", rendered_messages, flush=True)

    cursor.close()
    connection.close()

    if rendered:
        return rendered_messages

    text = ""
    for message in messages:
        for elem in message:
            if type(elem) == "text":
                text += elem
            else:
                text += str(elem)
            text += ","
        text += "\n"

    result = text

    print("result = ", result, flush=True)
    return result


