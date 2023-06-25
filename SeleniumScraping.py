# Import Modules
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import Union
import requests

# Basic Selenium Scaping Functions

def click(xpath:str, item:Union[WebElement, Chrome]) -> None:
    """Selenium Click on Page

    :param xpath: XPATH to Click
    :type xpath: str
    :param item: Page or Element based from XPATH
    :type item: Union[WebElement,webdriver.Chrome]
    """
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
    
    return item.find_elements(By.XPATH,xpath)
    
def execute(javaScript:str, item:Union[WebElement, Chrome],*args) -> None:
    """Execute JavaScript Code on Element

    :param javaScript: JavaScript Code to Run on Item or Page
    :type javaScript: str
    :param item: _description_
    :type item: Union[WebElement,webdriver.Chrome]
    """
    item.execute_script(javaScript,args)
    sleep(5)

def downloadOnlineMedia(mediaUrl:str, directoryMedia:str) -> None:
    """

    :param mediaUrl: URL of Media stored Online
    :type mediaUrl: str
    :param directoryMedia: Directory to Store Media
    :type directoryMedia: str
    """
    img_data = requests.get(mediaUrl).content
    with open(directoryMedia, mode="wb") as f:
        f.write(img_data)
        
        