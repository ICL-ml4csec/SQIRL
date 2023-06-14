import pprint
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import copy
from urllib.parse import urlsplit, urlunsplit
from regex import E
from Environment.Input.import_utilities import import_attr
import requests
from Environment.Input.Input import Input
from Environment.Input.Input_Identifier import Input_Identifier
from playwright.sync_api import sync_playwright 
import json
class Crawler:
    def __init__(self,max_depth_level,login_module, verbose=5, ) -> None:
        self.max_depth_level = max_depth_level
        self.max_urls_found = 10
        self.input_tokinizer = Input_Identifier()
        self.urls_queue = []
        self.verbose=verbose
        self.forms = []
        self.dynamic_inputs = []
        self.session = None
        self.urls_found = []
        self.pp = pprint.PrettyPrinter(indent=4)
        self.login_url = None
        self.data = None
        self.max_local_links = 1000
        if login_module['module_path'] is not None and login_module['function'] is not None: 
            self.login_function = import_attr(login_module['module_path'], login_module['function'])
        else:
            self.login_function = None
        self.login_module = login_module
        pass

    def login(self):
        self.session  = requests.Session()
        if self.login_function is not None:
            self.session = self.login_function(self.session)


            
            

    def crawl_possible_inputs(self,url):
        '''
            - get dynamic urls that are possible to send inputs
            - get token for input
            - create inputs to represent dynamic urls
        '''
        # create session and login

        self.login()

        # get inputs
        assert(url is not None)

        try:
            current_forms, current_dynamic_inputs = self.readlinks(url)
            self.forms.extend(current_forms)
            self.dynamic_inputs.extend(current_dynamic_inputs)
        except Exception as ex:
            print("[!] exception 1 at crawl_possible_inputs:")
            ex.with_traceback(0)
            
        level = 0
        while (int(level) <= int(self.max_depth_level)):
            level = level+1
            if (int(level) <= int(self.max_depth_level)):
                try:
                    copy_url_queue = self.urls_queue.copy()
                    self.urls_queue = []
                    for current_link in copy_url_queue:
                        current_forms, current_dynamic_inputs = self.readlinks(current_link)
                        self.forms.extend(current_forms)
                        self.dynamic_inputs.extend(current_dynamic_inputs)
                        
                except Exception as ex:
                    print("[!] exception 2 at crawl_possible_inputs: " + str(ex))
                    pass
            else:
                if len(self.urls_queue) > 0 and self.verbose > 0:
                    print("[-] stoping crawling due to max depth reached and urls queue not empty")
                break

        # replacate multivariables to have one injection point and rest as static
        self.forms.extend(self.dynamic_inputs)
        multivariables = self.forms
        multivariables = self.replacate_multivariable(multivariables)

        # tokinize and create inputs
        inputs = [Input(current_possible_input,self.input_tokinizer.get_next_token(), self.login_function) for current_possible_input in multivariables]
        return inputs

    def readlinks(self,url):

        # clean url
        new_url = re.sub(r"/#.*","",url)
        url = new_url
        if url in self.urls_found:
            return [],[]
        else:
            self.urls_found.append(url)

        forms = []
        dynamic_urls = []
        try:
            self.login()
            r  = self.session.get(url, verify=False)
            data = r.text


            soup = BeautifulSoup(data, "lxml")
            parsed_uri = urlparse(url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            domain = domain.split(':')[0]
        except Exception as ex:
            print("[!] exception at readlinks: " + str(ex))
            return [],[]
        

        # adding extra feature of reading js network
        links_to_be_explored = []
        with sync_playwright() as p: 

            def handle_response(response): 
                print(f"[Crawler->read links] intercept js request: {response.url}") 
                links_to_be_explored.append({"href":str(response.url)})
            try:
                browser = p.chromium.launch() 
                page = browser.new_page(storage_state=self.storage)


                # go to wanted page
                page.on("response", handle_response) 
                page.goto(url, wait_until="networkidle") 

                page.context.close() 
            except:
                pass

        # getting forms
        links_found = 0
        # get forms
        for form in soup.find_all('form'):
            details = self.get_form_details(form,url)
            if details is not None:
                # compare by action url
                current_action = str(details["action"])

                # compare by input
                current_inputs = Crawler.get_input_names(details["inputs"])
                if any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in forms]) or any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in self.forms]):
                    pass
                else:

                    forms.append(details)
            links_found += 1
            if links_found > self.max_local_links:
                break

        # getting dynamic links and normal links
        # get next links to be added into the queue and dynamic links
        links_to_be_explored.extend(soup.find_all('a'))
        for link in links_to_be_explored:

            # IF LINK IS NOT NULL
            if link.get('href') is not None:
                parsed_uri = urlparse(link.get('href'))
                # IF LINK STARTS WITH HTTP
                if link.get('href')[:4] == "http":
                    # SAME ORIGIN
                    if domain in link.get('href'):
                        # IF URL IS DYNAMIC
                        if "?" in link.get('href'):
                            details = self.get_dynamic_link_details(link.get('href'))


                            # compare the current details with the past data
                            # compare by action url
                            current_action = str(details["action"])

                            # compare by input
                            current_inputs = Crawler.get_input_names(details["inputs"])
                            if any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in dynamic_urls]) or any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in self.dynamic_inputs]):
                                pass
                            else:
                              self.urls_queue.append(re.sub(r"/#.*","",link.get('href')))
                              dynamic_url_details = self.get_dynamic_link_details(link.get('href'))
                              dynamic_urls.append(dynamic_url_details)
                        else:
                            proposed_url = link.get('href')
                            if  all([proposed_url != current_url for current_url in self.urls_queue]):
                              self.urls_queue.append(link.get('href'))
                # IF URL IS DYNAMIC
                elif "?" in link.get('href'):
                    details = self.get_dynamic_link_details(url + "/" + link.get('href'))
                    # compare the current details with the past data
                    # compare by action url
                    current_action = str(details["action"])

                    # compare by input
                    current_inputs = Crawler.get_input_names(details["inputs"])
                    if any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in dynamic_urls]) or any([current_action == current_details["action"] and current_inputs == Crawler.get_input_names(current_details["inputs"]) for current_details in self.dynamic_inputs]):
                        pass
                    else:
                      self.urls_queue.append(re.sub(r"/#.*","",url + "/" + link.get('href')))
                      dynamic_url_details = self.get_dynamic_link_details(url + "/" + link.get('href'))

                      dynamic_urls.append(dynamic_url_details)
                # ELSE NORMAL LINK FOUND
                else:
                    proposed_url = url + "/" + link.get('href')
                    if all([proposed_url != current_url for current_url in self.urls_queue]):
                      self.urls_queue.append(re.sub(r"/#.*","",url + "/" + link.get('href')))
            links_found += 1
            if links_found > self.max_local_links:
                break
        return forms, dynamic_urls

    def get_form_details(self,form,url):
        '''
            get all detatils of the form:
            - inputs and its type and value
            - action
            - method type
            - Returns the HTML details of a form,including action, method and list of form controls (inputs, etc)
        '''
        details = {}
        details["parent_link"] = url
        if form.attrs.get("action") is None or str(form.attrs.get("action")) == "":
            action = url
        else:
            # get the form action (requested URL)
            action = form.attrs.get("action").lower()
            url_parsed = urlsplit(url)
            if str(url_parsed.scheme) in action:
                pass
            else:
                action = str(url_parsed.scheme) + "://"  + str(url_parsed.netloc)  + "/" + str(action)
        # get the form method (POST, GET, DELETE, etc)
        # if not specified, GET is the default in HTML
        method = form.attrs.get("method", "get").lower()
        # extract inputs
        inputs = []
        for input_tag in form.find_all("input"):
            # print(input_tag)
            # get type of input form control
            input_type = input_tag.attrs.get("type", "text")
            # get name attribute
            input_name = input_tag.attrs.get("name")
            # get the default value of that input tag
            input_value =input_tag.attrs.get("value", "")

            input_id = input_tag.attrs.get("id")
            # add everything to that list
            inputs.append({"type": input_type, "name": input_name, "value": input_value, 'id': input_id})

        # extract select
        for select in form.find_all("select"):
            # get the name attribute
            select_name = select.attrs.get("name")
            # set the type as select
            select_type = "select"
            select_options = []
            # the default select value
            select_default_value = ""
            # iterate over options and get the value of each
            for select_option in select.find_all("option"):
                # get the option value used to submit the form
                option_value = select_option.attrs.get("value")
                if option_value:
                    select_options.append(option_value)
                    if select_option.attrs.get("selected"):
                        # if 'selected' attribute is set, set this option as default    
                        select_default_value = option_value
            if not select_default_value and select_options:
                # if the default is not set, and there are options, take the first option as default
                select_default_value = select_options[0]
            # add the select to the inputs list
            inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})

        # extarct textarea
        for textarea in form.find_all("textarea"):
            # get the name attribute
            textarea_name = textarea.attrs.get("name")
            # set the type as textarea
            textarea_type = "textarea"
            # get the textarea value
            textarea_value = textarea.attrs.get("value", "")
            # add the textarea to the inputs list
            inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})

        for current_button in form.find_all("button"):
            name = current_button.attrs.get("name")
            type = "button"
            value = current_button.attrs.get("value", "")
            inputs.append({"type": type, "name": name, "value": value})

        # put everything to the resulting dictionary
        details["type"] = "form"
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details
        
    def get_dynamic_link_details(self,url:str):
        '''
            get all detatils of the dynamic link:
            - inputs
            - base url
        '''

        # get list of variables
        base_url = url.split("?")[0]

        variables = url.split("?")[1]

        try:
          variables = variables.split("&")
        except:
          pass
        length = len(variables)
        current_idx = 0
        while current_idx < length:
            if len(variables[current_idx].split("=")) < 2:
                variables.pop(current_idx)
                length -= 1
            else:
                current_idx += 1

        variables = [{"name":current_var.split("=")[0],"value":current_var.split("=")[1]} for current_var in variables]
        details={}
        details["type"] = "dynamic_link"
        details["action"] = base_url
        details["inputs"] = variables
        details["parent_link"] = url

        return details
        pass

    def replacate_multivariable(self,multivariables):
        '''
            replecate forms and mark the injection input and static inputs
        '''
        result_forms = []
        for current_form in multivariables:
            # iterate over each input everytime creating
            # a copy of orig form and setting injection
            # point and static point
            for current_input in range(len(current_form["inputs"])):
                current_new_form = copy.deepcopy(current_form)
                for new_current_input in range(len(current_new_form["inputs"])):
                    if current_input == new_current_input:
                        current_new_form["inputs"][new_current_input]["input_use"] = "injection_point"
                    else:
                        current_new_form["inputs"][new_current_input]["input_use"] = "static"
                result_forms.append(current_new_form)
        return result_forms

    def get_input_names(inputs):
        return [current['name'] for current in inputs]