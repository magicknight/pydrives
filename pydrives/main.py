#!/usr/bin/env python3
import sys
import argparse


def main():
    """Main program.

    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    parser = argparse.ArgumentParser(prog="dropboxfs", description='Cloud storage process')
    parser.add_argument('action', nargs='?', default='list',
                        help="list or download or upload ")
    parser.add_argument('folder', nargs='?', default='/shabi',
                        help="Folder name in your Dropbox")
    parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                        help='Local directory to upload')
    parser.add_argument('--token', default=access_token,
                        help='Access token '
                             '(see https://www.dropbox.com/developers/apps)')

    args = parser.parse_args()


    if not args.token:
        print('--token is mandatory')
        sys.exit(3)

    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(2)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a foldder on your filesystem')
        sys.exit(2)


    #list files.
    if args.action.lower() =="list":
        res = list_folder(dbx, folder)
    # download files
    elif args.action.lower() == "download":
        download_files_folders(folder, rootdir)
    # upload files
    else:
        upload_files_folders(folder, rootdir)
