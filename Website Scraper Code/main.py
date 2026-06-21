import re
import time
from browser import web_driver
from selenium.webdriver.common.by import By
from productPatterns import product_patterns, category_patterns, avoid_patterns
from websites import websites
import pandas as pd

driver = web_driver()

def extractProductLinks(categoryLinks, website, start_time, duration):
    """Extract product links from given category links."""
    productLinks = []
    for category in categoryLinks:
        if not category or time.time() - start_time >= duration:
            break
        try:
            driver.get(category)
            allLinks = [a.get_attribute("href") for a in driver.find_elements(By.XPATH, "//a[@href]")]
            for link in allLinks:
                if not link or time.time() - start_time >= duration:
                    break
                for pat in product_patterns:
                    if re.search(pat, link, re.IGNORECASE):
                        productLinks.append({'url': link, 'pattern': pat, 'website': website})
                        break
        except Exception as e:
            print(f"Error on {category}: {e}")
            continue
    return productLinks

def randomSearch(allLinks, website, start_time, duration):
    """Randomly search links for product pages."""
    collected = []
    for link in allLinks:
        if not link or time.time() - start_time >= duration:
            break
        try:
            driver.get(link)
            pageLinks = [a.get_attribute("href") for a in driver.find_elements(By.XPATH, "//a[@href]")]
            collected.extend(extractProductLinks(pageLinks, website, start_time, duration))
        except Exception as e:
            print(f"Random search error: {e}")
            continue
    return collected

def getCategoryPages(allLinks, website, start_time, duration):
    """Find category pages and extract product links."""
    if time.time() - start_time >= duration:
        return []
    categoryPages = []
    for link in allLinks:
        if not link or time.time() - start_time >= duration:
            break
        for pat in category_patterns:
            try:
                if re.search(pat, link, re.IGNORECASE):
                    categoryPages.append(link)
                    break
            except Exception as regex_error:
                print(f"Category regex error {pat}: {regex_error}")
        if len(categoryPages) >= 10:
            break
    if categoryPages:
        return extractProductLinks(categoryPages, website, start_time, duration)
    direct = extractProductLinks(allLinks, website, start_time, duration)
    if direct:
        return direct
    return randomSearch(allLinks, website, start_time, duration)

def process_website(website):
    """Process a single website to extract product links."""
    start_time = time.time()
    duration = 300
    try:
        driver.get(website)
        print(f"\nLanded on {website}")
        time.sleep(2)
        allLinks = []
        for a in driver.find_elements(By.XPATH, "//a[@href]"):
            link = a.get_attribute("href")
            if link and not any(re.search(pat, link, re.IGNORECASE) for pat in avoid_patterns):
                allLinks.append(link)
        print(f"Found {len(allLinks)} links")
    except Exception as e:
        print(f"Could not open {website} or error gathering links: {e}")
        return
    products = getCategoryPages(allLinks, website, start_time, duration)
    print(f"Extracted {len(products)} product links")
    if len(products) > 5:
        df = pd.DataFrame(products)
        safe_name = website.replace("https://", "").replace("http://", "").replace("/", "_")
        df.to_csv(f"{safe_name}_product_links.csv", index=False)
        print(f"Saved {len(products)} links to {safe_name}_product_links.csv")

if __name__ == "__main__":
    for site in websites:
        process_website(site)
    driver.quit()
