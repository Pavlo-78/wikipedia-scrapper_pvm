import json
import requests
from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')


class wikiscrapper():
    def __init__(self, root_url):
            self.root_url = root_url
            self.web_status = None         
            self.cookie = None
            self.countries_lst=[]
            self.leaders_lst=[]


    def get_webstatus(self):
        """
        Check web status url, which is in property self.root_url

        :return: web status to the self.web_status property
        """     
        root_url = self.root_url  # "https://country-leaders.onrender.com"
        # query the /status endpoint using the get() method and store it in the req variable (1 line)
        req_status = requests.get(root_url+"/status")
        status = req_status.json()        
        self.web_status = req_status.status_code
        print(self.web_status)
        

    def get_cookies(self):
        """
        Receives cookies

        :return: Passes the cookie to the self.countries_lst property
        """ 
        root_url = self.root_url  # "https://country-leaders.onrender.com"
        # req_cookies = requests.get(root_url+"/cookie").cookies # print(cookie_file.status_code)
        self.cookie = requests.get(root_url+"/cookie").cookies # print(cookie_file.status_code)
        # get countries
        # req_countries = requests.get(root_url+"/countries",cookies=req_cookies)
        print("The cookies are received...")



    def get_countries(self):
        """
        Collects the list of countries from API.

        :return: list of countries to property self.countries_lst.
        """ 
        req_countries = requests.get(root_url+"/countries",cookies=self.cookie)
        # convert countries to dict
        lc=req_countries.json() # list_of_countries=list(ast.literal_eval(req_countries.text))        
        self.countries_lst = lc
        print("The country list is received...")
        


    def get_leaders(self, save_to_json = False ):
        """
        Collects the list of leaders from API. 
        If the parameter save_to_json=True , the data will be saved to a file

        :return: list of liders to property self.leaders_lst.
        Writes data to JSON-file "list_of_leadersData.json"(Optional)
        """   
        ls=[]
        for cc in (self.countries_lst):
            # define param of counrty code - #{"country": "us"} and  #get leaders list
            par_countrycode = {"country": cc }             
            rr = requests.get(root_url + "/leaders", par_countrycode,cookies = self.cookie)
            #convert response to list
            leaders_lst = rr.json() #            
            
            # leader-by-leader
            for a in(leaders_lst): # leaders_list >> list od dicts of leaders 
                  dct_leaderdata = {"country": cc}
                  dct_leaderdata.update(a)
                  ls.append(dct_leaderdata)
        self.leaders_lst=ls
        # saving if it needed
        if save_to_json == True:
            # Convert the list to a JSON-formatted string
            json_string = json.dumps(self.leaders_lst, indent=2, ensure_ascii=False) #indent=2 >> pretty-printing      
            # Leader's data to JSON-file
            with open("list_of_leaders.json", "w", encoding='utf-8') as json_file:
                json_file.write(json_string)  
        print("The leaders list is received...")       



    def get_1p_toJson(self):
        """
        Collects the first paragraph and saves it to a JSON file. 
        Uses the web link from the list of leaders in the self.leaders_lst property

        :return: writes data to JSON-file "list_of_leadersData.json"
        """         
        lst_leaders_data=[]
        # cycle lead-by_lead to get 1 paragraph
        for dct_x in(self.leaders_lst):            
            r = requests.get(dct_x['wikipedia_url']) # extract the link of this leader
            soup = BeautifulSoup(r.content, "lxml") # scrap data/1
            paragraphs = soup.find_all("p", attrs={"class": not "mw-empty-elp"}) # scrap data/2
            # extract 1 paragraph from tags
            first_paragraph=''            
            for paragraph in paragraphs:  # find article     
                if paragraph.find("b") is None:
                    continue
                else:
                    first_paragraph = paragraph.text
                    break           
            dct_xx = dct_x.copy()
            dct_xx["first_paragraph"] = first_paragraph
            lst_leaders_data.append(dct_xx)
        # Converting the data list to a JSON-formatted string (nice print)
        json_string = json.dumps(lst_leaders_data, indent=2, ensure_ascii=False) #indent=2 >> pretty-printing
        # SavinglLeader's data to JSON-file
        with open("list_of_leadersData.json", "w", encoding='utf-8') as json_file:
            json_file.write(json_string)
        print("The scrapped data is saved to Json.")


"""----------------------------------
-----------START SCRAPPING-----------
----------------------------------"""
root_url="https://country-leaders.onrender.com"
# create object of class
w = wikiscrapper(root_url)
# Running the data collection algorithm step-by-step
w.get_webstatus()
w.get_cookies()
w.get_countries()
w.get_leaders(True)
w.get_1p_toJson()        