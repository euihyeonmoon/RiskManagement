import numpy as np
import pandas as pd

#importing datetime libarary
import datetime
from datetime import date, timedelta

#
from collections import defaultdict

df = pd.read_excel('googling_filtered.xlsx')
df['Date'] = [datetime.datetime.strptime(x ,'%b %d, %Y') for x in df['Date']]
df['Date'] = [x.to_pydatetime().date() for x in df['Date']]

#searching datas within 30 days
end_date = date.today()
start_date = end_date - datetime.timedelta(days=30)

def risk_cal(df = df, startdate = start_date, enddate = end_date):
    # Search the data recorded within 30days in a speicific country
    mask = (df['Date'] >= startdate) & (df['Date'] <= enddate)
    df = df[mask]    
    #make an empty dictionary
    factor_dict = defaultdict(list)
    for time in df['Date'].unique():
        frequency_factor = len(df[df['Date'] == time])        
        
        time_factor = enddate - time
        time_factor = time_factor / timedelta (days=1)
        time_factor = 1 / ( time_factor + 1 )
        
        factor_dict['Date'].append(time)
        factor_dict['factor'].append(frequency_factor * time_factor)
    factor_frame = pd.DataFrame(factor_dict)
    if factor_frame.empty:
        return None    
    risk = factor_frame['factor'].sum() * 100
    return risk



Risk_Score = defaultdict(list)
while start_date <= end_date:
    dates = start_date #.strftime("%Y-%m-%d")
    print(dates , risk_cal(df = df, startdate = start_date, enddate = end_date))        
    Risk_Score['Date'].append(dates)
    Risk_Score['Risk_Score'].append(risk_cal(df = df, enddate = dates))
    start_date += datetime.timedelta(days=1)
        
Risk_Score = pd.DataFrame(Risk_Score)
Risk_Score.set_index('Date', inplace = True)
Risk_Score.fillna(0, inplace = True)

Risk_Score.to_excel('Risk_Score.xlsx')

print("Scoring is Done")