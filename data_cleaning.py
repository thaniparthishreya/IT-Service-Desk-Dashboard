import pandas as pd
import numpy as np
import random
import ast
df = pd.read_csv("data/raw_tickets.csv")
df['Ticket_ID'] = ['TCKT-' + str(i) for i in range(1, len(df)+1)]

start_date = pd.to_datetime("2025-01-01")
end_date = pd.to_datetime("2025-06-30")

df['Created_Date'] = pd.to_datetime(
    np.random.randint(start_date.value//10**9, end_date.value//10**9, len(df)),
    unit='s'
)

def generate_resolution_hours(priority):
    if priority in ['Critical','Urgent','High']:
        return random.randint(1, 24)
    elif priority == 'Medium':
        return random.randint(12, 48)
    else:
        return random.randint(24, 72)

df['Resolution_Hours'] = df['Priority'].apply(generate_resolution_hours)

df['Resolved_Date'] = df['Created_Date'] + pd.to_timedelta(df['Resolution_Hours'], unit='h')

df['Status'] = np.where(np.random.rand(len(df)) < 0.9, 'Closed', 'Open')
def check_sla(row):
    if row['Priority'] in ['Critical','Urgent']:
        return 'Met' if row['Resolution_Hours'] <= 6 else 'Breached'
    elif row['Priority'] == 'High':
        return 'Met' if row['Resolution_Hours'] <= 16 else 'Breached'
    elif row['Priority'] == 'Medium':
        return 'Met' if row['Resolution_Hours'] <= 24 else 'Breached'
    else:
        return 'Met' if row['Resolution_Hours'] <= 48 else 'Breached'

df['SLA_Status'] = df.apply(check_sla, axis=1)

df = df[['Ticket_ID','Created_Date','Resolved_Date','Status',
         'Department','Priority','Tags','Body','Resolution_Hours','SLA_Status']]

def clean_tags(tag):
    try:
        tag_list = ast.literal_eval(tag)  
        return ", ".join(tag_list)        
    except:
        return tag

df["Tags"] = df["Tags"].apply(clean_tags)

df.to_csv("data/cleaned_tickets.csv", index=False)

print("Cleaned dataset saved.")


