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

All the settings can be modified in config.py

##Usage
```python
from pydrives.drives_api.google_drive import  GDrive

google_drive = GDrive()
google_drive.authorization()
files = google_drive.list(folder='root')
```
