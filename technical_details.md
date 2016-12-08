# Structure
## drives_api
drives_api is an API wrapper for three different cloud drives: [Google Drive](https://www.google.com/drive/), 
[DropBox](https://www.dropbox.com/), and [The Box](https://www.box.com/). 

Actually each of these cloud drives has its own python API and SDK. However since these APIs are developed by different
 companies and (obviously) they have different coding style && name of methods, etc... So it is better to wrap them into
 a universal API wrapper, to simplify the work process with other teams(for example, the GUI and database team).

### methods
Each of the cloud drives has three basic methods: **list**, **upload**, **download**.
#### list

list a 

google drive:
```python
def list(self, folder):
    """
    list files under a folder
    :param folder: folder id
    :return: folder list
    """
```
dropbox:
```python
def list(self, folder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
```

the box:
```python
def list(self, folder_id, limits=100):
    """
    list files in a remote folder
    :param folder_id:
    :param limits:
    :return: a list of files metadata
    """
```

