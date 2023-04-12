from typing import Union
import time
import requests
from bs4 import BeautifulSoup
from googlesearch import search


class LinkGrabber:
    '''A class that grabs the first link from a Google search result'''
    
    def __init__(self, query: str) -> None:
        ''' 
            Initializes the class with the query.
            
            Args:
                query (str): The query to search for on Google.
            Returns:
                None
        
        '''
        self.query = query + " fandom wikia"
        self.links = []
    
    def get_wikia_links(self) -> Union[None,str]:
        '''
            Returns the first wikia link from the Google search result.
            
            Args:
                None
            Returns:
                Union[None,str]: The first wikia link from the Google search result.
        '''
        # search for the query
        for url in search(self.query, num=10, stop=10, pause=10):
            # check if the url is a wikia link
            if "fandom" in url and "Main_Page" not in url:
                self.links.append(url)
            
            # add timeout to prevent google from blocking the request
            time.sleep(10)
        # return the first link
        if len(self.links) > 0:
            return self.links[0]
        else:
            return None





        