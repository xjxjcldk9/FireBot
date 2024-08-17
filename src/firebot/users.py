
class USERS:
    def __init__(self, name, token, checker):
        self.name = name
        self.token = token
        self.checker = checker

    def check(self, case):
        return self.checker(case)
