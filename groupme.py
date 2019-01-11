import requests, re
from group_me_config import ACCESS_TOKEN

BASE_URL = "https://api.groupme.com/v3"
GROUPS_PATH = "/groups"
MESSAGES_PATH = "/messages"
GROUPS_PER_PAGE = 100
MESSAGES_PER_REQUEST = 100 # max allowed by group me


def get_messages(group_id):
    messages_url = __get_messages_url(group_id)
    messages_url_params = __get_messages_url_params()
    response = requests.get(messages_url, params=messages_url_params)
    if goodResponse(response):
        return __parse_messages( response.json() )
    print(response.status_code)    
    return None

def goodResponse(response):
    return response.status_code == 200

    
def __get_messages_url(group_id):
    return "{}{}/{}{}".format(BASE_URL, GROUPS_PATH, group_id, MESSAGES_PATH)

def __get_messages_url_params(before_id = None):
    params = {
        'limit' : MESSAGES_PER_REQUEST,
        'token' : ACCESS_TOKEN
    }
    if before_id == None:
        return params
    params['before_id'] = before_id
    return params

def __parse_messages(json_data):
    messages = json_data['response']['messages']
    messages = [ message['text'] for message in messages if message['text'] is not None ]
    return messages

def get_group_ids():
    groups_url = __get_groups_url()
    groups_url_params = __get_groups_url_params()
    response = requests.get(groups_url, params=groups_url_params)
    if goodResponse(response):
        return __parse_group_chat_ids( response.json() )
    print(response.status_code)
    return None

def __get_groups_url():
    return "{}{}".format(BASE_URL, GROUPS_PATH)

def __get_groups_url_params():
    return {
        'token' : ACCESS_TOKEN,
        'per_page' : GROUPS_PER_PAGE,
        'omit' : 'membership'
    }

def __parse_group_chat_ids(json_data):
    group_chats = json_data['response']
    group_chat_ids = [ group_chat['id'] for group_chat in group_chats ]
    return group_chat_ids