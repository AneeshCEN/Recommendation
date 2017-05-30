from config import host_inventory
from config import user_inventory 
from config import passwd_inventory
from config import db_inventory
import MySQLdb
import json
import pandas as pd

def connect_to_db():
    db = MySQLdb.connect(host=host_inventory,
                         user=user_inventory,
                         passwd=passwd_inventory,
                         db=db_inventory)
    return db


def score_calculation(frame):
    score = [int(len(frame)-i) for i in range(len(frame))]
    frame['score'] = score
    OldRange = frame.score.max()-frame.score.min()
    NewRange = 10
    similarityScore = (((frame.score.values - frame.score.min()) * NewRange) / OldRange)
    frame['similarityScore'] = similarityScore
    frame = frame[frame.similarityScore>=5]
    frame['message'] = 'Recommended by us'
    return frame




def get_entries(db, query):
    df = pd.read_sql(query, db)
    if len(df) != 0:
        string_cars = list(df.similar_cars)[0]
        list_entries = string_cars.replace('[','').replace(']','').replace('{','').replace('}','').replace('"year":"2016"','').split(',')
        list_entries = filter(None, list_entries)
        make_list = []
        model_list = []
        type_list = []
        for i in list_entries:
            if '"make":'in i:
                make_name = i.replace('"make":','').strip('"')
            elif '"model":' in i:
                model_name = i.replace('"model":','').strip('"').lower()
                query_type = "select type_name from \
gogo_dev.car_inventory where type_name!='' and type_name !='None' \
and make_name='%s'and model_name='%s' limit 1" %(make_name, model_name)
                df_type = pd.read_sql(query_type, db)
                if len(df_type.type_name) == 0:
                    model_name = i.replace('"model":','').strip('"').replace('-',' ').lower()
                    query_type = "select type_name from \
gogo_dev.car_inventory where type_name!='' and type_name !='None' and \
make_name='%s'and model_name='%s' limit 1" % (make_name, model_name)
                    df_type = pd.read_sql(query_type, db)
                if len(df_type.type_name) != 0:
                    make_list.append(make_name)
                    model_list.append(model_name)
                    type_list.append(list(df_type.type_name)[0])
        if len(type_list) != 0 and len(model_list) !=0 and len(type_list) == len(model_list):
            frame = pd.DataFrame({'model': model_list,'carType': type_list})
            frame = score_calculation(frame)
            return frame
        else:
            return []
    else:
        return []


def fetch_from_cd_class(Make_Name, Model_Name, response_count):
    make_name_user = Make_Name
    model_name_user = Model_Name
    year = 2016
    db = connect_to_db()
    query = "select similar_cars from gogo_dev.Ranking where \
model_year='%s' and make_name='%s' \
and model_name='%s'" %(year, make_name_user, model_name_user)
    frame = get_entries(db, query)
    if len(frame) != 0:
        frame = frame[frame.model != model_name_user.lower()]
        frame.drop('score', axis=1, inplace=True)
        frame_json = frame.to_json(path_or_buf=None,
                                   orient='records',
                                   date_format='epoch',
                                   double_precision=10,
                                   force_ascii=True,
                                   date_unit='ms',
                                   default_handler=None) 
        frame_json = json.loads(frame_json)
        if response_count > 0:
            frame_json = frame_json[0:response_count]
        return frame_json
    else:
        return 'no result'
