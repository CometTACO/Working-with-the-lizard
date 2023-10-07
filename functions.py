from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


IMPLICIT_WAIT_TIME = 5

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
        print("encoutered an exception while attempting to close a popup. here is the exception:", e)


def scrape_page(driver):
    try:
        driver.implicitly_wait(IMPLICIT_WAIT_TIME)
        search_result_box = driver.find_element(By.CLASS_NAME, "shopee-search-item-result__items")
        
        print("found result box. attempting scraping")
        
        search_result_items_divs = search_result_box.find_elements(By.TAG_NAME, "div")
        for div in search_result_items_divs:
            print(div.text)
            
    except Exception as e:
        print("exception encountered at scrape_page function:", e)



