
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import requests
from time import sleep
from utils.file import JSON, Folder
from datetime import datetime
import os

from webscraping.seleniumScraping import *




class instabot:
    
    # Selenium Options Variable
    options = Options()

    def __init__(self, username:str = None, password:str = None, headless:bool = False):
        """Instagram Bot 

        :param username: Username of Instagram Account, defaults to None
        :type username: str, optional
        :param password: Password of Instagram Account, defaults to None
        :type password: str, optional
        :param headless: Display Page `True`:displays page `False`:hides page, defaults to False
        :type headless: bool, optional
        """
    
        # Create the Chrome Driver for Selenium
        self.driver = None
        self.username = None

        # Username and Password is given, so login
        if username is not None and password is not None: self.login(username,password)
        
        # Headless Option
        if headless: self.options.add_argument("--headless")

    def _checkDriver(self) -> bool:
        """Check to see if Driver for Selenium Exists

        :raises ValueError: No Driver Found
        :return: `True`: Driver Exists `False`: Driver Does Not Exist
        :rtype: bool
        """
        # Check to see if the Bot is Logged In
        if self.driver is None:
            raise ValueError("No Driver Found")
        
        return True

    def _goToHomePage(self):
        """Go to Instagram Home Page
        """
        
        # Check Driver
        self._checkDriver()
        
        # Return to Instagram Home Page
        goToWebsite("https://www.instagram.com",self.driver)
        sleep(5)
        
        try:
            # Not Now Btn
            click('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]',self.driver)
            
        except:
            pass

    def _goToAccountPage(self, username:str):
        """Goes to Instagram Account Page

        :param username: Username of Account
        :type username: str
        """

        # Checks to make sure that Logged In
        self._checkDriver()

        # Go to Account Page
        self.driver.get(f'https://www.instagram.com/{username}/')
        sleep(5)

    def _goToFollowing(self, username:str):
        """Go to Followers of an Instagram Account
        """
        # Checks to make sure that Logged In
        self._checkDriver()

        # Go to Following in the Account
        self.driver.get(f'https://www.instagram.com/{username}/following/')
        sleep(5)

    def _goToHashtag(self, hashtag:str):
        """Instagram Search Hashtag Page

        :param hashtag: Name of hashtag with no (#)
        :type hashtag: str
        """
        # Checks to see if Logged IN
        self._checkDriver()

        # Goes to Hashtag
        self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        sleep(5)

    def login(self, username:str, password:str):
        """Login to Instagram Account

        :param username: Username of Instagram Account
        :type username: str
        :param password: Password of Instagram Account
        :type password: str
        :raises TypeError: Driver already Exists
        """

        # Driver Must be Empty or equal to None
        if self.driver is not None: raise TypeError("Driver already Exists")
        
        # Creates Driver
        self.driver = webdriver.Chrome(options = self.options)

        # Opens Instagram
        self._goToHomePage()

        # Enter the Username and Password
        elementInput(username,'//*[@name="username"]',self.driver)
        elementInput(password, '//*[@name="password"]',self.driver)

        # Find and click Login Button
        click('//button[@type="submit"]',self.driver)

        # NotNow To not Save Login info
        try:
            click("//button[contains(text(), 'Not Now')]",self.driver)
        except:
            pass

        # Turn on Notifications Not Now
        try:
            click("//button[contains(text(), 'Not Now')]",self.driver)
        except:
            pass

        # Sets Username
        self.username = username

    def logout(self):
        """Logout of Instagram Account with closing the driver
        """

        # Makes Sure that we are Logged In to Logout
        self._checkDriver()
        
        # Close Driver
        self.driver.quit()

        # Reset Username and Driver
        self.username = None
        self.driver = None

    def post(self, postFile:str, caption:str):
        """Post a video or image to Instagram Account

        :param postFile: Post File or the Directory of the Media
        :type postFile: str
        :param caption: Caption of the Post
        :type caption: str
        """

        # Check to see if the Instabot is Logged into an Account
        self._checkDriver()

        # Click Post Button
        postBtn = self.driver.find_element(By.XPATH,"//div[7]/div/div/a")
        postBtn.click()
        sleep(5)

        # Input the Post Media
        mediaInput = self.driver.find_element(By.XPATH,"//form/input[@accept = 'image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']")
        mediaInput.send_keys(postFile)
        sleep(5)

        # Only shows up on Video posts
        try:
            okBtn = self.driver.find_element(By.XPATH,"//button[contains(text(), 'OK')]")
            okBtn.click()
            sleep(5)
        except:
            pass

        # Expand Post
        try:
            expandBtn = self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button")
            expandBtn.click()
            sleep(3)

            orginalBtn = self.driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]")
            orginalBtn.click()
            sleep(5)

        except:
            pass

        # Leaves the Cropping of the Post
        try:
            nextBtn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        except:
            nextBtn = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Next')]")
        nextBtn.click()
        sleep(5)

        # Leave Edit with Filters
        nextBtn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        nextBtn.click()
        sleep(5)

        # Adds a Caption to the Post
        ca = self.driver.find_element(By.XPATH,'//*[@aria-label="Write a caption..."]')
        ca.send_keys(caption)
        sleep(5)

        # Button Clicked to Share Post
        shareBtn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Share')]")
        shareBtn.click()
        sleep(5)

        self._goToHomePage()

    def topHashtagPosts(self, hashtag:str) -> list:
        """Top Hashtag Posts Links"""

        # Goes to Hashtag Page
        self._goToHashtag(hashtag)

        # Retrieve Top Hashtag Posts
        while True:
            try:
                topPostsArea = self.driver.find_element(By.XPATH,"//article[]")
                break
            except:
                self._goToHashtag(hashtag)
                sleep(20)

        # Retrieve the Top Posts
        postLinks = [x.get_attribute('href') for x in topPostsArea.find_elements(By.TAG_NAME,'a')]
        sleep(5)

        self._goToHomePage()

        return postLinks

    # def hashtagPosts(self, hashtag:str, amount:int = 10):

    #     # Go to Hashtag Page
    #     self._goToHashTag(hashtag)

    #     # Retrieve Top Hashtag Posts
    #     postsArea = self.driver.find_element(By.XPATH,'//article/div[2]')

    #     postLinks = [x.get_attribute('href') for x in postsArea.find_elements(By.TAG_NAME,'a')][:amount]

    #     x = 1
    #     # Retrieves the Post Links
    #     while len(postLinks) < amount:
    #         self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight*{x});")
    #         sleep(5)

    #         # Retrieve Top Hashtag Posts
    #         postsArea = self.driver.find_element(By.XPATH,'//article/div[2]')

    #         postLinks = [x.get_attribute('href') for x in postsArea.find_elements(By.TAG_NAME,'a')][:amount]
    #         x+=1

    #     # Return to Instagram Home Page
    #     self._goToHomePage()
    #     return postLinks

    def likePost(self, postLink:str):
        """Like Post in Instagram

        :param postLink: Post Link
        :type postLink: str
        """
        # Checks to see if Logged In
        self._checkDriver()
        
        # Go to Post
        self.driver.get(postLink)
        sleep(5)
        

        # Clicks the Like Btn
        likeBtn = self.driver.find_element(By.XPATH,"//div[@class='x78zum5']//div[@role='button']//*[@aria-label='Like']")
        
        # attrs = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', likeBtn)
        # print(attrs)
        
        likeBtn.click()
        sleep(2)

        # Go to Instagram Home Page
        self._goToHomePage()

    def follow(self, postLink:str):
        """Follow Account based on Post Link

        :param postLink: Post Link
        :type postLink: str
        """
        # Checks to see if Logged In
        self._checkDriver()
        
        # Goes to Post
        self.driver.get(postLink)
        sleep(5)

        # Username
        username = self.driver.find_element(By.XPATH,'//div[@class="xt0psk2"]').text
        
        # Not Personal Account
        if username != self.username:
            
            # Go to Account Page
            self._goToAccountPage(username)

            # Find User Follow Btn and Clicks it
            followBtn = self.driver.find_element(By.XPATH,"//button[//*[contains(text(),'Follow')]]")
            followBtn.click()
            sleep(3)

            # Goes back to Instagram Home Page
            self._goToHomePage()
    
    def comment(self, comment:str):
        pass

    def downloadPost(self, postLink:str) -> dict:
        """Download Instagram Post

        :param postLink: Post Link
        :type postLink: str
        :return: Details Extracted from Post
        :rtype: dict
        """

        # Checks to see if Logged In
        self._checkDriver()
        
        # Creates Posts Folder
        folder = Folder("Posts")

        # Go to Post
        self.driver.get(postLink)
        sleep(5)

        # Collect Username
        username = self.driver.find_element(By.XPATH,'//span[@class="xt0psk2"]').text
        sleep(5)

        # Amount of Likes
        try:
            likes = self.driver.find_element(By.XPATH,"//span[contains(text(),' likes')]/span").text
        except:
            try:
                likes = self.driver.find_element(By.XPATH,"//span[contains(text(),' others')]/span").text
            except:
                likes = "0"

        postFile = username +"_"+ str(datetime.now().date()) +"_post"

        # Gets and Downloads the Media
        try:
            # Video
            media = self.driver.find_element(By.TAG_NAME,'video').get_attribute('src')
            postFile += ".mp4"

        except:
            # Image
            media = self.driver.find_element(By.XPATH,"//*/div/div/div/img").get_attribute('src')
            postFile += ".jpg"

        
        # Downloads Post
        img_data = requests.get(media).content
        with open(f"{folder.directory}/{postFile}", mode="wb") as f:
            f.write(img_data)

        sleep(5)

        # Collect Caption
        caption = self.driver.find_element(By.XPATH,"//span[@class = 'x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']").text
        
        sleep(5)

        # Creates JSON File for Post
        detailsFile = JSON(f"{folder.directory}/{username}_{str(datetime.now().date())}_details.json")
        details = detailsFile.read()
        details.update({"postDirectory":f"{folder.directory}/{postFile}"})
        details.update({"orgMedia":media})
        details.update({"postLink":postLink})
        details.update({"username":username})
        details.update({"caption":caption})
        details.update({"likes":likes})
        detailsFile.write(details)

        self._goToHomePage()
        return details

    def deleteOldPosts(self, numOldestPost:int):
        """Delete Old Posts

        :param numOldestPost: Number of Old Posts to Delete
        :type numOldestPost: int
        """
        # Go to Account Page
        self._goToAccountPage()

        prevAmount = 0

        postLinks = [x.get_attribute('href') for x in self.driver.find_element(By.TAG_NAME,"article").find_elements(By.TAG_NAME,"a")][::-1]
        sleep(3)

        
        while len(postLinks) != prevAmount :
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            prevAmount = len(postLinks)
            postLinks = sorted(list(set([x.get_attribute('href') for x in self.driver.find_element(By.TAG_NAME,"article").find_elements(By.TAG_NAME,"a")] + postLinks)))
            sleep(3)

    
        # Goes through and Delete Post
        for x in range(numOldestPost):
            link = postLinks[x]
            self.driver.get(link)
            sleep(5)

            moreBtn = self.driver.find_element(By.CLASS_NAME,'_aasm')
            moreBtn.click()
            sleep(3)

            deleteBtn = self.driver.find_element(By.XPATH,"//button[contains(text(), 'Delete')]")
            deleteBtn.click()
            sleep(3)

            actualDeleteBtn = self.driver.find_element(By.XPATH,"//button[contains(text(), 'Delete')]")
            actualDeleteBtn.click()
            sleep(5)

        self._goToHomePage()

    def unfollow(self, numAccounts:int):
        """Unfollow Amount of Accounts

        :param numAccounts: Number of Accounts
        :type numAccounts: int
        """

        # Go to Account Page
        self._goToFollowing(self.username)
        
        # Remove Buttons
        removeBtns = self.driver.find_elements(By.XPATH,"//button[contains(text(), 'Following')]")

        # Container which holds the Following
        container = self.driver.find_element(By.XPATH,"//div[@class = '_aano']")

        num = 1
        while len(removeBtns) < numAccounts:

            # Scrolls Down
            self.driver.execute_script(f"arguments[0].scrollTo(0, document.body.scrollHeight*{num});",container)
            sleep(5)

            # Finds Remove Buttons
            removeBtns = self.driver.find_elements(By.XPATH,"//button/div/div[contains(text(), 'Following')]")[:numAccounts]
            num+=1

        # Stops at Each Account and Unfollows it
        for x,removeBtn in enumerate(removeBtns):
            print(f"Account {x+1}")
            
            # Hits the Remove Button
            removeBtn.click()
            sleep(5)

            # Hits the Remove Button to Double check that we want to unfoll
            unfollowBtn = self.driver.find_element(By.XPATH,"//button[contains(text(),'Unfollow')]")
            unfollowBtn.click()
            sleep(5)

        self._goToHomePage()
  
    def _createCaption(self, mediaLocation:str):
        """Create AI Caption

        :param mediaLocation: _description_
        :type mediaLocation: str
        :param postComment: _description_
        :type postComment: str
        """
        # Go to https://ahrefs.com/writing-tools/instagram-caption-generator to generate Captions for Insta
        # https://www.copy.ai/tools/instagram-caption-generator 
        self._checkDriver()
        
        # Return to Instagram Home Page
        self.driver.get("https://www.copy.ai/tools/instagram-caption-generator")
        sleep(5)
        
        # '//div/input[@accept = 'image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']'
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight*.03);")
        sleep(10)
        
        mediaInput = self.driver.find_element(By.XPATH,'//*[@placeholder="The URL of the image to analyze"]')
    
        mediaInput.send_keys(mediaLocation)
        sleep(5)
        
        povInput = self.driver.find_element(By.ID,'pov')
        povInput.send_keys('first person')
        sleep(5)
        
        toneInput = self.driver.find_element(By.ID,'tone')
        toneInput.send_keys('friendly')
        sleep(5)
        
        submitBtn = self.driver.find_element(By.XPATH,"//button[@aria-label = 'Submit']")
        submitBtn.click()
        sleep(5)



            

            





b = instabot('the.fishing.frenzy','nate51025')

posts = b.topHashtagPosts('fishing')
for x, post in enumerate(posts):
    b.likePost(post)
    print(f"Liked {x+1} photo")
    
    if x+1 == 20:
        break  