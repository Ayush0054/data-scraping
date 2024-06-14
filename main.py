import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_Data():
    base_url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    product_list = []
    page = 1

    while True:
        url = base_url + str(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debug: Print the response content to inspect the HTML structure
        with open(f'response_page_{page}.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        products = soup.find_all('div', class_='c-pwa-tile-grid-inner')
        
        # Debug: Print the number of products found
        print(f'Page {page}: Number of products found: {len(products)}')
        
        if not products:
            break
        
        for product in products:
            try:
                link_tag = product.find('a', class_='c-pwa-link')
                link = '' + link_tag['href'] if link_tag else 'N/A'
                
                title_tag = product.find('p', class_='o-pwa-product-tile__heading')
                title = title_tag.text.strip() if title_tag else 'N/A'
                
                price_tag = product.find('span', class_='c-pwa-product-price__current s-pwa-product-price__current' , attrs={"aria-label": True})
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                image_tag = product.find('img' , class_="o-pwa-image__img o-pwa-product-tile__media")
                image = image_tag['src'] if image_tag else 'N/A'
                
                product_list.append({
                    'Title': title,
                    'Price': price,
                    'Link': link,
                    'Image URL': image
                })
            except AttributeError:
                print('AttributeError:', product.prettify())
                continue
        
        page += 1

    df = pd.DataFrame(product_list)
    df.to_csv('file.csv', index=False)
    print('Scraping complete. Data saved to file.csv')

if __name__ == "__main__":
    scrape_Data()
