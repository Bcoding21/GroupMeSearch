import re

HTTP_URL_PATTERN = "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

def find(key_word, messages):
    return [message for message in messages if key_word in message]

def find_links(messages):
    return [message for message in messages if re.fullmatch(HTTP_URL_PATTERN, message) is not None]

def get_keyword_occurences(key_word, messages):
    occurences_count = 0
    for message in messages:
        if key_word in message:
            occurences_count += 1
    return occurences_count