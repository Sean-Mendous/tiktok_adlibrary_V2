from bs4 import BeautifulSoup
import json
import time
from app.scraping.selenium_setting import open_url

TARGET_TAGS = ["h1", "h2", "h3", "h4", "p", "li", "a", "img"]

def extract_structured_content(html, target_tags=TARGET_TAGS):
    soup = BeautifulSoup(html, "html.parser")
    result = []

    for tag in target_tags:
        for element in soup.find_all(tag):
            if tag == "img":
                alt = element.get("alt", "").strip()
                if alt:
                    result.append({"tag": tag, "alt": alt})
            else:
                text = element.get_text(strip=True)
                if text:
                    result.append({"tag": tag, "text": text})
    
    return result

def merge_structured_data(structured_data):
    merged_data = {}
    for item in structured_data:
        tag = item["tag"]
        if not merged_data.get(tag):
            merged_data[tag] = []
        if item.get("text"):
            merged_data[tag].append(item["text"])
        else:
            continue
    return merged_data

def scrape_lp_and_extract(url):
    browser = open_url(url)
    time.sleep(3)
    html = browser.page_source
    browser.quit()
    structured_data = extract_structured_content(html)
    merged_data = merge_structured_data(structured_data)
    return merged_data


if __name__ == "__main__":
    url = "https://www.boniful.net/view/item/000000000018?utm_source=tiktok&utm_medium=paid&utm_id=__CAMPAIGN_ID__&utm_campaign=__CAMPAIGN_NAME__"
    content = scrape_lp_and_extract(url)

    # 出力を確認（LLMに渡せる形式）
    print(json.dumps(content, ensure_ascii=False, indent=2))

"""
python -m app.analysing.tag.website_tag
"""