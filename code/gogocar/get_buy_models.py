import json
import pandas as pd
import scipy.stats as ss


def people_like_me(params, db):
    customer_id = params
    query = "SELECT cluster FROM dream_garage where \
customer_id=%s" % (customer_id)
    cluster_list = pd.read_sql("%s" % query, db)
    print query, cluster_list
    cluster_list = list(set(cluster_list['cluster']))
    #print 'length', len(cluster_list)
    if len(cluster_list) != 0:
        id_list_to_access_from_buy = []
        for cluster_id in cluster_list:
            query = "SELECT customer_id from dream_garage \
where cluster=%s" % (cluster_id)
            id_df = pd.read_sql("%s" % query, db)
            print 's', query
            id_ = id_df['customer_id']
            id_list_to_access_from_buy.append(id_)
        id_list_to_access_from_buy = list(pd.concat(id_list_to_access_from_buy))
        id_list_to_access_from_buy = list(set(id_list_to_access_from_buy))
        print 'id', id_list_to_access_from_buy
        favorites_models = []
        for i in id_list_to_access_from_buy:
            query = 'SELECT model,type_name from buy where \
            customer_id=%s' % (i)
            model_df = pd.read_sql("%s" % query, db)
            if len(model_df) != 0:
                models = list(model_df['model'])
                types = list(model_df['type_name'])
                for index, value in enumerate(models):
                    model_to_search = value
                    type_to_search = types[index]
                    query = "select model,Normscore,carType From car_type_table1 where model ='%s'\
                    and carType='%s'" % (model_to_search, type_to_search)
                    model_df = pd.read_sql("%s" % query, db)
                    if len(model_df) != 0:
                        favorites_models.append(model_df)

        favorites_models = pd.concat(favorites_models)
        favorites_models = favorites_models.drop_duplicates()
        rank = ss.rankdata(list(favorites_models['Normscore']))
        favorites_models['Rank'] = rank
        e = (len(favorites_models.index) -
             favorites_models['Rank'])/(len(favorites_models.index))
        Score = e*10
        favorites_models['similarityScore'] = 10-Score
        favorites_models = favorites_models.sort(columns='similarityScore',
                                                 ascending=False)
        favorites_models = pd.DataFrame(favorites_models, columns=['model','carType','similarityScore'])
        favorites_models['message'] = "Recommended by like-minded People"
        myJSON = favorites_models.to_json(path_or_buf=None,
                                          orient='records',
                                          date_format='epoch',
                                          double_precision=10,
                                          force_ascii=True,
                                          date_unit='ms',
                                          default_handler=None)
        #myJSON['message'] = "favour"
        myJSON = json.loads(myJSON)
        #print 'tyyyyyyyyyyyyy',type(myJSON)
        print myJSON
        return myJSON
    else:
        return []
