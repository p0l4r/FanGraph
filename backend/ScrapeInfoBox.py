from typing import Union
import requests
from bs4 import BeautifulSoup
import re

from LinkGrabber import LinkGrabber

class ScrapeInfoBox:
    '''A class that scrapes the infobox from a wikia page'''
    def __init__(self, query: str) -> None:
        '''
            Initializes the class with the query and the wikia link.
            
            Args:
                query (str): The query to search for on Google.
            
            Returns:
                None
        
        '''
        self.query = query
        self.url = LinkGrabber(self.query).get_wikia_links()
        self.infobox = {}
    
    def scrape_relations(self) -> Union[None,dict]:
        '''
            Scrapes the relations section of the infobox from the wikia page, and recursively scrapes 
            the relations section of the infobox from the links in the relations section.
            
            Args:
                None
            
            Returns:
                Union[None,dict]: A dictionary containing the scraped relations data.
        '''
        # Send a GET request to the fandom wikia link
        response = requests.get(self.url)

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the infobox and get the character relations section
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            print("Infobox not found on the page")
            return None

        relations_section = infobox.find("th", text=re.compile(".*Relations.*", re.IGNORECASE))
        if not relations_section:
            print("Relations section not found in the infobox")
            return None

        # Find all links in the relations section and scrape their infoboxes recursively
        relations_links = [link.get("href") for link in relations_section.find_all("a")]
        relations_data = {}
        for link in relations_links:
            if "fandom.com" in link:
                relations_data[link] = self.scrape_relations(link)

        # Extract the character name from the infobox and return the data
        character_name = soup.find("h1", {"class": "page-header__title"}).text.strip()
        return {character_name: relations_data}