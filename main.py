from Downloader import Downloader
import requests
from Finder import Finder


def get_group_ids():

    try_count = 0

    while True:

        response = requests.get(Downloader.groups_path)
        try_count += 1

        if response.status_code == 200:
            data = response.json()
            return data['response']

        error_mess = response.text
        print("Error message: " + error_mess)

        if try_count == 100:
            return None


def get_id_input(group_id_list):
    group_map = dict()
    i = 1
    for group in group_id_list:
        group_id = group['id']
        group_name = group['name']
        group_map[str(i)] = [group_name, str(group_id)]
        i = i + 1

    for x in range(1, i):
        data = group_map[str(x)]
        print(str(x) + ". " + data[0])

    choice = input("Enter number: ")
    id_num = group_map[choice][1]
    return str(id_num)


def print_text_matches(matches):
    for match in matches:
        print(match)
        print("*" * 80 + "\n\n")


def prompt_key_words():
    key_words = list()
    print("Enter key words. Press s to stop: ")
    while True:
        word = input("Enter here: ")
        if word == 's':
            return key_words
        key_words.append(word)


def menu():
    pass


def main():
    downloader = Downloader()
    finder = Finder()
    group_id_list = get_group_ids()
    if group_id_list is not None:
        group_id = get_id_input(group_id_list)
        status = downloader.download(group_id)
        if status == downloader.Status.SUCCESS:
            keywords = prompt_key_words()
            matches = finder.get_text(keywords, group_id)
            print_text_matches(matches)
        else:
            print("Error occured")
    else:
        print("Response issue")


if __name__ == "__main__":
    main()


