import os
import re


class init_file_loader:
    def __init__(self):
        self.demo = None
        self.username = None
        self.url = None
        self.load_config_file()

    def load_config_file(self):
        fallback_string = "demo\nhttps://cs-bgu-wsep.herokuapp.com/\nSystem Manager Username: Alex\nSystem Manager Password: Alex_123456"
        try:
            conf_file = open("config.txt", "r")
            configFileString = conf_file.read()
            conf_file.close()
        except Exception as e:
            configFileString = fallback_string
            print("DEMO MODE ACTIVATED (config file not found)")
            print(os.getcwd())

        try:
            regex_pattern = "^(real|demo)[.]*\n(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}).*\nSystem Manager Username:\s+([a-zA-Z0-9]+)\nSystem Manager Password:\s+([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)\n([\_a-zA-Z0-9]+)"
            p = re.compile(regex_pattern)
            p = p.match(configFileString)
            self.demo = False if p.group(1) == "real" else True
            self.url = None
            self.username = p.group(3)
            self.password = p.group(4)

            self.u2 = p.group(5)
            self.u2password = p.group(6)
            self.u3 = p.group(7)
            self.u3password = p.group(8)
            self.u4 = p.group(9)
            self.u4password = p.group(10)
            if self.demo == 'real':
                self.url = p.group(2)
            if self.username is None:
                raise Exception("NO SYSADMIN USERNAME")
            if self.password is None:
                raise Exception("NO SYSADMIN PASSWORD")
        except Exception as e:
            print("DEMO MODE ACTIVATED (failed to PARSE config file)")
            self.demo = True
            self.url = None
            self.username = "Alex"
            self.password = "Alex_123456"


    def getManagerDetails(self):
        return self.username, self.password

    def getManagerDetailsa(self, id):
        if id == 1:
            return (self.username, self.password)
        if id == 2:
            return (self.u2, self.u2password)
        if id == 3:
            return (self.u3, self.u3password)
        if id == 4:
            return (self.u4, self.u4password)
        return self.username, self.password
    def getPaymentUrl(self):
        return self.url

    def getShipmentUrl(self):
        return self.url
