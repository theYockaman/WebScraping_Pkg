# Import Modules
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import Union
import requests
from utils.functions import checkType


__all__ = [
    "click"
    , "goToWebsite"
    , "input"
    , "element"
    , "elements"
    , "execute"
    , "downloadOnlineMedia"
]

# Basic Selenium Scaping Functions

def click(xpath:str, item:Union[WebElement, Chrome]) -> None:
    """Selenium Click on Page

    :param xpath: XPATH to Click
    :type xpath: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    """
    
    # Check Type
    checkType([xpath,item],[str,[WebElement, Chrome]])
    
    # Click XPATH
    element(xpath, item).click()
    sleep(5)

def goToWebsite(website:str, item:Union[WebElement, Chrome]) -> None:
    """Go to a Website Selenium

    :param website: Website to go to
    :type website: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    """
    
    # Check Type
    checkType([website,item],[str,[WebElement, Chrome]])
    
    # Go to the Website
    item.get(website)
    sleep(5)

def input(input:str, xpath:str, item:Union[WebElement, Chrome]) -> None:
    """Input into XPATH

    :param input: Input Value
    :type input: str
    :param xpath: XPATH of Input Element
    :type xpath: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    """
    
    # Check Type
    checkType([input,xpath,item],[str, str,[WebElement, Chrome]])
    
    # Send an Input
    element(xpath, item).send_keys(input)
    sleep(5)
        
def element(xpath:str, item:Union[WebElement, Chrome]) -> WebElement:
    """Selenium XPATH Element

    :param xpath: XPATH of Element
    :type xpath: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    :return: Selenium XPATH Element
    :rtype: WebElement
    """
    # Check Type
    checkType([xpath,item],[str,[WebElement, Chrome]])
    
    # Selenium Element
    return item.find_element(By.XPATH,xpath)

def elements(xpath:str, item:Union[WebElement, Chrome]) -> list[WebElement]:
    """Selenium XPATH Elements

    :param xpath: XPATH of Elements
    :type xpath: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    :return: Selenium XPATH Elements
    :rtype: WebElement
    """
    # Check Type
    checkType([xpath,item],[str,[WebElement, Chrome]])
    
    # Get the Elements
    return item.find_elements(By.XPATH,xpath)
    
def execute(javaScript:str, item:Union[WebElement, Chrome],*args) -> None:
    """Execute JavaScript Code on Element

    :param javaScript: JavaScript Code to Run on Item or Page
    :type javaScript: str
    :param item: WebDriver and Element of the Website
    :type item: Union[WebElement,webdriver.Chrome]
    """
    # Check Type
    checkType([javaScript,item],[str,[WebElement, Chrome]])
    
    # Execute Script
    item.execute_script(javaScript,args)
    sleep(5)

def downloadOnlineMedia(mediaUrl:str, directoryMedia:str) -> None:
    """Download Media from URL

    :param mediaUrl: URL of Photo or Video
    :type mediaUrl: str
    :param directoryMedia: Stored Download Media with correct Extensions
    :type directoryMedia: str
    """
    # Check Types
    checkType([mediaUrl,directoryMedia],[str,str])
    
    # Writes Photos and Videos
    img_data = requests.get(mediaUrl).content
    
    with open(directoryMedia, mode="wb") as f:
        f.write(img_data)
        
        
# All Attributes of a Element
      
    # attrs = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', likeBtn)
            # print(attrs)   