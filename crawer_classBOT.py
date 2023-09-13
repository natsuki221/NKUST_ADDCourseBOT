import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re

# 開啟網頁的基礎設定（停止顯示彈出視窗）
options = Options()
options.add_argument('--disable-notifications')
chrome = webdriver.Chrome(options=options)
# chrome = webdriver.Chrome('./chromedriver')
userID = '你的學號'
passwrd = '你的密碼'
course_code = '課程代碼'

urls = ['https://aais6.nkust.edu.tw/selcrs_std', 'https://aais7.nkust.edu.tw/selcrs_std', 'https://aais8.nkust.edu.tw/selcrs_std']
url1 = 'https://aais6.nkust.edu.tw/selcrs_std'
url2 = 'https://aais7.nkust.edu.tw/selcrs_std'
url3 = 'https://aais8.nkust.edu.tw/selcrs_std'
url_add_select = '/AddSelect/AddSelectPage'


def open_web(url):
    # 開啟網頁
    chrome.get(url)

    # 找到網頁上表格位置
    account_form = chrome.find_element(By.ID, 'UserAccount')
    password_form = chrome.find_element(By.ID, 'Password')
    account_form.send_keys(userID)
    password_form.send_keys(passwrd)
    time.sleep(3)
    chrome.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div[3]/div/button').click()

    # 檢查網頁是否刷新資料
    try:
        element = WebDriverWait(chrome, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav"))
        )
    except:
        chrome.quit()

    course_selection(url)


def course_selection(url):
    chrome.get(url+url_add_select)
    # 檢查網頁是否刷新資料
    try:
        WebDriverWait(chrome, 30).until(
            EC.presence_of_element_located((By.ID, "courseDataTable_info"))
        )
    except:
        chrome.quit()

    course_form = chrome.find_element(By.ID, 'scr_selcode')
    course_form.send_keys(course_code)
    chrome.find_element(By.ID, 'courseSearch').click()

    # 檢查網頁是否刷新資料
    try:
        WebDriverWait(chrome, 30).until(
            EC.presence_of_element_located((By.ID, course_code))
        )
        chrome.find_element(By.ID, course_code).click()
    except:
        chrome.quit()
    time.sleep(1)

    messages = chrome.find_element(By.ID, course_code).text
    # print(messages)

    if messages == '額滿 Failed':
        print('額滿')
        time.sleep(5)
        course_selection(url)
    elif messages == '已加入 Completed':
        print('已加入')
        chrome.quit()
    else:
        print('ERROR')
        chrome.quit()


open_web(url1)



# {result: 71, MessageBotton: '額滿\nFailed', MessageShow: '限修人數已額滿!<br/>No vacancy for the restricted courses'}
# {result: 1, MessageBotton: '已加入\nCompleted', MessageShow: '加入選課完成！<br/>Completed！'}
time.sleep(3)
chrome.quit()
