from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time, csv, json
from website.imagescrapper import imageFolder
from bs4 import BeautifulSoup
import pandas as pd
from website.database import firstdata, mongodata, mysqlfirstdata

path = "C:\Development\chromedriver"
s = Service(path)

print("final checking")


def youTubeScrapper(channelName):
    opt = webdriver.ChromeOptions()
    opt.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"')

    opt.add_argument("--start-maximized")
    # opt.add_argument("--headless")
    opt.add_argument("--mute-audio")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--incognito")
    opt.add_argument("--disable-dev-shn-usage")
    opt.add_argument("--disable-gpu")
    opt.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=s, options=opt)
    driver.delete_all_cookies()
    url = "https://www.youtube.com/results?search_query="+channelName
    driver.get(url)
    name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#channel-title #text')))
    subs = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#subscribers')))
    subscribers = subs.text
    print(subscribers)
    name.click()
    videotab = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div')))
    videotab.click()
    time.sleep(2)
    videoList10 = driver.find_elements(By.CSS_SELECTOR, "#dismissible #details h3 a")
    videoTitle = []
    videoLink = []
    subscriber = []
    time.sleep(2)
    views = driver.find_elements(By.CSS_SELECTOR, "#metadata-container #metadata-line span")
    viewList = [view.text for view in views]
    newview = [viewList[i] for i in range(len(viewList)) if i % 2 == 0]
    for video in videoList10:
        if video.text == "":
            pass
        else:
            link = video.get_attribute("href")
            videoLink.append(link)
            videoTitle.append(video.text)
            subscriber.append(subscribers)
    imagesList = imageFolder(videoLink, channelName)
    sr_no = [x + 1 for x in range(len(imagesList))]
    zipped = list(zip(sr_no, videoTitle, videoLink, imagesList, newview, subscriber))
    dataframe = pd.DataFrame(zipped, columns=["Sr.NO", "Title", "Links", "Image Link", "Views", "Subscriber"])
    firstdata(channelName, zipped)
    mysqlfirstdata(channelName, zipped)
    driver.quit()
    return dataframe



