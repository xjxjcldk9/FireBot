
class USERS:
    def __init__(self, token, checker):
        self.token = token
        self.checker = checker

    def check(self, case):
        self.checker(case)
