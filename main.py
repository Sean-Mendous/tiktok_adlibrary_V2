import argparse
import json
import os
import sys
import traceback
from app.db.supabase_setting import select_from_supabase, insert_to_supabase, spabase_supabase
from utilities.logger import logger

logger.info("🏃‍♀️🏃‍♀️ Starting main execution 🏃‍♀️🏃‍♀️")

search_feild = [
    {
        'url': 'https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/ja?period=180&region=JP&industry=14&object=3',
        'condition': 'スキンケア'
    }
]

table_name = "V2_format"

system_num = 4
"""
1: list scraping
2: indivisual scraping
3: video research
4: indivisual scraping + video research
"""
system_num = int(system_num)

logger.info("Running system")
if system_num == 1:
    try:
        supabase = spabase_supabase()
        for feild in search_feild:
            url = feild["url"]
            condition = feild["condition"]

            from app.scraping.list.logic_list import run_flow
            output = run_flow(url, condition)

            supabase.table(table_name).upsert(output).execute()
            logger.info(f"Successfully inserted: {url}")
    except Exception as e:
        logger.critical(f"🔴 {e}")
        traceback.print_exc()
        sys.exit(2)

elif system_num == 2:
    try:
        dict_list = select_from_supabase(table_name, "system_status", "list_scraping")
        supabase = spabase_supabase()
        for dict_dict in dict_list:
            try:
                id = dict_dict["system_id"]
                url = dict_dict["search_url"]

                from app.scraping.indivisual.logic_indivisual import run_flow
                output = run_flow(url)

                supabase.table(table_name).update(output).eq("system_id", id).execute()
                logger.info(f"Successfully updated: {id}")
            except Exception as e:
                logger.critical(f"🔴 {e}")
                traceback.print_exc()
                sys.exit(2)
    except Exception as e:
        logger.critical(f"🔴 {e}")
        traceback.print_exc()
        sys.exit(2)

elif system_num == 3:
    try:
        dict_list = select_from_supabase(table_name, "system_status", "indivisual_scraping")
        supabase = spabase_supabase()
        for dict_dict in dict_list:
            usable = dict_dict["system_usable"]
            id = dict_dict["system_id"]
            url = dict_dict["search_url"]

            logger.info(f"Processing {dict_dict['system_id']}")

            if not usable:
                logger.info(f"Skipping video research for {id} because its a unusable data")
                continue

            from app.analysing.video.logic import run_flow
            output = run_flow(url, id)

            supabase.table(table_name).update(output).eq("system_id", id).execute()
            logger.info(f"Successfully updated: {id}")
    except Exception as e:
        logger.critical(f"🔴 {e}")
        traceback.print_exc()
        sys.exit(2)

elif system_num == 4:
    try:
        dict_list = select_from_supabase(table_name, "system_status", "list_scraping")
        supabase = spabase_supabase()
        for dict_dict in dict_list:
            id = dict_dict["system_id"]
            url = dict_dict["search_url"]

            try:
                from app.scraping.indivisual.logic_indivisual import run_flow
                indivisual_output = run_flow(url)
                supabase.table(table_name).update(indivisual_output).eq("system_id", id).execute()
                logger.info(f"Successfully updated - indivisual: {id}")
            except Exception as e:
                logger.critical(f"🔴 {e}")
                continue

            if not indivisual_output["system_usable"]:
                logger.info(f"Skipping video research for {id} because its a unusable data")
                continue

            try:
                from app.analysing.video.logic import run_flow
                video_output = run_flow(url, id)
                supabase.table(table_name).update(video_output).eq("system_id", id).execute()
                logger.info(f"Successfully updated - video: {id}")
            except Exception as e:
                logger.critical(f"🔴 {e}")
                continue

    except Exception as e:
        logger.critical(f"🔴 {e}")
        traceback.print_exc()
        sys.exit(2)
else:
    logger.error(f"🔴 system number {system_num} is not valid")
    traceback.print_exc()
    sys.exit(1)

logger.info("🍺🍺 main execution completed 🍺🍺")

"""
python main.py --client client_samurai --start_row 3 --end_row 7 --system 1
python main.py --client client_test --start_row 4 --end_row 6 --system 2
"""





