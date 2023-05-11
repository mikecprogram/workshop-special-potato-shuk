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
            print("DEMO MODE ACTIVATED (config file not found, creating one)")
            conf_file = open("config.txt", "w+")
            conf_file.write(configFileString)
            conf_file.close()

        try:
            regex_pattern = "^(real|demo)[.]*\n(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}).*\nSystem Manager Username:\s+([a-zA-Z0-9]+)\nSystem Manager Password:\s+([\_a-zA-Z0-9]+)"
            p = re.compile(regex_pattern)
            p = p.match(configFileString)
            self.demo = False if p.group(1) == "real" else True
            self.url = None
            self.username = p.group(3)
            self.password = p.group(4)
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

    def getPaymentUrl(self):
        return self.url

    def getShipmentUrl(self):
        return self.url
