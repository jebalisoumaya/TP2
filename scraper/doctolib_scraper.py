from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_doctolib(params):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("Script started...")
    driver.get("https://www.doctolib.fr/")
    print("Browser opened and navigated to Doctolib.")

    wait = WebDriverWait(driver, 40)

    # Enter the location
    place_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input"))
    )
    place_input.clear()
    place_input.send_keys(params.get("location", "75008"))

    # Enter the occupation/query
    query_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input"))
    )
    query_input.clear()
    query_input.send_keys(params.get("query", "dermatologue"))
    print("Query entered:", params.get("query", "dermatologue"))
    time.sleep(1)

    print("Location entered:", params.get("location", "75008"))

    wait.until(
        EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,
             "input.searchbar-input.searchbar-place-input"),
             params.get("location", "75008"))
    )
    query_input.send_keys(Keys.ENTER)
    place_input.send_keys(Keys.ENTER)

    try:
        # Wait for search results to load
        total_results = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[data-test='total-number-of-results']")
        ))
        print("Found results:", total_results.text)

        # Store search results URL to return to after visiting each doctor
        search_results_url = driver.current_url
        print(f"Search results URL: {search_results_url}")

        # Get all doctor cards/links from the search results page
        doctor_cards = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.dl-search-result, div.dl-card-content")
        ))

        print(f"Found {len(doctor_cards)} doctor cards to process")

        # Collect doctor URLs first to avoid stale element references
        doctor_urls = []
        for i, card in enumerate(doctor_cards[:10]):  # Limit to first 10 for testing
            try:
                link_element = card.find_element(By.CSS_SELECTOR, "a[href*='/']")
                doctor_url = link_element.get_attribute("href")
                if doctor_url:
                    doctor_urls.append((i, doctor_url))
            except Exception as e:
                print(f"Error getting URL for doctor card {i+1}: {e}")

        print(f"Collected {len(doctor_urls)} doctor URLs to visit")

        # Now process each doctor by visiting their page
        doctors = []
        for index, url in doctor_urls:
            try:
                print(f"Visiting doctor {index+1} at URL: {url}")
                driver.get(url)

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                time.sleep(2)

                doctor_info = {
                    "name": "Unknown",
                    "specialty": "Unknown",
                    "address": "Unknown",
                    "availability": "Unknown",
                    "phone": "Unknown",
                    "biography": "Unknown"
                }

                # Name
                try:
                    name_element = driver.find_element(By.CSS_SELECTOR, "h1.dl-profile-header-name, h1.dl-text")
                    doctor_info["name"] = name_element.text.strip()
                except:
                    try:
                        name_element = driver.find_element(By.CSS_SELECTOR, ".dl-profile-header-name")
                        doctor_info["name"] = name_element.text.strip()
                    except Exception as name_error:
                        print(f"Error extracting name: {name_error}")

                # Specialty
                try:
                    specialty_element = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-header-speciality")
                    doctor_info["specialty"] = specialty_element.text.strip()
                except Exception as specialty_error:
                    print(f"Error extracting specialty: {specialty_error}")

                # Address
                try:
                    address_element = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-text-address")
                    doctor_info["address"] = address_element.text.strip()
                except:
                    try:
                        address_element = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-practice-address")
                        doctor_info["address"] = address_element.text.strip()
                    except Exception as address_error:
                        print(f"Error extracting address: {address_error}")

                # Phone
                try:
                    phone_element = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-text-phone")
                    doctor_info["phone"] = phone_element.text.strip()
                except Exception as phone_error:
                    print(f"No phone number found or error: {phone_error}")

                # Biography
                try:
                    bio_element = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-text-bio")
                    doctor_info["biography"] = bio_element.text.strip()
                except Exception as bio_error:
                    print(f"No biography found or error: {bio_error}")

                # Availability
                try:
                    slot_element = driver.find_element(By.CSS_SELECTOR, "div.availabilities-slot")
                    doctor_info["availability"] = slot_element.text.strip()
                except:
                    try:
                        avail_element = driver.find_element(By.CSS_SELECTOR, "div.booking-availabilities")
                        doctor_info["availability"] = avail_element.text.strip()
                    except Exception as avail_error:
                        print(f"Error extracting availability: {avail_error}")

                doctors.append(doctor_info)
                print(f"Successfully scraped doctor {index+1}: {doctor_info['name']}")

                driver.get(search_results_url)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-test='total-number-of-results']")
                ))

            except Exception as visit_error:
                print(f"Error processing doctor {index+1}: {visit_error}")
                driver.get(search_results_url)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-test='total-number-of-results']")
                ))

        print(f"\nSuccessfully scraped {len(doctors)} doctors")
        return doctors

    except Exception as e:
        print("Error occurred during the scraping process:")
        print(e)
        return []

    finally:
        driver.quit()
