import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_reaction_time():
    service = Service("C:\Program Files (x86)\Google\Chrome\Application\132.0.6834.84")
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://www.human-benchmark.org/reaction-time-test")
        
        # 1) Click the start area
        start_area = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "buttClick"))
        )
        start_area.click()
        print("Clicked the start area!")
        
        # 2) Wait for the page to show the red box, then turn green
        slight_div = driver.find_element(By.ID, "slight")  # The red box area
        print("Waiting for green color...")
        
        WebDriverWait(driver, 10).until(
            lambda d: "green" in slight_div.get_attribute("style").lower()
        )
        
        # 3) Click again when it's green
        slight_div.click()
        print("Clicked on green!")
        
        time.sleep(5)  # Pause to observe outcome

    finally:
        driver.quit()

if __name__ == "__main__":
    test_reaction_time()
