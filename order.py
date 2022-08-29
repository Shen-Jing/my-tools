import sys
import yaml
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import datetime

if datetime.today().weekday() >= 5:
    print("Today is weekend. No action.")
    sys.exit()
    
td = datetime.today().strftime('%Y/%m/%d')
url = "http://oas/leave/pages/OrderList01.jsp?queryStartDate={}&queryEndDate={}".format(td, td)
conf = yaml.load(open('order_auth.yaml'))  # deprecated, need to modify
userid = conf['user']['userid']
pwd = conf['user']['password']
response = requests.post(url, verify=False, auth=HTTPBasicAuth(userid, pwd))
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())

with open("coworker.txt") as f:
    user_list = f.read().splitlines()
user_set = set(user_list)
td_list = []
num_users = 0
rows = soup.find("tbody").find_all("tr")
for row in rows:
    cells = row.find_all("td")
    uid_idx = 1
    if uid_idx >= len(cells):
        continue
    uid = cells[uid_idx].get_text().strip()
    # print(uid)
    if uid in user_set:
        num_users += 1
        td_list.append(uid)
print(num_users)
print(td_list)