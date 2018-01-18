class Message:

    def __init__(self, text="", id_num=0, creator=""):
        self.t = text
        self.i = id_num
        self.c = creator

    def get_text(self):
        return self.t

    def get_id(self):
        return self.i

    def get_sender(self):
        return self.c

