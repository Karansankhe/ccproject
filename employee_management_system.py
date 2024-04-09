
# Import required libraries
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import ServerSelectionTimeoutError

# Load environment variables from .env file
load_dotenv()

# Access environment variables
MONGO_URI = os.getenv('MONGO_URI')

try:
    # Connect to MongoDB with a longer timeout (e.g., 10 seconds)
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)  # 10 seconds timeout
    db = client.employee_db
    collection = db.employees

    # Streamlit UI
    st.title('Employee Management System')

    option = st.sidebar.selectbox('Menu', ['Add Employee', 'Delete Employee', 'View Employees'])

    if option == 'Add Employee':
        name = st.text_input('Enter Name:')
        position = st.text_input('Enter Position:')
        salary = st.number_input('Enter Salary:')
        if st.button('Add'):
            new_employee = {'Name': name, 'Position': position, 'Salary': salary}
            collection.insert_one(new_employee)
            st.success('Employee added successfully!')

    elif option == 'Delete Employee':
        name = st.text_input('Enter Name to Delete:')
        if st.button('Delete'):
            collection.delete_one({'Name': name})
            st.success('Employee deleted successfully!')

    elif option == 'View Employees':
        employees = list(collection.find())
        if employees:
            employee_df = pd.DataFrame(employees)
            st.table(employee_df)
        else:
            st.info('No employees found.')

except ServerSelectionTimeoutError as err:
    st.error(f"Error connecting to MongoDB: {err}. Please check your MongoDB connection settings and try again.")
except Exception as e:
    st.error(f"An error occurred: {e}")
