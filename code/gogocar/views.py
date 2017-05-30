from django.shortcuts import render
# Create your views here.
# import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import pandas as pd
import json
import MySQLdb
from __builtin__ import True
from finalquerybuilder import buildQuery1
from people_like_me import people_like_me
#from get_buy_models import people_like_me
from people_in_my_network import get_models_people_in_my_network
from fetch_cd_class import fetch_from_cd_class
from config import host_dev
from config import password_dev
from config import user_dev
from config import database_dev

from config import host_qa
from config import password_qa
from config import user_qa
from config import database_qa

from config import host_qa2
from config import password_qa2
from config import user_qa2
from config import database_qa2

from config import host
from config import password
from config import user
from config import database


from config import host_beta
from config import password_beta
from config import user_beta
from config import database_beta

from config import host_dealeron
from config import password_dealeron
from config import user_dealeron
from config import database_dealeron
from gogocar import fetch_cd_class


@permission_classes((permissions.AllowAny,))
class GoGoCarScore(viewsets.ViewSet):
    def create(self, request):
        response_from_cd = 'no result'
        Cartype = ""
        maritalstatus = ""
        emplyr = ""
        Gender = ""
        profesionalqualification = ""
        Model_Name = ""
        age_flag = False
        zipcode = 0
        label = 0
        budget = 0
        Make_Name = ""
        Class = ""
        features = ""
        annual_income = ""
        sub_type = ""
        city_mpg = 0
        userid = 0
        highway_mpg = 0
        response_count = 0
        favourite = []
        people_in_network = []
        myJSON = []
        result = {}
        final_list = []
        data = request.data['data']
        host_id = request.get_host()
        if ("Cartype" in data) and len(data['Cartype']) > 0:
            Cartype = str(data['Cartype'])
        if ("budget" in data):
            budget = int(data['budget'])
        if ("zipcode" in data):
            zipcode = int(data['zipcode'])
        if ("citympg" in data):
            city_mpg = int(data['citympg'])
        if ("annualincome" in data):
            annual_income = int(data['annualincome'])
        if ("highwaympg" in data):
            highway_mpg = int(data['highwaympg'])
        if ("responsecount" in data):
            response_count = int(data['responsecount'])
        if ("userid" in data):
            userid = int(data['userid'])
        if ("age" in data):
            age_flag = True
            age = int(data['age'])
        if ("class" in data):
            Class = str(data['class'])
        if ("subtype" in data):
            sub_type = str(data['subtype'])
        if ("gender" in data):
            Gender = str(data['gender'])
        if ("features" in data):
            features = str(data['features'])
        if ('maritalstatus' in data):
            maritalstatus = str(data['maritalstatus'])
        if ('Employer' in data):
            emplyr = str(data['Employer'])
        if ('professionalqualification' in data):
            profesionalqualification = str(
                                           data['professional\
qualification']
                                           )
        if ("Make_Name" in data):
            Make_Name = data['Make_Name']
        if ("Model_Name" in data):
            Model_Name = data['Model_Name']
        try:
            if age_flag:
                if age < 35:
                    label = 1
                elif 35 <= age < 45:
                    label = 2
                elif 45 <= age < 55:
                    label = 3
                elif age >= 55:
                    label = 4
                else:
                    label = 1
        except:
                print "Error in age assignment block"

        if host_id == 'recommendation.qa.gogocar.com':
            db = MySQLdb.connect(host=host_qa,
                                 user=user_qa,
                                 passwd=password_qa,
                                 db=database_qa)
            
        elif host_id == 'recommendation.qa2.gogocar.com':
            db = MySQLdb.connect(host=host_qa2,
                                 user=user_qa2,
                                 passwd=password_qa2,
                                 db=database_qa2)
        elif host_id == 'recommendation.beta.gogocar.com':
            db = MySQLdb.connect(host=host_beta,
                                 user=user_beta,
                                 passwd=password_beta,
                                 db=database_beta)
        elif host_id == 'recommendation.dev.gogocar.com':
            db = MySQLdb.connect(host=host_dev,
                                 user=user_dev,
                                 passwd=password_dev,
                                 db=database_dev)
        elif host_id == 'recommendation.dealeron.gogocar.com' or host_id == '127.0.0.1:8000':
            db = MySQLdb.connect(host=host_dealeron,
                                 user=user_dealeron,
                                 passwd=password_dealeron,
                                 db=database_dealeron)
        #elif host_id == '127.0.0.1:8000':
         #   db = MySQLdb.connect(host=host,
          #                       user=user,
          #                       passwd=password,
           #                      db=database)
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please \
Enter a valid host name'})
        queryParams = {}
        queryParams["make"] = Make_Name
        queryParams["CarType"] = Cartype
        queryParams['Model_Name'] = Model_Name
        queryParams["Msrp"] = budget
        queryParams["zipCode"] = zipcode
        queryParams["label"] = label
        queryParams["gender"] = Gender
        queryParams['MaritalStatus'] = maritalstatus
        queryParams['employer'] = emplyr
        queryParams['prof_qualification'] = profesionalqualification
        queryParams['city_mpg'] = city_mpg
        queryParams['highway_mpg'] = highway_mpg
        print queryParams
        Attr = [key for key, value in queryParams.items() if (value != 0 and
                                                              value != '')]
        if Make_Name != "" and Model_Name != "":
            response_from_cd = fetch_from_cd_class(Make_Name, Model_Name, response_count)
            myJSON = response_from_cd
        if response_from_cd == 'no result':
            if userid != 0:
                print 'host id', host_id
                people_in_network = get_models_people_in_my_network(userid, host_id, db)
                favourite = people_like_me(userid, host_id, db)
                if response_count > 0:
                    favourite = favourite[0:response_count]
                    people_in_network = people_in_network[0:response_count]
                #print 'yes', favourite, people_in_network
                final_list.extend(favourite)
                final_list.extend(people_in_network)
               # print "final_list", final_list
     #           result = {'TopScoring': final_list}
            if userid == 0 or len(Attr) != 0:
                if len(Attr) != 0:
                    Query = buildQuery1(queryParams)
                    if Query.endswith('order by DistanceScore DESC') and 'final_score_table' in Query:
                        Query = Query.replace('order by DistanceScore DESC', 'order by similarityScore DESC')
                    print Query
                else:
                    output_text = {'status': '404',
                                   'error': """No Suitable \
        Recommendation """}
        
                    return Response(output_text)
                try:
                    x1 = pd.read_sql("%s" % Query, db)
                except:
                    output_text = {'status': '404',
                                   'error': """No Suitable \
        Recommendation """}
        
                    return Response(output_text)
                #print x1
                if x1.empty:
                    print 'The input doesnt \
        contain any matching records please give another input'
                    output_text = {'status': '404',
                                   'error': """No Suitable \
        Recommendation """}
    
                    return Response(output_text)
                else:
                    if 'DistanceScore' in x1.columns and not 'similarityScore' in x1.columns:
                        x1 = x1.rename(columns={'DistanceScore': 'similarityScore'})
                    if 'Msrp' in x1:
                        x1.drop('Msrp', axis=1, inplace=True)
                    x1.drop_duplicates(subset=['model','carType'],inplace=True)
                    x1 = x1[x1.similarityScore > 5]
                    x1['message'] = 'Recommended by us'
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1

                    myJSON = json.loads(myJSON)
                    if response_count > 0:
                        myJSON = myJSON[0:response_count]
        final_list.extend(myJSON)
        if len(final_list) != 0:
            print 'final list', final_list
            if Model_Name != "":
                model = Model_Name.lower()
                for dic in final_list:
                    if dic['model'].lower() == model:
                        final_list.remove(dic)
            if len(final_list) != 0:
                result['TopScoring'] = final_list
                return Response(result)
            else:
                output_text = {'status': '404', 
                           'error': """No Suitable \
Recommendation """}

            return Response(output_text)

        else:
            output_text = {'status': '404', 
                           'error': """No Suitable \
Recommendation """}

            return Response(output_text)
