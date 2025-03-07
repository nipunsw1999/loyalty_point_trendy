import streamlit as st
from functions import services_list,cursor,conn,check_available_customer,is_valid_mobile
import pandas as pd
import os 
from groq import Groq
import re
from dotenv import load_dotenv

load_dotenv()

st.title('Settings')  

if "mode" not in st.session_state:
    st.session_state.mode = 0

if "open" not in st.session_state:
    st.session_state.open = 0

if "openName" not in st.session_state:
    st.session_state.openName = ""

# Creating columns for navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    b1 = st.button("Open service settings ⚙️")
with col2:
    b2 = st.button("Open Customers settings 💁🏽")
with col3:
    b3 = st.button("Open Analytics 📈")

if b1:
    st.session_state.mode = 0
    st.session_state.mode = 1
if b2:
    st.session_state.mode = 0
    st.session_state.mode = 2
if b3:
    st.session_state.mode = 0
    st.session_state.mode = 3

if st.session_state.mode == 1:
    tab1, tab2 = st.tabs(["List services", "Update services"])
    
    with tab1:
        cursor.execute("SELECT SID, Service, Price, Point FROM services")
        data = cursor.fetchall()
        new_df = pd.DataFrame(data, columns=["SID", "Service", "Price", "Point"])
        st.table(new_df)
    
    with tab2:
        df = pd.read_csv("data/services.csv")
        edited_df = st.data_editor(df,num_rows="dynamic")
        service_update = st.button(":green[Service Update]")
        if service_update:
            cursor.execute("TRUNCATE TABLE services")
            for _, row in edited_df.iterrows():
                cursor.execute("INSERT INTO services (SID, Service, Price, Point) VALUES (%s, %s, %s, %s)", tuple(row))
            conn.commit()
            cursor.execute("SELECT SID, Service, Price, Point FROM services")
            data = cursor.fetchall()
            new_df = pd.DataFrame(data, columns=["SID", "Service", "Price", "Point"])
            csv_path = "data/services.csv"
            new_df.to_csv(csv_path, index=False,mode="w")
            st.success("Updated services successfully.")
            
                

