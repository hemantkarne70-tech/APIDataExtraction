import os
import glob
import re
import time
import json
import hashlib
import random
import string
import shutil
import traceback
import requests
import subprocess
import pandas as pd
import numpy as  np
from math import cos, asin, sqrt
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import pytz
from neo4j import GraphDatabase
from multiprocessing import Pool
import Config as config
from Logger import get_logger

logger = get_logger("apidata.log")

class GetApiData:

    def __init__(self, systemName):
        self.systemName = systemName
        self.es = Elasticsearch(config.ES_URI, **config.ES_CONFIG)
        self.neo_driver = GraphDatabase.driver(f"bolt://{config.NEO_IP}:{config.NEO_PORT}", encrypted=False)
        self.neo_session = self.neo_driver.session()

    def dateUnix(self, date_string):
        try:
            ist = pytz.timezone('Asia/Kolkata')
            utc = pytz.utc
            
            if isinstance(date_string, str):
                try:
                    dt_obj = datetime.strptime(date_string, '%d/%m/%Y %H:%M')
                    dt_obj = ist.localize(dt_obj, is_dst=None)
                    utc_dt_obj = dt_obj.astimezone(utc)
                except ValueError:
                    try:
                        date_string = date_string.split('.')[0]
                        dt_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
                        utc_dt_obj = utc.localize(dt_obj)
                    except ValueError:
                        return ""
                
                return int(utc_dt_obj.timestamp())
            return ""
        except Exception as e:
            return ""

    def toDate(self, timestamp):
        try:
            # Check if the timestamp is 0 or not valid
            if timestamp == 0 or not isinstance(timestamp, (int, float)):
                return ""  # Return an empty string if the input is 0 or not a valid number
            
            dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            return dt
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def getWPH(self, timestamp):
        try:
            if isinstance(timestamp, str) and timestamp.strip() == "":
                return pd.Series(["","",""])

            dt = datetime.fromtimestamp(timestamp)
            weekday = dt.strftime("%A")  # Full weekday name
            perOfDay = ""
            hour = dt.hour

            # Determine the period of the day
            if 5 <= hour < 12:
                period_of_day = "Morning"
            elif 12 <= hour < 17:
                period_of_day = "Afternoon"
            elif 17 <= hour < 21:
                period_of_day = "Evening"
            else:
                period_of_day = "Night"

            return pd.Series([weekday,period_of_day,hour])
        except Exception as e:
            traceback.print_exc()
            return pd.Series(["","",""])

    def getYMQ(self, timestamp):
        try:
            dt = datetime.fromtimestamp(timestamp)
            year = dt.year
            month = dt.strftime("%B")  # Full month name
            quarter = (dt.month - 1) // 3 + 1

            return pd.Series([year,month,quarter])
        except Exception as e:
            traceback.print_exc()
            return pd.Series(["","",""])

    def neo_ingest(self, data):
        tx = self.neo_session.begin_transaction()
        try:
            for counter, row in enumerate(data):
                query = """create(n:node) set n+={row} return id(n)"""
                tx.run(query, parameters={'row': row})

                if counter % 500 == 0:
                    tx.commit()
                    tx = self.neo_session.begin_transaction()

            tx.commit()
            return True
        except Exception as e:
            logger.error(f"Neo4j ingestion error: {str(e)}")
            return False

    def week_of_month(self, unix_dt):
        dt = datetime.utcfromtimestamp(unix_dt)
        first_day_of_month = dt.replace(day=1)
        first_day_weekday = first_day_of_month.weekday()
        week_of_month = ((dt.day + first_day_weekday - 1) // 7) + 1
        # print(f"Week {week_of_month}")
        return f"Week {week_of_month}"

    def fetch_api_data(self, current_date):
        try:
            config.PARAMS["Fromdate"] = current_date
            config.PARAMS["Todate"] = current_date
            
            headers = {'Host': 'XXXXXXXXXXXX'}
            response = requests.get(config.URL, params=config.PARAMS, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # logger.info(f"Raw API response: {data}")
                if data and data.get("Status") == 1:
                    header = data.get("Header", "")
                    content = data.get("Content", [])
                    df = pd.DataFrame(content)
                    df["Header"] = header

                    df = df.rename(columns=config.col_names)

                    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
                    year_dir = os.path.join(config.data_dump, str(date_obj.year))
                    month_dir = os.path.join(year_dir, date_obj.strftime("%B"))

                    os.makedirs(month_dir, exist_ok=True)

                    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
                    year_dir = os.path.join(config.data_dump, str(date_obj.year))
                    month_dir = os.path.join(year_dir, date_obj.strftime("%B"))

                    os.makedirs(month_dir, exist_ok=True)

                    excel_file_name = f"{current_date}.xlsx"
                    data_dump_path = os.path.join(month_dir, excel_file_name)
                    input_folder_path = os.path.join(config.input_path, excel_file_name)

                    df.to_excel(data_dump_path, index=False)
                    print(f"Data added in Excel- {excel_file_name}")

                    shutil.copy(data_dump_path, input_folder_path)
                    print(f"File copied to input folder...")

                    return input_folder_path
                else:
                    # logger.error("Invalid data returned from API")
                    return None
            else:
                # logger.error(f"Failed to fetch API data. Status code: {response.status_code}")
                return None
            # return None
        except Exception as e:
            logger.error(f"Error fetching API data: {str(e)}")
            return None

    def process_getapidata(self, filename):
        try:
            pandas_df = pd.read_excel(filename)

            pandas_df = pandas_df.rename(columns=config.col_names)
            pandas_df = pandas_df.replace(np.nan, '', regex=True)

            pandas_df['Date'] = pandas_df['Date'].apply(lambda x: self.dateUnix(x) if isinstance(x, str) else x)

            pandas_df['Week'] = pandas_df['Date'].apply(lambda x: self.week_of_month(x))
            pandas_df[['Weekday','PeriodOfDay','Hour']] = pandas_df['Date'].apply(lambda x: self.getWPH(x))
            pandas_df[['Year','Month','Quarter']] = pandas_df['Date'].apply(lambda x: self.getYMQ(x))

            pandas_df['DateString'] = pandas_df['Date'].apply(lambda x: self.toDate(x))

            pandas_df['IngestionDate'] = int(time.time())
            pandas_df['OriginalName'] = os.path.basename(filename).split('.')[0]
            pandas_df['OriginalPath'] = filename
            pandas_df['SystemName'] = self.systemName
            pandas_df['SystemPath'] = config.output_path + self.systemName
            pandas_df['DataSource'] = "APIData"

            data_dict = pandas_df.to_dict(orient='records')
            response = self.neo_ingest(data_dict)

            subprocess.run(["python3.7", "CalendarEvent_SpecificDate.py"], check=True)  # for specific date
            # subprocess.run(["python3.7", "CalendarEvent.py"], check=True)  # for overall Data

            return response
        except Exception as e:
            print(f"Error processing Excel data: {e}")
            logger.error(f"Error in process_excel_data: {str(e)}")
            return False


def getrid():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

def get_file_list():
    return glob.glob(config.input_path + "*")

def process_file(file_path):
    if 'filepart' in file_path:
        pass
    else:
        baseName = os.path.basename(file_path)
        print("Processing File : " + baseName)
        systemName = ".".join(baseName.split(".")[:-1]) + "_" + getrid() + "." + baseName.split(".")[-1]
        try:
            obj = GetApiData(systemName)
            flag = obj.process_getapidata(file_path)
            if flag:
                shutil.move(file_path, config.output_path + systemName)
                print("Processing Done of : " + baseName)
            else:
                shutil.move(file_path, config.error_path + systemName)
                print("Processing Failed of : " + baseName)
        except Exception as e:
            logger.error(str(e))
            traceback.print_exc()
            shutil.move(file_path, config.error_path + systemName)
            print("Processing Failed of : " + baseName)

if __name__ == '__main__':
    t1 = time.time()

    start_date = datetime.strptime("2025-05-17", "%Y-%m-%d")
    end_date = datetime.strptime("2025-05-27", "%Y-%m-%d")

    current_date = start_date

    while current_date <= end_date:
        current_date_str = current_date.strftime("%Y-%m-%d")
        api_processor = GetApiData(systemName="getapi_" + getrid())
        api_file = api_processor.fetch_api_data(current_date_str)

        if api_file:
            FILE_LIST = get_file_list()
            if len(FILE_LIST) != 0:
                pool = Pool(config.pool_size)
                pool.map(process_file, FILE_LIST)
                pool.close()
                pool.join()

        current_date += timedelta(days=1)

    t2 = time.time()
    print("Total time taken: ", t2 - t1)
