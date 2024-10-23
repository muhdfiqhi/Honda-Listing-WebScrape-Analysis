from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time

# For Chrome
driver = webdriver.Chrome()

# Set the maximum number of pages to scrape
max_pages = 50  
unique_links = set()
car_data = []

# Step 1: Collect Car Listing Links
for page_num in range(1, max_pages + 1):
    url = f"https://www.mudah.my/malaysia/cars-for-sale/honda?o={page_num}"
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Collect unique links
    data = soup.find_all('a', href=True)
    for link in data:
        href = link['href']
        if href.endswith('.htm') and "security" not in href:
            unique_links.add(href)
    print(f"Page {page_num}: Collected {len(unique_links)} unique links so far.")

# Step 2: Scrape Car Information
for unique_link in unique_links:
    driver.get(unique_link)
    time.sleep(3)

    # Try to click the "SHOW MORE" button
    try:
        show_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'SHOW MORE')]")
        actions = ActionChains(driver)
        actions.move_to_element(show_more_button).perform()  # Scroll to the button
        show_more_button.click()
        time.sleep(2)
    except:
        pass  

    # Scrape data using your previous logic
    try:
        title = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
    except:
        title = 'N/A'

    try:
        price = driver.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute('content')
    except:
        price = 'N/A'

    try: 
        loc = driver.find_elements(By.XPATH, "//div[contains(@class, 'font-bold') and contains(@class, 'truncate')]")
        if len(loc) >= 4:
            location = loc[3].text  # Access the 4th element (index 3)
        elif len(loc) == 3:
            location = loc[2].text    
        else:
            location = 'N/A'
        location = location.split('-')[0].strip()
    except:
        location = 'N/A'

    try: 
        mile = driver.find_elements(By.XPATH, "//div[contains(@class, 'font-bold') and contains(@class, 'truncate')]")
        if len(mile) >= 4:
            mileage = mile[2].text 
        elif len(mile) == 3:
            mileage = mile[1].text    
        else:
            mileage = 'N/A'
    except:
        mileage = 'N/A'

    try: 
        trans = driver.find_elements(By.XPATH, "//div[contains(@class, 'font-bold') and contains(@class, 'truncate')]")
        if len(trans) >= 4:
            transmission = trans[1].text  
        elif len(trans) == 3:
            transmission = trans[0].text    
        else:
            transmission = 'N/A'
    except:
        transmission = 'N/A'

    try:
        year = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[3]"))
        ).text
    except:
        year = 'N/A'

    try:
        model = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[2]"))
        ).text
    except:
        model = 'N/A'

    try:
        type = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[7]"))
        ).text
    except:
        type = 'N/A'

    try:
        cc = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[11]"))
        ).text
        cc = float(cc)
        cc = round(cc / 1000, 1)
    except:
        cc = 'N/A'

    try:
        origin = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[10]"))
        ).text
    except:
        origin = 'N/A'
    try:
        variant = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='text-sm flex-1'])[4]"))
        ).text
    except:
        variant = 'N/A'

    car_data.append({
        "Title": title,
        "Model": model,
        "Type": type,
        "Year": year,
        "Mileage": mileage,
        "Transmission": transmission,
        "Location": location,
        "CC": cc,
        "Variant": variant,
        "Price": price,
        "Origin": origin
    })

# Save data to CSV
df = pd.DataFrame(car_data)
df.to_csv('car_data.csv', index=False)

driver.quit()
