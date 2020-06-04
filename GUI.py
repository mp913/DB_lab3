import log_in
import datetime
import math
import matplotlib.pyplot as plt
from numpy import polyfit as pf
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tkinter import *
from tkinter import scrolledtext

login = ""
password = ""


def log_in_function():
    log_in_window = Toplevel(main_window)
    log_in_window.title("authorization")
    log_in_window.geometry('270x150')

    label_login = Label(log_in_window, text="Login:")
    label_login.grid(column=0, row=0)

    input_text_box_login = Entry(log_in_window, justify=CENTER)
    input_text_box_login.grid(column=1, row=0)

    label_password = Label(log_in_window, text="Password:")
    label_password.grid(column=0, row=1)

    input_text_box_password = Entry(log_in_window, justify=CENTER)
    input_text_box_password.grid(column=1, row=1)

    log_text_box = scrolledtext.ScrolledText(log_in_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=4, rowspan=1, sticky=S + W + E)

    def log_in_internal():
        global login
        global password
        login = input_text_box_login.get()
        password = input_text_box_password.get()
        log_text_box.insert(END, "Authorization completed\n")

    log_in_button = Button(log_in_window, text="Log in", command=log_in_internal)
    log_in_button.grid(column=0, row=3)


def show_tables_content_function():
    show_database_content_window = Toplevel(main_window)
    show_database_content_window.title("Database viewer")
    show_database_content_window.geometry('400x400')

    label_database_name = Label(show_database_content_window, text="Database name:")
    label_database_name.grid(column=0, row=0)

    input_text_box_database_name = Entry(show_database_content_window, justify=CENTER)
    input_text_box_database_name.grid(column=1, row=0)

    log_text_box = scrolledtext.ScrolledText(show_database_content_window, width=100, height=10)
    log_text_box.grid(column=0, columnspan=7, row=2, rowspan=1, sticky=S + W + E)

    def show_database_content_internal():
        global login
        global password
        database_name = input_text_box_database_name.get()
        try:
            con = psycopg2.connect(
                dbname=database_name,
                user=login,
                host='127.0.0.1',
                password=password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('select select_all_from_quest_giver()')
            table = cur.fetchall()
            log_text_box.insert(END, 'Quest givers:\n')
            log_text_box.insert(END, ' id |    name    | quests amount\n')
            for line in table:
                line = line[0][1:-1:].split(',')

                qg_id = line[0]
                qg_name = line[1]
                qg_count = line[2]

                qg_id = ' ' * max(0, 4-len(qg_id)) + qg_id[:4:]
                qg_name = ' ' * max(0, 12-len(qg_name)) + qg_name[:12:]
                qg_count = ' ' + qg_count

                log_text_box.insert(END, qg_id + '|' + qg_name + '|' + qg_count)
                log_text_box.insert(END, '\n')
            log_text_box.insert(END, '\n\n')

            cur.execute('select select_all_from_quest()')
            table = cur.fetchall()
            log_text_box.insert(END, 'Quests:\n')
            log_text_box.insert(END, ' id |    name    | owner id | payment\n')
            for line in table:
                line = line[0][1:-1:].split(',')

                q_id = line[0]
                q_name = line[1]
                qg_id = line[2]
                q_payment = line[3]

                q_id = ' ' * max(0, 4 - len(q_id)) + q_id[:4:]
                q_name = ' ' * max(0, 12 - len(q_name)) + q_name[:12:]
                qg_id = ' ' * max(0, 10 - len(qg_id)) + qg_id[:10:]
                q_payment = ' ' + q_payment

                log_text_box.insert(END, q_id + '|' + q_name + '|' + qg_id + '|' + q_payment)
                log_text_box.insert(END, '\n')

            log_text_box.insert(END, '\n\n')

            cur.close()
            con.close()
        except:
            log_text_box.insert(END, 'Permission denied\n')

    show_database_content_button = Button(show_database_content_window,
                                          text="Show database content",
                                          command=show_database_content_internal)
    show_database_content_button.grid(column=0, row=1)


def clean_tables_function():
    clean_table_window = Toplevel(main_window)
    clean_table_window.title("Database cleaner")
    clean_table_window.geometry('400x400')

    label_database_name = Label(clean_table_window, text="Database name:")
    label_database_name.grid(column=0, row=0)

    input_text_box_database_name = Entry(clean_table_window, justify=CENTER)
    input_text_box_database_name.grid(column=1, row=0)

    label_table_name = Label(clean_table_window, text="Table name:")
    label_table_name.grid(column=0, row=1)

    input_text_box_table_name = Entry(clean_table_window, justify=CENTER)
    input_text_box_table_name.grid(column=1, row=1)

    log_text_box = scrolledtext.ScrolledText(clean_table_window, width=100, height=10)
    log_text_box.grid(column=0, columnspan=7, row=3, rowspan=1, sticky=S + W + E)

    def clean_table_internal():
        global login
        global password
        database_name = input_text_box_database_name.get()
        table_name = input_text_box_table_name.get()
        try:
            con = psycopg2.connect(
                dbname=database_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()
            if table_name == 'quest':
                cur.execute('call clean_quest_table()')
            elif table_name == 'quest_giver':
                cur.execute('call clean_quest_giver_table()')
            con.commit()
            con.close()
            cur.close()
            log_text_box.insert(END, 'Clean completed\n')
        except:
            log_text_box.insert(END, 'Permission denied\n')

    def clean_all_tables():
        global login
        global password
        database_name = input_text_box_database_name.get()
        try:
            con = psycopg2.connect(
                dbname=database_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()
            cur.execute('call clean_quest_giver_table()')
            cur.execute('call clean_quest_table()')
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, 'Clean completed\n')
        except:
            log_text_box.insert(END, 'Clean failed\n')

    clean_table_button = Button(clean_table_window,
                                          text="Clean table",
                                          command=clean_table_internal)
    clean_table_button.grid(column=0, row=2)

    clean_all_tables_button = Button(clean_table_window,
                                text="Clean all tables",
                                command=clean_all_tables)
    clean_all_tables_button.grid(column=1, row=2)


def insert_into_quest_giver_function():
    insert_window = Toplevel(main_window)
    insert_window.title("Insert")
    insert_window.geometry('270x150')

    label_db_name = Label(insert_window, text="Database name:")
    label_db_name.grid(column=0, row=0)

    input_text_box_db_name = Entry(insert_window, justify=CENTER)
    input_text_box_db_name.grid(column=1, row=0)

    label_qg_id = Label(insert_window, text="Quest giver id:")
    label_qg_id.grid(column=0, row=1)

    input_text_box_qg_id = Entry(insert_window, justify=CENTER)
    input_text_box_qg_id.grid(column=1, row=1)

    label_qg_name = Label(insert_window, text="Quest giver name:")
    label_qg_name.grid(column=0, row=2)

    input_text_box_qg_name = Entry(insert_window, justify=CENTER)
    input_text_box_qg_name.grid(column=1, row=2)

    log_text_box = scrolledtext.ScrolledText(insert_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=4, rowspan=1, sticky=S + W + E)

    def insert_into_quest_giver_internal():
        global login
        global password
        try:
            db_name = input_text_box_db_name.get()
            qg_id = input_text_box_qg_id.get()
            qg_name = input_text_box_qg_name.get()
            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()
            cur.execute("call insert_into_quest_giver(" + qg_id + ", '" + qg_name + "');")
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Insertion completed\n")
        except:
            log_text_box.insert(END, "Insertion failed\n")

    insert_to_quest_giver_button = Button(insert_window,
                                          text="Insert to quest giver",
                                          command=insert_into_quest_giver_internal)
    insert_to_quest_giver_button.grid(column=0, row=3)


def insert_into_quest_function():
    insert_window = Toplevel(main_window)
    insert_window.title("Insert")
    insert_window.geometry('270x150')

    label_db_name = Label(insert_window, text="Database name:")
    label_db_name.grid(column=0, row=0)

    input_text_box_db_name = Entry(insert_window, justify=CENTER)
    input_text_box_db_name.grid(column=1, row=0)

    label_qid = Label(insert_window, text="Quest id:")
    label_qid.grid(column=0, row=1)

    input_text_box_qid = Entry(insert_window, justify=CENTER)
    input_text_box_qid.grid(column=1, row=1)

    label_qname = Label(insert_window, text="Quest name:")
    label_qname.grid(column=0, row=2)

    input_text_box_qname = Entry(insert_window, justify=CENTER)
    input_text_box_qname.grid(column=1, row=2)

    label_qgid = Label(insert_window, text="Quest giver id:")
    label_qgid.grid(column=0, row=3)

    input_text_box_qgid = Entry(insert_window, justify=CENTER)
    input_text_box_qgid.grid(column=1, row=3)

    label_payment = Label(insert_window, text="Payment:")
    label_payment.grid(column=0, row=4)

    input_text_box_payment = Entry(insert_window, justify=CENTER)
    input_text_box_payment.grid(column=1, row=4)

    log_text_box = scrolledtext.ScrolledText(insert_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=6, rowspan=1, sticky=S + W + E)

    def insert_into_quest_internal():
        global login
        global password
        try:
            db_name = input_text_box_db_name.get()
            q_id = input_text_box_qid.get()
            q_name = input_text_box_qname.get()
            qg_id = input_text_box_qgid.get()
            payment = input_text_box_payment.get()
            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            cur.execute("call insert_into_quest({qid}, '{qname}', {qgid}, {payment});"
                        .format(qid=q_id, qname=q_name, qgid=qg_id, payment=payment))
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Insertion completed\n")
        except:
            log_text_box.insert(END, "Insertion failed\n")

    insert_to_quest_giver_button = Button(insert_window,
                                          text="Insert into quest table",
                                          command=insert_into_quest_internal)
    insert_to_quest_giver_button.grid(column=0, row=5)


def search_by_field_function():
    search_by_field_window = Toplevel(main_window)
    search_by_field_window.title("search")
    search_by_field_window.geometry('270x150')

    label_db_name = Label(search_by_field_window, text="Database name:")
    label_db_name.grid(column=0, row=0)

    input_text_box_db_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_db_name.grid(column=1, row=0)

    label_qname = Label(search_by_field_window, text="Quest/Owner name:")
    label_qname.grid(column=0, row=1)

    input_text_box_qname = Entry(search_by_field_window, justify=CENTER)
    input_text_box_qname.grid(column=1, row=1)

    label_table_name = Label(search_by_field_window, text="Table name:")
    label_table_name.grid(column=0, row=2)

    input_text_box_table_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_table_name.grid(column=1, row=2)

    log_text_box = scrolledtext.ScrolledText(search_by_field_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=5, row=4, rowspan=4, sticky=S + W + E)

    def search_by_field_internal():
        global login
        global password
        try:
            db_name = input_text_box_db_name.get()
            q_name = input_text_box_qname.get()
            table_name = input_text_box_table_name.get()
            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            if table_name == 'quest_giver':
                cur.execute("select select_name_from_quest_giver('{search_name}')".format(search_name=q_name))
                table = cur.fetchall()
                log_text_box.insert(END, 'Quest givers:\n')
                log_text_box.insert(END, ' id |    name    | quests amount\n')
                for line in table:
                    line = line[0][1:-1:].split(',')

                    qg_id = line[0]
                    qg_name = line[1]
                    qg_count = line[2]

                    qg_id = ' ' * max(0, 4 - len(qg_id)) + qg_id[:4:]
                    qg_name = ' ' * max(0, 12 - len(qg_name)) + qg_name[:12:]
                    qg_count = ' ' + qg_count

                    log_text_box.insert(END, qg_id + '|' + qg_name + '|' + qg_count)
                    log_text_box.insert(END, '\n')
            if table_name == 'quest':
                cur.execute("select select_name_from_quest('{search_name}')".format(search_name=q_name))
                table = cur.fetchall()
                log_text_box.insert(END, 'Quests:\n')
                log_text_box.insert(END, ' id |    name    | owner id | payment\n')
                for line in table:
                    line = line[0][1:-1:].split(',')

                    q_id = line[0]
                    q_name = line[1]
                    qg_id = line[2]
                    q_payment = line[3]

                    q_id = ' ' * max(0, 4 - len(q_id)) + q_id[:4:]
                    q_name = ' ' * max(0, 12 - len(q_name)) + q_name[:12:]
                    qg_id = ' ' * max(0, 10 - len(qg_id)) + qg_id[:10:]
                    q_payment = ' ' + q_payment

                    log_text_box.insert(END, q_id + '|' + q_name + '|' + qg_id + '|' + q_payment)
                    log_text_box.insert(END, '\n')

            cur.close()
            con.close()
            log_text_box.insert(END, "Search completed\n")
        except:
            log_text_box.insert(END, "Search failed\n")

    search_by_field_button = Button(search_by_field_window, text="Search", command=search_by_field_internal)
    search_by_field_button.grid(column=0, row=3)


def update_quest_function():
    update_quest_window = Toplevel(main_window)
    update_quest_window.title("Update quest")
    update_quest_window.geometry('270x150')

    label_dbname = Label(update_quest_window, text="Database name:")
    label_dbname.grid(column=0, row=0)

    input_text_box_dbname = Entry(update_quest_window, justify=CENTER)
    input_text_box_dbname.grid(column=1, row=0)

    label_qid = Label(update_quest_window, text="Quest id:")
    label_qid.grid(column=0, row=1)

    input_text_box_qid = Entry(update_quest_window, justify=CENTER)
    input_text_box_qid.grid(column=1, row=1)

    label_qname = Label(update_quest_window, text="New quest name:")
    label_qname.grid(column=0, row=2)

    input_text_box_qname = Entry(update_quest_window, justify=CENTER)
    input_text_box_qname.grid(column=1, row=2)

    label_qgid = Label(update_quest_window, text="New quest giver id:")
    label_qgid.grid(column=0, row=3)

    input_text_box_qgid = Entry(update_quest_window, justify=CENTER)
    input_text_box_qgid.grid(column=1, row=3)

    label_payment = Label(update_quest_window, text="New payment:")
    label_payment.grid(column=0, row=4)

    input_text_box_payment = Entry(update_quest_window, justify=CENTER)
    input_text_box_payment.grid(column=1, row=4)

    log_text_box = scrolledtext.ScrolledText(update_quest_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=6, rowspan=1, sticky=S + W + E)

    def update_quest_internal():
        global login
        global password
        try:
            db_name = input_text_box_dbname.get()
            q_id = input_text_box_qid.get()
            q_name = input_text_box_qname.get()
            qg_id = input_text_box_qgid.get()
            payment = input_text_box_payment.get()

            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            cur.execute("call update_quest({qid}, '{qname}', {qgid}, {payment})"
                        .format(qid=q_id, qname=q_name, qgid=qg_id, payment=payment))
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Update completed\n")
        except:
            log_text_box.insert(END, "Update failed\n")

    update_quest_button = Button(update_quest_window, text="Update quest\n", command=update_quest_internal)
    update_quest_button.grid(column=0, row=5)


def update_quest_giver_function():
    update_quest_giver_window = Toplevel(main_window)
    update_quest_giver_window.title("Update quest giver")
    update_quest_giver_window.geometry('270x150')

    label_dbname = Label(update_quest_giver_window, text="Database name:")
    label_dbname.grid(column=0, row=0)

    input_text_box_dbname = Entry(update_quest_giver_window, justify=CENTER)
    input_text_box_dbname.grid(column=1, row=0)

    label_qgid = Label(update_quest_giver_window, text="Quest giver id:")
    label_qgid.grid(column=0, row=1)

    input_text_box_qgid = Entry(update_quest_giver_window, justify=CENTER)
    input_text_box_qgid.grid(column=1, row=1)

    label_qgname = Label(update_quest_giver_window, text="New quest giver name:")
    label_qgname.grid(column=0, row=2)

    input_text_box_qgname = Entry(update_quest_giver_window, justify=CENTER)
    input_text_box_qgname.grid(column=1, row=2)

    log_text_box = scrolledtext.ScrolledText(update_quest_giver_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=3, rowspan=1, sticky=S + W + E)

    def update_quest_giver_internal():
        global login
        global password
        try:
            db_name = input_text_box_dbname.get()
            qg_id = input_text_box_qgid.get()
            qg_name = input_text_box_qgname.get()

            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            cur.execute("call update_quest_giver({qid}, '{qname}')"
                        .format(qid=qg_id, qname=qg_name))
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Update completed\n")
        except:
            log_text_box.insert(END, "Update failed\n")

    update_quest_giver_button = Button(update_quest_giver_window,
                                       text="Update quest giver",
                                       command=update_quest_giver_internal)
    update_quest_giver_button.grid(column=0, row=5)


def delete_by_field_function():
    search_by_field_window = Toplevel(main_window)
    search_by_field_window.title("delete")
    search_by_field_window.geometry('270x150')

    label_db_name = Label(search_by_field_window, text="Database name:")
    label_db_name.grid(column=0, row=0)

    input_text_box_db_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_db_name.grid(column=1, row=0)

    label_qname = Label(search_by_field_window, text="Quest/Owner name:")
    label_qname.grid(column=0, row=1)

    input_text_box_qname = Entry(search_by_field_window, justify=CENTER)
    input_text_box_qname.grid(column=1, row=1)

    label_table_name = Label(search_by_field_window, text="Table name:")
    label_table_name.grid(column=0, row=2)

    input_text_box_table_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_table_name.grid(column=1, row=2)

    log_text_box = scrolledtext.ScrolledText(search_by_field_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=4, rowspan=1, sticky=S + W + E)

    def search_by_field_internal():
        global login
        global password
        try:
            db_name = input_text_box_db_name.get()
            q_name = input_text_box_qname.get()
            table_name = input_text_box_table_name.get()
            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            if table_name == 'quest_giver':
                cur.execute("call delete_quest_giver('{search_name}')".format(search_name=q_name))
            if table_name == 'quest':
                cur.execute("call delete_quest('{search_name}')".format(search_name=q_name))
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Deletion completed\n")
        except:
            log_text_box.insert(END, "Deletion failed\n")

    delete_by_field_button = Button(search_by_field_window, text="Delete", command=search_by_field_internal)
    delete_by_field_button.grid(column=0, row=3)


def delete_by_id_function():
    search_by_field_window = Toplevel(main_window)
    search_by_field_window.title("delete")
    search_by_field_window.geometry('270x150')

    label_db_name = Label(search_by_field_window, text="Database name:")
    label_db_name.grid(column=0, row=0)

    input_text_box_db_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_db_name.grid(column=1, row=0)

    label_qname = Label(search_by_field_window, text="Quest/Owner id:")
    label_qname.grid(column=0, row=1)

    input_text_box_qname = Entry(search_by_field_window, justify=CENTER)
    input_text_box_qname.grid(column=1, row=1)

    label_table_name = Label(search_by_field_window, text="Table name:")
    label_table_name.grid(column=0, row=2)

    input_text_box_table_name = Entry(search_by_field_window, justify=CENTER)
    input_text_box_table_name.grid(column=1, row=2)

    log_text_box = scrolledtext.ScrolledText(search_by_field_window, width=30, height=2)
    log_text_box.grid(column=0, columnspan=2, row=4, rowspan=1, sticky=S + W + E)

    def search_by_field_internal():
        global login
        global password
        try:
            db_name = input_text_box_db_name.get()
            q_name = input_text_box_qname.get()
            table_name = input_text_box_table_name.get()
            con = psycopg2.connect(
                dbname=db_name,
                user=login,
                host='127.0.0.1',
                password=password)
            cur = con.cursor()

            if table_name == 'quest_giver':
                cur.execute("call delete_quest_giver_by_id({search_name})".format(search_name=q_name))
            if table_name == 'quest':
                cur.execute("call delete_quest_by_id({search_name})".format(search_name=q_name))
            con.commit()
            cur.close()
            con.close()
            log_text_box.insert(END, "Deletion completed\n")
        except:
            log_text_box.insert(END, "Deletion failed\n")

    delete_by_field_button = Button(search_by_field_window, text="Delete", command=search_by_field_internal)
    delete_by_field_button.grid(column=0, row=3)


main_window = Tk()
main_window.title("GTA online mission helper")
main_window.geometry('400x400')

log_in_button = Button(main_window, text="Log in", command=log_in_function)
log_in_button.grid(column=0, row=0)

show_tables_content_button = Button(main_window, text="Show tables content", command=show_tables_content_function)
show_tables_content_button.grid(column=1, row=0)

clean_tables_content_button = Button(main_window, text="Clean tables", command=clean_tables_function)
clean_tables_content_button.grid(column=2, row=0)

insert_quest_giver_button = Button(main_window, text="Insert quest giver", command=insert_into_quest_giver_function)
insert_quest_giver_button.grid(column=3, row=0)

insert_quest_button = Button(main_window, text="Insert quest", command=insert_into_quest_function)
insert_quest_button.grid(column=4, row=0)

search_name_button = Button(main_window, text="Search by name", command=search_by_field_function)
search_name_button.grid(column=0, row=1)

update_quest_button = Button(main_window, text="Update quest", command=update_quest_function)
update_quest_button.grid(column=1, row=1)

update_quest_giver_button = Button(main_window, text="Update quest giver", command=update_quest_giver_function)
update_quest_giver_button.grid(column=2, row=1)

delete_by_name_button = Button(main_window, text="Delete by name", command=delete_by_field_function)
delete_by_name_button.grid(column=3, row=1)

delete_by_id_button = Button(main_window, text="Delete by id", command=delete_by_id_function)
delete_by_id_button.grid(column=4, row=1)

main_window.mainloop()
