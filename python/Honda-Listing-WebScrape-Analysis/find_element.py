# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# # Initialize the Chrome WebDriver
# driver = webdriver.Chrome()

# # Open the URL
# driver.get('https://www.mudah.my/2017-honda-accord-2-0-vti-l-facelift-a-108654972.htm')

# time.sleep(5)  # Wait for the page to load

# # Find all elements using XPath that contain the text we're interested in
# elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'font-bold') and contains(@class, 'truncate')]")
# a1 = driver.find_element(By.XPATH, "//div[contains(@class, 'font-bold') and contains(@class, 'truncate')[4]]").text
# print(a1) 

# # Loop through each element and print the text along with its index
# for index, element in enumerate(elements):
#     print(f"Element {index + 1}: {element.text}")

# # Close the WebDriver
# driver.quit()



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get('https://www.mudah.my/2017-honda-accord-2-0-vti-l-facelift-a-108654972.htm')

time.sleep(5)  # Wait for the page to load

show_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'SHOW MORE')]")
    
    # Scroll to the element if necessary (some buttons are only clickable when visible on the screen)
actions = ActionChains(driver)
actions.move_to_element(show_more_button).perform()

    # Click the button
show_more_button.click()
time.sleep(2)

# Find all elements using XPath that contain the text we're interested in
elements = driver.find_elements(By.XPATH, "(//div[@class='text-sm flex-1'])")



# Loop through each element and print the text along with its index
for index, element in enumerate(elements):
    print(f"Element {index + 1}: {element.text}")

# Close the WebDriver
driver.quit()