# Customers Section
if st.session_state.mode == 2:
    tab3, tab4, tab5 = st.tabs(["List Customers","Add new Customer", "Update customer details"])
    with tab3:
        tab89, tab90 = st.tabs(["View Mode","Advanced Mode"])
        with tab89:
            cursor.execute("SELECT Name, Mobile, Gender, Points FROM customer ORDER BY Points ASC")
            data = cursor.fetchall()
            new_df = pd.DataFrame(data, columns=["Name", "Mobile", "Gender", "Points"])
            st.table(new_df)
        
        with tab90:
            cursor.execute("SELECT Name, Mobile, Gender, Points FROM customer ORDER BY Points ASC")
            data = cursor.fetchall()
            new_df = pd.DataFrame(data, columns=["Name", "Mobile", "Gender", "Points"])
            st.data_editor(new_df)
            
    with tab4:
        with st.form("Add Customer"):
            name = st.text_input("Customer Name")
            mobile = st.text_input("Mobile Number (077-1234567)")
            gender = st.selectbox("Gender", ("Male", "Female","Prefer not to say"))
            submit = st.form_submit_button("Add Customer")
            if submit:
                if name == "" or mobile == "":
                    st.error("Please fill all the fields.")
                elif not is_valid_mobile(mobile):
                    st.error("Invalid mobile number format! Use 077-1234567 or 0712345678.")
                elif check_available_customer("customer", mobile):
                    st.error("Customer already exists.")
                else:
                    cursor.execute("INSERT INTO customer (Name, Mobile, Gender, Points) VALUES (%s, %s, %s, %s)",
                                (name, mobile, gender, 0))
                    conn.commit()
                    st.success("Customer added successfully.")
                    
    with tab5:
        cursor.execute("SELECT Mobile FROM customer")
        data = cursor.fetchall()
        mobiles = []
        for row in data:
            mobiles.append(row[0])
            
        customer_mobile = st.selectbox("Select Customer Mobile", mobiles)
        customer_btn = st.button(":blue[Select by Mobile/ Refresh 🔄]")

        if customer_btn:
            st.session_state.open = 1
            st.session_state.openName = f"{customer_mobile}"
        
        if st.session_state.open == 1:
            mobile_number  = str(st.session_state.openName)
            cursor.execute(f"SELECT Name, Mobile, Gender, Points FROM customer WHERE Mobile = '{mobile_number}'")
            data0 = cursor.fetchall()
            data0 = data0[0]
            st.markdown(f"""
                <style>
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    table, th, td {{
                        border: 1px solid #ff3a9d;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: center;
                        
                    }}
                    td {{
                        border: 1px solid #ff3a9d;
                    }}
                </style>
                <table>
                    <tr>
                        <th colspan="2" style="color:rgb(255, 0, 0);background:rgb(0, 0, 0); text-align: center;">Selected Customer Details</th>
                    <tr>
                        <td style="color:rgb(60, 255, 0);background:rgb(10, 44, 0)">Name</td>
                        <td style="color:rgb(0, 255, 255);background:rgb(10, 44, 0)">{data0[0]}</td>
                    </tr>
                    <tr>
                        <td style="color:rgb(60, 255, 0);background:rgb(12, 31, 0)">Mobile</td>
                        <td style="color:rgb(0, 255, 255);background:rgb(12, 31, 0)">{data0[1]}</td>
                    </tr>
                    <tr>
                        <td style="color:rgb(60, 255, 0);background:rgb(10, 44, 0)">Gender</td>
                        <td style="color:rgb(0, 255, 255);background:rgb(10, 44, 0)">{data0[2]}</td>
                    </tr>
                    <tr>
                        <td style="color:rgb(60, 255, 0);background:rgb(12, 31, 0)">Points</td>
                        <td style="color:rgb(0, 255, 255);background:rgb(12, 31, 0)">{data0[3]}</td>
                    </tr>
                </table>
            """, unsafe_allow_html=True)
            
            new_mobile = st.text_input(":red[Update mobile]")
            btn_mobile = st.button(":red[Update Mobile]")
            if btn_mobile:
                if new_mobile == "":
                    st.error("Please fill the field.")
                elif not is_valid_mobile(new_mobile):
                    st.error("Invalid mobile number format! Use 077-1234567 or 0712345678.")
                elif check_available_customer("customer", new_mobile):
                    st.error("Customer already exists.")
                else:
                    cursor.execute(f"UPDATE customer SET Mobile = '{new_mobile}' WHERE Mobile = '{mobile_number}'")
                    conn.commit()
                    st.success("Mobile number updated successfully.")
                    st.session_state.open = 0
            
            new_name = st.text_input(":blue[Update name]")
            btn_name = st.button(":blue[Update name]")
            if btn_name:
                if new_name == "":
                    st.error("Please fill the field.")
                else:
                    cursor.execute(f"UPDATE customer SET Name = '{new_name}' WHERE Mobile = '{mobile_number}'")
                    conn.commit()
                    st.success("Name updated successfully.")
            new_gender = st.selectbox(":green[Gender]", ("Not selected","Male", "Female","Prefer not to say"))
            btn_gender = st.button(":green[Update Gender]")
            if btn_gender:
                if new_gender == "Not selected":
                    st.error("Please select gender.")
                else:
                    cursor.execute(f"UPDATE customer SET Gender = '{new_gender}' WHERE Mobile = '{mobile_number}'")
                    conn.commit()
                    st.success("Gender updated successfully.")
            
            

        
