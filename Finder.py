import pickle
from Message import Message


class Finder:
    access_code = "?token=pbYteuau9pn1TASKB0xSjlouL9esisv76XU1mxfe"
    base_url = "https://api.groupme.com/v3"
    group_url = "/groups"
    messages_url = "/messages"
    group_path = "Groups/"
    message_count_ending = "_mess_amount"

    def get_text(self, keyword, id_num):
        path = self.group_path + id_num + self.message_count_ending
        keywords = self.get_variations(keyword)
        amount = 0
        with open(path, 'r') as file:
            amount = int(file.readline())

        count = 0
        path = self.group_path + id_num
        matches = list()
        with open(path, 'rb') as file:
            while count != amount:
                message = pickle.load(file)
                text = message.get_text()
                if text is not None:
                    text = text.lower()
                    for word in keywords:
                        if word in text:
                            matches.append(text)
                            break
                count += 1

        matches = set(matches)
        return matches

    def get_users_text(self):
        pass

    def get_variations(self, keyword):
        variations = list()
        for word in keyword:
            variations.append(" " + word)
            variations.append(" " + word + " ")
            variations.append(" " + word + ".")
            variations.append(" " + word + "!")
            variations.append(" " + word + "?")
        return variations

