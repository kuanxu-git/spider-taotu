# -*- coding:utf-8 -*-

import time
import random
import sqlite3
import hashlib
import requests
import threading
import os

IMG_DIR = "imgs/"
#MD5函数
def hash_str(plain_str):
    md5 = hashlib.md5()
    md5.update(plain_str.encode('utf-8'))
    return md5.hexdigest()

def down_imgs(img_url, sub_dir):
    path = os.path.join(IMG_DIR, sub_dir)
    fname = os.path.join(path , hash_str(img_url) + '.jpg')
    if not os.path.exists(path):
        os.mkdir(path)
    r = requests.get(img_url)
    with open(fname,"wb+") as f:
        f.write(r.content)
        print("Success      " + hash_str(img_url) + '.jpg')


db = sqlite3.connect("spider_tt8.db",check_same_thread=False)
cur = db.cursor()
cur.execute("select name, urls from xiuren")
lines = cur.fetchall()

for line in lines:
    track_name = line[0].strip()
    urls = line[1]
    for url in str(urls).split(","):
        slim_url = url.strip()
        if "http" in slim_url:
            try:
                thread_name = "t" + str(random.randint(0, 9999))
                thread_name = threading.Thread(target=down_imgs, args=(slim_url, track_name))
                thread_name.start()
                time.sleep(0.1)
            except:
                pass