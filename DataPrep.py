#%% Import Packages
import pandas as pd
import numpy as np
import os
#%% Where the data is located
path = r'C:\Users\victo\OneDrive - University of Texas at San Antonio\Classes\Semester 5\Web GIS\FinalProject\Data'
os.chdir(path)

#%% Filtering Schools
hd = pd.read_csv('hd2019.csv', encoding = "ISO-8859-1")

hd1 = hd[["UNITID",'INSTNM','CITY','LONGITUD',"LATITUDE",
          "GROFFER","WEBADDR","CYACTIVE",]] #Variables of interest based on data plan

hd2 = hd1.loc[(hd1["GROFFER"] == 1) & (hd1["CYACTIVE"] == 1)] #Only interested in Active Graduate Schools

#Fixing Website variable all variables need https://
def httpscorrector(vector):
    """
    Parameters
    ----------
    vector : string itrrable

    Returns
    -------
    corrected : list
        string list that contains all the vector but with https:// in it

    """
    corrected = []
    for i in vector:
        if "https://" not in i:
            corrected.append("https://" + i) #Adds https:// to each string
        else:
            corrected.append(i)
    return corrected
hd2["WEBADDR"] = httpscorrector(hd2["WEBADDR"])

key = np.array(hd2["UNITID"]) #Schools of interest

#%% School Cost Info
ic = pd.read_csv("ic2019_ay.csv")

ic1 = ic.loc[[x in key for x in ic["UNITID"]]] # Schools of Interest in the ic data

ic2 = ic1[["UNITID","TUITION6","FEE6","TUITION7","FEE7"]] #Interested in Graduate School Costs

#%% Demographics
effy = pd.read_csv("effy2019.csv")

effy1 = effy.loc[effy["EFFYLEV"] == 4] #Only Graduate School Rows

effy2 = effy1.loc[[x in key for x in effy1["UNITID"]]] #Only Schools of Interest

effy3 = effy2[["UNITID","EFFYLEV",'EFYTOTLT',"EFYTOTLM","EFYTOTLW",
              'EFYASIAT',"EFYBKAAT","EFYHISPT"]]

#Calculate Demographic Percentages
effy3["Percent_Male"] = np.round(effy3["EFYTOTLM"]/effy3["EFYTOTLT"]*100) #Calculating Percent Male

effy3["Percent_Female"] = np.round(effy3["EFYTOTLW"]/effy3["EFYTOTLT"]*100) #Calculating Percent Female

effy3["Percent_Asian"] = np.round(effy3["EFYASIAT"]/effy3["EFYTOTLT"]*100) #Calculating Percent Asian

effy3["Percent_Black"] = np.round(effy3["EFYBKAAT"]/effy3["EFYTOTLT"]*100) #Calculating Percent Black

effy3["Percent_Hispanic"] = np.round(effy3["EFYHISPT"]/effy3["EFYTOTLT"]*100) #Calculating Percent Hispanic

#%% Graduation Infomation
gr = pd.read_csv("gr200_19.csv")

gr1 = gr.loc[[x in key for x in gr["UNITID"]]] #Big drop off here.

gr2 = gr1[["UNITID","BAGR100","BAGR150"]]

#%% Merge All Data 

merge1=pd.merge(hd2,ic2, how = "outer", on = "UNITID")

merge2= pd.merge(merge1,effy3, how = "outer", on = "UNITID")

merge3 = pd.merge(merge2, gr2, how = "outer", on = "UNITID")

#%% Save Data as CSV
merge3.to_csv("GraduateSchoolData.csv")