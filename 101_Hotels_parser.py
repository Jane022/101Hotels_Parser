from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def collect_hotels_rates(city):
    driver = webdriver.Chrome()
    data = []
    page_num = 1

    while True:
        url = f'https://101hotels.com/main/cities/{city}?viewType=list&page={page_num}'
        driver.get(url)

        WebDriverWait(driver, 10, 1).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//li[@itemtype="https://schema.org/Hotel"]'))
        )

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('li', itemtype='https://schema.org/Hotel')

        if not entries:
            break

        for entry in entries:

            hotel_data = entry.find('div', class_='item-name')
            hotel_name = hotel_data.find('a').text

            rating_elem = entry.find('span', class_='d-block rating-value')
            hotel_rating = rating_elem.text.split('/')[0] if rating_elem else 'Нет рейтинга'

            price_elem = entry.find('span', class_='price-value price-highlight')
            minimal_price = price_elem.text.strip() if price_elem else 'Цена не указана'

            data.append({
                'hotel_name': hotel_name,
                'hotel_rating': hotel_rating,
                'minimal_price': minimal_price
            })

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.page-link.next'))
            )
            if 'disabled' in next_button.get_attribute('class'):
                break
            page_num += 1
        except:
            break



    driver.quit()
    print(f"Всего найдено: {len(data)} отелей")
    print(data)
    return data


hotel_rates = collect_hotels_rates('vladimir')
df = pd.DataFrame(hotel_rates)

df.to_excel('hotel_rates.xlsx')
