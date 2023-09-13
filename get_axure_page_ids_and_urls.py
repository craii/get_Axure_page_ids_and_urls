from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep

# open your axure file, preview it and copy any url of it from opened Chrome tab, then paste it here
start_page = "http://127.0.0.1:32768/start.html#"

driver = webdriver.Chrome()
driver.get(start_page)
links = driver.find_elements(By.CSS_SELECTOR, "a.sitemapPageLink")

all_page_name = [link.get_attribute("nodeurl").rstrip(".html") for link in links]
# print(all_page_name)

re_page = [start_page + "p=" + name for name in all_page_name]
# print(re_page)

redirect_page = list()
for page_name in re_page:
    sleep(0.2)
    driver.get(page_name)
    redirect_page.append(driver.current_url)
print(redirect_page)

# # dirty work below, you may use re instead
ids_and_urls = list()
for page in redirect_page:
    # print(page)
    try:
        id_part = [part[part.index("=")+1:] for part in page.split("&") if "id=" in part][0]
        ids_and_urls.append((id_part, page))
    except IndexError:
        ids_and_urls.append(("Missing", page))
# print(ids_and_urls)
driver.quit()

data = dict(url=None, id=None)
urls = [url for id, url in ids_and_urls]
ids = [id for id, url in ids_and_urls]

data["url"] = urls
data["id"] = ids
df = pd.DataFrame(data)
df.to_csv("Axure_pages_and_ids.csv")
