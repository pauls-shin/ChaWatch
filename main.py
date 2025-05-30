import requests
from bs4 import BeautifulSoup

# List of product URLs to check for stock status
PRODUCT_SOURCES = {
    # Marukyu Koyamaen product URLs
    "marukyu": [
    # Principal products
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1g36020c1",           # Kiwami Choan
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1",           # Unkaku
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1",           # Wako
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1111020c1",           # Tenju
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1121020c1",           # Choan
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1131020c1",           # Eiju
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1151020c1",           # Kinrin
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1171020c1",           # Yugen
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1181040c1",           # Chigi no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1",           # Isuzu
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1",           # Aorashi

    # Kancho products
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1134040c1",           # Daitokuji Temple Favored Matcha Itteikisui (GOLD)
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11a4040c1",           # Daitokuji Temple Favored Matcha Itteikisui
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1174040c1",           # Shokokuji Temple Favored Matcha Mannen no Midori
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1184040c1",           # Shokokuji Temple Favored Matcha Joko

    # Tea School products
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1152020c1",           # Urasenke School Favored Matcha Shoun no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1f62020c1-1f62200c1", # Yabunouchi School Iemoto Favored Matcha Yoyo no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1f52020c1-1f52200c1", # Yabunouchi School Iemoto Favored Matcha Hekiun no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1172020c1",           # Urasenke School Favored Matcha Shoka no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1182020c1",           # Urasenke School Favored Matcha Seijo no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1112020c1",           # Urasenke School Favored Matcha Keichi no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1132020c1",           # Urasenke School Favored Matcha Tama no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1122020c1",           # Urasenke School Favored Matcha Kiu
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1142020c1",           # Urasenke School Favored Matcha Shohaku
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1192020c1-1192040c1", # Omotesenke School Favored Matcha Myofu no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11a2020c1-11a2040c1", # Omotesenke School Favored Matcha Saiun
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11b2040c1",           # Omotesenke School Favored Matcha Sanyu no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11c2020c1-11c2040c1", # Omotesenke School Favored Matcha Kissho
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1f68020c1-1f68100c6", # Omotesenke School Yuyusai Iemoto Favored Matcha Saiho no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1f78020c1-1f78100c6", # Omotesenke School Yuyusai Iemoto Favored Matcha Yukyu no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1114020c1-1114040c1", # Mushakojisenke School Favored Matcha Suisho no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1124020c1-1124040c1", # Mushakojisenke School Favored Matcha Shofu
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1144020c1-1144040c1", # Yabunouchi School Favored Matcha Seiwa no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1154020c1-1154040c1", # Yabunouchi School Favored Matcha Ao no Mori
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1143020c1-1143200c1", # Enshuryu School Favored Matcha Ichigen no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1153020c1-1153040c1", # Enshuryu School Favored Matcha Hatsu no Mori
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1183040c1-1183200c1", # Sohenryu School Favored Matcha Kokonoe no Mukashi
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11c3020c1",           # Sohenryu School Favored Matcha Miya no Shiro
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1d23040c1",           # Sohenryu School Favored Matcha Tomo no Shiro

    # Syokuhin products
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/11b1100c1",           # Wakatake
    "https://www.marukyu-koyamaen.co.jp/english/shop/products/1262040c1",            # Cooking Matcha (in a sifter can) – Excellent

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
        "user4": ["marukyu"],
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
# if __name__ == "__main__":
#     lambda_handler()



# LEFT OFF ON: 
# Finish main.py logic	    -- Get scraping + subscriptions solid & testable
# Then add DB storage	    -- So users can manage alerts dynamically
# Final: Alert integration	-- Hook in Discord/SMS based on main.py results
