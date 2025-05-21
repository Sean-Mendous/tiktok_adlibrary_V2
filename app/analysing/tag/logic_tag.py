import json
from app.analysing.tag.website_tag import scrape_lp_and_extract
from app.analysing.chatgpt_setting import chatgpt_4omini
from app.db.supabase_setting import insert_to_supabase, spabase_supabase
from utilities.logger import logger

def run_flow(url):
    try:
        content = scrape_lp_and_extract(url)
        content_json = json.dumps(content, ensure_ascii=False, indent=2)
        logger.info(f'Successfully scraped lp and extracted')
    except Exception as e:
        raise RuntimeError(f'Failed to scrape lp and extract: {e}') from e

    try:
        prompt = open("app/analysing/tag/prompt_tag.md", "r").read()
        overall_prompt = (f'{prompt}\n\n## ページの内容\n{content_json}')
        response = chatgpt_4omini(overall_prompt)
        response_dict = json.loads(response)
        logger.info(f'Successfully got response')
    except Exception as e:
        raise RuntimeError(f'Failed to get response: {e}') from e

    def convert_keys_to_db(response):
        return {
            "tag_product_big_category": response["big_genre_product"],
            "tag_product_small_category": response["small_genre_product"],
            "tag_product_details": response["detail_product"],
            "tag_target_age": response["age_target"],
            "tag_target_gender": response["gender_target"],
            "system_status": "tag_analysing"
        }
    
    try:
        converted_response_dict = convert_keys_to_db(response_dict)
        logger.info(f'Successfully converted keys')
    except Exception as e:
        raise RuntimeError(f'Failed to convert keys: {e}') from e

    return converted_response_dict


if __name__ == "__main__":
    url = "https://www.boniful.net/view/item/000000000018?utm_source=tiktok&utm_medium=paid&utm_id=__CAMPAIGN_ID__&utm_campaign=__CAMPAIGN_NAME__"
    response_json = run_flow(url)
    print(response_json)

"""
python -m app.analysing.tag.logic_tag
"""



