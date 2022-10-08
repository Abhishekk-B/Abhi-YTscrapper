import re
import requests
import os

def imagedown(url, name):
    try:
        exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
        s = re.findall(exp, url)[0][-1]
        url_new = f"https://i.ytimg.com/vi/{s}/hqdefault.jpg"
    except:
        exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(shorts))\??v?=?([^#&?]*).*"
        s = re.findall(exp, url)[0][-1]
        url_new = f"https://i.ytimg.com/vi{s}/hqdefault.jpg"

    link = url_new
    with open(name + '.jpeg', 'wb') as f:
        im = requests.get(link)
        f.write(im.content)
        return url_new
main = os.getcwd()

def folder_creation(name):
    try:
        pathl = "website/static/images"
        os.chdir(pathl)
        os.mkdir(os.path.join(os.getcwd(), name))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), name))

def imageFolder(links, img_name):
    i = 1
    folder_creation(img_name)
    img_list = []
    while i<(len(links)+1):
        fileName = img_name + "-" + str(i)
        image_link = imagedown(links[i-1], fileName)
        i +=1
        img_list.append(image_link)
    os.chdir(main)
    return img_list
