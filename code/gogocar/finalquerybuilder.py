# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:03:18 2016

"""
from numpy.core.test_rational import denominator


def buildQuery1(Queryparams):
    Attr = [key for key, value in Queryparams.items()
            if (value != 0 and value != '')]
    print Attr
    if (len(Attr) == 1 and Attr[0] == 'CarType') or (
                                                     len(Attr) == 2 and
                                                     Attr[0] == 'CarType' and
                                                     Attr[1] == 'Msrp'
                                                     ):
        print "Cartype table"
        SelectStat = "SELECT model ,similarityScore AS DistanceScore,\
carType,Msrp from car_type_table1 "
    elif Queryparams['city_mpg'] != 0 or Queryparams['highway_mpg'] != 0:
        print 'mpg case'
        SelectStat = "SELECT model ,similarityScore AS DistanceScore,\
carType,Msrp from car_type_table1 "
    elif len(Attr) == 1 and (Queryparams['Model_Name'] != '' or Queryparams['make'] != ''):
        SelectStat = 'Select model,\
similarityScore,carType from master_table1'
    elif len(Attr) == 2 and Queryparams[
                                        'Model_Name'
                                        ] != '' and Queryparams[
                                                                'make'
                                                                ] != '':
        SelectStat = 'Select model,\
similarityScore,carType from master_table1'
    elif len(Attr) == 3 and Queryparams[
                                        'Model_Name'
                                        ] != '' and Queryparams[
                                                                'make'
                                                                ] != '' and Queryparams['CarType'] != '':
        SelectStat = 'Select model,\
similarityScore,carType from master_table1'
    else:
        print 'final score table'
        carType = Queryparams['CarType']
        zipcode = Queryparams["zipCode"]
        label = Queryparams["label"]
        Gender = Queryparams["gender"]
        maritalstatus = Queryparams['MaritalStatus']
        emplyr = Queryparams['employer']
        profesionalqualification = Queryparams['prof_qualification']
        SelectStat = "SELECT Msrp,model,carType"
        if ("carType" in Queryparams) and carType != "":
            SelectStat += " , " if len(SelectStat) > 0 else ""
            SelectStat += " carType "
        if zipcode != 0 or label != 0 or Gender != "" or maritalstatus != "" or emplyr != "":
            SelectStat += ",("
        if zipcode != 0:
            SelectStat += "zipScore"
        if Gender != "":
            if SelectStat.endswith('Score'):
                SelectStat += "+genderScore"
            else:
                SelectStat += 'genderScore'
        if maritalstatus != "":
            if SelectStat.endswith('Score'):
                SelectStat += "+maritalstatusScore"
            else:
                SelectStat += 'maritalstatusScore'
        if emplyr != "":
            if SelectStat.endswith('Score'):
                SelectStat += "+employerScore"
            else:
                SelectStat += 'employerScore'
        if profesionalqualification != '':
            if SelectStat.endswith('Score'):
                SelectStat += "+qualificationScore"
            else:
                SelectStat += 'qualificationScore'
        if label != 0:
            if SelectStat.endswith('Score'):
                SelectStat += "+ageScore"
            else:
                SelectStat += 'ageScore'
        if zipcode != 0 or label != 0 or Gender != '' or maritalstatus != '' or emplyr != '':
            denominator_list = [zipcode, label, Gender, maritalstatus, emplyr]
            denominator_list = [i for i in denominator_list if (i>0)]
            denominator_list = [i for i in denominator_list if (i!='')]
            #print denominator_list
            denominator = len(denominator_list)
            if denominator == 0 or denominator < 0:
                denominator = 1
            SelectStat += ")/%s AS similarityScore" % (denominator)
        conditions123 = " FROM final_score_table"
        SelectStat = SelectStat+conditions123
        print 'length', len(Queryparams)
    conditions = ""
    if ("Msrp" in Queryparams) and Queryparams['Msrp'] != 0:
        conditions += " AND " if len(conditions) > 0 else ""
        budget = Queryparams['Msrp']
        budget_high = budget + 0.4*budget
        budget_low = 0.75*budget
        conditions += " Msrp > %s AND Msrp < %s" % (budget_low, budget_high)
    if ("city_mpg" in Queryparams) and Queryparams['city_mpg'] != 0:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " city_mpg > %s " % (Queryparams['city_mpg'])
    if ("highway_mpg" in Queryparams) and Queryparams['highway_mpg'] != 0:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += "highway_mpg > %s " % (Queryparams['highway_mpg'])
    if ("zipCode" in Queryparams) and Queryparams['zipCode'] != 0:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " zipCode = %s" % Queryparams["zipCode"]
    if ("label" in Queryparams) and Queryparams['label'] != 0:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " label = %s" % Queryparams["label"]
    if ("gender" in Queryparams) and Queryparams['g\
ender'] != '' and not Queryparams['gender'].isdigit():
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " gender = '%s' " % Queryparams["gender"]
    if ("MaritalStatus" in Queryparams) and Queryparams['M\
aritalStatus'] != '' and not Queryparams['MaritalStatus'].isdigit():
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " MaritalStatus = '%s' " % Queryparams["MaritalStatus"]
    if ("employer" in Queryparams) and Queryparams['e\
mployer'] != ''and not Queryparams['employer'].isdigit():
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " employer = '%s' " % Queryparams["employer"]
    if ("prof_qualification" in Queryparams) and Queryparams['p\
rof_qualification'] != '' and not Queryparams['prof_qualification'].isdigit():
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " prof_qualification\
 = '%s' " % Queryparams["prof_qualification"]
    if ("CarType" in Queryparams) and Queryparams['CarType'] != '' and Queryparams['Model_Name'] == '':
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += "carType = '%s' " % Queryparams["CarType"]
    if Queryparams['CarType'] != '' and Queryparams['Model_Name'] != '' and Queryparams['make'] != '':
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += " Make_Name = '%s' AND Testmodel = '%s' AND carType = \
'%s' " % (Queryparams["make"], Queryparams['Model_Name'], Queryparams['CarType'])
    if ('Model_Name' in Queryparams) and Queryparams[
                                                     'Model_Name'
                                                     ] != '' and Attr[0] == '\
Model_Name':
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += "Testmodel ='%s' AND DistanceScore > 0 " % Queryparams['Model_Name'] 
    elif ('make' in Queryparams) and Queryparams['make'] != '' and len(Attr) == 1:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += "Make_Name ='%s' AND DistanceScore > 0" % Queryparams['make']
    elif Queryparams[
                     'Model_Name'
                     ] != '' and Queryparams[
                                             'make'
                                             ] != '' and len(Attr) == 2:
        conditions += " AND " if len(conditions) > 0 else ""
        conditions += "Testmodel ='%s' AND Make_Name = '%s' AND DistanceScore > 0 " % (Queryparams['Model_Name'],Queryparams['make'])
    conditions += " order by similarityScore DESC"
    conditions = (" WHERE " if len(conditions) > 0 else "") + conditions
    a = SelectStat+conditions
    return (a)