def videoDetails(url, channel):
    opt = webdriver.ChromeOptions()
    opt.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"')

    opt.add_argument("--start-maximized")
    # opt.add_argument("--headless")
    opt.add_argument("--mute-audio")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--incognito")
    opt.add_argument("--disable-dev-shn-usage")
    opt.add_argument("--disable-gpu")
    opt.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=s, options=opt)
    driver.delete_all_cookies()
    driver.get(url)
    # driver.implicitly_wait(15)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_text = soup.select_one("#container h1")
    if title_text.text =="":
        print("No Title")
        titleinfo = driver.find_element(By.CSS_SELECTOR, '.overlay .title')
        title = titleinfo.text
        three_dots = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#shorts-container #menu #button')))
        three_dots.click()
        desc = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="items"]/ytd-menu-service-item-renderer[1]/tp-yt-paper-item')))
        desc.click()
        info = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#items #factoids .factoid')))
        infotext = [x.text for x in info]
        likes = infotext[0].split("\n")[0]
        views = infotext[1].split("\n")[0]
        cross = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#header #visibility-button #button')))
        cross.click()
        time.sleep(2)
        comments = driver.find_element(By.CSS_SELECTOR, '#actions #comments-button')
        comments.click()
        print("comment button clicked")
        pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contents"]')))
        i = 0
        while i < 5:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)
            time.sleep(1)
            i += 1
        commentor_names = driver.find_elements(By.CSS_SELECTOR, '#header-author #author-text')
        comment_texts = driver.find_elements(By.CSS_SELECTOR, '#content #content-text')
        comment_list = [x.text for x in comment_texts]
        commentors = [x.text.lstrip().rstrip() for x in commentor_names]
        comments = comment_list
        driver.quit()
        total_comments = len(comment_list)
    else:
        try:
            like = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#top-level-buttons-computed a #text')))
            likes = like.text
        except:
            likes = "Unable to fetch"
        view = soup.select_one("#info #count .view-count")
        prev_h = 0
        while True:
            height = driver.execute_script("""function getActualHeight() {
                        return Math.max(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                        );
                    }
                    return getActualHeight();
                """)
            driver.execute_script(f"window.scrollTo({prev_h}, {prev_h +400})")
            time.sleep(1)
            prev_h +=800
            if prev_h >= 8000:
                break
        newsoup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        commentor_names = newsoup.select("#header-author #author-text")
        comment_texts = newsoup.select("#content #content-text")
        comment_list = [x.text for x in comment_texts]
        commentors = [x.text.lstrip().rstrip() for x in commentor_names]
        comments = comment_list
        print('comment extracting')
        total_comments = len(comment_list)
        title = title_text.text
        views = view.text
    vDict = {
        channel: {
            "title": title,
            "comment": comments,
            "commentor":commentors,
            "total comments":total_comments,
            "likes": likes,
            "view": views
        }
    }
    try:
        with open(" ".join(channel.split(" ")[:-1])+ ".json", "r") as data_file:
            data = json.load(data_file)
            data.update(vDict)
        with open(" ".join(channel.split(" ")[:-1])+ ".json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    except:
        with open(" ".join(channel.split(" ")[:-1])+ ".json", "w") as data_file:
            json.dump(vDict, data_file, indent=4)
    return vDict


def commentFile(chan):
    with open(chan + ".json", "r") as json_data:
        data1 = json.load(json_data)
        commentorList = []
        commentList = []
        for i in range(len(data1)):
            commentorList.append((data1[chan + " "+ str(i + 1)]["commentor"]))
            commentList.append(data1[chan + " "+ str(i + 1)]["comment"])
        commentorNames = [val.lstrip().rstrip().replace('"',"'") for sublist in commentorList for val in sublist]
        finalcomments = [val.replace('"',"'") for sublist in commentList for val in sublist]
        sr_no = [x + 1 for x in range(len(commentorNames))]
        zipped = list(zip(sr_no, commentorNames, finalcomments))
        dataframe = pd.DataFrame(zipped, columns=["Sr.NO", "Commentor", "Comments"])
        return dataframe
        # with open(chan + " videos comments.csv","w", encoding="utf-8", newline='') as datafile:
        #     fieldnames = ["Sr_No", "Commentor", "Comment"]
        #     writer = csv.writer(datafile)
        #     writer.writerow(fieldnames)
        #     sr_no = [x + 1 for x in range(len(commentorNames))]
        #     zipped = list(zip(sr_no, commentorNames, finalcomments))
        #     for i in range(len(zipped)):
        #         writer.writerow(zipped[i])

def ytScrapper(links, channel):
    start = time.time()
    a = 0
    while a < len(links):
        video = channel + " " + str(a+1)
        k = videoDetails(links[a], video)
        print("Scrapping the content, please wait.........")
        print(f"Video {str(a + 1)} added.")
        a +=1
    with open(channel + ".json", "r") as json_data:
        data1 = json.load(json_data)
        mongodata(data1, channel)
    print("Finally done")
    end = time.time()
    total_time = end - start
    print("\n"+ str(total_time))

def jsonfile(channel, k):
    with open(channel +".json", "r") as json_data:
        data1 = json.load(json_data)
        comments = data1[channel + " "+str(k)]["comment"]
        commentor = data1[channel + " " + str(k)]["commentor"]
        title = data1[channel + " " + str(k)]["title"]
        titlelist = [title for i in range(len(data1))]
        sr_no = [x+1 for x in range(len(data1))]
        zipped = list(zip(sr_no, titlelist, commentor, comments))
        data = pd.DataFrame(zipped, columns=["Sr.NO","Title", "Commentor", "Comments"])
        return data
