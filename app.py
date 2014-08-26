import requests
import butler
import pymongo


def get_posts(til):
	r = requests.get('http://reddit.com/r/todayilearned/hot.json')
	content = r.json()
	b = butler.Butler(content)
	articles = til.find({}, {'_id': 1})
	for child in b.find(["data", "children"]):
		if child["data"]["ups"] > 1000 :
			data = {"_id": child["data"]["id"], "link": child["data"]["permalink"], "ups": child["data"]["ups"]}
			yo = send_yo(api_token, "http://reddit.com" + child["data"]["permalink"])
			til.insert(data)
	return

			
def send_yo(api_token, link):
	r = requests.post("http://api.justyo.co/yoall/", data={"api_token": api_token, "link": link})
	return r


with open("api_token.txt", "r") as f:
	api_token = f.read()
# connection = pymongo.Connection(<arguments>)
# db = connection.reddit
# til = db.til
get_posts(til)