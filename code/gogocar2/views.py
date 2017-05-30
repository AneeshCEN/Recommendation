from django.shortcuts import render

# Create your views here.
import numpy as np
import json
from scipy import stats
from sklearn import linear_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from scipy.spatial.distance import mahalanobis
import scipy as sp
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from pandas import DataFrame
from python_mysql_dbconfig import read_db_config
import json
import MySQLdb
from pandas.io import sql
from finalquerybuilder import buildQuery1
from finalquerybuilder import buildQuery2
from finalquerybuilder import buildQuery3
from finalquerybuilder import buildQuery4
from finalquerybuilder import buildQuery5
from finalquerybuilder import buildQuery6
from finalquerybuilder import buildQuery7
from finalquerybuilder import buildQuery8
from finalquerybuilder import buildQuery9


@permission_classes((permissions.AllowAny,))
class GoGoCarScore(viewsets.ViewSet):

    def list(self, request):
        increment_value = .10
        Cartype = ""
        if ("Cartype" in request.query_params):
            Cartype = request.query_params['Cartype']
        else:
            return Response({'status': 'ERROR', 'error': 'Please\
Enter a valid Cartype '})
        Cartype = str(Cartype)

        if ("Stateid" in request.query_params):
            if not request.query_params['Stateid'].isdigit():
                return Response({'status': 'ERROR', 'error': 'INVALID_\
Stateid '})
            else:
                Stateid = request.query_params['Stateid']
        else:
            Stateid = 0
        if ("Msrp" in request.query_params):
            if not request.query_params['Msrp'].isdigit():
                return Response({'status': 'ERROR', 'error': 'INVALID_Msrp'})
            else:
                Msrp = request.query_params['Msrp']
        else:
            Msrp = 0

        if ("MarketSegment" in request.query_params):
            MarketSegment = request.query_params['MarketSegment']
        else:
            MarketSegment = ""

        if ("Gender" in request.query_params):
            Gender = request.query_params['Gender']
        else:
            Gender = ""

        MarketSegment = str(MarketSegment)
        Gender = str(Gender)

        dict = read_db_config()

        db = MySQLdb.connect(host=dict.get('host'),
                             user=dict.get('user'),
                             passwd=dict.get('password'),
                             db=dict.get('database'))
        # 1st block
        if Cartype and Msrp < 1:
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                Query = buildQuery1(queryParams)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    return Response({'status': '404', 'error': 'The input doesnt\
    contain any matching records please give another input'})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print " Error in 1st block"
                return Response({'status': '404', 'error': """Error occure in cartype
score calculation block """})
            # print "am first block"
        # 2 nd block
        elif Cartype and Msrp > 1 and Stateid == 0 and MarketSegment == "" and Gender == "":
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Query = buildQuery2(queryParams)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records
found in block 2 Cartype and Msrp"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}

            except:
                print "Error in 2nd block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print "am second block"
        # 3 rd block
        elif Cartype and Msrp > 1 and MarketSegment and Stateid == 0 and Gender == "":
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                casefieldinputname = "segment1"
                casetablename = "s"
                Constant = 0.16
                casefieldoutputname = "segScore"
                fieldsname = ['mt.model,', 'mt.similarityScore,', 'mt.carType,',
                              's.Segment1,', 's.car_type,', 'l.StudentRank,', 'l.FamilyRank']
                Query = buildQuery3(
                    queryParams, fieldsname, casetablename, casefieldinputname, Constant, casefieldoutputname)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records
