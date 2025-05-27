import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from utilities.google_spreadsheet import *
from utilities.save_file import *
from utilities.logger import logger
from app.scraping.indivisual.scrape_indivisual import get_htmls
from app.scraping.indivisual.extract_indivisual import extract_indivisual
from app.db.supabase_setting import insert_to_supabase, spabase_supabase

cookie_path = "app/scraping/cookies.json"

def run_flow(url, cookie_path=cookie_path):
    try:
        htmls = get_htmls(url, cookie_path)
        if not htmls:
            raise RuntimeError(f'Failed to get html')
        logger.info(f'Successfully got html')
    except Exception as e:
        raise RuntimeError(f'Failed to get html: {e}') from e

    try:
        output_data = extract_indivisual(htmls)
        if not output_data:
            raise RuntimeError(f'Failed to extract data')
        logger.info(f'Successfully extracted data')
    except Exception as e:
        raise RuntimeError(f'Failed to extract data: {e}') from e
    
    def convert_keys(output_data):
        converted_data = {}
        
        converted_data["scraping_brand"] = output_data["about_brand"]
        converted_data["scraping_industry"] = output_data["about_industry"]
        converted_data["scraping_caption"] = output_data["about_caption"]
        converted_data["scraping_landingpage"] = output_data["about_landingpage"]

        converted_data["scraping_likes"] = output_data["data_likes"]
        converted_data["scraping_comments"] = output_data["data_comments"]
        converted_data["scraping_shares"] = output_data["data_shares"]
        converted_data["scraping_ctr"] = output_data["data_ctr"]
        converted_data["scraping_budget"] = output_data["data_budget"]

        converted_data["scraping_ctr_top"] = output_data["time_ctr_top"]
        converted_data["scraping_ctr_sec"] = output_data["time_ctr_sec"]
        converted_data["scraping_cvr_top"] = output_data["time_cvr_top"]
        converted_data["scraping_cvr_sec"] = output_data["time_cvr_sec"]

        converted_data["system_status"] = "indivisual_scraping"

        return converted_data
    
    try:
        converted_data = convert_keys(output_data)
        logger.info(f'Successfully converted data')
    except Exception as e:
        raise RuntimeError(f'Failed to convert data: {e}') from e
    
    return converted_data

def to_db(table_name="V2_format", amount=10000):
    supabase = spabase_supabase()
    rows = supabase.table(table_name).select("*").eq("system_status", "list_scraping").execute().data
    logger.info(f'Successfully got rows: {len(rows)}')

    for i, row in enumerate(rows, start=1):
        if i < amount:
            logger.info(f'{i}/{len(rows)}: Start to run flow')
            url = row["search_url"]
            id = row["system_id"]

            data = run_flow(url)

            status = "indivisual_scraping"
            data["system_status"] = status
            logger.info(f'Successfully extracted data:\n{data}')
            supabase.table(table_name).update(data).eq("system_id", id).execute()
            logger.info(f'{i+1}/{len(rows)}: Successfully ran flow')
        else:
            logger.info(f'Finished all rows')
            break
    
    logger.info(f'Successfully ran flow for all rows')

if __name__ == "__main__":
    to_db(amount=5)

"""
python -m app.scraping.indivisual.logic_indivisual
"""
