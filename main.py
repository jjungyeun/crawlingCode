from bs4 import BeautifulSoup
import time
import os
import urllib.request
from urllib.error import URLError, HTTPError

from selenium import webdriver

count = 0

dir_name = time.strftime("DOWNLOAD_%Y%m%d_%H%M%S", time.gmtime())
os.mkdir('./img/' + dir_name)

def downloadImage(download_url, img_name):
    # error 처리 필요
    try:
        urllib.request.urlretrieve(download_url, "./img/"+ dir_name + '/' + img_name + '.jpg')
        print("download image : ",download_url)
        global count
        count += 1

    except HTTPError as e:
        print("HTTPError on url "+str(download_url))
        print (e)
    except URLError as e:
        print("URLError on url "+str(download_url))
        print (e)

def crawling(url, page):
    start = time.time()
    path = "C:/Users/wjy/Downloads/chromedriver/chromedriver.exe" # chromedriver.exe 다운로드 필수
    driver = webdriver.Chrome(path)

    original_url = url
    tmp_url = original_url.split('&')
    if tmp_url[2].find('Page=') == -1:
        tmp_url.insert(2,'')
    for i in range(1,page+1):
        print('\nPage ',i)
        tmp_url[2] = "Page="+str(i)
        url = "&".join(tmp_url)

        try:
            driver.get(url)

            elem = driver.find_element_by_id("usedcarList")
            l = elem.get_attribute("outerHTML")

            soup = BeautifulSoup(l, "html.parser")
            img = soup.find_all("img")

            for i in img:
                img_src = str(i.get("src"))
                arr_src = img_src.split('/')
                # print(arr_src)

                # site에 따른 다운로드 링크 생성
                site = arr_src[2]
                if site == "autoimg.danawa.com":
                    if arr_src[5] == 'icon' or arr_src[5] == 'banner':
                        continue
                    arr_src[8] = arr_src[8].replace('_thumb','')

                    img_name = arr_src[8].split('.')[0]
                    img_name = img_name[:len(img_name) - 1]
                    for i in range(1,5):
                        arr_src[8] = img_name + str(i) + '.jpg'
                        download_url = '/'.join(arr_src)
                        # 이미지 다운로드
                        downloadImage(download_url, arr_src[8])

                elif site == "www.m-park.co.kr":
                    img_name = arr_src[7].split('.')[0]
                    img_name = img_name[:len(img_name)-1]
                    for i in range(1,5):
                        arr_src[7] = img_name + str(i) + '.jpg'
                        download_url = '/'.join(arr_src)
                        # 이미지 다운로드
                        downloadImage(download_url, arr_src[7])

                elif site == "www.kukmincha.com":
                    arr_src[4] = 'original'
                    img_name = arr_src[6].split('.')[0]
                    img_name = img_name[:len(img_name) - 1]
                    for i in range(1, 5):
                        arr_src[6] = img_name + str(i) + '.jpg'
                        download_url = '/'.join(arr_src)
                        # 이미지 다운로드
                        downloadImage(download_url,arr_src[6])
                else:
                    img_name = arr_src[len(arr_src)-1]
                    downloadImage(img_src, img_name)
        except:
            break

    print("\n크롤링 종료")
    print("다운로드한 이미지 개수 : ",count)
    print("크롤링 소요 시간 : ",round(time.time() - start, 6))


# url = "http://auto.danawa.com/usedcar/?Work=list&Tab=list&Page=1&Order=7&Brand=371&Series=2857&Model="
url = input("다나와자동차-중고차-특정 브랜드(&시리즈&모델) 리스트 주소를 입력해주세요\n(입력 안되면 스페이스바 누르고 엔터):\n")
crawling(url,page=10)
