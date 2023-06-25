from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from SeleniumScraping import *

 
# Instagram Post Object
class Post:
    def __init__(self, postLink:str, driver:webdriver.Chrome) -> None:
        
        # Post Link
        self._postLink = postLink 
        
        # Driver
        self._driver = driver
         
    @property
    def driver(self) -> None:
        return self._driver
    
    @property
    def postLink(self) -> None:
        return self._postLink
        
    @property     
    def username(self) -> str:
        # Go to Post
        goToWebsite(self.postLink,self._driver)
        
        return element("//div/span/a",self._driver).text
    
    '''
    @property
    def num_likes(self) -> int:
        pass
    
    @property
    def location(self) -> str:
        pass
    
    @property
    def caption(self) -> str:
        pass
    
    @property
    def date(self) -> str:
        pass
    '''
            
    def like(self) -> None:
        
        # Go to Post
        goToWebsite(self.postLink, self.driver)

        
        # Clicks the Like Btn
        click("//section/span[0]/button", self.driver)
    
    def comment(self, comment:str) -> None:
        
        # Go to Post
        goToWebsite(self.postLink, self.driver)
        
        click("//section/span[1]/button", self.driver)

    def send(self, username:str) -> None:
        
        # Go to Post
        goToWebsite(self.postLink, self.driver)
        
        click("//section/span[2]/button", self.driver)
        
    def save(self) -> None:
        
        # Go to Post
        goToWebsite(self.postLink, self.driver)
        
        # Click Save Button
        click("//span/div/div/button[/div[1]]", self.driver)
    
