import csv
import requests
from bs4 import BeautifulSoup

# Step 1: Scrape product data from multiple pages
def scrape_products(max_products=30):
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    products = []
    page = 1

    while len(products) < max_products:
        response = requests.get(base_url.format(page))
        if response.status_code != 200:
            break  # Stop if we run out of pages

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.product_pod')

        for item in items:
            if len(products) >= max_products:
                break

            name = item.h3.a['title']
            price = item.select_one('.price_color').text.strip().replace("£", "$")
            rating = item.p['class'][1]  # e.g., "One", "Two", etc.

            products.append({
                "Name": name,
                "Price": price,
                "Rating": rating
            })

        page += 1

    return products

# Step 2: Save to CSV
def save_to_csv(products, filename='products_30.csv'):
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Price", "Rating"])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# Step 3: Run the script
if __name__ == "__main__":
    product_data = scrape_products(30)
    save_to_csv(product_data)
    print(f"Saved {len(product_data)} products to 'products_30.csv'")

