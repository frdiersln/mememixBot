import time
import os
import shutil
import datetime
from datetime import date


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from moviepy.editor import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def download():
    
    driver = webdriver.Chrome() 
    urls = ["https://coub.com/community/memes", "https://coub.com/community/animals-pets", "https://coub.com/community/sports", "https://coub.com/community/cars"]
    
    for url in urls:
        driver.get(url)
        dropdown = driver.find_element(By.CLASS_NAME, "page-menu__period-selector")
        dropdown.click()
        daily = driver.find_element(By.CLASS_NAME, "daily")
        daily.click()
        time.sleep(1)
        links = []
        for i in range(2):
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

    del(driver)
    del(urls)
    del(dropdown)
    del(daily)
    del(links) #clear ram

def move():
    winUserName = "frdie"
    source = 'C:/Users/{}/Downloads/'.format(winUserName)
    destination = 'C:/mememixBot/videos/'
    
    allfiles = os.listdir(source)
    
    u = open("uploaded.txt", "a+")
    u.seek(0)
    uploadedVideos = u.read().splitlines() 
    
    print(uploadedVideos)
    for f in allfiles:
        if f.endswith('.mp4'):
            if (f in uploadedVideos):
                os.remove(source + f)
                print("Uploaded video deleted.")
            else:
                shutil.move(source + f, destination + f)
                u.write(f + "\n")
            
    u.close()
    
    del(u)
    del(uploadedVideos)
    del(winUserName)
    del(source)
    del(destination)
    del(allfiles) #clear ram
            
def merge():
    videoFolder = 'C:/mememixBot/videos/'
    videos = os.listdir(videoFolder)

    clips1 = []
    clips2 = []
    clips3 = []
    clips4 = []

    quarterOfVid = len(videos) / 4

    for video in videos[:int(quarterOfVid)]:  
        clips1.append(VideoFileClip("C:/mememixBot/videos/" + video))
    quarter1 = concatenate_videoclips(clips1, method='compose')
    print("quarter1 created")

    for video in videos[int(quarterOfVid):(int(quarterOfVid)*2)]:
        clips2.append(VideoFileClip("C:/mememixBot/videos/" + video))
    quarter2 = concatenate_videoclips(clips2, method='compose')
    print("quarter2 created")

    half1 = concatenate_videoclips([quarter1, quarter2], method='compose')
    half1.write_videofile("half1.mp4")
    print("half1 created")

    del(clips1)
    del(clips2)
    del(quarter1)
    del(quarter2)
    del(half1) #clear ram

    for video in videos[(int(quarterOfVid)*2):(int(quarterOfVid)*3)]: 
        clips3.append(VideoFileClip("C:/mememixBot/videos/" + video))
    quarter3 = concatenate_videoclips(clips3, method='compose')
    print("quarter3 created")

    for video in videos[(int(quarterOfVid)*3):]: 
        clips4.append(VideoFileClip("C:/mememixBot/videos/" + video))
    quarter4 = concatenate_videoclips(clips4, method='compose')
    print("quarter4 created")

    half2 = concatenate_videoclips([quarter3, quarter4], method='compose')
    print("half2 created")

    del(clips3)
    del(clips4)
    del(quarter3)
    del(quarter4) #clear ram

    
    final = concatenate_videoclips([VideoFileClip("C:/mememixBot/half1.mp4"), half2], method='compose')
    final.write_videofile("result.mp4")
    print("final created")
    
    for video in videos:
        os.remove("C:/mememixBot/videos/" + video)
    print("videos deleted")

    del(half2)
    del(final)
    del(videos) #clear ram
    
def createThumbnail():
    img = Image.open('thumbnailBG.png')
    myFont = ImageFont.truetype('BADABB__.ttf', 189)
    with open('s.txt') as f:
        s = f.read()
        
    I1 = ImageDraw.Draw(img)
    I1.text((141, 89), "MEMEMIX \n  COMPILATION \n          #{}".format(s), font=myFont, fill =(255, 255, 255))
    img.save("thumbnail.png")
    
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
        'notifySubscribers': True
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

    del(CLIENT_SECRET_FILE)
    del(API_NAME)
    del(API_VERSION)
    del(SCOPES)
    del(service)
    del(upload_date_time)
    del(s)
    del(request_body)
    del(mediaFile)
    del(response_upload) #clear ram

# while True:
#     download()
#     print("downloaded")
#     move()
#     merge()
#     print("merged \n uploading")
#     upload()
#     createThumbnail()
#     for i in range(86000, 0, -1):
#         print("sleeping: " + str(i))
#         time.sleep(0.989)
