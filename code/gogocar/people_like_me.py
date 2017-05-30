'''
Created on Oct 6, 2016

@author: aneesh.c
'''

import json
import MySQLdb
import pandas as pd
import scipy.stats as ss

host_inventory = "kapowdb.gogocar.com"
user_inventory = "ggc_user"
passwd_inventory = "G5uq$NH@AXNd"
db_inventory = "homenet_dealer_inventory"


def cluster_user(df):
    event_list = list(set(df['model_name']))
    frame_list = []
    for index, events in enumerate(event_list):
        sub_frame = df.loc[df['model_name'] == events]
        sub_frame['label'] = index+1
        frame_list.append(sub_frame)
    
    return(pd.concat(frame_list))


def get_favourites_id(db, user_id):
    query = 'select * from frame_with_cluster'
    df = pd.read_sql(query, db)
    cluster_id = list(set(df.loc[df['user_id'] == user_id]['label']))
    id_list = []
    for elements in cluster_id:
        ids = list(set(df.loc[df['label'] == elements]['user_id']))
        id_list.extend(ids)
    return list(set(id_list))


def read_from_buy_and_get_score(favourites, qa_db, db_where_score_table):
    frame_list = []
    for ids in favourites:
        query = 'SELECT make,model FROM gogo_dev.customer_journey where \
        associated_customer_id=%s and main_stage="connect"' % (ids)
        buy_frame = pd.read_sql("%s" % query, qa_db)
        if len(buy_frame) == 0:
            print 'no buyer for this id'
        elif len(buy_frame) != 0:
            model_list = list(buy_frame['model'])
            for model_name in model_list:
                query = "select model,Normscore,carType From car_type_table1 \
                         where model ='%s'" % (model_name)
                model_df = pd.read_sql("%s" % query, db_where_score_table)
                if len(model_df) != 0:
                    frame_list.append(model_df)
    if len(frame_list) != 0:
        frame = pd.concat(frame_list)
        return frame
    else:
        return []


def rescore(favorites_models):
    rank = ss.rankdata(list(favorites_models['Normscore']))
    favorites_models['Rank'] = rank
    e = (len(favorites_models.index) -
         favorites_models['Rank'])/(len(favorites_models.index))
    Score = e*10
    favorites_models['similarityScore'] = 10-Score
    favorites_models = favorites_models.sort(columns='similarityScore',
                                             ascending=False)
    favorites_models = pd.DataFrame(favorites_models, columns=[
                                                               'model',
                                                               'carType',
                                                               'similarityScore'
                                                               ])
    favorites_models['message'] = "Recommended by like-minded People"
    favorites_models = favorites_models[favorites_models.similarityScore >= 5]
    myJSON = favorites_models.to_json(path_or_buf=None,
                                      orient='records',
                                      date_format='epoch',
                                      double_precision=10,
                                      force_ascii=True,
                                      date_unit='ms',
                                      default_handler=None)

    myJSON = json.loads(myJSON)
    return myJSON


def people_like_me(userid, host_id, db_where_score_table):

    if host_id == 'recommendation.beta.gogocar.com':
        host_name_beta = '10.50.0.170'
        user = 'cognub'
        password = 'y3GfCA1wwh10'
        database = 'gogo_dev'
        db = MySQLdb.connect(host=host_name_beta,
                             user=user,
                             passwd=password,
                             db=database)

    elif host_id == 'recommendation.qa.gogocar.com':
        host_name = "mysqldb.qa.gogocar.com"
        user = "cognubqa"
        password = 'JxlQETTFxTNz'
        database = 'gogo_dev'
        db = MySQLdb.connect(host=host_name,
                             user=user,
                             passwd=password,
                             db=database)
    elif host_id == 'recommendation.qa2.gogocar.com':
        host_name = "20.70.40.145"
        user = "cognubqa"
        password = 'JxlQETTFxTNz'
        database = 'gogo_dev'
        db = MySQLdb.connect(host=host_name,
                             user=user,
                             passwd=password,
                             db=database)
    elif host_id == 'recommendation.dealeron.gogocar.com' or host_id == '127.0.0.1:8000':
        host_name = '10.90.40.160'
        user = "recommend_user"
        password = "srizZOwwaGhr"
        database='gogo_dev'
        db = MySQLdb.connect(host=host_name,
                             user=user,
                             passwd=password,
                             db=database)


        '''
    car_inventory_db = MySQLdb.connect(host=host_inventory,
                                       user=user_inventory,
                                       passwd=passwd_inventory,
                                       db=db_inventory)
  

    read_query = "select customer_id, car_inventory_vin from \
    customer_favorite_cars where customer_id is not null \
    and car_inventory_vin is not null and customer_id != ' ' \
    and car_inventory_vin != ' ' "
    print 'connecting *****'
    data_frame_user_vin = pd.read_sql(read_query, db)
    df_user_vin = data_frame_user_vin.drop_duplicates()
    user_id_list = list(df_user_vin['customer_id'])
    frame_list = []
    for index, vin in enumerate(list(df_user_vin['car_inventory_vin'])):
        query = "select make_name,model_name, type_name from \
        car_inventory where vin='%s'" % (vin)
        car_info_from_inventory = pd.read_sql(query, car_inventory_db)
        sub_frame = car_info_from_inventory
        sub_frame['user_id'] = user_id_list[index]
        print sub_frame
        frame_list.append(sub_frame)
    print "connected"

    frame_to_cluster = pd.concat(frame_list)
    frame_to_cluster = frame_to_cluster.drop_duplicates()
    frame_with_cluster = cluster_user(frame_to_cluster)
    '''
    favourites = get_favourites_id(db_where_score_table, userid)
    if len(favourites) != 0:
        frame_df = read_from_buy_and_get_score(favourites, db,
                                               db_where_score_table)
        if len(frame_df) != 0:
            favorites_models = frame_df.drop_duplicates()
            dict_to_return = rescore(favorites_models)
            return dict_to_return
        else:
            print 'No buy for these favourites'
            return []
    else:
        print 'No favourites for this id'
        return []
