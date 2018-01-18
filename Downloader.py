from Message import Message
import pickle
import requests
from pathlib import Path
from enum import Enum


class Downloader:
    access_code = "?token=pbYteuau9pn1TASKB0xSjlouL9esisv76XU1mxfe"
    base_url = "https://api.groupme.com/v3"
    group_url = "/groups"
    messages_url = "/messages"
    groups_dir = "Groups/"
    last_id_ending = "_last_id"
    message_count_ending = "_mess_amount"
    groups_path = base_url + group_url + access_code + "&per_page=100"

    def download(self, group_id):
        path = self.groups_dir + group_id + self.last_id_ending
        last_id = self.get_last_id(path)
        if last_id is None:
            return self.first_download(group_id)
        return self.subsequent_download(group_id, last_id)

    def first_download(self, group_id):
        before_id = ""
        count = 0
        first = True
        print("Started...")
        while True:

            url = self.base_url + self.group_url + '/' + group_id + self.messages_url + self.access_code +\
                  "&limit=100&before_id=" + before_id

            try_count = 0
            while True:

                response = requests.get(url)
                try_count += 1

                if response.status_code == 200:
                    break

                if response.status_code == 304:
                    path = self.groups_dir + group_id + self.message_count_ending
                    self.store_mess_count(path, count)
                    return self.Status.SUCCESS

                if response.status_code != 200:
                    print("Error: " + response.text)

                if try_count == 10:
                    return self.Status.FAILURE

            json_data = response.json()
            message_list = json_data['response']['messages']
            total = json_data['response']['count']

            if first:
                last_id = message_list[0]['id']
                path = self.groups_dir + group_id + self.last_id_ending
                self.store_last_id(path, last_id)
                first = False

            for message in message_list:
                path = self.groups_dir + group_id
                self.store_message(path, message)
                before_id = message['id']
                count += 1
            print("Progress: " + str(total) + "/" + str(count))

    def subsequent_download(self, group_id, last_mess_id):
        after_id = last_mess_id
        count = 0

        while True:
            url = self.base_url + self.group_url + '/' + group_id + self.messages_url + self.access_code +\
                  "&limit=100&after_id=" + after_id

            try_count = 0
            while True:
                response = requests.get(url)
                try_count += 1

                if response.status_code == 200:
                    break

                if response.status_code != 200:
                    print("Error: " + response.text)
                    continue

                if try_count == 10:
                    return self.Status.FAILURE

            json_data = response.json()
            message_list = json_data['response']['messages']

            if len(message_list) == 0:
                path = self.groups_dir + group_id + self.message_count_ending
                self.store_mess_count(path, count)

                path = self.groups_dir + group_id + self.last_id_ending
                self.store_last_id(path, after_id)

                return self.Status.SUCCESS

            for message in message_list:
                path = self.groups_dir + group_id
                self.store_message(path, message)
                count += 1
                after_id = message['id']

    def get_last_id(self, path):
        file = Path(path)
        if file.is_file():
            with open(file, 'r') as id_file:
                return id_file.readline()
        return None

    def store_message(self, path, message):
        message = Message(message['text'], message['id'], message['user_id'])
        with open(path, 'ab') as file:
            pickle.dump(message, file)

    def store_last_id(self, path, id_num):
        with open(path, 'w') as file:
            file.writelines(id_num)

    def store_mess_count(self, path, amount):

        file = Path(path)

        if file.is_file():
            last_count = 0
            with open(path, 'r') as file:
                last_count = file.read()
            with open(path, 'w') as file:
                last_count = str(int(last_count) + amount)
                file.write(last_count)

        else:
            with open(path, 'w') as file:
                file.write(str(amount))

    class Status(Enum):
        SUCCESS = 1
        FAILURE = 2

