from datetime import datetime

class mockdatetime:  # mock datetime

    def __init__(self, time = datetime.now()):
        self.time = time

    def now(self):
        return self.time