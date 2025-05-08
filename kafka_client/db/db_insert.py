import psycopg2

def insert_heartbeat(data):
    conn = psycopg2.connect("dbname=postgres user=postgres password=pgpass007 host=localhost")
    cur = conn.cursor()
    cur.execute("INSERT INTO heartbeats (customer_id, timestamp, heart_rate) VALUES (%s, %s, %s)",
                (data["customer_id"], data["timestamp"], data["heart_rate"]))
    conn.commit()
    cur.close()
    conn.close()
