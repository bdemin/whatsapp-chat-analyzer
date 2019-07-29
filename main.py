import numpy as np
import pandas as pd
import re

import matplotlib.pyplot as plt


def is_datetime_pattern(s):
    # mm/dd/yyyy, hh:mm -
    pattern = '^([0-2][0-9]|[0-9])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
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
    
    if is_author(message):
        split_message = message.split(': ') # Split message from author
        author = split_message[0]
        message = ' '.join(split_message[1:])
    else:
        author = None
    return date, time, author, message

def parse_data(path):
    parsed_data = []
    with open(path, encoding = "utf-8") as fp:
        message_buffer = [] # buffer for capturing long messages
        date, time, author = None, None, None # Set default
        
        while True:
            line = fp.readline()
            if not line: # Reached EOF
                break
            line = line.strip() # clean line from whitespaces
            if is_datetime_pattern(line): # Beginning of a new message
                if len(message_buffer) > 0: # Add message data from previous line, if needed
                    parsed_data.append([date, time, author, ' '.join(message_buffer)]) # Save message data
                message_buffer = []
                date, time, author, message = get_message_data(line)
                message_buffer.append(message)
            else:
                message_buffer.append(line) # Continue message from previous lines

    print('Parsing done')
    return parsed_data


def main():
    path = 'ts_chat.txt' # WhatsApp data file
    parsed_data = parse_data(path)

    # Initialize Pandas df
    df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])
    df.head()

    # Count number of messages per author
    author_value_counts = df['Author'].value_counts()
    messages_author_plt = author_value_counts.plot.barh() # Create a Pandas bar chart

    # Plot   
    messages_author_plt.plot()
    plt.title("Number of WhatsApp messages")
    plt.show()


if __name__ == '__main__':
    main()
    