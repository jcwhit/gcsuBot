import praw
import config
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import date

def getToday():
    today = date.today()
    time = today.strftime("%b %-d %Y")
    #print time
    return time

def getTodaysPost():
    resp = BeautifulSoup(urllib2.urlopen("https://frontpage.gcsu.edu/announcementarchive").read(), 'html.parser') 
    announcements = resp.find_all('tr')
    #print announcements
    
    #get the posts with date in paralell lists for some 
    trOdd = resp.findAll('tr', class_=re.compile("odd"))
    trEven = resp.findAll('tr', class_=re.compile("even"))
    toPost = []
    for even in trEven:
        if(getToday() in even.getText()):
            toPost.append(str(even.contents))
    for odd in trOdd:
        if(getToday() in odd.getText()):
            toPost.append(str(odd.contents))
    return toPost

def bot_login():
    r = praw.Reddit(username = config.username, 
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
           user_agent = "gcsuBot v0.1")
    return r
    
def run_bot(r):
    posts = getTodaysPost()
    #scrape the data and format the post
    #get the links
    links = []
    titles = []
    for p in posts:
        soup = BeautifulSoup(p, 'html.parser')
        l = soup.find('a')
        links.append("https://frontpage.gcsu.edu"+str(l['href']))
        titles.append(str(l.getText()))
            
    #format to mark down
    markDown = "Beep Boop I'm a bot here to bring you fresh frontpage links! \n\n"
    if(len(titles)>0)
        for entry, title in zip(links,titles):
                markDown += "["+title+"]" + "(" + entry + ") \n\n"
        print markDown
    #make the submit when formatted correctly
        r.subreddit('gcsu').submit("Frontpage Daily Post: "+getToday(), markDown)
    else
        print "No links today"
    
#cron command 00 12 * * * cd /home/Documents/redditBot/; ./gcsuBot.py
r = bot_login()
run_bot(r)