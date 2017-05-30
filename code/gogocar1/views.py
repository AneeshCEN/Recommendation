from django.shortcuts import render

# Create your views here.
import numpy as np
import json
import urllib2
from scipy import stats
from sklearn import linear_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from scipy.spatial.distance import mahalanobis
import scipy as sp
import pandas as pd
import datetime
from time import time
from sklearn.metrics.pairwise import euclidean_distances
from pandas import DataFrame
#import pandas as pd
import MySQLdb
from pandas.io import sql
from python_mysql_dbconfig import read_db_config


@permission_classes((permissions.AllowAny,))
class GoGoCarScore(viewsets.ViewSet):

    def list(self, request):
        dict = read_db_config()

        db = MySQLdb.connect(host=dict.get('host'),
                             user=dict.get('user'),
                             passwd=dict.get('password'),
                             db=dict.get('database'))
        Make_Name = ""

        if ("Make_Name" in request.query_params):
            Make_Name = request.query_params['Make_Name']
        else:
            return Response({'status': 'ERROR', 'error': 'Please Enter a valid Make_Name'})

        Model_Name = ""

        if ("Model_Name" in request.query_params):
            Model_Name = request.query_params['Model_Name']
        else:
            return Response({'status': 'ERROR', 'error': 'Please Enter a valid Model_Name'})

        try:
            Make_Name = str(Make_Name)
            Model_Name = str(Model_Name)
            # print Car_type

            #x=pd.read_sql("select cartype1,simiarity,type FROM pima.car_inventory WHERE  car_type = '%s' and simiarity < 1 order by simiarity Desc limit 3" % text, db1 )
            x=pd.read_sql("Select model,DistanceScore,similarityScore,carType from master_table1 where Testmodel ='%s' AND DistanceScore > 0 order by DistanceScore ASC limit 3" % Model_Name, db )
            #x = pd.read_sql("Select model,DistanceScore,similarityScore,carType from gogo_car.master_table1 where Testmodel ='%s' AND model = '%s' AND DistanceScore > 0 order by DistanceScore ASC limit 3" % (
            #    Make_Name, Model_Name), db)

            if x.empty:
                return Response({'status': '404', 'error': 'The input doesnt contain any matching records please give another input'})
            else:
                myJSON = x.to_json(path_or_buf=None, orient='records', date_format='epoch',
                                   double_precision=10, force_ascii=True, date_unit='ms', default_handler=None)  # Attempt 1
                myJSON = json.loads(myJSON)
                myJSON = {'TopScoring': myJSON}

                return Response(myJSON)

        except:
            return Response({'status': '404', 'error': 'Error in  score calculation block'})