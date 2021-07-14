from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import json
import shutil
import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import detect_matzip


def open_driver():
    if platform.system() == "Windows":
        driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    else:
        driver = webdriver.Chrome(executable_path="./chromedriver")

    # 인스타그램 계정 입력
    user_id = ""
    user_pw = ""

    driver.implicitly_wait(30)
    driver.get("https://www.instagram.com/")
    time.sleep(0.5)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(user_id)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(user_pw)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]").click()
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]")))
    return driver

def matzip_deep(driver, plusUrl = "홍대맛집"):
    baseUrl = 'https://www.instagram.com/explore/tags/'
    # plusUrl = input('검색할 태그를 입력하세요 : ')
    url = baseUrl + quote_plus(plusUrl)
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/header/div[1]/div/div/img")))
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    imglist = []
    postlist = []

    insta = soup.select(".v1Nh3.kIKUG._bz0w")

    for i in insta:
        print('https://www.instagram.com' + i.a['href'])
        img_url = i.select_one('.KL4Bh').img['src']
        # post_url = i.select_one('.KL4Bh').img['srcset'].split(',')[2][:-5]
        post_url = 'https://www.instagram.com' + i.a['href']
        imglist.append(img_url)
        postlist.append(post_url)
        print(img_url)
    print("여기까지 기본")

    # 스크롤하며 추가
    for count in range(7):
        print(count, "번째스크롤")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        insta = soup.select('.v1Nh3.kIKUG._bz0w')
        for i in insta:
            img_url = i.select_one(".KL4Bh").img["src"]
            if img_url not in imglist:
                print('https://www.instagram.com' + i.a['href'])
                print(img_url)
                post_url = 'https://www.instagram.com' + i.a['href']
                imglist.append(img_url)
                postlist.append(post_url)

    # 이미지 다운로드 코드
    n = 0

    for _ in range(len(imglist)):
        image_url = imglist[n]
        with urlopen(image_url) as f:
            with open("./media/" + postlist[n][28:-1] + str(n) + ".jpg", "wb") as h:
                img = f.read()
                h.write(img)
        n += 1

    eval_list = list(False for _ in range(len(imglist)))
    bowl_evaluated_list = list(False for _ in range(len(imglist)))

    detect_matzip.detector(imglist, ["Food"], ["person"], eval_list)


    # 사진들 ./img에 저장
    # n = 0
    # for _ in range(len(imglist)):
    #     if eval_list[n] is True:
    #         image_url = imglist[n]
    #         with urlopen(image_url) as f:
    #             with open("./img/" + plusUrl + str(n) + ".jpg", "wb") as h:
    #                 img = f.read()
    #                 h.write(img)
    #     elif eval_list[n] is False:
    #         pass
    #     n += 1

    n = 0
    for _ in range(len(imglist)):
        image_url = imglist[n]
        if eval_list[n] is True:
            post_json = {
                "post_url": postlist[n],
                "img_url": image_url,
                "keyword": plusUrl,
                "allowed": True,
            }
            resp = requests.post("http://127.0.0.1:8000/matzip/", data=post_json)
        elif eval_list[n] is False:
            post_json = {
                "post_url": postlist[n],
                "img_url": image_url,
                "keyword": plusUrl,
                "allowed": False,
            }
            resp = requests.post("http://127.0.0.1:8000/matzip/", data=post_json)
        print(resp.status_code)
        n += 1
    print(resp.text)
    print("total", len(imglist), "posts posted")

    # driver.close()


if __name__ == "__main__":
    driver = open_driver()
    search_text = input('검색할 태그를 입력하세요 : ')
    matzip_deep(driver, search_text)
