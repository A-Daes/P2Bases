import psycopg2
from config import config
 
 
def get_client(id):
    """ insert a new vendor into the vendors table """

    sql = """SELECT * FROM public."Cliente" WHERE public."Cliente"."ID" = """ + str(id) 
    print sql
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        ##Get all data to a list
        client = cur.fetchone()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print client
        return client
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
