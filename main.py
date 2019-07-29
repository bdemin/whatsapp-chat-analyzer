import numpy as np
import pandas as pd
import re
import os

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
    files = []
    for file in os.listdir():
        if file.endswith(".txt"):
            files.append(file)

    path = files[1] # WhatsApp data file
    parsed_data = parse_data(path)

    # Initialize Pandas df
    df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])
    df.head()

    # Count and plot number of messages per author
    author_value_counts = df['Author'].value_counts()
    messages_author_plt = author_value_counts.plot.barh() # Create a Pandas bar chart
    messages_author_plt.plot()
    plt.title("Number of WhatsApp messages")
    plt.show()

    # Count and plot media messages per author
    media_messages_df = df[df['Message'] == '<Media omitted>']
    author_media_counts = media_messages_df['Author'].value_counts()
    media_author_plt = author_media_counts.plot.barh()
    media_author_plt.plot()
    plt.title("Number of WhatsApp media messages")
    plt.show()

    # Add fields to df - letter count and word count
    df['Letter_Count'] = df['Message'].apply(lambda s : len(s))
    df['Word_Count'] = df['Message'].apply(lambda s : len(s.split(' ')))

    # Plot word count by author
    word_count_by_author = df[['Author', 'Word_Count']].groupby('Author').sum()
    word_count_by_author = word_count_by_author.sort_values('Word_Count', ascending=False) # Sort
    word_count_plt = word_count_by_author.plot.barh()
    word_count_plt.plot()
    plt.xlabel('Number of Words')
    plt.ylabel('Authors')
    plt.show()

if __name__ == '__main__':
    main()
