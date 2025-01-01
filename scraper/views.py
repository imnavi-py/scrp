import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse

def get_market_data(request):
    count = int(request.GET.get('count', 10)) 
    print(count)

    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver_path = r"C:\chromedriver-win64\chromedriver.exe"

    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    try:

        driver.get("******************************")

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        posts = driver.find_elements(By.CSS_SELECTOR, ".tag-page__posts-col li")

        data = []
        for post in posts[:count]:
            try:
                title = post.find_element(By.CLASS_NAME, "post-card-inline__title").text
                title_link = post.find_element(By.CLASS_NAME, "post-card-inline__title-link").get_attribute("href")
                text = post.find_element(By.CLASS_NAME, "post-card-inline__text").text

                image_element = WebDriverWait(post, count).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "lazy-image__img"))
                )
                image_url = image_element.get_attribute("src")
                

                data.append({
                    "title": title,
                    "title_link": title_link,
                    "text": text,
                    "image_url": image_url
                })
            except Exception as e:
                print(f"Error: {e}")

        information = {
            "scraped_count": len(data),
            "data": data
        }

        return JsonResponse(information)

    except Exception as e:

        return JsonResponse({"error": str(e)}, status=400)

    finally:

        driver.quit()
