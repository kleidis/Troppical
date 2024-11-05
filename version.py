from datetime import datetime

def get_version():
    return datetime.now().strftime('%y.%m%d')

version = get_version()