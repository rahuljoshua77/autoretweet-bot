import random,time,os
cwd = os.getcwd()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
 
mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 650, "pixelRatio": 3.4 },
    }

firefox_options = webdriver.ChromeOptions()
firefox_options.add_argument('--no-sandbox')
 
firefox_options.headless = True
firefox_options.add_argument('--disable-setuid-sandbox')
firefox_options.add_argument('disable-infobars')
firefox_options.add_argument('--ignore-certifcate-errors')
firefox_options.add_argument('--ignore-certifcate-errors-spki-list')

firefox_options.add_argument("--incognito")
firefox_options.add_argument('--no-first-run')
firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--disable-popup-blocking")
firefox_options.add_argument('--log-level=3') 
firefox_options.add_argument("--window-size=500,1600")
firefox_options.add_argument('--disable-blink-features=AutomationControlled')
firefox_options.add_experimental_option("useAutomationExtension", False)
firefox_options.add_experimental_option("excludeSwitches",["enable-automation"])
firefox_options.add_experimental_option('excludeSwitches', ['enable-logging'])
firefox_options.add_argument('--disable-notifications')
from selenium.webdriver.common.action_chains import ActionChains
random_angka = random.randint(100,999)
random_angka_dua = random.randint(10,99)
def xpath_ex(el):
    element_all = wait(browser,0.3).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all)

def xpath_long(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all)



def auto(username,password):

    xpath_long('//button[contains(@data-testid,"follow")]')

    print(f"[*] [{username}] Follow Done!")
   
    try:
        wait(browser,0.5).until(EC.presence_of_element_located((By.XPATH, '(//div[@data-testid="unlike"])[1]'))).click()
    except:
        pass
    xpath_long('(//button[@data-testid="like"])[1]')
    print(f"[*] [{username}] Like Done!")
    
    
    xpath_ex("(//button[@aria-haspopup='menu' and contains(@aria-label,'Posting ulang') or contains(@aria-label,'Repost') or contains(@aria-label,'Retweet')])[1]")
    
    choice = open(f"{cwd}\\choice.txt","r")
    choice = choice.read()
    
    if "y" in choice.lower() or "Y" in choice:
        xpath_ex('//div[@data-testid="Dropdown"]/a[@href="/compose/post"]')
        sleep(1)

        myfile = open(f"{cwd}\\quotes.txt","r")
        get_quotes = myfile.read()
        get_quotes = get_quotes.split("\n")
        quotes = random.choice(get_quotes)
        myfile = open(f"{cwd}\\friend.txt","r")
        get_friend = myfile.read()
        get_friend = get_friend.split("\n")
        s = random.sample(get_friend, 3)
        friends = ', '.join([str(elem) for elem in s])
        input_quotes = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, '(//*[@autocapitalize="sentences"])[1]')))
        input_quotes.send_keys(f"{quotes} {friends}")
        xpath_ex('(//button[@data-testid="tweetButton"])[1]')
        browser.get(f'https://twitter.com/{username}')
        try:
            get_url = wait(browser,40).until(EC.presence_of_element_located((By.XPATH, f'(//a[contains(@href,"/{username}/status/")])[1]'))).get_attribute('href')
            print(f"[*] [{username}] Link Quoted: {get_url}")
            with open('results.txt','a') as f:
                f.write(f"{username}|{get_url}")
        except:
            pass
        print(f"[*] [{username}] Retweet Done!")
        
    else:
        xpath_ex('(//div[@data-testid="retweetConfirm"])[1]')
        
        print(f"[*] [{username}] Retweet Done!")
    
    
def login(acc):
    acc = acc.split("|")
    
    username = acc[0]
    password = acc[1]
    try:
        verif = acc[2]
    except:
        pass
    global browser
    
    #firefox_options.add_experimental_option("mobileEmulation", mobile_emulation)
    firefox_options.add_argument(f"user-agent=Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1")
    browser = webdriver.Chrome(options=firefox_options)
    myfile = open(f"{cwd}\\url.txt","r")
    url = myfile.read()
    browser.get("https://mobile.twitter.com/i/flow/login")
    
    
    user_input = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]')))
    user_input.send_keys(username)
    user_input.send_keys(Keys.ENTER)
    try:
       verif_input = wait(browser,2.5).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')))
       verif_input.send_keys(verif)
       verif_input.send_keys(Keys.ENTER)
     
    except:
        pass
    sleep(2)

    pw_input = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]')))
    pw_input.send_keys(password)
    pw_input.send_keys(Keys.ENTER)
    sleep(10)
    browser.get(url)
    try:
        auto(username,password)
        browser.quit()
    except Exception as e:
        print(f"[*] [{username}] Error: {e}")
        browser.quit()


if __name__ == '__main__':
    print("[*] Auto Twitter")
    voucher = input('[+] Input URL: ')
    with open('url.txt','w') as f: f.write(f'{voucher}\n')

    choice = input('[+] Input choice retweet with quote (y/n): ')
    with open('choice.txt','w') as f:
            f.write(f'{choice}')
    myfile = open(f"{cwd}\\list.txt","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split("\n")
    for i in list_accountsplit:
        try:
            login(i)
        except IndexError:
            print("[*] Need More Data!")
      
