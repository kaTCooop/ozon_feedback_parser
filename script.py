import os, time
import seleniumbase as sb 

from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from termcolor import colored


global span_class, hidden_span_class

span_class = None
hidden_span_class = None

def get_random_chrome_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random

def create_driver():
    driver = sb.Driver(browser = 'chrome', headless = False, uc = True, incognito = True)
    wait = webdriver.Chrome.implicitly_wait(driver, 20)

    driver.set_page_load_timeout(100)

    stealth(driver=driver,
                user_agent=get_random_chrome_user_agent(),
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                wait=wait
                )

    return driver

def find_span_class(driver):
    script = open('ozonFindSpan.js', 'r').read()
    return driver.execute_script(script)

def check_for_el(driver, html, c):
    e = driver.find_element(By.CLASS_NAME, c)
    return e

def mouse_click(driver, element):
    element.click()
    time.sleep(0.1)

def get_hidden(span_class):
    hidden  = span_class[1] + str(int(span_class[2]) + 1) + span_class[0] + '_' + span_class[4] + span_class[5]
    return hidden

def get_star_class(span_class):
    star = span_class[0] + span_class[1] + str(int(span_class[2]) - 1) + span_class[3:]
    return star

def get_parent_star_class(hidden_span_class):
    return hidden_span_class[2] + str(int(hidden_span_class[1]) - 3) \
            + hidden_span_class[0] + hidden_span_class[3:]

def main_login(url, pause=300, rev=False, driver=None):
    global span_class, hidden_span_class
    
    if driver is None:
        driver = create_driver()
        driver.uc_open_with_reconnect(url, 4)
        time.sleep(pause)

    h = login_for_hidden_spans(driver)

    SCROLL_PAUSE_TIME = 0.3

    result = []
    
    if rev is False:
        step = 1600
        height = step
        last_len = 0

    else:
        step = -700
        height = driver.execute_script("return document.body.scrollHeight")

    start = time.time()

    # scrolling web
    while True:

        if span_class is None and rev is False:
            span_class = find_span_class(driver)
            print(span_class)
            
            if span_class is not None:
                hidden_span_class = get_hidden(span_class)
                print(hidden_span_class)

                time.sleep(3)

                return main_login(url, pause=pause, rev=True, driver=driver)
                
        if rev is True:
            html = driver.page_source
            result.append(html)

        # Scroll down to bottom
        driver.execute_script(f"window.scrollTo(0, {height});")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = height + step

        if rev is False:
            if new_height >= driver.execute_script("return document.body.scrollHeight"):
                break
        else:
            if new_height <= 300:
                break

        height = new_height
    
    diff = time.time() - start

    if diff <= 5:
        raise ValueError('Restart sctipt')
  
    time.sleep(3)
    driver.quit()
    print('quitting driver')
    return result[::-1]

def login_for_hidden_spans(driver):
    global hidden_span_class
    
    if hidden_span_class is None:
        return None
    
    print('hidden span searching loop')

    SCROLL_PAUSE_TIME = 0.3
    
    result = []
    step = 500
    height = step
    last_len = 0

    start = time.time()

    # scrolling web
    while True:
        
        html = driver.page_source
        
        try:
            hidden_element = check_for_el(driver, html, hidden_span_class)
        
        except NoSuchElementException:
            hidden_element = None

        print(hidden_element)

        if hidden_element is not None:
            
            try:
                mouse_click(driver, hidden_element)
            
            except ElementClickInterceptedException:
                pass
            
            else: 
                result.append(html)
        
        # Scroll down to bottom
        driver.execute_script(f"window.scrollTo(0, {height});")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = height + step

        if new_height >= driver.execute_script("return document.body.scrollHeight"):
            break

        height = new_height
   
    diff = time.time() - start

    if diff <= 5:
        driver.quit()
        raise ValueError('Restart sctipt')

    return result

def parse(html, search=None, attr=None, string=None):
    soup = BeautifulSoup(html, features = "html.parser")
    
    if soup is not None:
        result = soup.find_all(search, attrs=attr, string=string)

    return result

def line_break_remove(text):
    text = text[:-1] if text[-1] == '\n' else text
    return text


if __name__ == '__main__':
    useragent = get_random_chrome_user_agent()
    
    target_url = 'https://www.ozon.ru/product/grechnevaya-krupa-agroholding-step-900g-1597288781/?oos_search=false'

    pause_to_set_up = 15

    # add pause to get time to add attr values
    result = main_login(target_url, pause=pause_to_set_up)

    span = []
    hid_span = []
    last_len = 0
    
    if span_class is not None:

        print('span_class ' + span_class)
        print('hidden_span_class ' + hidden_span_class)
        print('star_class ' + get_star_class(span_class))
        print('parent_star_class ' + get_parent_star_class(hidden_span_class))
        print(colored('...working...', 'red'), end='\n\n')

        for html in result:
            current_span = parse(html, 'span', {'class' : span_class})[last_len:]
            span += current_span
            last_len += len(current_span)
        
        n = 0     
        concatenate = False
        saved = None
        
        for s in span:
            par = s.parent.parent.parent.parent
            cl = par['class'][0]
            parent_divs = par.parent.children

            for i, e in enumerate(parent_divs):
                
                if i == 0:
                    x = e
                
            div = x.find('div', {'class' : get_parent_star_class(hidden_span_class)})
            stars = div.find('div', {'class' : get_star_class(span_class)})
            acc = 0

            for star in stars.find().children:

                if star['style'] == 'color: rgb(255, 168, 0);':
                    acc += 1
                
                else:
                    break

            text = s.text

            if (saved is not None) and (concatenate is False):
                text = saved + '\n'+ text
            
            elif concatenate is True:
                text = saved + '\n' + text
                concatenate = False  
                saved = text
                saved = line_break_remove(saved)
                continue       

            elif 'Достоинства' in s.parent.parent.find('div').text:
                saved = text
                saved = line_break_remove(saved)
                concatenate = True
                continue
        
            text = line_break_remove(text)
            print('feedback #' + colored(str(n), 'green'), end='')
            print(' ' + str(acc) + ' / 5')
            print(text, end='\n\n')
            n += 1
            saved = None

    else:
        print('there are not any comments')

