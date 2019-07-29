import numpy as np
import pandas as pd
import re


def is_datetime_pattern(s):
    # mm/dd/yyyy, hh:mm -
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def is_author(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def get_message_data(line):
    split_line = line.split(' - ') # Split datetime from message

    datetime = split_line[0]
    date, time = datetime.split(', ')
    
    message = ' '.join(split_line[1:])
    
    if is_author(message): # Split message from author
        split_message = message.split(': ')
        author = split_message[0]
        message = ' '.join(split_message[1:])
    else:
        author = None
    return date, time, author, message
