# PyDrives, A lightweight cloud drive interface written in Python

##Installation
pip install git+https://github.com/magicknight/pydrives


##Usage
```python
from pydrives.drives_api.google_drive import  GDrive

google_drive = GDrive()
google_drive.authorization()
files = google_drive.list(folder='root')

