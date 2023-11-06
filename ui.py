import streamlit as st
import pyodbc as odbc
import pandas as pd
from dotenv import load_dotenv
import openai



# def init_connection():
#     return pyodbc.connect(
#         "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
#         + st.secrets["SERVER_NAME"]
#         + ";DATABASE="
#         + st.secrets["DATABASE_NAME"]



with st.sidebar:
    st.header("Interact with Database")
    key=st.text_input("Enter your API key")
    st.markdown("""
    ## About 
    Works with the help of OpenAI""")
    st.write("For Reference")
    st.write('''-[Streamlit](https://streamlit.io/) 
            -  [OpenAI](https://platform.openai.com/docs/models)''')
@st.cache_resource
@st.cache_data(ttl=600)
def init_connection():
        return odbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["SERVER_NAME"]
        + ";DATABASE="
        + st.secrets["DATABASE_NAME"]
        + ";UID="
        + st.secrets["UID"]
        + ";PWD="
        + st.secrets["PASSWD"])


def main():
    load_dotenv()
    
    
    openai.api_key =key
    st.header("AdventureWorks querying to a database🗃️ in Natural Language")
    
   
    # DRIVER_NAME='ODBC Driver 17 for SQL Server'                                                                                 # Details of the SQL Server with its Database
    # SERVER_NAME='Bharti-PC'
    # DATABASE_NAME='AdventureWorks2022'
    cnxn=init_connection()
    

    # connection_string=f'''
    #     DRIVER={{{DRIVER_NAME}}};
    #     SERVER={SERVER_NAME};
    #     DATABASE={DATABASE_NAME};
    #     trusted_connection=yes'''
    
    # cnxn = odbc.connect(connection_string)                                                                                      # Establishing the connection with the SQL Server
    cursor=cnxn.cursor()
    cursor1=cnxn.cursor()
    cursor2=cnxn.cursor()
    a=cursor.execute("SELECT concat (Table_schema,'.',Table_name) FROM information_schema.tables")
    st.write("Connection Established")
    option=st.selectbox("Select Your Table",options=a.fetchall(),placeholder='Choose your option')                              # It shows all the Tables in the database
    st.write("Table Chosen",option)                                                                                             # And user can select a table
    option=str(option).strip('(').strip(')').strip(',')
    st.markdown(f"## {option}")
    option1=str(option).split(".")[1].strip("'")
    # st.write(option)
    b=cursor2.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{option1}'")                     # To show all the columns in that particular table
    st.radio("Columns",options=b.fetchall())


    query=st.text_input("Write your query")                                                                                     # User inputs natural language query
    if query:  
        prompt=f"Generate a SQL server query to retrive {query} from the database with table {option} "
        response=openai.Completion.create(engine='text-davinci-003',prompt=prompt,max_tokens=100)                               # Selection of engine for openai
        query=response.choices[0].text.strip()                                                                                  # Selecting the first response generated from openai engine
        st.write(query)
        result=cursor1.execute(query)                                                                                           # Executing the query
        field_names = [i[0] for i in cursor1.description]   
        
        df=pd.DataFrame(result.fetchall())          
        st.write(field_names)                                                                                                   # Showing the columns of the data
        df[0]=df[0].astype(str)
        columns = df[0].str.split(',', expand=True)
        new_df = pd.DataFrame(columns)
        st.write(new_df)                                                                                                        # Displaying the result in tabular form
        
        
    else:
        pass   
  






if __name__ == '__main__':
    main()













