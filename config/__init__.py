from configparser import ConfigParser
from service.utils import resource_path

config = ConfigParser()
config.read(resource_path('config/env.ini'), encoding='utf-8') 

def get_config(key)-> any:
    if not '/' in key: return ""
    
    section, key= key.split('/')
    if not section in config: return None
    if not key in config[section]: return None
    
    data = config[section][key]    
    return eval(data)