import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

driver = webdriver.Chrome()
web_page_url = "https://stockanalysis.com/stocks/"
driver.get(web_page_url)
driver.maximize_window()

# close the subscription popup if shown
# popup_button_xpath = "/html/body/div/div[2]/div/button/svg"
popup_button_selector = "button[aria-label='Close']"
try:
    # Wait for the popup button to be clickable
    popup_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, popup_button_selector))
    )
    popup_button.click()
    print("Popup closed successfully.")
except TimeoutException:
    print("Popup button did not become clickable in time.")
except NoSuchElementException:
    print("Popup button not found on the page.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


def scrap_data(num_pages):
    """Function to extract the data from the main table"""
    counter = 1
    # table id
    table_xpath = '//*[@id="main-table-wrap"]'
    table = driver.find_element(By.XPATH, table_xpath)

    # list to hold the data
    table_data = []

    while counter <= num_pages:
        # rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            # all columns in the current row
            cols = row.find_elements(By.TAG_NAME, "td")

            # create dictionary for current row and change the column name
            row_data = {}
            for i, col in enumerate(cols):
                if i == 0:
                    row_data[f"ticker"] = col.text
                elif i == 1:
                    row_data["company_name"] = col.text
                elif i == 2:
                    row_data["investment_type"] = col.text
                elif i == 3:
                    row_data["investment_amount"] = col.text

            # append row data to table data list
            table_data.append(row_data)

        # click to the next page
        next_page_xpath = '//*[@id="main"]/div/div/nav/button[2]/span'
        next_page_button = driver.find_element(By.XPATH, next_page_xpath)
        next_page_button.click()

        # increment counter
        counter += 1

    # write the data to the json file
    with open("stock_tickers_data.json", "w") as json_file:
        json.dump(table_data, json_file, indent=4)


# define the number of loops the program will perform
number_pages_xpath = '//*[@id="main"]/div/div/nav/div/span'
number_pages = driver.find_element(By.XPATH, number_pages_xpath)
pages_text = number_pages.text
number_pages_total = int(pages_text[-2:])
total_clicks_next = number_pages_total - 1

# call the scrap_Data function
scrap_data(total_clicks_next)
