"""
Owner: neha.karekar@zeno.health
Purpose: to get patients nearest store
"""

import argparse
import sys
import os
import json
import dateutil
import datetime
from dateutil.tz import gettz
import numpy as np
import pandas as pd
from datetime import date, timedelta
import geopy as geopy
import geopy.distance

sys.path.append('../../../..')

sys.path.append('../../../..')
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-bs', '--batch_size', default=10000, type=int, required=False)
parser.add_argument('-d', '--full_run', default=0, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
full_run = args.full_run
batch_size = args.batch_size

os.environ['env'] = env
logger = get_logger()
logger.info('logger start')

rs_db = DB()
rs_db.open_connection()
s3 = S3()

schema = 'prod2-generico'
table_name = "patient-nearest-store"
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


def geo_distance(lat1, long1, lat2, long2):
    geo_dist = geopy.distance.geodesic((lat1, long1), (lat2, long2)).km
    return geo_dist


max_q = """
select
            date(max("created-at")) max_exp
        from
            "prod2-generico"."patient-nearest-store"  
        """

max_exp_date = rs_db.get_df(max_q)
max_exp_date = max_exp_date['max_exp'][0]
logger.info(f'max exp date: {max_exp_date}')

# params
if full_run or max_exp_date is None:
    start = '2017-05-13'
    start = dateutil.parser.parse(start)
else:
    start = max_exp_date
logger.info(f'start date: {start}')

pat_count_q = f"""select
                count(distinct id) cnt
            from
                "prod2-generico"."patients-metadata-2"
            where
                date("last-bill-date")>= '{start}' 
             """
pat_count = rs_db.get_df(pat_count_q)
pat_count = pat_count['cnt'][0].astype('int')
logger.info(f'patient count: {pat_count}')


# pat_count = 100
# batch_size = 10


def nearest_store(batch=1):
    pat_q = f"""
        
                select
                    pm.id "patient-id",
                    pm."primary-store-id",zpa.latitude,zpa.longitude,
                    "previous-store-id"
                from
                    (select *,rank() over (partition by "patient-id" order by "created-at" desc ) r
                    from "prod2-generico"."zeno-patient-address") zpa
                inner join "prod2-generico"."patients-metadata-2" pm on
                    zpa."patient-id" = pm.id
                    and zpa.latitude != ''
                where
                    zpa.latitude is not null and zpa.latitude !=''
                    and zpa.longitude is not null and zpa.longitude !=''
                    --and pm.id =5
                    and pm.id is not null
                    --and pm."primary-store-id" in (16,2)
                    --and pm."last-bill-date" >= CURRENT_DATE -90 
                    and r=1
                    group by 1,2,3,4,5 LIMIT {batch_size} OFFSET {(batch - 1) * batch_size}
                    """

    pat = rs_db.get_df(pat_q)
    logger.info(f'patient count: {pat.shape}')
    if not pat.empty:
        store_q = """
            select id as nearest_store_id,store as nearest_store,latitude,longitude,"store-type" 
            from "prod2-generico"."stores-master" sm
            where
                    sm.latitude != ''
            and sm.longitude != ''
                    and sm.latitude is not null
                    and sm."id" is not null and "store-type" != 'dc'
                """
        store = rs_db.get_df(store_q)
        logger.info(f'store count: {store.shape}')
        pat['i'] = 1
        store['i'] = 1
        hash_join = pat.merge(store, how='left', on='i')
        hash_join['geo_dist'] = hash_join.apply(
            lambda x: geo_distance(x.latitude_x, x.longitude_x, x.latitude_y, x.longitude_y), axis=1)
        hash_join['rank'] = hash_join.sort_values(by=['geo_dist']).groupby(['patient-id']).cumcount() + 1
        hash_join = hash_join[hash_join['rank'] == 1].copy()
        hash_join.columns = [c.replace('_', '-').lower() for c in hash_join.columns]
        hash_join = hash_join[['patient-id', 'nearest-store-id']]
        hash_join['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        return hash_join
    else:
        return None


try:
    truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where date("created-at")>= '{start}' '''
    logger.info(f'truncate query1:{truncate_query}')
    rs_db.execute(truncate_query)
    logger.info(f'truncate query:{truncate_query}')
    logger.info(f'pat count type:{type(pat_count)}')
    logger.info(f'batch size type:{type(batch_size)}')
    for i in range(1, int(pat_count / batch_size) + 1):
        logger.info(f'batch run:{i}')
        nearest_store_df = nearest_store(batch=i)
        if nearest_store_df is not None:
            s3.write_df_to_db(df=nearest_store_df[table_info['column_name']], table_name=table_name, db=rs_db,
                              schema=schema)
            logger.info(f"Total drug count: {len(nearest_store_df)}")
        else:
            pass

except Exception as error:
    raise Exception(error)
finally:
    rs_db.close_connection()
    # nearest_store_id = pd.concat([nearest_store_id, temp_df])
