# PyDrives, A lightweight cloud drive interface written in Python

##Installation
```bash
pip install git+https://github.com/magicknight/pydrives
```

## Requirement 
#### redis
Ubuntu: 
```bash
sudo apt install redis
```

##Settings
All the settings can be modified in config.py

##Usage
### Use it as a universal cloud drive api
```python
from pydrives.drives_api.google_drive import  GDrive

google_drive = GDrive()
google_drive.authorization()
files = google_drive.list(folder='root')
```
### As a command line tool
```bash
./main.py ['google_drive', 'drop_box', 'the_box'] ['list', 'upload', 'download'] <source> <destination>  
```
