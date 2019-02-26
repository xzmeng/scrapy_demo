import os

from pymongo import MongoClient

BASE_DIR = '/home/xzmeng/图片/mm131/'
client = MongoClient(host='localhost', port=27017)
db = client['mm131']
girls = db['girls'].find()

girl_count = girls.count()
girl_completed = 0
pic_count = 0
pic_downloaded = 0

for girl in girls:
    girl_path = BASE_DIR + girl['title']
    to_download = int(girl['count'])
    downloaded = len(os.listdir(girl_path))
    if downloaded != to_download:
        print(girl['title'], '({}/{})'.format(downloaded, to_download))
    else:
        girl_completed += 1
    pic_count += to_download
    pic_downloaded += downloaded

print('girls: ({}/{})'.format(girl_completed, girl_count))
print('pics: ({}/{})'.format(pic_downloaded, pic_count))
