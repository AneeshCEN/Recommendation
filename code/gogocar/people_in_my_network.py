import re
import json
import scipy.stats as ss


def extract_zip_code(data_frame):
    regx = re.compile(r'(\d\d\d\d\d)')
    zip_code = []
    for address in data_frame['customer_influencers_address']:
        try:
            ptr = regx.search(address)
            match = ptr.group()
            zip_code.append(match)
#            print 'splitted ' , match.split(' ')[0]
        except:
            zip_code.append('Not found')
    data_frame['zip_code'] = zip_code
    sorted_under_zip = data_frame.sort(columns='zip_code')
    return sorted_under_zip


def get_models_people_in_my_network(user_id, host_id, db_local):
    import MySQLdb
    import pandas as pd
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
    elif host_id == 'recommendation.dealeron.gogocar.com' or host_id== '127.0.0.1:8000':
        host_name = '10.90.40.160'
        user = "recommend_user"
        password = "srizZOwwaGhr"
        database='gogo_dev'
        db = MySQLdb.connect(host=host_name,
                             user=user,
                             passwd=password,
                             db=database)

    influencer_query = 'SELECT customer_influencers_id,\
customer_influencers_name,\
customer_influencers_address,customer_influencers_email \
FROM gogo_dev.customer_influencers \
where customer_influencers_id is not null and \
customer_id=%s' % (user_id)
    print influencer_query
    influencer_table = pd.read_sql("%s" % influencer_query, db)
    if len(influencer_table) != 0:
        influencer_id_list = list(set(influencer_table['customer_influencers_id']))
        print 'influencer_id_list', influencer_id_list
        frame_list = []
        for ids in influencer_id_list:
            query = 'SELECT make,model FROM gogo_dev.customer_journey \
where associated_customer_id=%s and main_stage="connect"' % (ids)
            buy_frame = pd.read_sql("%s" % query, db)
            print 'buy_frame', buy_frame
            if len(buy_frame) != 0:
                model_list = list(buy_frame['model'])
                for model_name in model_list:
                    query = "select model,Normscore,carType From car_type_table1 \
where model ='%s'" % (model_name)
                    model_df = pd.read_sql("%s" % query, db_local)
                    if len(model_df) != 0:
                        frame_list.append(model_df)
        if len(frame_list) != 0:
            final_frame = pd.concat(frame_list)
            rank = ss.rankdata(list(final_frame['Normscore']))
            final_frame['Rank'] = rank
            e = (len(final_frame.index) -
                 final_frame['Rank'])/(len(final_frame.index))
            Score = e*10
            final_frame['similarityScore'] = 10-Score
            final_frame = final_frame.sort(columns='similarityScore',
                                           ascending=False)
            print final_frame
            favorites_models = pd.DataFrame(final_frame, columns=['model','carType','similarityScore'])
            favorites_models.drop_duplicates(inplace = True)
            favorites_models['message'] = "Recommended by People you Know"
            favorites_models = favorites_models[favorites_models.similarityScore >= 5]
            myJSON = favorites_models.to_json(path_or_buf=None,
                                              orient='records',
                                              date_format='epoch',
                                              double_precision=10,
                                              force_ascii=True,
                                              date_unit='ms',
                                              default_handler=None)
            myJSON = json.loads(myJSON)
            print myJSON
            return myJSON

        elif len(frame_list) == 0:
            print 'from sales data'
            influencer_table = extract_zip_code(influencer_table)

            influencer_name_list = list(influencer_table['customer_influencers_name'])
            influencer_zip_code = list(influencer_table['zip_code'])
            frame_list_sales = []
            for index, zip_code in enumerate(influencer_zip_code):
                query = 'select model,carType,zipScore AS similarityScore from final_score_table \
                where zipCode = %s and name="%s"' % (zip_code, 
                                                     influencer_name_list[index])
                try:
                    people_in_my_network_sales = pd.read_sql("%s" % query, db_local)
                    frame_list_sales.append(people_in_my_network_sales)
                except:
                    print 'invalid zipcode'
            if len(frame_list_sales) != 0:
                network_models = pd.concat(frame_list_sales)
                network_models = network_models.drop_duplicates()
                rank = ss.rankdata(list(network_models['similarityScore']))
                network_models['Rank'] = rank
                e = (len(network_models.index) -
                     network_models['Rank'])/(len(network_models.index))
                Score = e*10
                network_models['similarityScore'] = 10-Score
                favorites_models = network_models.sort(columns='similarityScore',
                                                 ascending=False)
                print favorites_models
                favorites_models = pd.DataFrame(favorites_models, columns=['model','carType','similarityScore'])
                favorites_models['message'] = "Recommended by People you Know"
                favorites_models = favorites_models[favorites_models.similarityScore >= 5]
                myJSON = favorites_models.to_json(path_or_buf=None,
                                  orient='records',
                                  date_format='epoch',
                                  double_precision=10,
                                  force_ascii=True,
                                  date_unit='ms',
                                  default_handler=None)

                myJSON = json.loads(myJSON)
                print 'json', myJSON
                return myJSON
            else:
                return []
    else:
        return []  
