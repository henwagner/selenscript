from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from datetime import datetime

def log(message):
    print(datetime.now().isoformat() + "\t" + message)
    return

def check_robots_txt():
    return True

def accept_terms(driveratroot):
    nonclickables = ['script', 'iframe', 'fieldset', 'embed', 'frame', 'form', 'frameset', 'noframe', 'br', 'wbr', 'link']
    driver.switch_to.default_content()
    for element in driveratroot.find_elements_by_xpath('//*[contains(text(), "I agree")]'):
        log(element.tag_name)
        if element.tag_name not in nonclickables and element.is_enabled() and element.is_displayed():
            try:
                element.click()
                tostring = element.get_attribute('outerHTML')
                if len(tostring)>10:
                    tostring = tostring[:10] + "..."
                log("clicked: " + tostring)
            except Exception as e:
                log(str(e))
    
    iframes = driveratroot.find_elements_by_tag_name("iframe")
    for frm in iframes:
        driveratroot.switch_to.frame(frm)
        for element in driveratroot.find_elements_by_xpath('//*[contains(text(), "I agree")]'):
            try:
                log(element.tag_name)
                if element.tag_name not in nonclickables and element.is_enabled() and element.is_displayed():
                    try:
                        # to string
                        tostring = element.get_attribute('outerHTML')
                        if len(tostring)>10:
                            tostring = tostring[:10] + "..."
                        #log and click
                        log("clicking: " + tostring)
                        element.click()
                        log("clicked: " + tostring)
                    except Exception as e:
                        log(str(e))
            except (StaleElementReferenceException, NoSuchElementException) as ex: # in case the DOM is changeing, for example from an earlier click
                log(str(ex))
    return

def search_for_epping(driver):
    driver.switch_to.default_content()
    serachbox = driver.find_element_by_id("searchboxinput")
    serachbox.send_keys("Epping Forest")
    serachbox.send_keys(Key.ENTER)
    return

def pan_and_zoom_in():
    return

def switch_to_aerial():
    return

def click_on_map():
    return

def measure_area():
    return

def main():
    """ Main program """
    if check_robots_txt():
        # set preferences
        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.enabled", True)
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.provider.use_corelocation", False)
        profile.set_preference("geo.wifi.uri", 'data:application/json,{"location": {"lat": 0.00, "lng":-77.036185}, "accuracy": 20.0}')
        driver = webdriver.Firefox(executable_path='./geckodriver', firefox_profile=profile)

        # window size
        driver.set_window_size(700,500)

        # launch google maps
        driver.get('https://maps.google.co.uk')
        driver.implicitly_wait(2)
        driver.get_screenshot_as_file('./step0-maps.png')

        # accept terms
        accept_terms(driver)
        driver.get_screenshot_as_file('./step1-t&c.png')

        # search for epping
        search_for_epping(driver)
        driver.get_screenshot_as_file('./step2-search.png')

        # pan the map
        #driver.get_screenshot_as_file('./step3-pan.png')

    
        driver.quit()
    
    
    
    #WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located(By.XPATH("//*[contains(text(), 'I agree')]")))
    

    #print(str(len(driver.find_elements_by_xpath('//*[contains(text(), "I agree")]'))))
    #print(str(len(driver.find_elements_by_xpath('//*[contains(text(), "I agree")]'))))
    #iagreebutton, = driver.find_elements_by_xpath("//*[contains(text(), 'I agree')]") # expecting exactly one
    #iagreebutton.click()
    #driver.get("https://www.w3schools.com/html/html5_geolocation.asp")
    #driver.find_element_by_class_name("w3-blue").click()
    #driver.quit()
    return 0

if __name__ == "__main__":
    main()