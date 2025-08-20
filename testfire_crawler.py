"""
Simple Selenium Crawler for demo.testfire.net
============================================
This script crawls the TestFire demo banking site, performs login,
and records 5 pages with screenshots and action logs.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

class TestFireCrawler:
    def __init__(self):
        """Initialize the Selenium WebDriver"""
        print("🚀 Starting Selenium WebDriver...")
        
        # Setup Chrome driver with automatic driver management
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 10)
        self.page_count = 0
        
        print("✅ WebDriver ready!")

    def take_screenshot_and_log(self, page_name, action):
        """Take screenshot and log the action"""
        self.page_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Take screenshot
        screenshot_name = f"page_{self.page_count}_{page_name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_name)
        
        # Log information
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        print(f"\n📸 PAGE {self.page_count}: {page_name}")
        print(f"   Action: {action}")
        print(f"   URL: {current_url}")
        print(f"   Title: {page_title}")
        print(f"   Screenshot: {screenshot_name}")
        print("-" * 60)
        
        # Small delay to see the page
        time.sleep(2)

    def crawl_testfire(self):
        """Main crawling function - visits 5 pages"""
        print("🔥 Starting TestFire.net Crawl")
        print("=" * 50)
        
        try:
            # PAGE 1: Homepage
            print("🌐 Navigating to TestFire homepage...")
            self.driver.get("https://demo.testfire.net/")
            self.take_screenshot_and_log("Homepage", "Loaded demo.testfire.net homepage")
            
            # PAGE 2: Sign In Page
            print("🔐 Navigating to Sign In page...")
            sign_in_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))
            )
            sign_in_link.click()
            self.take_screenshot_and_log("Sign_In_Page", "Clicked Sign In link")
            
            # PAGE 3: Login Process
            print("👤 Performing login...")
            # Enter demo credentials
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "uid"))
            )
            password_field = self.driver.find_element(By.NAME, "passw")
            
            username_field.send_keys("admin")
            password_field.send_keys("admin")
            
            login_button = self.driver.find_element(By.NAME, "btnSubmit")
            login_button.click()
            time.sleep(3)
            
            self.take_screenshot_and_log("Account_Summary", "Successfully logged in")
            
            # PAGE 4: View Account Details
            print("💰 Viewing account details...")
            try:
                account_link = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "View Account Details"))
                )
                account_link.click()
                self.take_screenshot_and_log("Account_Details", "Clicked View Account Details")
            except:
                # Alternative navigation if link text is different
                print("⚠️ Account Details link not found, trying alternative...")
                self.driver.get("https://demo.testfire.net/bank/account")
                self.take_screenshot_and_log("Account_Details", "Navigated to account details page")
            
            # PAGE 5: Transfer Funds or Another Page
            print("💸 Accessing transfer funds...")
            try:
                # Go back to main account page first
                self.driver.get("https://demo.testfire.net/bank/main.jsp")
                time.sleep(2)
                
                transfer_link = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
                )
                transfer_link.click()
                self.take_screenshot_and_log("Transfer_Funds", "Clicked Transfer Funds")
            except:
                # Alternative: Try to access any other available page
                print("⚠️ Transfer Funds not found, accessing Contact page...")
                self.driver.get("https://demo.testfire.net/")
                contact_links = self.driver.find_elements(By.LINK_TEXT, "Contact Us")
                if contact_links:
                    contact_links[0].click()
                    self.take_screenshot_and_log("Contact_Page", "Navigated to Contact Us page")
                else:
                    # Just take screenshot of current page
                    self.take_screenshot_and_log("Current_Page", "Captured current page state")
            
            # BONUS: Logout (if possible)
            print("🚪 Attempting logout...")
            try:
                logout_links = self.driver.find_elements(By.LINK_TEXT, "Sign Off")
                if logout_links:
                    logout_links[0].click()
                    time.sleep(2)
                    print("✅ Successfully logged out")
                else:
                    print("⚠️ Logout link not found")
            except:
                print("⚠️ Logout process failed")
            
        except Exception as e:
            print(f"❌ Error during crawling: {str(e)}")
            self.take_screenshot_and_log("Error_Page", f"Error occurred: {str(e)}")
        
        finally:
            print(f"\n🎯 Crawling Summary:")
            print(f"   Total pages recorded: {self.page_count}")
            print(f"   Screenshots taken: {self.page_count}")
            print(f"   Target website: https://demo.testfire.net/")
            
            print("\n🔄 Closing browser in 5 seconds...")
            time.sleep(5)
            self.driver.quit()
            print("✅ Browser closed successfully!")

def main():
    """Run the TestFire crawler"""
    print("🔥 TestFire.net Selenium Crawler")
    print("This will visit 5+ pages and take screenshots")
    print("=" * 50)
    
    crawler = TestFireCrawler()
    crawler.crawl_testfire()
    
    print("\n🎉 Crawling completed!")
    print("Check the current directory for screenshot files:")
    print("- page_1_Homepage_*.png")
    print("- page_2_Sign_In_Page_*.png") 
    print("- page_3_Account_Summary_*.png")
    print("- page_4_Account_Details_*.png")
    print("- page_5_Transfer_Funds_*.png")

if __name__ == "__main__":
    main()