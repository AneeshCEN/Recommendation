from django.shortcuts import render

# Create your views here.
import numpy as np
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import scipy as sp
import pandas as pd
from pandas import DataFrame
import json
import MySQLdb
from pandas.io import sql
from python_mysql_dbconfig import read_db_config


@permission_classes((permissions.AllowAny,))
class GoGoCarScore(viewsets.ViewSet):

    def list(self, request):
        Cartype = ""
        if ("Cartype" in request.query_params) and len(request.query_params['Cartype'])>0:
            Cartype = request.query_params['Cartype']
        else:
            return Response({'status': 'ERROR', 'error': 'Please \
Enter a Cartype '})
        Cartype = str(Cartype)
         
        if not ("budget" in request.query_params):
                return Response({'status':'ERROR','error':'Please Enter a budget'})   
        else:
            budget=request.query_params['budget']
#         try:
        if not budget.isdigit():
            return Response({'status':'ERROR','error':'Please Enter a valid budget'})
#         except:
#                 return Response({'status':'ERROR','error':'NO_budget_SPECIFIED'})
            
        if not ("zipcode" in request.query_params):
            return Response({'status':'ERROR','error':'Please Enter a zipcode'})
        else:
            zipcode=request.query_params['zipcode']
        
        if not request.query_params['zipcode'].isdigit():
            return Response({'status':'ERROR','error':'Please Enter a valid zipcode'})

         
        if ("userid" in request.query_params):
            if not request.query_params['userid'].isdigit():
                return Response({'status': 'ERROR', 'error': 'Please \
Enter a valid userid '})
            else:
                userid = request.query_params['userid']
            
        if ("age" in request.query_params):
            if not request.query_params['age'].isdigit():
                return Response({'status': 'ERROR', 'error': 'Please \
Enter a valid age '})
            else:
                age = int(request.query_params['age'])
                
        else:
            age = 0
        
        if ('maritialstatus' in request.query_params):
            maritialstatus = str(request.query_params['maritialstatus'])
      
        
        if ('Employer' in request.query_params):
            emplyr = str(request.query_params['Employer'])
 
        if ('profesionalqualification' in request.query_params):
            profesionalqualification = str(request.query_params['profesionalqualification'])
    
        if ("gender" in request.query_params):
            Gender = str(request.query_params['gender'])
        else:
            Gender = ""

        
        try:
                age=int(age)
                
                if age<35:
                   label = 1
                elif 35<=age<45:
                   label = 2
                elif 45<=age<55:
                   label = 3
                elif age>=55:
                   label = 4
                else:
                    label = 1 
        
                budget=int(budget)
                #budget_low=budget-0.05*budget 
                budget_high=budget+0.05*budget  
                 
        except:
                print "Error in assignment block"
                return Response({'status': '404', 'error': """Error occure in cartype
 score calculation block"""})
        dict = read_db_config()

        db = MySQLdb.connect(host=dict.get('host'),
                             user=dict.get('user'),
                             passwd=dict.get('password'),
                             db=dict.get('database'))
        # 1st block
        if Cartype and budget > 1 and zipcode > 1 and age == 0 and Gender == "":
            
            try:

                x1 =pd.read_sql("SELECT  Msrp,model,TRIM(TRAILING CHAR(13) FROM carType) as carType,zipScore AS similarityScore FROM master_table3 WHERE  TRIM(TRAILING CHAR(13) FROM carType) = '%s' AND Msrp < %s AND zipCode = %s" %(Cartype,budget_high,zipcode) , db )
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
                return Response({'status': '404', 'error': """No Suitable\
                Recommendation """})
            
            #print "am first block"
        # 2 nd block
        elif  Cartype and budget > 1 and zipcode > 1 and age > 1 and Gender:
            
            try:

                x1 =pd.read_sql("SELECT Msrp,model,TRIM(TRAILING CHAR(13) FROM carType) as carType,(zipScore + genderScore + ageScore) / 2.5 AS similarityScore FROM   master_table3 WHERE  TRIM(TRAILING CHAR(13) FROM carType) = '%s' AND Msrp < %s AND zipCode = %s  AND label = %s AND gender = '%s'" %(Cartype,budget_high, zipcode, label, Gender), db )
                if x1.empty:
                    print """there is no records
found in block 2 Cartype and Msrp"""
                    return Response({'status': '404', 'error': """No Suitable\
 Recommendation"""})
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
                return Response({'status': '404', 'error': """Error occured in cartype
 score calculation block"""})
            
            #print "am second block"
        else:
            myJSON = {'error' : '404','Error' : 'Please enter both age and gender'}
        return Response(myJSON)
