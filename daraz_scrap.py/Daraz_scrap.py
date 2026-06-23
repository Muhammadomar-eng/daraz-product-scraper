import time
import pandas as pd
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.daraz.lk/",
}

BASE_URL = "https://www.daraz.lk/catalog/?ajax=true&isFirstRequest=true&page={page}&q=I%20phone%20cover&spm=a2a0e.tm80335410.search.d_go"

def scrape_daraz(pages=5):
    products = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        response = requests.get(BASE_URL.format(page=page), headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status: {response.status_code}")
            continue

        data = response.json()
        items = data.get("mods", {}).get("listItems", [])

        if not items:
            print("No more products found.")
            break

        for item in items:
            products.append({
                "Product Name": item.get("name"),
                "Price (LKR)":  item.get("price"),
                "Brand":        item.get("brandName", "No Brand"),
                "Rating":       item.get("ratingScore", "No Rating"),
            })

        time.sleep(1)

    return products


if __name__ == "__main__":
    products = scrape_daraz(pages=5)
    df = pd.DataFrame(products)
    df.to_csv("daraz_iphone_covers.csv", index=False, encoding="utf-8-sig")
    print(f"Done! {len(products)} products saved.")