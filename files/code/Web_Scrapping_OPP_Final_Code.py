print('Author: Sanele Zondo')
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

class Scraper_Data:

    def __init__(self,url,no_pages):
        self.url=url
        self.no_pages=no_pages
        self.ListOfPages = []
        self.names =[]
        self.prices = []
        self.descriptions = []
        self.ratings = []
        self.reviews = []

    def fetch_page(self):
        for page in range(1,self.no_pages+1,1):
            CurrentPageUrl = f'{self.url}{page}'
            try:
                response = requests.get(CurrentPageUrl)
                if response.status_code == 200:
                    self.ListOfPages.append(response.text)
                    print(f'Successfully Fetched the URL For Page: {CurrentPageUrl}')
                else:
                    print(f'Error Fetching The Page. Status Code Details: {response.status_code}')
            except Exception as error:
                print(f'Error fetching the page. Details: {error}')
            """Sleeper For making the website not detect that it is code"""
            sleep(1)
       
    def parse_data(self,html_contents):
        if not html_contents:
            return None
            print(f'No HTML Content Available For Parsing')
        else:
            for html_content in html_contents:
                try:
                    soup=BeautifulSoup(html_content,'html.parser')
                    laptops = soup.find_all('div',class_='col-md-4 col-xl-4 col-lg-4')

                    for laptop in laptops:
                        name=laptop.find('div',class_='caption').h4.find_next_siblings()[0].text
                        price=laptop.find('div',class_='caption').h4.text
                        description=laptop.find('div',class_='caption').p.text
                        review=laptop.find('div',class_='ratings').p.text.replace(' reviews','')
                        rating=laptop.find('div',class_='ratings').p.find_next_siblings()[0].get("data-rating")
                        
                        if name and price and description and review and rating:
                            self.names.append(name)
                            self.prices.append(price)
                            self.descriptions.append(description)
                            self.ratings.append(rating)
                            self.reviews.append(review)
                        
                        else:
                            print(f'Error adding data: Missing required information.')

                except Exception as error:
                    print(f'Error occurred while parsing the HTML content. Details: {error}')

    def scrape_data(self):
        self.fetch_page()
        self.parse_data(self.ListOfPages)
        data={
            'Names':self.names
            ,'Prices':self.prices
            ,'Descriptions':self.descriptions
            ,'Ratings':self.ratings
            ,'Reviews':self.reviews
        }
        print(f'Data has been scrapped from the website')
        return data
    def transform_data(self):
        data=self.scrape_data()
        if data is not None:
            try:
                data_df=pd.DataFrame(data)
                print('Data has been transformed into a DataFrame.')
                return data_df

            except Exception as error:
                print(f'Error convertting data into DataFrame. Details:{error}')
                return None
        else:
            print('Error: No data provided.')
            return None
        
    def save_to_csv(self,save_directory):
        data = self.transform_data()
        if not data.empty:
            try:
                saved_data=data.to_csv(f'{save_directory}.csv',index=False)
                print(f'Data has been saved to: {save_directory}.csv')
            except Exception as error:
                print(f'Error saving data into csv. Details:{error}')
        else:
            print('Error: No data provided.')

    """Ensuring that the Number of Pages is Always Correct."""
    @property
    def no_pages(self):
        return self._no_pages
    @no_pages.setter
    def no_pages(self,value):
        if isinstance(value, int) and value>=0:
            self._no_pages = value
            print(f'Updated: The number of pages to be scraped is {value}.')
        else:
            print(f'Invalid data type, or the value is less than 0.')

if __name__=='__main__':
    """Parameters"""
    url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page='
    number_of_pages = 21
    save_directory='C:/Users/SaneleZondo/Documents/Becoming A Data Scientist/Data_ Project_1_Original/data'

    scraper=Scraper_Data(url,number_of_pages)
    scraper.save_to_csv(save_directory)



