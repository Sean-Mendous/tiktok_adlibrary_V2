import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import re
from utilities.logger import logger
from app.scraping.list.scrape_list import get_html
from app.scraping.list.extract_list import extract_list
from app.db.supabase_setting import insert_to_supabase

cookie_path = "app/scraping/cookies.json"

def run_flow(url, condition, cookie_path=cookie_path):
    input_url = url
    
    try:
        html = get_html(input_url, cookie_path)
        if not html:
            raise RuntimeError(f'Failed to get html')
        logger.info(f'Successfully got html')
    except Exception as e:
        raise RuntimeError(f'Failed to get html: {e}') from e
        
    try:
        url_list = extract_list(html)
        if not url_list:
            raise RuntimeError(f'Failed to extract urls')
        logger.info(f'Successfully extracted "{len(url_list)}" urls')
    except Exception as e:
        raise RuntimeError(f'Failed to extract urls: {e}') from e
        
    datas = []
    for url in url_list:
        try:
            match = re.search(r'/topads/(\d+)', url)
            if match:
                system_id = match.group(1)
            else:
                continue
        except Exception as e:
            raise RuntimeError(f'Failed to extract system_id from {url}: {e}') from e
        
        data = {
            "system_id": system_id,
            "system_status": "list_scraping",
            "search_url": url,
            "search_condition": condition
        }

        datas.append(data)
    
    return datas

def to_db(dict_list, table_name="V2_format"):
    logger.info(f'Start to insert data to supabase: {len(dict_list)} urls')

    for dict_dict in dict_list:
        url = dict_dict['url']
        condition = dict_dict['condition']
        datas = run_flow(url, condition)
        insert_to_supabase(datas, table_name)
        logger.info(f'Successfully inserted data to supabase: {len(datas)} datas')

    logger.info(f'Successfully inserted data to supabase: {len(dict_list)} urls')

if __name__ == "__main__":
    url_list = [
        {
            'url': 'https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/ja?period=180&region=JP&industry=14&object=3',
            'condition': 'skincare + CVR + Japan'
        }
    ]
    to_db(url_list)

"""
python -m app.scraping.list.logic_list
"""