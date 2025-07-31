
from typing import List, Dict
import mysql.connector as mysql_connector
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('/app/common'),
    autoescape=select_autoescape(['html'])
)
template_tab = env.get_template('tab_template.html')
template_stat = env.get_template('stat_template.html')


def get_tss_message(sql, template, rendered):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tss'
    }
    connection = mysql_connector.connect(**config)
    cursor = connection.cursor()

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

def get_tss_msg(rendered = True):

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


    return get_tss_message(sql=sql, template = template_tab, rendered=rendered)


def get_tss_stat(rendered = True):

    sql = """SELECT COUNT(*) AS n_KM,
                    DATE(date),
                    first_name
            FROM tss_messages
            WHERE msg LIKE '%КМ %'
            GROUP BY first_name, username, DATE(date)
        """

    return get_tss_message(sql=sql, template = template_stat, rendered=rendered)