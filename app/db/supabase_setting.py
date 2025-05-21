import os
from supabase import create_client, Client
from utilities.logger import logger

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_to_supabase(data: dict, table_name: str):
    try:
        response = supabase.table(table_name).insert(data).execute()
        logger.info(f'Successfully inserted data to {table_name}: {response.data}')
    except Exception as e:
        logger.error(f'Failed to insert data to {table_name}: {e}')

def select_from_supabase(table_name: str, column: str, value: str):
    try:
        response = supabase.table(table_name).select("*").eq(column, value).execute()
        logger.info(f'Successfully selected data from {table_name}')
    except Exception as e:
        logger.error(f'Failed to select data from {table_name}: {e}')
        return None
    return response.data

def spabase_supabase():
    return supabase

if __name__ == "__main__":
    data = {"system_id": "1234567890", "system_url": "https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/ja?period=180&region=JP&industry=14&object=3"}
    res = insert_to_supabase(data)
    print(res)
