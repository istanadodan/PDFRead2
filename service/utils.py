import os

def resource_path(relative_path):
    return os.path.join(os.path.abspath("."), relative_path)
