import pandas as pd
import json


file_path = "test_excel.xlsx"

df = pd.read_excel(file_path)


tickets = []


for index, row in df.iterrows():
     comment_body = (
          f"Vin:{row.get('VIN','')}\n"
          f"Unit Number:{row.get('Unit','')}\n"
          f"technote:{row.get('Tech note on R','')}\n"
     )

     ticket = {
          "subject": row.get("Subject",""),
          "priority": row.get("Priority", "normal"),
          "assignee_id": row.get("Assignee ID", 0),
          "group_id": row.get("Group ID", 0),
          "comment":{
               "body":comment_body
          }
     }

     tickets.append(ticket)


final_json = {"tickets": tickets}

print(json.dumps(final_json, indent = 2))

