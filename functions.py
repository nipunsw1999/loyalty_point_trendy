import mysql.connector
import streamlit as st
import re
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trendy"
)
cursor = conn.cursor()

def check_available_customer(table,name):
    cursor.execute(f"SELECT * FROM {table} WHERE Mobile = '{name}'")
    data = cursor.fetchall()
    if len(data) > 0:
        return True
    else:
        return False


def is_valid_mobile(mobile):
    """Check if mobile number is in valid Sri Lankan format (077-1234567 or 0712345678)."""
    pattern = r"^(0\d{2})[-]?\d{7}$"
    return re.match(pattern, mobile)

services_list = [
    {'id': 1, 'service_name': 'Hair Cut', 'service_price': 90, 'service_point': 11},
    {'id': 2, 'service_name': 'Shampoo & Condition', 'service_price': 71, 'service_point': 16},
    {'id': 3, 'service_name': 'Facial Treatment', 'service_price': 171, 'service_point': 9},
    {'id': 4, 'service_name': 'Manicure', 'service_price': 196, 'service_point': 12},
    {'id': 5, 'service_name': 'Pedicure', 'service_price': 197, 'service_point': 13},
    {'id': 6, 'service_name': 'Hair Coloring', 'service_price': 113, 'service_point': 13},
    {'id': 7, 'service_name': 'Waxing', 'service_price': 163, 'service_point': 11},
    {'id': 8, 'service_name': 'Hair Styling', 'service_price': 98, 'service_point': 20},
    {'id': 9, 'service_name': 'Bridal Makeup', 'service_price': 50, 'service_point': 12},
    {'id': 10, 'service_name': 'Massage', 'service_price': 72, 'service_point': 10}
]






def warn(text:str,seconds:int,done_display_time: int = 2):
    done_message = st.empty()
    done_message.warning(text, icon="⚠️")
    time.sleep(seconds)
    time.sleep(done_display_time)
    done_message.empty()

def err(text:str,seconds:int,done_display_time: int = 2):
    done_message = st.empty()
    done_message.error(text)
    time.sleep(seconds)
    time.sleep(done_display_time)
    done_message.empty()
    
def inf(text:str,seconds:int,done_display_time: int = 2):
    done_message = st.empty()
    done_message.info(text, icon="ℹ️")
    time.sleep(seconds)
    time.sleep(done_display_time)
    done_message.empty()

def completed(text:str,done_display_time:int = 2):
    done_message = st.empty()
    done_message.success(text)
    time.sleep(done_display_time)
    done_message.empty()
    
    