import time
import os
import shutil
import datetime
from datetime import date


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from moviepy.editor import *

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def download():
    
    driver = webdriver.Chrome()
    url = "https://coub.com/community/memes"
    driver.get(url)

    dropdown = driver.find_element(By.CLASS_NAME, "page-menu__period-selector")
    dropdown.click()
    daily = driver.find_element(By.CLASS_NAME, "daily")
    daily.click()
    time.sleep(1)
    links = []
    for i in range(10):
        titles = driver.find_elements(By.CLASS_NAME, "description__info")
        for title in titles:
            a = title.find_element(By.TAG_NAME , "a")
            link = a.get_attribute('href')
            if link[17] == 'v':
                if not link in links:
                    links.append(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
    for link in links:
        driver.get(link)
        time.sleep(0.26)
        download = driver.find_element(By.CLASS_NAME, "coub__download")
        download.click()

def move():
    winUserName = "frdie"
    source = 'C:/Users/{}/Downloads/'.format(winUserName)
    destination = 'C:/mememixBot/videos/'
    
    allfiles = os.listdir(source)
    
    for f in allfiles:
        if f.endswith('.mp4'):
            shutil.move(source + f, destination + f)
            
def merge():
    videoFolder = 'C:/mememixBot/videos/'
    videos = os.listdir(videoFolder)
    clips = []
    for video in videos:
        clips.append(VideoFileClip("C:/mememixBot/videos/" + video))
    final = concatenate_videoclips(clips, method='compose')
    final.write_videofile("result.mp4")
    for video in videos:
        os.remove("C:/mememixBot/videos/" + video)
    
def upload():
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = datetime.datetime(date.today().year, date.today().month, date.today().day, 14, 0, 0).isoformat() + '.000Z'

    with open('s.txt') as f:
        s = f.read()

    request_body = {
        'snippet': {
            'categoryI': 24,
            'title': 'mememix compilation V{}'.format(s),
            'description': 'Thanks for watching :)',
            'tags': ['meme', 'daily', 'coub', 'coubs', 'funny', 'trend', 'memes', 'compilation']
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload('result.MP4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()
    
    s = int(s) + 1
    s = str(s)
    f = open("s.txt", "w")
    f.write(s)
    f.close()
    
while True:
    download()
    print("downloaded")
    move()
    merge()
    print("merged \n uploading")
    upload()
    time.sleep(86000)