from selenium import webdriver
from selenium.webdriver.common.by import By


site = "https://shopee.vn/"
driver = webdriver.Chrome()

driver.get(site)
# web load hết thì mới có đủ content
driver.implicitly_wait(10)

try:    
    # popup của shopee không thể đc access theo kiểu bình thường
    # do là ở trong một cái "shadow DOM" gì đó
    custom_shopee_tag = driver.find_element(By.TAG_NAME, "shopee-banner-popup-stateful")
    custom_shopee_tag_shadow_root = custom_shopee_tag.shadow_root
    button = custom_shopee_tag_shadow_root.find_element(By.CLASS_NAME, "shopee-popup__close-btn")
    button.click()

except Exception as e:
    print(e)

finally:
    driver.quit()