# Analytics Section
if st.session_state.mode == 3:
    tab6, tab7 = st.tabs(["Leading Points", "Chat with AI"])
    with tab6:
        st.write("Leading points section.")
        cursor.execute("SELECT Name, Mobile, Gender, Points FROM customer ORDER BY Points DESC")
        data = cursor.fetchall()
        new_df = pd.DataFrame(data, columns=["Name", "Mobile", "Gender", "Points"])
        st.table(new_df)
    with tab7:
        os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
        
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        
        def check_question(answer):
            check_answer = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""Classify the following user question into one of two categories:
                        1. **Database-related questions** (retrieving data from a MySQL database). Examples:
                           - How many services are available?
                           - Who has the most points?
                           - What is the total price of all services?
                        2. **General/unrelated questions** (not related to database queries). Examples:
                           - Good morning!
                           - Show me Java Hello World code.
                           - Tell me a joke.
                        
                        If the question is database-related, respond only with 'yes'.
                        If the question is general/unrelated, respond only with 'no'.
                        
                        The user's question is: {answer}""",
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            return check_answer.choices[0].message.content == "yes"
        
        def check_q(answer):
            check_answer = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""Determine whether the following MySQL query is a **SELECT query** (retrieving data).
                        - If it is a SELECT query, respond only with 'yes'.
                        - If it is an INSERT, UPDATE, DELETE, or any query modifying data, respond only with 'no'.
                        
                        MySQL query: {answer}""",
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            return check_answer.choices[0].message.content == "yes"
        
        def q_return(prompt):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )  
            return chat_completion.choices[0].message.content
        
        def q_check_again(query):
            modifying_commands = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "RENAME", "CREATE", "GRANT", "REVOKE"]
            query_upper = query.upper()
            return any(re.search(rf"\b{cmd}\b", query_upper) for cmd in modifying_commands)
        
        def return_best_output(question, query, output):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Give me the output regarding this.:\n\n"
                            f"- **User Question:** {question}\n"
                            f"- **Generated Query:** {query}\n"
                            f"- **Query Output:** {output}\n\n"
                            "Ensure the response is user-friendly"
                        ),
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        
        answer = st.chat_input("Enter your question...")
        if answer:
            st.write(answer)
        if answer:
            if check_question(answer):
                prompt = (
                    "The database contains the following tables:\n\n"
                    "### Tables Overview\n"
                    "- **services**: Contains service details.\n"
                    "    - `SID` (Service ID - Primary Key)\n"
                    "    - `Service` (Name of the service)\n"
                    "    - `Price` (Cost of the service)\n"
                    "    - `Point` (Reward points for the service)\n\n"
                    "- **customer**: Holds customer information.\n"
                    "    - `CID` (Customer ID - Primary Key)\n"
                    "    - `Name` (Customer's name)\n"
                    "    - `Mobile` (Customer's mobile number)\n"
                    "    - `Gender` (Customer's gender)\n"
                    "    - `Points` (Total reward points accumulated)\n\n"
                    "- **bills**: Stores details of customer transactions.\n"
                    "    - `ID` (Bill ID - Primary Key)\n"
                    "    - `Date` (Transaction date in `YYYY-MM-DD` format, e.g., `2025-02-28`)\n"
                    "    - `Name` (Customer's name)\n"
                    "    - `Mobile` (Customer's mobile number)\n"
                    "    - `Total` (Total amount spent)\n"
                    "    - `Services` (List of services taken)\n"
                    "    - `Prices` (List of corresponding prices for each service)\n"
                    "    - `Points` (Total reward points earned in this bill)\n"
                    "    - `Discount` (Indicates if a discount was applied: `YES` or `NO`)\n\n"
                    "### Important Notes\n"
                    "- `Date` strictly follows the format `YYYY-MM-DD`.\n"
                    "- The `Discount` column will contain either:\n"
                    "    - `YES`: Discount was applied.\n"
                    "    - `NO`: No discount was applied.\n\n"
                    "### Task\n"
                    "Write an **SQL query** to answer the following question:\n"
                    f"{answer}\n\n"
                    "### Output\n"
                    "Return **only the SQL query** — no explanations, no extra text."
                )


                q = q_return(prompt)
                if check_q(q):
                    if q_check_again(q):
                        st.write(":red[Please ask a valid question from the AI] 🤖")
                    else:
                        q = q.strip("```sql").strip("```").strip()
                        try:
                            cursor.execute(q)
                            data = cursor.fetchall()
                            final_response = return_best_output(answer, q, data)
                            message = st.chat_message("assistant")
                            message.write(final_response)
                        except Exception as e:
                            st.write(":red[Entered question has misleading information]")
                else:
                    st.write(":red[Please ask a valid question from the AI] 🤖")
            else:
                st.write(":red[Please ask a relevant question from the AI] 🤖")