# Instagram Account Object
class Account:
    def __init__(self, username:str, driver:webdriver.Chrome) -> None:
        
        # Driver for Selenium
        self._driver = driver
        
        # Username
        self._username  = username

    @property
    def driver(self) -> webdriver.Chrome:
        return self._driver
    
    @property
    def username(self) -> webdriver.Chrome:
        return self._username

    def goToAccountPage(self) -> None:
        
        # Go to Account Page
        goToWebsite(f'https://www.instagram.com/{self.username}/', self.driver) 

    def follow(self) -> None:
        
        # Go to Account Page
        self.goToAccountPage()
        
        # Click Gollow Button
        click("//button[//*[contains(text(),'Follow')]]", self.driver)
    
    def unfollow(self) -> None:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Click on Unfollow
        click("//button[//*[contains(text(),'Following')]]", self.driver)

    @property
    def bio(self) -> str:
        # Goes Account Page
        self.goToAccountPage(self.username)
        
        # Returns the Bio Text
        return element("//div[@class ='_aa_c']/h1", self.driver).text
        
    @property
    def accountImage(self) -> str:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Return Account Image
        return element("//header//div/span/img", self.driver).get_attribute('href')
    
    @property
    def posts(self) -> list[str]:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Gets the Number of Posts
        numPosts = int(elements("//span/span", self.driver)[0].text)
        
        # Posts
        posts = [x.get_attribute('href')for x in elements("//article//div/a",self.driver)]
        
        # Scroll Down to retrieve more Posts
        x = 1
        while len(posts) < numPosts:
            execute(f"window.scrollTo(0, document.body.scrollHeight*{x});", self.driver)
            
            posts.extend(x.get_attribute('href') for x in elements("//article//div/a",self.driver))
            posts = list(set(posts))
            x+=1
            
        return posts
    
    @property
    def num_posts(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Returns Number of Posts
        return element('//li/span/span', self.driver).text
    
    @property
    def num_followers(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Returns Number of Followers
        return elements('//li//a/span/span', self.driver)[0].text
    
    @property
    def num_following(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Return Number of Following
        return elements('//li//a/span/span', self.driver)[1].text
    
    @property
    def followers(self) -> list:
        
        # Got To Followers
        goToWebsite(f"https://www.instagram.com/{self.username}/followers/", self.driver)
        
        # Main Followers Area
        box = element("//div[@class = '_aano']", self.driver)
        
        # Accounts in Following
        following = [Account(x.text, self.driver) for x in elements("//div[@class ='xt0psk2']", self.driver)]
        
        # Number of Previous Following
        prev_amount  = 0
        
        # Scrolling and Adding Accounts of Following
        x= 1
        while prev_amount != len(following):
            
            # Scroll
            self.driver.execute_script(f"arguments[0].scrollTo(0, document.body.scrollHeight*{x});",box)
            sleep(5)
            
            p = len(following)
            following.extend([Account(x.text, self.driver) for x in elements("//div[@class ='xt0psk2']", self.driver)])
            following = list(set(following))
            
            prev_amount = p
            x+=1
            
        return following
    
    @property
    def following(self) -> list:
        
        # Go to Following Username
        goToWebsite(f"https://www.instagram.com/{self.username}/following/", self.driver)
        
        # Main Following Area
        box = element("//div[@class = '_aano']", self.driver)
        
        # Following Accounts
        following = [Account(x.text, self.driver) for x in elements("//div[@role = 'dialog']//a//span/div", self.driver)]
        prev_amount  = 0
        
        # Scroll to Add More to Following Accounts
        x= 1
        while prev_amount < len(following):
            
            # Scroll
            self._driver.execute_script(f"arguments[0].scrollTo(0, document.body.scrollHeight*{x});",box)
            sleep(5)
            p = len(following)
            
            following.extend([Account(x.text, self.driver) for x in elements("//div[@role = 'dialog']//a//span/div", self.driver)])
            following = list(set(following))
            
            prev_amount = p
            x+=1
            
        return following
         
# Instagram Bot Object
class Instabot:
    
    def __init__(self, driverDirectory:str, username:str = None, password:str = None,  headless:bool = False) -> None:
        
        # Username & Password of Instagram Account
        self._username = username
        self._password = password
        
        # Selenium Driver
        if headless: 
            self._driver = webdriver.Chrome(executable_path = driverDirectory, options = Options().add_argument("--headless"))
        else:
            self._driver = webdriver.Chrome(executable_path = driverDirectory)
            
        # Login into Instagram Account
        if username is not None or password is not None:
            self.login()
            
    def login(self, username:str = None, password:str = None) -> None:
        
        # Change to Self
        if username is None or password is None:
            username = self.username
            password = self.password
        
        # Opens Instagram
        self.goToHomePage()

        # Retrieve the Input Fields for Username and Password
        input(username,"//*[@name='username']",self.driver)
        input(password,"//*[@name='password']", self.driver)

        # Find and click Login Button
        try:
            click('//button[@type="submit"]',self.driver)
        except:
            pass

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
        
        sleep(5)
        
    def logout(self) -> None:
        pass
              
    def goToHomePage(self) -> None:
        
        # Go to Instagram Home Page
        goToWebsite("https://www.instagram.com", self.driver)
    
        # Clicks Button if it is there
        try:
            click('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]',self.driver)
        except:
            pass 
        
    def goToAccountPage(self, username:str) -> None:
        
        # Goes to Account
        goToWebsite(f'https://www.instagram.com/{username}/',self.driver) 
    
    def goToHashtag(self, hashtag:str) -> None:
        
        # Goes to the Hashtag
        goToWebsite(f"https://www.instagram.com/explore/tags/{hashtag}/",self.driver)
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def driver(self) -> webdriver.Chrome:
        return self._driver
    
    
    
    # Account Functions and Data
    @property
    def bio(self) -> str:
        
        # Goes Account Page
        self.goToAccountPage(self.username)
        
        # Returns the Bio Text
        return element("//div[@class ='_aa_c']/h1",self.driver).text
            
    @property
    def accountImage(self) -> str:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Return Account Image
        return element("//header//div/span/img",self.driver).get_attribute('href')
    
    @property
    def posts(self) -> list[Post]:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Gets the Number of Posts
        numPosts = int(elements("//span/span",self.driver)[0].text)
        
        # Posts
        posts = [Post(x.get_attribute('href'),self.driver) for x in elements("//article//div/a",self.driver)]
        
        # Scroll Down to retrieve more Posts
        x = 1
        while len(posts) < numPosts:
            execute(f"window.scrollTo(0, document.body.scrollHeight*{x});", self.driver)
            
            posts.extend(Post(x.get_attribute('href'), self.driver) for x in elements("//article//div/a",self.driver))
            posts = list(set(posts))
            x+=1
            
        return posts
    
    @property
    def num_posts(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Returns Number of Posts
        return element('//li/span/span',self.driver).text
    
    @property
    def num_followers(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Returns Number of Followers
        return elements('//li//a/span/span',self.driver)[0].text
    
    @property
    def num_following(self) -> int:
        
        # Go to Account Page
        self.goToAccountPage(self.username)
        
        # Return Number of Following
        return elements('//li//a/span/span',self.driver)[1].text
    
    @property
    def followers(self) -> list[Account]:
        
        # Got To Followers
        goToWebsite(f"https://www.instagram.com/{self.username}/followers/",self.driver)
        
        # Main Followers Area
        box = element("//div[@class = '_aano']",self.driver)
        
        # Accounts in Following
        following = [Account(x.text,self.driver) for x in elements("//div[@class ='xt0psk2']",self.driver)]
        
        # Number of Previous Following
        prev_amount  = 0
        
        # Scrolling and Adding Accounts of Following
        x= 1
        while prev_amount != len(following):
            
            # Scroll
            self.driver.execute_script(f"arguments[0].scrollTo(0, document.body.scrollHeight*{x});",box)
            sleep(5)
            
            p = len(following)
            following.extend([Account(x.text,self.driver) for x in elements("//div[@class ='xt0psk2']",self.driver)])
            following = list(set(following))
            
            prev_amount = p
            x+=1
            
        return following
    
    @property
    def following(self) -> list[Account]:
        """Following Accounts

        :return: Following Accounts
        :rtype: list[Account]
        """
        
        # Go to Following Username
        goToWebsite(f"https://www.instagram.com/{self.username}/following/",self.driver)
        
        # Main Following Area
        box = element("//div[@class = '_aano']",self.driver)
        
        # Following Accounts
        following = [Account(x.text,self.driver) for x in elements("//div[@role = 'dialog']//a//span/div",self.driver)]
        prev_amount  = 0
        
        # Scroll to Add More to Following Accounts
        x= 1
        while prev_amount < len(following):
            
            # Scroll
            self._driver.execute_script(f"arguments[0].scrollTo(0, document.body.scrollHeight*{x});",box)
            sleep(5)
            p = len(following)
            
            following.extend([Account(x.text,self.driver) for x in elements("//div[@role = 'dialog']//a//span/div",self.driver)])
            following = list(set(following))
            
            prev_amount = p
            x+=1
            
        return following
         
    def post(self, postDirectory:str, caption:str) -> None:
        
        # Go to Home Page
        self._goToHomePage()
        
        # Click Post Button
        click("//div[7]/div/div/a",self._driver)

        # Input the Post Media
        input(postDirectory,"//form/input[@accept = 'image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']",self._driver)

        # Only shows up on Video posts
        click("//button[contains(text(), 'OK')]", self._driver)

        # Expand Post
        click("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button", self._driver)
        
        click("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]",self._driver)
        
        # Leaves the Cropping of the Post
        click("//*[contains(text(), 'Next')]",self._driver)
        

        # Leave Edit with Filters
        click("//button[contains(text(), 'Next')]",self._driver)

        # Adds a Caption to the Post
        input(caption,'//*[@aria-label="Write a caption..."]',self._driver)

        # Button Clicked to Share Post
        click("//button[contains(text(), 'Share')]",self._driver)

    def deletePost(self, post:Post) -> None:
        
        # Check to see if that this Post is part of this account
        if post.username == self.username:
    
            # Go to Account Page
            goToWebsite(post.postLink,self._driver)
            
            # Go to More
            click("//div[@class = '_aasm']/button",self._driver)
            
            # Click Delete Button
            click("//button[contains(text(), 'Delete')]",self._driver)
            
            # Finalize Click Delete Button
            click("//button[contains(text(), 'Delete')]",self._driver)
        
    def getHashtagPosts(self, hashtag:str, amount:int) -> list[Post]:
        
        # Go to Hashtag Page
        self.goToHashtag(hashtag)

        # Retrieve Top Hashtag Posts
        postsArea = element('//article/div[2]',self.driver)

        postLinks = [x.get_attribute('href') for x in elements("//a",postsArea)][:amount]

        x = 1
        # Retrieves the Post Links
        while len(postLinks) < amount:
            execute(f"window.scrollTo(0, document.body.scrollHeight*{x});", self.driver)

            # Retrieve Top Hashtag Posts
            postsArea = element('//article/div[2]',self.driver)

            postLinks = [x.get_attribute('href') for x in elements("//a",postsArea)][:amount]
            x+=1
            
        return [Post(x) for x in postLinks]
    
    def getTopHashtagPosts(self, hashtag:str) -> list[Post]:
        
        # Goes to Hashtag Page
        self.goToHashtag(hashtag)

        # Retrieve Top Hashtag Posts
        topPostsArea = None
        while topPostsArea is None:
            topPostsArea = element("//article/div[@class ='_aaq8']/div",self.driver)
            
        # Retrieve the Top Posts
        postLinks = [x.get_attribute('href') for x in elements("//a",topPostsArea)]

        return [Post(x) for x in postLinks]
   
   