import time
import os
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By

from moviepy.editor import *

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
    for i in range(14):
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
    source = 'C:/mememixBot/videos/'
    videos = os.listdir(source)
    clips = []
    for video in videos:
        clips.append(VideoFileClip("C:/mememixBot/videos/" + video))
    final = concatenate_videoclips(clips)
    final.write_videofile("result.mp4")
    for video in videos:
        os.remove("C:/mememixBot/videos/" + video)
    
