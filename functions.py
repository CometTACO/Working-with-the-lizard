import re
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


IMPLICIT_WAIT_TIME = 5

def load_cookies(driver):
    cookies = pickle.load( open( "./cookies.pkl", "rb" ) )
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.refresh()

def close_popup(driver):
    try:    
        # popup của shopee không thể đc access theo kiểu bình thường
        # do là ở trong một cái "shadow DOM" gì đó
        driver.implicitly_wait(IMPLICIT_WAIT_TIME)
        custom_shopee_tag = driver.find_element(By.TAG_NAME, "shopee-banner-popup-stateful")
        custom_shopee_tag_shadow_root = custom_shopee_tag.shadow_root
        button = custom_shopee_tag_shadow_root.find_element(By.CLASS_NAME, "shopee-popup__close-btn")
        button.click()
        
    except Exception as e:
        print("[LOGGING] encoutered an exception while attempting to close a popup. here is the exception:", e)

 
def scrape_product_links(driver, action_chains):
    try:
        driver.implicitly_wait(IMPLICIT_WAIT_TIME)
        search_result_box = driver.find_element(By.CLASS_NAME, "shopee-search-item-result__items")
        
        action_chains.scroll_to_element(search_result_box)
        print("[LOGGING] found result box. attempting scraping")
        
        search_result_items_divs = search_result_box.find_elements(By.CLASS_NAME, "col-xs-2-4")
        product_links = []
        for div in search_result_items_divs:
            try:
                a_tag = div.find_element(By.TAG_NAME, "a")
                product_link = a_tag.get_attribute("href")
                product_links.append(product_link)
                
                print(f"[LOGGING] found link: {product_link}")

            except Exception as e:
                print("[LOGGING] exception encountered while scraping product links:", e)

        return product_links

    except Exception as e:
        print("[LOGGING] exception encountered at scrape_page function:", e)


def scrape_categoryID(driver, product_link):
    try:
        driver.get(product_link)
        driver.implicitly_wait(IMPLICIT_WAIT_TIME)
        
        div_containing_xem_shop_button = driver.find_element(By.CLASS_NAME, "Uwka-w")
        xem_shop_button = div_containing_xem_shop_button.find_element(By.TAG_NAME, "a")
        shop_link = xem_shop_button.get_attribute("href")
        match = re.search("categoryId=(\d)+", shop_link)        
        categoryID = shop_link[match.start()+11:match.end()] 

        return categoryID

    except Exception as e:
        print(e)

def get_page(driver, site):
    driver.get(site)
    close_popup(driver)
   
