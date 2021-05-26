# -*- coding:utf-8 -*-
import os
import sys
import re
import requests

UC_PATH = 'D:/CloudMusic/cache/Cache'  # 缓存路径 例 D:/CloudMusic/Cache/
MP3_PATH = 'D:/CloudMusic/converter'  # 存放歌曲路径


class Transform():
    def __init__(self, uc_path, mp3_path):
        super().__init__()
        self.uc_path = uc_path
        self.mp3_path = mp3_path
    
    def do_transform(self):
        if self.uc_path[-2:] != 'uc':  # 后缀uc结尾为歌曲缓存
            print('Not an uc file!')
            return 1
        uc_file = open(self.uc_path, mode='rb')
        uc_content = uc_file.read()
        mp3_content = bytearray()
        for byte in uc_content:
            byte ^= 0xa3
            mp3_content.append(byte)
        song_id = self.get_songid_by_filename(self.uc_path)
        print('song_id:', song_id)
        song_name = self.get_song_info(song_id)
        print('song_name:', song_name)
        mp3_file_name = self.mp3_path + '%s.mp3' % (song_name)
        mp3_file = open(mp3_file_name, 'wb')
        mp3_file.write(mp3_content)
        uc_file.close()
        mp3_file.close()
        print('success %s' % mp3_file_name)
        return 0

    def get_songid_by_filename(self, file_name):
        match_inst = re.search('[0-9]+', file_name)
        print('match_inst:', match_inst)
        # -前面的数字是歌曲ID，例：1347203552-320-0aa1
        if match_inst.group():
            return match_inst.group()
        return 'song'

    def get_song_info(self, song_id):
        if not song_id:
            return str(song_id), ''
        try:
            url = 'https://api.imjad.cn/cloudmusic/'
        # 请求url 例子：https://api.imjad.cn/cloudmusic/?type=detail&id=1347203552
            payload = {'type': 'detail', 'id': song_id}
            reqs = requests.get(url, params=payload)
            jsons = reqs.json()
            song_name = jsons['songs'][0]['name']
            return song_name
        except Exception as e:
            print('Exception', e)
            return str(song_id)


def check_path():
    global UC_PATH, MP3_PATH
    if not os.path.exists(UC_PATH):
        print('缓存路径错误: %s' % UC_PATH)
        return False
    if not os.path.exists(MP3_PATH):
        print('目标路径错误: %s' % MP3_PATH)
        return False
    if MP3_PATH[-1] != '\\':
        MP3_PATH += '\\'
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        UC_PATH = sys.argv[1]
    if len(sys.argv) > 2:
        MP3_PATH = sys.argv[2]
    if not check_path():
        exit()

    transform = Transform(UC_PATH, MP3_PATH)
    transform.do_transform()
    print('Done.')
