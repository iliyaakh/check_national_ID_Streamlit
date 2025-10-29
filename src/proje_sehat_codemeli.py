import requests
import streamlit as st
import sqlite3

def get_code(code):
    url = f"https://api.codebazan.ir/codemelli/?code={code}"
    try:
        respoonse = requests.get(url)
        if respoonse.status_code != 200 :
            return'page not finde'
        else:
            respoonse = respoonse.json()
            result = respoonse['Result']
            return result
    except Exception as e:
        return None

con = sqlite3.connect('code.db')
cursor = con.cursor()

sql_creat_table = ''' CREATE TABLE IF NOT EXISTS codes 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  National_ID INTEGER, result TEXT)
                              '''
cursor.execute(sql_creat_table)
con.commit()

def insert(National_ID, result):
    cursor.execute('INSERT INTO codes (National_ID, result) VALUES (?,?)',(National_ID, result))
    con.commit()

def delete(id):
    cursor.execute('DELETE FROM codes WHERE id = ?', (id,))
    con.commit()

def delete_all():
    cursor.execute('DELETE FROM codes')
    con.commit()

def read_where1(National_ID):
    cursor.execute('SELECT * FROM codes WHERE National_ID = ?', (National_ID,))
    return cursor.fetchall()

def read_where2(id):
    cursor.execute('SELECT * FROM codes WHERE id = ?', (id,))
    return cursor.fetchall()

def read_full():
    cursor.execute('SELECT * FROM codes')
    return cursor.fetchall()

st.sidebar.title('seting')
setting = st.sidebar.selectbox('diagrees', ('National ID','Delete from history','Delete all history','search national ID','search by ID',
                                            'Make Table','About Us'))

if setting == 'National ID':
    st.title("Welcom to your Website")
    st.write("Let's check the National ID")
    National_ID = st.text_input('Enter your national ID (10 digits) : ')
    if National_ID:

        result = get_code(National_ID)
        if result == 'The code is valid':
        
            st.success(result)
            st.write('would you like to save it?')
            x = st.button('yes')
            if x:
                insert(National_ID, result)
                st.success('insert the table')
        elif result == 'The number of digits is incorrect':
            st.error(result)
        elif result == 'Invalid code':
            st.error(result)
        elif result is None:
            st.error('network error')
        elif result == 'page not finde':
            st.error('request error')

elif setting == 'Delete from history':
    st.title('Delete by ID')
    id = st.number_input("Enter ID:", min_value=1, step=1)
    if st.button("Delete"):
        results = read_where2(id)
        if results:
            delete(id)
            st.success(f'Record with ID {id} deleted')
        else:
            st.error(f'No record found with ID {id}')

elif setting == 'Delete all history':
    st.title('Do you want Delete all history?')
    if st.button('yes'):
        delete_all()
        st.success('History cleared')

elif setting == 'search national ID':
    National_ID = st.text_input('Enter national ID :')
    if st.button('search'):
        results = read_where1(National_ID)
        if results:
            st.dataframe(results, column_config={"0": "ID", "1": "National ID", "2": "Result"})
        else:
            st.info("No records found")
        
elif setting == 'search by ID':
    id = st.number_input('Enter ID :', step = 1, min_value = 1)
    if st.button('search'):
        results = read_where2(id)
        if results:
            st.dataframe(results, column_config={"0": "ID", "1": "National ID", "2": "Result"})
        else:
            st.info("No records found")

elif setting == 'Make Table':
    data = read_full()
    if data:
        st.dataframe(data, column_config={"0": "ID", "1": "National ID", "2": "Result"})
    else:
        st.info("No records in database")

elif setting == 'About Us':
    st.title('About This Project')
    st.write("This Streamlit project, developed by Iliya, you can check the National ID. Store your results," \
    " view history, and manage records easily.")
    st.title('Contact Us')

    st.write('you can contact us via :')
    col1 , col2 , col3 = st.columns(3)
    with col1 : 
        st.write('Telegram : @iliya_12344')
        st.link_button('Go to Telegram', 'https://t.me/iliya_12344')
    with col2 :
        st.write('Instagram : @iliyakh177')
        st.link_button('Go to Instagram', 'https://www.instagram.com/iliyakh177?igsh=dXpkNHM2OTl6OHho')
    with col3 :
        st.write('Email : iliyakh660@gmail.com')
