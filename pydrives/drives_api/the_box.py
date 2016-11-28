#!/usr/bin/env python3
import webbrowser
import redis
import os
from time import sleep
from boxsdk import OAuth2
from boxsdk import Client
from boxsdk.object.folder import Folder, File
from termcolor import colored
from pydrives.config import config


class Box:
    def __init__(self):
        self.client = None
        self.refresh_token = None
        self.authorization_url = None
        self.authorization_code = None
        self.access_token = None
        self.user = None
        self.oauth = OAuth2(
            client_id=config['the_box']['client_id'],
            client_secret=config['the_box']['client_secret']
        )
        self.redirect_url = config['redirect']['url']
        self.root_directory = config['the_box']['root_directory']

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
        r = redis.StrictRedis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
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
        """
        list files in a remote folder
        :param folder_id:
        :param limits:
        :return:
        """
        items = self.client.folder(folder_id=folder_id).get_items(limit=limits, offset=0)
        for file in items:
            is_folder = 'folder' if self.is_folder(file) else 'file'
            print(file.name, colored('(id: '+file.id+')', 'blue'), colored(is_folder, 'yellow'))
        return items

    def download(self, file, destination):
        """
        download a file to local
        :param file:
        :param destination:
        :return:
        """
        if not isinstance(file, File):
            file = self.client.file(file)
        with open(os.path.join(destination, file.get().name), 'wb') as f:
            file.download_to(f)
        print(file.get().name, 'downloaded from the box to', destination)
        return True

    def upload(self, file, folder_id):
        self.client.folder(folder_id=folder_id).upload(file_path=file)
        print(os.path.basename(file), 'uploaded to the box at', self.client.folder(folder_id=folder_id).get().name)
        return True

    def is_folder(self, file):
        """
        check if file is a folder
        :param file:
        :return:
        """
        return isinstance(file, Folder)


if __name__ == '__main__':
    box = Box()
    box.authorization()
    box_items = box.list(box.root_directory)
    upload_folder = None
    for each_item in box_items:
        print(each_item)
        print(isinstance(each_item, Folder))
        if each_item.name == 'test':
            upload_folder = each_item
            test_items = box.list(each_item.id)
            for each_file in test_items:
                print(each_file)
                print(isinstance(each_file, Folder))
                box.download(each_file.id, '/home/zhihua/work/sunyi/temp/')
    box.upload(folder_id=upload_folder.id, file='/home/zhihua/work/sunyi/temp/test.pdf')


