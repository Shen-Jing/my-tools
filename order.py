import sys
import yaml
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import pymsteams

def send_teams(webhook_url: str, content: str, subtitle: str, title: str, color: str="000000") -> int:
    """
      - Send a teams notification to the desired webhook_url
      - Returns the status code of the HTTP request
        - webhook_url : the url you got from the teams webhook configuration
        - content : your formatted notification content
        - title : the message that'll be displayed as title, and on phone notifications
        - color (optional) : hexadecimal code of the notification's top line color, default corresponds to black
    """
    response = requests.post(
        url = webhook_url,
        headers = {"Content-Type": "application/json"},
        json = {
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": subtitle,
                "text": content
            }],
        },
    )
    return response.status_code # Should be 200

if datetime.today().weekday() >= 5:
    print("Today is weekend. No action.")
    sys.exit()
    
taipei_timezone = pytz.timezone("Asia/Taipei")
taipei_date = datetime.now(taipei_timezone).strftime('%Y/%m/%d')
url = "http://oas/leave/pages/OrderList01.jsp?queryStartDate={}&queryEndDate={}".format(taipei_date, taipei_date)
# url = "http://oas/leave/pages/OrderList01.jsp?queryStartDate={}&queryEndDate={}".format("2022/09/16", "2022/09/16")  # For testing

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

    #for idx, cell in enumerate(cells):
    #    print(idx, cell)
    uid_idx = 1
    location_idx = 6
    if location_idx >= len(cells):
        continue
    uid = cells[uid_idx].get_text().strip()
    location = cells[location_idx].get_text().strip()
    # print(uid)
    # print(location)
    if uid in user_set and location == "TW52":
        num_users += 1
        td_list.append(uid)

webhook_url = conf['webhook']
teams_title = "[Overtime Meal] " + taipei_date
# TODO: mention all
teams_subtitle = "The Number of Users: ***{}***".format(num_users)
teams_content = "Lists: *{}*".format(" ".join(td_list))
send_teams(webhook_url = webhook_url, title = teams_title, subtitle = teams_subtitle, content = teams_content)
# print(num_users)
# print(td_list)
