from configparser import ConfigParser
from service.utils import resource_path

# def resource_path(relative_path):
#     return os.path.join(os.path.abspath("."), relative_path)

file_path = resource_path('config/env.ini')
config = ConfigParser()
config.read(file_path, encoding='utf-8') 

def get_config(key)-> any:
    if not '/' in key: return ""
    
    section, key= key.split('/')
    if not section in config: return None
    if not key in config[section]: return None
    
    data = config[section][key]    
    return eval(data)

if __name__=='__main__':
    a = get_config('FILE/working_file')
    print(a)
    
    b = get_config('FILE/doc1')
    print(b[0])
    
    c = get_config('LAYTENCY_TIME/time1')
    print(c)
    
    d= get_config('FILE/result_file')
    print(d)