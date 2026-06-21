import pandas as pd
from browser import web_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

excel_path = r""

driver = web_driver()
iterator = 1
try:
    original_data = pd.read_excel(excel_path)
    links_data = []

    for index, row in original_data.iterrows():
        if len(links_data) >= 100:
            pd.DataFrame(links_data).to_excel(f"scraped links {iterator}.xlsx", index=False)
            print(f"{iterator} batch of data saved successfully.")
            iterator = iterator + 1
            links_data = []

        link = row["Links"]

        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            extracted_images = []
            images = driver.find_elements(By.XPATH, "//img")

            for image in images:
                src = (image.get_attribute("srcset") or image.get_attribute("src") or image.get_attribute("data-src") or image.get_attribute("data-lazy-src"))

                if src and src.startswith(('http', '//')):
                    if 'srcset' in str(src):
                        src = src.split(',')[0].split(' ')[0]

                    if src not in extracted_images:
                        extracted_images.append(src)

            try:
                body = driver.find_element(By.XPATH, "//body")
                all_text = body.text.strip()

                cleaned_text = ' '.join(all_text.split())

            except Exception as text_error:
                print(f"Error extracting text: {text_error}")
                cleaned_text = ""

            if cleaned_text and extracted_images:
                links_data.append({
                    "Website": row["Website"],
                    "Links": link,
                    "Status": "Scraped Successfully",
                    "Images": str(extracted_images),
                    "Text": cleaned_text
                })
                print(f"Successfully extracted {len(extracted_images)} images and text")

            elif extracted_images and not cleaned_text:
                links_data.append({
                    "Website": row["Website"],
                    "Links": link,
                    "Status": "Images Only",
                    "Images": str(extracted_images),
                    "Text": ""
                })
                print(f"Extracted {len(extracted_images)} images, no text")

            elif cleaned_text and not extracted_images:
                links_data.append({
                    "Website": row["Website"],
                    "Links": link,
                    "Status": "Text Only",
                    "Images": "",
                    "Text": cleaned_text
                })
                print(f"Extracted text, no images")

            else:
                links_data.append({
                    "Website": row["Website"],
                    "Links": link,
                    "Status": "No Data Found",
                    "Images": "",
                    "Text": ""
                })
                print("No data extracted")

            time.sleep(1)

        except TimeoutException:
            error_msg = "Page load timeout"
            links_data.append({
                "Website": row["Website"],
                "Links": link,
                "Status": f"Error: {error_msg}",
                "Images": "",
                "Text": ""
            })
            print(f"{error_msg}")

            time.sleep(1)

        except WebDriverException as e:
            error_msg = f"WebDriver error: {str(e)[:100]}"
            links_data.append({
                "Website": row["Website"],
                "Links": link,
                "Status": f"Error: {error_msg}",
                "Images": "",
                "Text": ""
            })
            print(f"{error_msg}")

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)[:100]}"
            links_data.append({
                "Website": row["Website"],
                "Links": link,
                "Status": f"Error: {error_msg}",
                "Images": "",
                "Text": ""
            })
            print(f"{error_msg}")

    if links_data:
        pd.DataFrame(links_data).to_excel(f"scraped links {iterator}.xlsx", index=False)
        print(f"Final data saved successfully.")
    else:
        print(f"No data to save for last links.")

finally:
    driver.quit()
    print("\nDriver closed successfully.")
