# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 17:00:28 2024

@author: 2305004
"""

import pandas as pd
from datetime import datetime
from datetime import timedelta
import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT

# 讀取txt檔案
with open('C:\\Users\\2305004\\Desktop\\Tool\\Plink\\test_output.txt', 'r') as file:
    lines = file.readlines()

# 建立空的data table
data = []
subject = ''
content = 'For the latest update.\n\n Last day log check:\n'
# 解析每一行資料
for line in lines:
    line = line.strip().split()
    if len(line) > 2:
        file_size = line[4]
        file_name = line[8]
        file_date = file_name[-8:]
        data.append([file_size, file_name,file_date])

# 建立data table
df = pd.DataFrame(data, columns=['File Size', 'File Name','File Date'])
df = df.assign(**{'File exist': ""})

df = df[df['File Size']!='0']
#df = df.drop(df[df['File Size'] == '0'].index)    
    


print(df)

timenow = datetime.now().strftime('%Y%m%d')
yesterday = (datetime.now()- timedelta(days=1)).strftime('%Y-%m-%d')
#sixmonago = datetime.now() - timedelta(days=199)
sixmonago = datetime.now() - timedelta(days=5)
print("Targe date: ",sixmonago.strftime('%Y%m%d'))
print('---------------------------\n')


def find_date_in_column(data_table, column_index, target_date):

    print ('Data Table1=\n',data_table)
    for index, row in data_table.iterrows():
          #  print ('Data table2=\n',data_table)      
          #  print("row1=" ,row)
            date_str = row['File Date']
            print("row index =", index)
            print("Data_STR = ", date_str)
            try:
                target_date_str = target_date.strftime('%Y%m%d')
                if (date_str == target_date_str) and (int(row['File Size']) > 0):  # 比較日期並檢查 'File Size'
                    data_table.loc[index, 'File exist'] = 'OK'
                    print("Date: ", date_str)
                    return True
            except (ValueError, TypeError):
                pass  # 忽略無法轉換為日期的字串或其他錯誤

    return False

#find_date_in_column(df, 2, sixmonago)
date_exists = find_date_in_column(df,1, datetime.now() - timedelta(days=1))

if date_exists:
    print("%f 日期存在於指定欄位中",yesterday)
    subject+=f"[Backup Success] {yesterday} Check for logs"
    content+=f"備份檔案： {yesterday}  存在於備份中\n\n\n"
    content+=f"{df}\n\n"
else:
    print("%f日期不存在於指定欄位中",yesterday)
    subject+=f"[Backup Fail] {yesterday} Firewall Backup Check"
    content+=f"{yesterday} 不存在於備份中\n\n\n"
    content+="現有備份資料如下： \n"
    content+=f"{df[['File Size','File Name']]}\n\n"
#print('\nUpdated Data Table:')

#for row2 in df:
print(df)


def find_missing_logs(data_table, column_index, start_date, end_date):
    existing_dates = set()  # 使用集合來存儲已存在的日期，避免重複
  
    for row in data_table:
        date_str2 = row
       # if date_str2
        transday = datetime.strptime(date_str2, "%Y%m%d").date()
        print("find missing date_str=",transday)
        print("find missing start date=",start_date)
        print("find missing end date=",end_date)
        try:
         #   date = datetime.strptime(date_str2, "%Y%m%d")  # 將日期字串轉換為datetime物件
                
          #  if start_date <= date.date() <= end_date:  # 檢查日期是否在範圍內
            if start_date <= transday <= end_date:  # 檢查日期是否在範圍內
                existing_dates.add(transday)
                print("find missing date=",transday)
                print("find missing start date=",start_date)
                print("find missing end date=",end_date)

        except ValueError:
            pass  # 忽略無法轉換為日期的字串或其他錯誤
    
    #missing_dates = [date_in_range for date_in_range in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)) if date_in_range not in existing_dates]
    missing_dates = []
    date_generator = (start_date + timedelta(n) for n in range((end_date - start_date).days + 1))

    for date_in_range in date_generator:
        if date_in_range not in existing_dates:
            missing_dates.append(date_in_range)
            
    return missing_dates

#print(timenow) 

###############################記得改成6個月前
target_start_date = datetime(2024, 2, 1).date()  # 起始日期
#target_start_date = sixmonago.date()  # 起始日期
target_end_date = datetime.now().date()  # 結束日期（當前日期）





print("target_start_date",target_start_date)
print("target_end_date",target_end_date)

missing_dates = find_missing_logs(df['File Date'], 0, target_start_date, target_end_date)

#content += '\n\nMissing logs for dates:\n'
content += f"\n\n應保存有{sixmonago.strftime('%Y-%m-%d')} 之備份\n"

if missing_dates:
    print("Missing Dates:")
    content += "以下為缺少資料：\n"
    for missing_date in missing_dates:
        print(missing_date.strftime("%Y%m%d"))
        
        content += f"- {missing_date.strftime('%Y-%m-%d')}\n"
else:
    print("All dates are present.")
    content+="All dates are present.\n"
    




#======================Email=================
APP_ID = '10040737-dc21-48af-9fb6-f6603ecb5979'
SCOPES = ['Mail.Send']

access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

endpoint = GRAPH_API_ENDPOINT + '/me/sendMail'
# endpoint = GRAPH_API_ENDPOINT + '/user/<emial address>'

request_body = {
    'message': {
        'toRecipients': [
            {
                'emailAddress': {
                    'address': 'liam.huang@iisigroup.com',
                    'name': 'Liam Huang'
                }
                
            },
            {
                'emailAddress': {
                    'address': 'liamhuang1994@gmail.com',
                    'name': 'Liam Huang'
                }
                
            }
        ],
        #'subject': 'Check for logs ',
        'body': {
            'contentType': 'text', # or html
            
        },
        'importance': 'High'
    }
}
request_body['message']['subject'] = subject
request_body['message']['body']['content'] = content
print(request_body)
response = requests.post(endpoint, headers=headers, json=request_body)
print(response.status_code)