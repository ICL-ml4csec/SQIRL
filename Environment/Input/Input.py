import random
from bs4 import BeautifulSoup

import requests
from Environment.Payload import Payload
from Environment.Input.import_utilities import import_attr
from urllib.parse import urljoin
from requests_html import HTMLSession
from nltk.corpus import words

words_ = ['string']
class Input:
    def __init__(self,details,token, login_function) -> None:
        self.details = details
        self.token = token
        self.sql_starting_stmt= None
        assert(details["type"] == "form" or details["type"] == "dynamic_link")
        self.type = details["type"]
        if self.type =="form":
            self.action = details["action"]
            self.method = details["method"]
            self.inputs = details["inputs"]
            self.parent_link = details["parent_link"]
        else:
            self.action = details["action"]
            self.inputs = details["inputs"]
            self.method = "GET"
            self.parent_link = details["parent_link"]

        # how many responce seen in the past
        self.seen_responce = 0

        # how many request sent in the past
        self.sent_request = 0

        self.session = None
        self.login_function = login_function

        self.static_param ={}

    def login(self):
        self.session  = requests.Session()
        if self.login_function is not None:
            self.session = self.login_function(self.session)

        
    def send_token(self):
        self.login()
        self.sent_request += 1
        body = self.create_request_body(self.token)
        try:
            if self.type == "form":
                # print(f"[Input] send form with token {self.token} to {self.action}")
                # join the url with the action (form request URL)
                url = self.action
                # print(f"[input->send token] body of post data {body}")
                if self.method == "post":
                    res = self.session.post(url, data=body)
                elif self.method == "get":
                    res = self.session.get(url, params=body)
            else:
                # print(f"[Input] send dynamic with token {self.token} to {self.action}")
                # print(f"[input->send token] body of post data {body}")

                url = self.action

                res = self.session.get(url, params=body)
            # print(f"[input->send_token] responce found {res.status_code}")
            # input(res.text)
            return res

        except:
            print("[Input->send token] exceed redirects")
            
        return None

    def send_request(self,payload:Payload):
        self.login()
        self.sent_request += 1
        payload = str(payload)
        body = self.create_request_body(payload)
        if self.type == "form":
            # join the url with the action (form request URL)
            url = self.action
            if self.method == "post":
                res = self.session.post(url, data=body)
            else:
                res = self.session.get(url, params=body)
            
        else:
            url = self.action
            res = self.session.get(url, params=body)
        # print(f"[input->send_request] responce found{res}")
        # f = open(f"req{self.sent_request}.stat","w+")
        # f.write(res.text)
        # f.close()
        return res
            

    def create_request_body(self,payload):
        data = {}
        if self.type =="form":
            # print(self.inputs)
            for input_tag in self.inputs:
                # check if in static list
                if input_tag["name"] in self.static_param.keys():
                    data[input_tag["name"]] =self.static_param[input_tag["name"]]
                elif input_tag["type"] == "hidden":
                    # if it's hidden and not injection point use defult
                    if input_tag["input_use"] == "xx":
                        if input_tag["value"] == "":
                            data[input_tag["name"]] =random.choice(words_)
                        else:
                            data[input_tag["name"]] = input_tag["value"]
                    else:
                        data[input_tag["name"]] = payload
                elif input_tag["type"] == "select":
                    if input_tag["input_use"] == "static":
                        if input_tag["value"] == "":
                            value = random.choice(words_)
                        else:
                            value = input_tag["value"]
                    else:
                        value = payload
                    data[input_tag["name"]] = value
                elif input_tag["type"] != "submit":
                    if input_tag["input_use"] == "static":
                        if input_tag["value"] == "":
                            value = random.choice(words_)
                        else:
                            value = input_tag["value"]
                    else:
                        value = payload
                    data[input_tag["name"]] = value
                else:
                    data[input_tag["name"]] = ""
        else:
            for input_tag in self.inputs:
                    if input_tag["input_use"] == "static":
                        if "value" in input_tag.keys():
                            if input_tag["value"]:
                                value = input_tag["value"]
                            else:   
                                value = random.choice(words_)
                        else:
                            value = random.choice(words_)
                    else:
                        value = payload
                    
                    data[input_tag["name"]] = value
        
                
        return data

    def reset(self):
        # # how many responce seen in the past
        # self.seen_responce = 0

        # # how many request sent in the past
        # self.sent_request = 0
        pass

