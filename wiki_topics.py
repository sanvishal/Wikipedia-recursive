from __future__ import unicode_literals
import bs4
import random as rand
try:
  import urllib.request as urllib2
except ImportError:
  import urllib2

#disguise as a human, but in reality you are a bot....hehe
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report"
f=opener.open(url)
data=str(f.read().decode("ascii",errors="ignore"))
f.close()
soup = bs4.BeautifulSoup(data,"html.parser")

#first name in the table
#print(soup.find("table",{"class" : "wikitable"}).find_all("td")[1].find("a").get("href"))
#the full list
topics = []
for i in range(1,26):
  link = soup.find("table",{"class" : "wikitable"}).find_all("tr")[i].find_all("td")[1].find("a").get("href")
  topics.append(link.split("/")[-1])

def print_topics():
  for i in topics:
    print(i)

def get_topics(n=5):
  return topics[:n+1]

def get_random_topics(n=5):
  return rand.sample(topics,n)
