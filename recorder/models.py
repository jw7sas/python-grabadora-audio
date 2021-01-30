import uuid

class Audio:
    def __init__(self, filename, short_message, uid=None):
        self.filename = filename
        self.short_message = short_message
        self.uid = uid or uuid.uuid4()
    
    def to_dict(self):
        return vars(self)

    @staticmethod
    def schema():
        return ['filename', 'short_message', 'uid']