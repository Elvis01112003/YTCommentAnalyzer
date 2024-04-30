from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import io
import pandas as pd
import numpy as np
import csv

## function definition

def scrapfyt(url):

  ## Opening Firefox and url

  option = Options()
  option.headless = True

  # Path to Firefox binary
  option.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe" 

  # Path to geckodriver executable
  geckodriver_path = r"C:\Users\elvis\OneDrive\Desktop\driver\geckodriver.exe"  

  driver = webdriver.Firefox(service=Service(geckodriver_path), options=option)

  driver.set_window_size(960, 800)  # minimizing window for optimum performance

  driver.get(url)
  time.sleep(2)

  ## Pause youtube video

  pause = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))

  pause.click()
  time.sleep(0.2)
  pause.click()
  time.sleep(4)

  ## Scrolling through all the comments

  # Initial Scroll
  driver.execute_script("window.scrollBy(0,500)")

  last_height = driver.execute_script("return document.documentElement.scrollHeight")

  while True:
    # Scroll down till "next load".
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load everything thus far.
    time.sleep(4)

    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
      break
    last_height = new_height

  # One last scroll just in case
  driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

  ## Scraping details

  ## title of video
  video_title = driver.find_element(By.NAME, 'title').get_attribute('content')

  ## owner of video
  video_owner1 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
  video_owner = []
  for owner in video_owner1:
    video_owner.append(owner.text)
  video_owner = video_owner[0]

  # total comments with replies
  video_comment_with_replies = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text + ' Comments'

  ## Scraping all the comments
  users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
  comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

  with io.open('comments.csv', 'w', newline='', encoding="utf-16") as file:
    writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(["Username", "Comment"])
    for username, comment in zip(users, comments):
      writer.writerow([username.text, comment.text])

  commentsfile = pd.read_csv("comments.csv", encoding="utf-16")

  all_comments = commentsfile.replace(np.nan, '-', regex=True)
  all_comments = all_comments.to_csv("Full Comments.csv", index=False)

  ##total comments without replies
  video_comment_without_replies = str(len(commentsfile.axes[0])) + ' Comments'

  ## Close driver

  driver.close()

  return all_comments, video_title, video_owner, video_comment_with_replies, video_comment_without_replies
