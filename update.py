import psycopg2
import sys

##Настриваю соединение с требующей обновления таблицей
con_to_updatable_table = psycopg2.connect(database='', user='', password='', host='', port='', sslmode='require')

cur_updatable = con_to_updatable_table.cursor()
cur_updatable_new = con_to_updatable_table.cursor()

## Настраиваю соединение с таблицей, чьими данными буду обновлять

con_to_table_from = psycopg2.connect(database='', user='', password='', host='', port='', sslmode='require')

cur_to_take_from = con_to_table_from.cursor()

def max_id(cur_updatable):
  query = """select max("id") from updatable_table"""
  cur_updatable.execute(query)
  result = cur_updatable.fetchone()[0]
  return result

counter = 0
for i in range (0, max_id(cur_updatable)):
  counter += 1
  query_updatable = """select date from updatable_table where id = {}""".format(i)
  result_updatable = cur_updatable.fetchone()[0]
  query_for_table_from = """select IPO, company_name where date_ipo = {}""".format(result_updatable)
  cur_to_take_from.execute(query_for_table_from)
  result_from = cur_to_take_from.fetchone
  try:
    IPO = str(result_from[0]).replace("'", '')
    company_name = str(result_from[1]).replace("'", '')
  except Exception as D:
    print(D)
  try:
    query_to_update = """update updatable_table set IPO = '{}', company_name = '{}' where id = '{}' """.format(IPO, company_name, i)
    cur_updatable_new.execute(query_to_update)
  except Exception as A:
  print(A)
  if counter %1000 == 0:
    sys.stdout.write("\r{}".format(counter))
    con_to_updatable_table.commit()
con_to_updatable_table.commit()
con_to_updatable_table.close()
  
