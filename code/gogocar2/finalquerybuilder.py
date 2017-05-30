# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:03:18 2016

@author: dhiwakar
"""



#1 query builder


  
def buildQuery1(Queryparams):
    ColNames=""
    
    SelectStat="SELECT model ,similarityScore,carType,Msrp  from master_table2 "
    where="where"
    conditions=""
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " carType='%s'" % Queryparams["cartype"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    a=SelectStat+conditions   
    
    return (a)



#2 query builder


def buildQuery2(Queryparams):
    ColNames=""
    
    SelectStat="SELECT model ,similarityScore,carType,Msrp from master_table2 "
    where="where"
    conditions=""
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " carType='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    a=SelectStat+conditions

    return (a)




 #case block:

def case(c,d,a,b):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(d,c,a,b)
      return casestatement



#3rd Block

def buildQuery3(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname):
    ColNames=""
    SelectStat1="select *,(car.segScore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case=case(casetablename,casefieldinputname,Constant,casefieldoutputname)
    fromvalue=" FROM  master_table2 AS mt LEFT JOIN rank_data l ON mt.model = l.car_type LEFT JOIN  segment s ON mt.model = s.car_type "
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction= " AND TRIM(TRAILING CHAR(13) FROM s.segment1) = 'Family') as car"
    result =SelectStat1+case+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fieldsname[5]+fieldsname[6]+fromvalue+conditions+trimfuction
    return(result)
    
 #4th Block


def buildQuery4(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname):
    ColNames="" 
    SelectStat1="select *,(car.sexscore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case=case(casetablename,casefieldinputname,Constant,casefieldoutputname)
    fromvalue=" FROM  master_table2 AS mt LEFT JOIN gender g ON mt.model = g.car_type "
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction="  and  TRIM(TRAILING CHAR(13) FROM g.sex) = 'Female') as car"    
    result =SelectStat1+case+fieldsname[0]+fieldsname[1]+fieldsname[2]+fromvalue+conditions+trimfuction
    return(result)
        
#5th Block
    
def buildQuery5(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname,stateid):
    ColNames="" 
    SelectStat1="select *,(car.stateidscore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case=case(casetablename,casefieldinputname,Constant,casefieldoutputname)
    fromvalue=" FROM master_table2 AS mt LEFT JOIN location l ON mt.model = l.model"
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction="  AND l.stateid = %s) as car"%stateid
    result =SelectStat1+case+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fromvalue+conditions+trimfuction
    return(result)
      

#6th Block
    

def buildQuery6(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname,stateid,gender,Segment1):
    ColNames="" 
    SelectStat1="select *,(car.stateidscore+car.genScore+car.segScore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case1=case(casetablename[0],casefieldinputname[0],Constant[0],casefieldoutputname[0])
    case2=case(casetablename[1],casefieldinputname[1],Constant[1],casefieldoutputname[1])
    case3=case(casetablename[2],casefieldinputname[2],Constant[2],casefieldoutputname[2])
    fromvalue=" FROM  master_table2 AS mt  LEFT JOIN location l ON mt.model = l.model AND l.stateid = %s LEFT JOIN segment s ON mt.model = s.car_type and TRIM(TRAILING char(13) FROM s.Segment1)='%s' LEFT JOIN gender g ON mt.model = g.car_type and TRIM(TRAILING char(13) FROM g.sex)='%s'"%(stateid,Segment1,gender)
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction=" ) as car"  
    result =SelectStat1+case1+case2+case3+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fromvalue+conditions+trimfuction
    return(result)
#7th Block   Cartype and Msrp >1 and Stateid ==0 and  MarketSegment and Gender :

def buildQuery7(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname,gender,Segment1):
    ColNames="" 
    SelectStat1="select *,(car.genScore+car.segScore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case1=case(casetablename[0],casefieldinputname[0],Constant[0],casefieldoutputname[0])
    case2=case(casetablename[1],casefieldinputname[1],Constant[1],casefieldoutputname[1])
    
    fromvalue=" FROM  master_table2 AS mt  LEFT JOIN segment s ON mt.model = s.car_type and TRIM(TRAILING char(13) FROM s.Segment1)='%s' LEFT JOIN gender g ON mt.model = g.car_type and TRIM(TRAILING char(13) FROM g.sex)='%s'"%(Segment1,gender)
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction=" ) as car"  
    result =SelectStat1+case1+case2+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fromvalue+conditions+trimfuction
    return(result)

    
#8th block  Cartype and Msrp >1 and Stateid >0 and  MarketSegment and Gender=="": 
    
def buildQuery8(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname,stateid,Segment1):
    ColNames="" 
    SelectStat1="select *,(car.stateidscore+car.segScore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case1=case(casetablename[0],casefieldinputname[0],Constant[0],casefieldoutputname[0])
    case2=case(casetablename[1],casefieldinputname[1],Constant[1],casefieldoutputname[1])
   
    fromvalue=" FROM  master_table2 AS mt  LEFT JOIN location l ON mt.model = l.model AND l.stateid = %s LEFT JOIN segment s ON mt.model = s.car_type and TRIM(TRAILING char(13) FROM s.Segment1)='%s'"%(stateid,Segment1)
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction=" ) as car"  
    result =SelectStat1+case1+case2+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fromvalue+conditions+trimfuction
    return(result)
#9th block Cartype and Msrp >1 and Stateid >0 and  MarketSegment=="" and Gender:   
def buildQuery9(Queryparams,fieldsname,casetablename,casefieldinputname,Constant,casefieldoutputname,stateid,sex):
    ColNames="" 
    SelectStat1="select *,(car.stateidscore+car.genScore+car.similarityScore) as overallScore from (SELECT "
    where="where"
    conditions=""
    def case(casetablename,casefieldinputname,Constant,casefieldoutputname):
      casestatement=" CASE WHEN %s.%s IS NULL THEN 0 ELSE %s END AS %s ,"%(casetablename,casefieldinputname,Constant,casefieldoutputname)
      return casestatement
    case1=case(casetablename[0],casefieldinputname[0],Constant[0],casefieldoutputname[0])
    case2=case(casetablename[1],casefieldinputname[1],Constant[1],casefieldoutputname[1])
    fromvalue=" FROM  master_table2 AS mt  LEFT JOIN location l ON mt.model = l.model AND l.stateid = %s LEFT JOIN gender g ON mt.model = g.car_type and TRIM(TRAILING char(13) FROM g.sex)='%s'"%(stateid,sex)
    if (Queryparams.has_key("cartype")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " mt.type='%s'" % Queryparams["cartype"]
    if (Queryparams.has_key("msrp")):
        conditions+=" AND " if len(conditions)>0 else ""
        conditions+= " msrp<%s" % Queryparams["msrp"]
    conditions=(" WHERE " if len(conditions)>0 else "") + conditions
    trimfuction=" ) as car"  
    result =SelectStat1+case1+case2+fieldsname[0]+fieldsname[1]+fieldsname[2]+fieldsname[3]+fieldsname[4]+fromvalue+conditions+trimfuction
    return(result)
    