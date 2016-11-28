config = {
    'modules': ['google_drive', 'drop_box', 'the_box'],
    'actions': ['list', 'upload', 'download'],
    'redis': {
        'host': '104.154.43.233',
        'port': 6379,
        'db': 0
    },
    'redirect': {
        'url': 'http://localhost:8080',
        'host': 'localhost',
        'port': 8080
    },

    'the_box': {
        'client_id': '77bubh1k3d3f0e06606o6mcuvl1w6brg',
        'client_secret': 'c77Xma34aNdvBMkURvElDGS4RNO3goZh',
        'root_directory': '0'
    },

    'drop_box': {
        'APP_KEY': 'v402gpdosumtj0o',
        'APP_SECRET': 't2042a18uef5lqy',
        'root_directory': ''
    },

    'google_drive': {
        'root_directory': 'root'
    }

}


