from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from datetime import datetime
import time

def log(message):
    print(datetime.now().isoformat() + "\t" + message)
    return

def check_robots_txt():
    return True

def accept_terms(driver):
    ariatext = "Agree to the use of cookies and other data for the purposes described"
    
    # find the button
    driver.switch_to.default_content()
    agreebutton = None
    try:
        agreebutton = driver.find_element_by_xpath("//*[@aria-label='" + ariatext + "']")
    except NoSuchElementException as outerex:
        log(str(outerex))
        iframes = driver.find_elements_by_tag_name("iframe")
        for frm in iframes:
            try:
                driver.switch_to.frame(frm)
                agreebutton = driver.find_element_by_xpath("//*[@aria-label='" + ariatext + "']")
                break
            except NoSuchElementException as innerex:
                log(str(innerex))
    
    # try clicking it
    try:
        if agreebutton.is_enabled() and agreebutton.is_displayed():
            agreebutton.click()
    except (StaleElementReferenceException, NoSuchElementException) as e:
        log(str(e))

    return

def search_for_epping(driver):
    driver.switch_to.default_content()
    serachbox = driver.find_element_by_xpath("//*[@aria-label='Search Google Maps']")
    serachbox.send_keys("Epping Forest")
    serachbox.send_keys(Keys.ENTER)
    return

def pan_and_zoom_in(driver):
    driver.switch_to.default_content()
    zoominbutton = driver.find_element_by_xpath("//*[@aria-label='Zoom in']")
    for i in range(5):
        log("zoom in")
        zoominbutton.click()
        time.sleep(0.2)

    mapcontainer = driver.find_element_by_xpath("//*[@aria-label='Map']")
    panactions = [(Keys.UP, "up"), (Keys.UP, "up"), (Keys.RIGHT, "right"), (Keys.RIGHT, "right"), (Keys.UP, "up")]
    for key,name in panactions:
        log(name)
        mapcontainer.send_keys(key)
        time.sleep(0.2)

    for i in range(3):
        log("zoom in")
        zoominbutton.click()
        time.sleep(0.2)

    return

def switch_to_aerial(driver):
    driver.switch_to.default_content()
    basemapswitcher = driver.find_element_by_xpath("//*[@aria-labelledby='widget-minimap-caption']") # there is a separate label hence labelledby
    basemapswitcher.click()
    time.sleep(2) # allowing extra time for the new tiles to download
    return

def click_on_map(driver):
    driver.switch_to.default_content()
    size = driver.get_window_size()
    centreheight = size['height'] / 2
    centrewidth = size['width'] / 2
    body, = driver.find_elements_by_tag_name('body') # unpacking to ensure a single body tag
    action = ActionChains(driver)
    action.move_to_element_with_offset(body, centrewidth, centreheight).click().perform()

    return

def measure_area(driver):
    driver.switch_to.default_content()
    size = driver.get_window_size()
    centreheight = size['height'] / 2
    centrewidth = size['width'] / 2
    body, = driver.find_elements_by_tag_name('body') # unpacking to ensure a single body tag

    areacoordsoffests = [(10,50), (20, 50), (20, 100), (10, 100), (10, 70), (10, 50)]
    #areacoordsoffests = [(100,100), (200, 200), (300, 300)]
    areacoords = [(centrewidth + a[0], centreheight + a[1]) for a in areacoordsoffests]

    action = ActionChains(driver)
    action.move_to_element_with_offset(body, areacoords[0][0], areacoords[0][1]).context_click().perform()
    time.sleep(0.5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-menu"]//*[contains(text(), "Measure distance")]/ancestor::li'))).click()
    time.sleep(5)
    #distancebutton, = driver.find_elements_by_xpath('//*[@id="action-menu"]//*[contains(text(), "Measure distance")]/ancestor::li') # expecting a single element


    for coords in areacoords[1:]:
        action = ActionChains(driver)
        action.move_to_element_with_offset(body, coords[0], coords[1]).click().perform()
        time.sleep(2)

    #contextmenu = driver.get_element_by_id("action-menu")
    #distancebutton = contextmenu.find_elements_by_xpath('//*[@id="action-menu"]/child::*[contains(text(), "Measure distance")]')
    #distancebutton.click()
    
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
        driver.set_window_size(1024,768)

        # launch google maps
        time.sleep(2)
        driver.get('https://maps.google.co.uk')
        driver.get_screenshot_as_file('./step0-maps.png')

        # accept terms
        time.sleep(2)
        accept_terms(driver)
        driver.get_screenshot_as_file('./step1-t&c.png')

        # search for epping
        time.sleep(2)
        search_for_epping(driver)
        driver.get_screenshot_as_file('./step2-search.png')

        # pan the map
        time.sleep(2)
        #pan_and_zoom_in_kayboard(driver)
        pan_and_zoom_in(driver)
        driver.get_screenshot_as_file('./step3-panzoomin.png')

        # switch to aerial
        time.sleep(2)
        switch_to_aerial(driver)
        driver.get_screenshot_as_file('./step4-aerial.png')

        # click on the map
        time.sleep(2)
        click_on_map(driver)
        driver.get_screenshot_as_file('./step4-mapclick.png')

        # click on the map
        time.sleep(2)
        measure_area(driver)
        driver.get_screenshot_as_file('./step5-mapclick.png')

        time.sleep(10)
    
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