found in block 2 Cartype and Msrp"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}

            except:
                print "Error in 3nd block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print "am third block"
        # 4 th block
        elif Cartype and Msrp > 1 and Gender and Stateid == 0 and MarketSegment == "":

            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = 0.10
                casefieldoutputname = "sexscore"
                casefieldinputname = "sex"
                casetablename = "g"
                fieldsname = ['mt.model,', 'mt.similarityScore,', 'mt.carType']
                Query = buildQuery4(
                    queryParams, fieldsname, casetablename, casefieldinputname, Constant, casefieldoutputname)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 4 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 4nd block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print "am fourth block"
        # 5 th block
        elif Cartype and Msrp > 1 and Stateid > 0 and MarketSegment == "" and Gender == "":

            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = 0.10
                casefieldoutputname = "stateidscore"
                casefieldinputname = "stateid"
                casetablename = "l"
                fieldsname = [
                    'mt.model,', 'mt.similarityScore,', 'mt.carType,', 'mt.Msrp,', 'l.stateid']
                stateid = Stateid
                Query = buildQuery5(queryParams, fieldsname, casetablename,
                                    casefieldinputname, Constant, casefieldoutputname, stateid)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 5 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 5nd block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print 'hai am five'
        # 6 th block
        elif Cartype and Msrp > 1 and Stateid > 0 and MarketSegment and Gender:
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = [0.10, 0.10, 0.10]
                casefieldoutputname = ['segScore', 'genScore', 'stateidscore']
                casefieldinputname = ['Segment1', 'sex', 'stateid']
                casetablename = ['s', 'g', 'l']
                fieldsname = [
                    'mt.carType,', 'mt.similarityScore,', 'mt.Msrp,', 'l.stateid,', 'g.sex']
                stateid = Stateid
                gender = Gender
                Segment1 = MarketSegment
                Query = buildQuery6(queryParams, fieldsname, casetablename,
                                    casefieldinputname, Constant, casefieldoutputname, stateid, gender, Segment1)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 6 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 6th block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print 'hai am sixth'
        # 7 th block
        elif Cartype and Msrp > 1 and Stateid == 0 and MarketSegment and Gender:
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = [0.10, 0.10]
                casefieldoutputname = ['segScore', 'genScore']
                casefieldinputname = ['Segment1', 'sex']
                casetablename = ['s', 'g']
                fieldsname = ['mt.carType,', 'mt.similarityScore,', 'mt.Msrp,', 'g.sex,', 's.Segment1']
                gender = Gender
                Segment1 = MarketSegment
                Query = buildQuery7(queryParams,
                                    fieldsname,
                                    casetablename,
                                    casefieldinputname,
                                    Constant,
                                    casefieldoutputname,
                                    gender,
                                    Segment1)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 7 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 7th block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print 'hai am seventh'
        # 8 th block
        elif Cartype and Msrp > 1 and Stateid > 0 and MarketSegment and Gender == "":
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = [0.10, 0.10]
                casefieldoutputname = ['segScore', 'stateidscore']
                casefieldinputname = ['Segment1', 'stateid']
                casetablename = ['s', 'l']
                fieldsname = [
                    'mt.carType,', 'mt.similarityScore,', 'mt.Msrp,', 'l.stateid,', 's.Segment1']
                stateid = Stateid
                Segment1 = MarketSegment
                Query = buildQuery8(queryParams, fieldsname, casetablename,
                                    casefieldinputname, Constant, casefieldoutputname, stateid, Segment1)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 8 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 8th block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
            # print 'hai am eigth'
        # 9 nd block
        elif Cartype and Msrp > 1 and Stateid > 0 and MarketSegment == "" and Gender:
            try:
                queryParams = {}
                queryParams["cartype"] = Cartype
                queryParams["msrp"] = Msrp
                Constant = [0.10, 0.10]
                casefieldoutputname = ['genScore', 'stateidscore']
                casefieldinputname = ['sex', 'stateid']
                casetablename = ['g', 'l']
                fieldsname = [
                    'mt.carType,', 'mt.similarityScore,', 'mt.Msrp,', 'l.stateid,', 'g.sex']
                stateid = Stateid
                gender = Gender
                Query = buildQuery9(queryParams, fieldsname, casetablename,
                                    casefieldinputname, Constant, casefieldoutputname, stateid, gender)
                x1 = pd.read_sql("%s" % Query, db)
                if x1.empty:
                    print """there is no records \
found in block 9 Cartype and Msrp and Gender"""
                    return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
                else:
                    myJSON = x1.to_json(path_or_buf=None,
                                        orient='records',
                                        date_format='epoch',
                                        double_precision=10,
                                        force_ascii=True,
                                        date_unit='ms',
                                        default_handler=None)  # Attempt 1
                    myJSON = json.loads(myJSON)
                    myJSON = {'TopScoring': myJSON}
            except:
                print "Error in 9th block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
              # print 'hai am ninth'
        else:
            myJSON = {'error' : '404','Error' : 'there is no data'}
        return Response(myJSON)
