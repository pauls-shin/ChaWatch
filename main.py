import requests
from bs4 import BeautifulSoup

# List of product URLs to check for stock status
PRODUCT_SOURCES = {
    # Marukyu Koyamaen product URLs
    "marukyu": [
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/principal",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/kancho?viewall=1",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/tea-schools?viewall=1",
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/catalog/matcha/syokuhin",
    # "https://www.marukyu-koyamaen.co.jp/english/shop/products/1g28200c6" # Added for "IN STOCK" check
    ],

    # Ippodo Tea product URLs
    "ippodotea": [
    "https://ippodotea.com/collections/matcha/products/ummon-no-mukashi-40g",
    "https://ippodotea.com/collections/matcha/products/sayaka-100g",
    "https://ippodotea.com/collections/matcha/products/sayaka-no-mukashi",
    "https://ippodotea.com/collections/matcha/products/ikuyo-100",
    "https://ippodotea.com/collections/matcha/products/ikuyo",
    "https://ippodotea.com/collections/matcha/products/wakaki-shiro",
    # "https://ippodotea.com/collections/matcha/products/uji-shimizu", # Added for "IN STOCK" check
    # "https://ippodotea.com/collections/matcha/products/uji-shimizu-sticks" # Added for "IN STOCK" check
    ],

    # Rocky's Matcha product URLs
    "rockysmatcha": [
    "https://www.rockysmatcha.com/products/rockys-matcha-ceremonial-blend-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-osada-ceremonial-blend-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-tsujiki-blend-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-yamabuki-100g",
    "https://www.rockysmatcha.com/products/rockys-matcha-uji-premium-blend-matcha-100g",
    "https://www.rockysmatcha.com/products/rockys-matcha-shirakawa-ceremonial-blend-matcha-100g",
    "https://www.rockysmatcha.com/products/rockys-matcha-ceremonial-blend-matcha-100g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-koshun-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-asahi-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-gokou-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-narino-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-uji-hikari-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-for-awake-ny-single-cultivar-samidori-matcha-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-saeakari-matcha-20g",
    "https://www.rockysmatcha.com/products/rocky-s-matcha-organic-sugimoto-single-cultivar-okumidori-20g",
    "https://www.rockysmatcha.com/products/rockys-matcha-organic-tsujiki-blend-matcha-20g",
    "https://www.rockysmatcha.com/products/rocky-s-matcha-for-saie-ceremonial-blend-matcha-20g",
    # "https://www.rockysmatcha.com/products/rockys-matcha-single-cultivar-okumidori-matcha-20g", # Added for "IN STOCK" check 
    # "https://www.rockysmatcha.com/products/rockys-matcha-essential-tea-kit" # Added for "IN STOCK" check
    ]
}

def check_marukyu(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("li", class_="product-type-variable")
        for product in products:
            if "instock" in product.get("class", []):
                print(f"🟢 [Marukyu] In Stock: {url} → {product.get('id')}")
                return True
        print(f"🔴 [Marukyu] Out of Stock: {url}")
    except Exception as e:
        print(f"❌ Error checking Marukyu URL: {url} | {e}")

def check_ippodotea(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Check for "Sold out" inside <a class="product-addbtn">
        sold_out_tag = soup.select_one("a.product-addbtn .product-stock-status")
        if sold_out_tag and "sold out" in sold_out_tag.get_text(strip=True).lower():
            print(f"🔴 [Ippodo] Out of Stock: {url}")
            return False

        # Check for "Add to bag" inside <button class="product-addbtn">
        add_to_bag_tag = soup.select_one("button.product-addbtn .product-stock-status")
        if add_to_bag_tag and "add to bag" in add_to_bag_tag.get_text(strip=True).lower():
            print(f"🟢 [Ippodo] In Stock: {url}")
            return True

        # Fallback: No recognized tag
        print(f"🟢 [Ippodo] Soft Confirmation — assuming In Stock: {url}")
        return False

    except Exception as e:
        print(f"❌ Error checking IppodoTea URL: {url} | {e}")
        return False

def check_rockysmatcha(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        button = soup.find("button", {"name": "add"})
        if button:
            text = button.get_text(strip=True).lower()
            if "add to cart" in text:
                print(f"🟢 [RockysMatcha] In Stock: {url}")
                return True
        print(f"🔴 [RockysMatcha] Out of Stock: {url}")
    except Exception as e:
        print(f"❌ Error checking Rocky's Matcha URL: {url} | {e}")

def lambda_handler(event=None, context=None):
    user_subscriptions = {
        # "user1": ["marukyu", "ippodotea"],
        # "user2": ["rockysmatcha"],
        # "user3": ["marukyu", "ippodotea", "rockysmatcha"]
        "user4": ["ippodotea"],
    }

    for user, subscriptions in user_subscriptions.items():
        print(f"\n🔔 Checking for {user}")
        for site in subscriptions:
            for url in PRODUCT_SOURCES.get(site, []):
                if site == "marukyu":
                    check_marukyu(url)
                elif site == "ippodotea":
                    check_ippodotea(url)
                elif site == "rockysmatcha":
                    check_rockysmatcha(url)
    

# COMMENT OUT WHEN USING LAMBDA 
# HERE FOR LOCAL TESTING
if __name__ == "__main__":
    lambda_handler()



# LEFT OFF ON: 
# Finish main.py logic	    -- Get scraping + subscriptions solid & testable
# Then add DB storage	    -- So users can manage alerts dynamically
# Final: Alert integration	-- Hook in Discord/SMS based on main.py results
