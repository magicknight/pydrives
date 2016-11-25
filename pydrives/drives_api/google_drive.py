#!/usr/bin/env python3
import os
from pprint import pprint
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GDrive:
    def __init__(self):
        """
        Initialization
        """
        self.drive = None
        self.auth = None

    def authorization(self):
        """
        google authorization
        :return:
        """
        self.auth = GoogleAuth()
        self.auth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.auth)

    def list(self, folder):
        """
        list files under a folder
        :param folder: folder id
        :return: folder list
        """
        query = {
            'q': "'" + folder + "'" + ' in parents and trashed=false'
        }
        pprint(query)
        file_list = self.drive.ListFile(query).GetList()
        return file_list

    def upload(self, local_file, remote_folder):
        """
        upload a file to a drive folder
        :param local_file: path to local file
        :param remote_folder: remote folder id
        :return: file's metadata
        """
        metadata = {
            'title': os.path.basename(local_file),
            'parents': [{'id': remote_folder}]
        }
        file = self.drive.CreateFile(metadata=metadata)
        file.SetContentFile(local_file)
        file.Upload()
        return file.metadata

    def download(self, remote_file, local_folder):
        """
        download google file
        :param remote_file: remote id
        :param local_folder: local folder
        :return:
        """
        metadata = {
            'id': remote_file
        }
        file = self.drive.CreateFile(metadata=metadata)
        file.GetContentFile(os.path.join(local_folder, file['title']))


if __name__ == '__main__':
    google_drive = GDrive()
    google_drive.authorization()
    files = google_drive.list(folder='root')
    # pprint(files)
    for each_file in files:
        print(each_file['title'], each_file['id'], each_file['mimeType'])
        if 'folder' in each_file['mimeType']:
            print('it is a folder ')
            second_files = google_drive.list(folder=each_file['id'])
            pprint(second_files)
            for each_second_file in second_files:
                print(each_second_file['title'], each_file['id'], each_file['mimeType'])
            print('uploading a file to folder', each_file['title'])
            uploaded_file = google_drive.upload('/home/zhihua/temp/57fb1d5e9cc87a7f7f2119b9',
                                                each_file['id'])
            google_drive.download(uploaded_file['id'], '/home/zhihua/temp')






