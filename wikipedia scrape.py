from __future__ import unicode_literals
import bs4
import random as rand
try:
  import urllib.request as urllib2
except ImportError:
  import urllib2

#to graph...
import pydot as pd

#to generate topics
import wiki_topics

#disguise as a human, but in reality you are a bot....hehe
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def get_url(pagename):
    return "https://en.wikipedia.org/wiki/"+urllib2.quote(pagename.encode("utf-8"))

#gets title of the page
def get_page_title(url):
    return url.rstrip('/').split('/')[-1]

#gets title but incase there is a hyphen seperating the words
def get_page_name(page):
    return get_wiki_soup(get_url(page)).title.string.split("-")[0].strip()

#soups the URL
def get_wiki_soup(url):
    f=opener.open(url)
    data=str(f.read().decode("ascii",errors="ignore"))
    f.close()
    return bs4.BeautifulSoup(data,"html.parser")

#gets random article(mostly returns garbage)
def get_random_article():
  randomurl="https://en.wikipedia.org/wiki/Special:Random"
  o = opener.open(randomurl)
  pageurl = o.geturl()
  return pageurl.split("/")[-1]

#get first paragraph links
def first_paragraph_links(page):
    soup=get_wiki_soup(get_url(page))
    content=soup.find("div",id="mw-content-text")
    paragraphs=content.find_all("p")
    paragraph1=paragraphs[2]

    #If the first paragraph is just numbers, use the second paragraph(which doesn't seem to work for some reason)
    firstlink = paragraph1.find("a")
    '''if "id" in firstlink.parent.attrs and firstlink.parent["id"]=="coordinates":
        paragraph1=paragraphs[1]'''

    links = list(set([link.get("href") for link in paragraph1.find_all("a")]))
    pagenames = [str(l.split("/")[-1]) for l in links if l.startswith("/wiki/")]
    pagenames = [pn for pn in pagenames if not pn.startswith(("File:","Wikipedia:","Help:"))]
    pagenames = [pn.replace("_"," ") for pn in pagenames]
    return [pn.rsplit("#")[0] for pn in pagenames]

#number of links to limit - 6
def limit_links(links):
  ltemp = []
  if(len(links) > 6):
    ltemp = links[:6]
  else:
    return links
  return ltemp

#add info to the graph
def add_to_graph(links,nameurl):
  for i in links:
    if(i != nameurl):
      edge = pd.Edge(nameurl,i)
      graph.add_edge(edge)

#get random link from links
def get_random_link(links):
  return links[rand.randint(0,len(links)-1)]
  
#######################debug stuff##########################
nameurl = "Video_game"
links = limit_links(first_paragraph_links(nameurl))
link = get_random_link(links)
print("main link: {}".format(nameurl))
print("related articles: ")
print(", ".join(links))
print()
#plot the root graph
graph = pd.Dot(graph_type="digraph")
add_to_graph(links,nameurl)

for i in range(5):
  nameurl = link
  links = limit_links(first_paragraph_links(nameurl))
  link = get_random_link(links)
  print("next link: {}".format(nameurl))
  print("related articles: ")
  print(", ".join(links))
  print()
  add_to_graph(links,nameurl)

graph.write_png('graph1.png')

#next_link = get_wiki_soup(get_url("Norodom_Ranariddh")).find_all("p")[0].find("a").get("href").split('/')[-1]
#print(next_link)
#print()
#print(get_wiki_soup(get_url(next_link)).find_all("p")[0].find("a").get("href").split('/')[-1])

