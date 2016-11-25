#!/usr/bin/env python3
import webbrowser
import redis
import os
from time import sleep
from pprint import pprint
from boxsdk import OAuth2
from boxsdk import Client


class Box:
    def __init__(self):
        self.client = None
        self.refresh_token = None
        self.authorization_url = None
        self.authorization_code = None
        self.access_token = None
        self.user = None
        self.oauth = OAuth2(
            client_id='77bubh1k3d3f0e06606o6mcuvl1w6brg',
            client_secret='c77Xma34aNdvBMkURvElDGS4RNO3goZh'
        )
        self.redirect_url = 'http://localhost:8080'
        self.root_directory = '0'

    def authorization(self):
        self.authorization_url, self.refresh_token = self.oauth.get_authorization_url(self.redirect_url)
        webbrowser.open(self.authorization_url)
        if not self.get_auth_tocken():
            return False
        self.access_token, dummy = self.oauth.authenticate(self.authorization_code)
        self.client = Client(self.oauth)
        self.user = self.client.user(user_id='me').get()

    def get_auth_tocken(self):
        """
        get auth code for oauth
        :return: auth code
        """
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        for i in range(60):
            auth_code = r.get(self.refresh_token)
            if not auth_code:
                sleep(1)
            else:
                # print(auth_code)
                self.authorization_code = auth_code
                return True
        return False

    def list(self, folder_id, limits=100):
        items = self.client.folder(folder_id=folder_id).get_items(limit=limits, offset=0)
        return items

    def download(self, file, destination):
        with open(os.path.join(destination, file.name), 'wb') as f:
            self.client.file(file_id=file.id).download_to(f)

    def upload(self, folder, file):
        folder.upload(file_path=file)


if __name__ == '__main__':
    box = Box()
    box.authorization()
    box_items = box.list(box.root_directory)
    upload_folder = None
    for each_item in box_items:
        if each_item.name == 'test':
            print(each_item)
            upload_folder = each_item
            test_items = box.list(each_item.id)
            for each_file in test_items:
                print(each_file)
                box.download(each_file, '/home/zhihua/work/sunyi/temp/')
    box.upload(folder=upload_folder, file='/home/zhihua/work/sunyi/temp/test.pdf')


