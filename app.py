import requests
import butler
import os
import urlparse
import psycopg2


def get_posts(cur):
	r = requests.get('http://reddit.com/r/todayilearned/hot.json')
	content = r.json()
	b = butler.Butler(content)
	articles = cur.execute("SELECT id FROM REDDIT")
	for child in b.find(["data", "children"]):
		if int(child["data"]["ups"]) > 1000 and child["data"]["id"] not in articles:
			post_data = (child["data"]["id"], child["data"]["permalink"], int(child["data"]["ups"]))
			yo = send_yo(api_token, "http://reddit.com" + child["data"]["permalink"])
			cur.execute("INSERT INTO REDDIT VALUES (%s)", post_data)
	return

			
def send_yo(api_token, link):
	r = requests.post("http://api.justyo.co/yoall/", data={"api_token": api_token, "link": link})
	return r


def start():
	with open("api_token.txt", "r") as f:
		api_token = f.read()
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])
	conn = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	cur = conn.cursor()
	get_posts(cur)
	return

start()