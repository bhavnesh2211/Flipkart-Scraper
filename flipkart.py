import requests
from pprint import pprint 
from bs4 import BeautifulSoup
import json,os

def scrape_mobile_details(page_url):
	file = "Flipkart/" + page_url[len(page_url) - 2:] + ".json"
	if os.path.isfile(file):
		with open (file, "r+") as data:
			read = data.read()
			return read
	else:		

		url = requests.get(page_url)
		soup = BeautifulSoup(url.text,"html.parser")
		All_mobile_details = {}
		div = soup.find_all("div", class_ = "_1UoZlX")
		for i in div:
			mobile_details = {}
			divs = i.find("div",class_ = "_1-2Iqu row")
			name = divs.find("div", class_ = "_3wU53n").getText()
			mobile_details["Name"] = [name]
			ratings = divs.find("div", class_ = "niH0FQ")
			if ratings == None:
				mobile_details["Ratings"] = [ratings]
			else:
				mobile_details["Ratings"] = [ratings.getText()]
			other_details = divs.find_all("li", class_ ="tVe95H")
			all_details = []
			for details in other_details:
				a = details.getText().split("\n")
				all_details.append(a)
			for j in range(len(all_details)):
				if j == 0:
					mobile_details["Memory"] = all_details[j]
				elif j == 1:
					mobile_details["Display"] = all_details[j]
				elif j == 2:
					mobile_details["Camera"] = all_details[j]
				elif j == 3:
					mobile_details["Battery"] = all_details[j]
				elif j == 4:
					mobile_details["Processor"] = all_details[j]
				else:
					mobile_details["Warranty"] = all_details[j]
			prize = divs.find("div",class_ = "_1vC4OE _2rQ-NK").getText()
			mobile_details["Prize"] = [prize]
			All_mobile_details[name] = mobile_details.copy()
			with open (file, "w+") as data_file:
				json.dump(All_mobile_details,data_file)
		return (All_mobile_details)
# pprint (scrape_mobile_details(page_url))
# pprint (details)


def All_pages_details():
	All_pages_mobile_details = {}
	url = requests.get("https://www.flipkart.com/search?q=all%204g%20mobile%20phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=offss")
	soup = BeautifulSoup(url.text,"html.parser")
	links = soup.find("nav", class_ = "_1ypTlJ")
	pages_links = links.find_all("a")
	count = 0
	for i in pages_links[:len(pages_links) - 1]:
		count += 1
		a = "https://www.flipkart.com" + i.get("href") 
		page = scrape_mobile_details(a)
		All_pages_mobile_details["Page" + str(count)] = page 
	return (All_pages_mobile_details)

pprint(All_pages_details())