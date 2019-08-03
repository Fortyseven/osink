import sys
import utils
import re
import json
import datetime
from pprint import pprint
from bs4 import BeautifulSoup
from UsernameProbe import UsernameProbe


class InstagramProbe(UsernameProbe):
    def __init__(self, state, username):
        UsernameProbe.__init__(self,
            state,
            "Instagram",
            username,
            "get",
            "https://www.instagram.com/{}/")
        self.run()


    def processResponse(self, response):
        html = response.text.encode('utf-8').strip()
        regex = r"\"biography\":\"([^\"]*)\""
        matches = re.search(regex, html)

        self.profile_data['URL'] = self.url.format(self.username)
        self.profile_data['Bio'] = matches.group(1)

        content = BeautifulSoup(response.text, 'html.parser')

        title = content.findAll("meta", property="og:title")[0]['content'].encode('utf-8')
        self.profile_data['Title'] = title[:-31].strip()
        desc = content.findAll("meta", property="og:description")[0]['content'].encode('utf-8')
        self.profile_data['Desc'] = desc[:-70].strip()
        # self.profile_data['URL2'] = content.findAll("meta", property="og:url")[0]['content'].encode('utf-8')