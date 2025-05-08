import streamlit as st
import pandas as pd
import psycopg2

conn = psycopg2.connect("dbname=heart_beat user=postgres password=pgpass007 host=localhost")
df = pd.read_sql("SELECT * FROM heartbeats ORDER BY timestamp DESC LIMIT 100", conn)
st.line_chart(df.set_index('timestamp')['heart_rate'])
