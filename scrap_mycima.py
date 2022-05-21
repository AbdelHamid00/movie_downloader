from bs4 import BeautifulSoup as bs
import requests
import sys


def url(soup, class_tag, href_tag):
    a = []
    for link in soup.find_all('a'):
        link_file = link.get('class')
        if type(link_file) == list:
            if class_tag == link_file:
                if href_tag in link.get('href'):
                    a.append(link.get('href'))
    return a

def check(link, a):
    for i in a:
        if i in link:
            return False
    return True

def url_file(soup, href_file, quality):
    q1 = quality + "p"
    for link in soup.find_all('a'):
        l = link.get('href')
        if href_file in l:
            if q1 in l:
                print("Dowload...")
                file_name = l.split(sep="/")[-1].split(sep=".mp4")[0] + ".mp4"
                fd = open(file_name, "wb")
                fd.write(requests.get(l).content)
                print("Dowload succes :", file_name)
                fd.close()

def add(list_saisons, ad):
    p = []
    p.append(ad)
    for i in list_saisons:
        p.append(i)
    return p

quality = ["480", "720", "1080"]
if len(sys.argv) != 5 or sys.argv[1] != '-q' or not(sys.argv[2] in quality):
    print("Run it in this way : python3 beautifulsoup.py -q [1080 or 720 or 480] [-s for serie or -f for film][URL]")
    exit()
href_episodes = "/watch/"
href_series = "/series/"
href_file = ".mp4"

soup = bs(requests.get(sys.argv[4]).text, "lxml")
tag = ["hoverable", "activable"]

if sys.argv[3] == '-s':
    list_saisons = add(url(soup, tag, href_series) , sys.argv[4])
    for lien in list_saisons:
        soup = bs(requests.get(lien).text, "lxml")
        list_episodes = url(soup, tag, href_episodes)
        for i in list_episodes:
            soup = bs(requests.get(i).text, "lxml")
            url_file(soup, href_file, sys.argv[2])
elif sys.argv[3] == '-f':
    url_file(soup, href_file, sys.argv[2])
else:
    print("Run it in this way : python3 beautifulsoup.py -q [1080 or 720 or 480] [-s for serie or -f for film][URL]")
