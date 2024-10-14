class USERS:

    def __init__(self, name, token, web_hook_url, checker):
        self.name = name
        self.token = token
        self.web_hook_url = web_hook_url
        self.checker = checker

    def check(self, case):
        return self.checker(case)
