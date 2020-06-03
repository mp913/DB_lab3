import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

login = "postgres"
password = "intel_love2020"

database_name = 'gta_online_helper_template'
con = psycopg2.connect(
    dbname=database_name,
    user=login,
    host='127.0.0.1',
    password=password)

cur = con.cursor()
q_id = '2'
q_name = 'mission1'
qg_id = '1'
payment = '1000'

cur.execute("call insert_into_quest({qid}, '{qname}', {qgid}, {payment});".format(qid=q_id, qname=q_name, qgid=qg_id, payment=payment))
#print("call insert_into_quest_giver({qid}, '{qname}', {qgid}, {payment});".format(qid=q_id, qname=q_name, qgid=qg_id, payment=payment))

print("Insertion completed\n")


