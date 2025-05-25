# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'body': 'ChaWatch is deployed!'
#     }
import requests
from bs4 import BeautifulSoup

# Define product pages to check on the Marukyu Koyamaen website
PRODUCT_URLS = [
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/principal",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/kancho?viewall=1",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/tea-schools?viewall=1",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/syokuhin"

]

def lambda_handler(event, context):
    for url in PRODUCT_URLS:
        try:
            print(f"Checking: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Check for any "instock" class element
            instock_items = soup.find_all("li", class_="product-type-variable")
            found_in_stock = False

            for item in instock_items:
                class_list = item.get("class", [])
                if "instock" in class_list:
                    print(f"🟢 In Stock: {url} -> {item.get('id')}")
                    found_in_stock = True

            if not found_in_stock:
                print(f"🔴 Out of Stock: {url}")

        except requests.RequestException as e:
            print(f"❌ Error checking {url}: {e}")
    

# LEFT OFF ON: 
# - Final Step: Under "Main -- Project Development" -> Automate with CloudWatch (Run Every 2-3 minutes)
#
#
#