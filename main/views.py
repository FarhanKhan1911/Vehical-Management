from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import json 
# Create your views here.

########################################################
########### Generating Filtereated Dataframe ###########  
########################################################

def filtering_dataframe():

    #Reading excel sheet data into dataframe with no header
    df1 = pd.read_excel('data/April-2021.xlsx',header = None)
    df2 = pd.read_excel('data/May-2021.xlsx',header = None)
    df3 = pd.read_excel('data/June-2021.xlsx',header = None)

    # Assigning column header to each columns
    df1.columns = ["Sr_No", "Vehicle_Class", "Total"]
    df2.columns = ["Sr_No", "Vehicle_Class", "Total"]
    df3.columns = ["Sr_No", "Vehicle_Class", "Total"]

    # Droping Serial column
    df1.drop('Sr_No',inplace=True,axis='columns')
    df2.drop('Sr_No',inplace=True,axis='columns')
    df3.drop('Sr_No',inplace=True,axis='columns')

    # Dropping first 3 row of each dataframe
    df1.drop([0,1,2],inplace=True,axis='rows')
    df2.drop([0,1,2],inplace=True,axis='rows')
    df3.drop([0,1,2],inplace=True,axis='rows')
    
    # Mergining all 3 dataframe on 'Vehicle_Class'column with 'how' = outer so that we can get all data in final dataframe
    merged = df1.merge(df2,on='Vehicle_Class',how='outer').merge(df3,on='Vehicle_Class',how='outer')
    merged.columns = ['Vehicle_Class','April_Total','May_Total','June_Total']

    # returning merged dataframe
    return merged

##################################
########### DOWNLOAD #############  
##################################

def download(request):
    # Calling filtering_dataframe() 
    download_data = filtering_dataframe()

    #filling empty cell with 0
    download_data.fillna(0)

    # Renaming columns headers
    download_data.columns = ['Vehicle Class','April Total','May Total','June Total']

    # Making http response with content type of text/csv
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename=vehicle.csv'
    download_data.to_csv(path_or_buf=res)

    return res

##################################
########### VIEW DATA ############  
##################################

def homepage(request):

    # Calling filtering_dataframe()
    df = filtering_dataframe()

    # Reset the index and converting into JSON format
    json_record = df.reset_index().to_json(orient ='records') 
    datas = [] 
    # Load the JSON in the list
    datas = json.loads(json_record) 
    context = {'data': datas} 
    return render(request, "main/index.html", context)