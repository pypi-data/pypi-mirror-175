from datetime import date

__version__ = "0.6.2"
__author__ = 'BentouDev'

def get_author_desc():
     return f'{__author__} @ 2021-{date.today().year}'
