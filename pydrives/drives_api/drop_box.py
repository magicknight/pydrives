#!/usr/bin/env python3
import dropbox
from dropbox.files import FolderMetadata, FileMetadata
from dropbox import DropboxOAuth2Flow
from termcolor import colored
from pydrives.config import config

import redis
import webbrowser
import os
from time import sleep
from urllib.parse import urlparse, parse_qs


class DropBox:
    def __init__(self):
        self.APP_KEY = config['drop_box']['APP_KEY']
        self.APP_SECRET = config['drop_box']['APP_SECRET']
        self.csrf_token_session_key = 'pyDrives_DropBox'
        self.state = ''
        self.access_parameters = {}
        self.access_token = ''
        self.dbx = None
        self.dfx = None

    def authorization(self):
        """
        oauth2
        :return:
        """
        auth_flow = DropboxOAuth2Flow(self.APP_KEY, self.APP_SECRET, redirect_uri=config['redirect']['url'], session={},
                                      csrf_token_session_key=self.csrf_token_session_key)
        authorize_url = auth_flow.start()
        self.state = parse_qs(urlparse(authorize_url).query)['state'][0]
        webbrowser.open(authorize_url)
        if not self.get_auth_tocken():
            print('Authorization failed')
            return False
        self.access_token = auth_flow.finish(self.access_parameters)
        self.dbx = dropbox.Dropbox(self.access_token.access_token)
        self.dfx = dropbox.files
        return True

    def get_auth_tocken(self):
        """
        get auth code for oauth
        :return:
        """
        r = redis.StrictRedis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
        for i in range(60):
            auth_code = r.get(self.state)
            if not auth_code:
                sleep(1)
            else:
                # print(auth_code)
                self.access_parameters = {'state': self.state, 'code': auth_code}
                return True
        return False

    def list(self, folder):
        """List a folder.

        Return a dict mapping unicode filenames to
        FileMetadata|FolderMetadata entries.
        """
        path = '/%s' % folder
        while '//' in path:
            path = path.replace('//', '/')
        path = path.rstrip('/')
        res = self.dbx.files_list_folder(path)
        for file in res.entries:
            is_folder = 'folder' if self.is_folder(file) else 'file'
            print(file.name, colored('(id: '+file.id+')', 'blue'), colored(is_folder, 'yellow'))
        return res

    def upload(self, local_file, remote_folder):
        """
        upload a file to remote folder
        :param local_file:
        :param remote_folder:
        :return:
        """
        with open(local_file, 'rb') as f:
            data = f.read()
            self.dbx.files_upload(data, '/'.join([remote_folder, os.path.basename(local_file)]), autorename=True)

    def download(self, remote_file, local_folder):
        """
        download a file to local
        :param remote_file:
        :param local_folder:
        :return:
        """
        self.dbx.files_download_to_file(os.path.join(local_folder, remote_file.name), remote_file)

    def upload_folder(self, local_folder, remote_folder):
        """
        upload files from local_folder to dropbox_folder
        :param local_folder:
        :param remote_folder:
        :return:
        """
        result = os.path.isdir(local_folder)
        if not result:
            print('local path is not a folder')
            return False
        local_files = os.listdir(local_folder)
        print('uploading', local_folder, 'to', remote_folder)
        print(local_files)
        for each_file in local_files:
            full_path = os.path.join(local_folder, each_file)
            if os.path.isdir(full_path):
                folder_create = '/'.join([remote_folder, each_file])
                print('creating path', folder_create, 'on dropbox')
                self.dfx.CreateFolderArg(folder_create, autorename=False)
                self.upload_folder(folder_create, full_path)
            else:
                dropbox_file_path = '/'.join([remote_folder, each_file])
                print('uploading file', each_file, 'to', dropbox_file_path)
                if each_file.startswith('.'):
                    print('Skipping dot file:', each_file)
                elif each_file.startswith('@') or each_file.endswith('~'):
                    print('Skipping temporary file:', each_file)
                else:
                    with open(full_path, 'rb') as f:
                        data = f.read()
                        self.dbx.files_upload(data, dropbox_file_path, autorename=True)

    def download_folder(self, remote_folder, local_folder):
        """
        download files from dropbox_folder to local folder
        :param remote_folder:
        :param local_folder:
        :return:
        """
        result = self.check_folder(remote_folder)
        if result:
            # the path of a folder has been given
            listing_downloads = self.list(remote_folder)
            for file in listing_downloads.entries:
                if not self.check_folder('/'.join([remote_folder, file.name])):
                    path = str(remote_folder)
                    filename = str(file.name)
                    download_path = os.path.join(local_folder, filename)
                    remote_path = path + '/' + filename
                    self.dbx.files_download_to_file(download_path, remote_path)
                else:
                    next_local_dir = os.path.join(local_folder, file.name)
                    next_remote_dir = '/'.join([remote_folder, file.name])
                    if not os.path.exists(next_local_dir):
                        os.mkdir(next_local_dir)
                    self.download_folder(next_remote_dir, next_local_dir)

        else:
            # the path of a file has been given to be downloaded
            self.dbx.files_download_to_file(local_folder, remote_folder)

    def check_folder(self, folder):
        """
        check the path given is a file or a folder.
        :param folder:
        :return:
        """
        try:
            folder_metadata = self.dbx.files_get_metadata(folder)
        except Exception as e:
            print(e)
            return False
        is_folder = isinstance(folder_metadata, FolderMetadata)
        if is_folder:
            return True
        else:
            return False

    def is_folder(self, file):
        """
        check if the file is a folder
        :param file:
        :return:
        """
        return isinstance(file, FolderMetadata)


if __name__ == '__main__':
    drop_box = DropBox()
    drop_box.authorization()
    print(drop_box.dbx.users_get_current_account())
    for entry in drop_box.dbx.files_list_folder('').entries:
        print(entry.name)
        print('is folder?', drop_box.check_folder(entry.id))
        if entry.name == 'test':
            drop_box.upload_folder('/home/zhihua/temp', '/'+entry.name)




