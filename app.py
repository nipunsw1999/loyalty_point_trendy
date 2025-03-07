import streamlit as st
from datetime import datetime
from functions import conn,cursor,completed,err

DISPOINTVALUE = 30
DISPOINTVALUERATE = 0.35
DISCOUNTAVAIABLE = 50

if "mode" not in st.session_state:
    st.session_state.mode = 0

if "cusMob" not in st.session_state:
    st.session_state.cusMob = ""

if "cusMobShow" not in st.session_state:
    st.session_state.cusMobShow = 0

if "customer_data" not in st.session_state:
    st.session_state.customer_data = 0

if "discount" not in st.session_state:
    st.session_state.discount = False

if "bill_total" not in st.session_state:
    st.session_state.bill_total = 0

if "bill_total_points" not in st.session_state:
    st.session_state.bill_total_points = 0

if "check_bill_show" not in st.session_state:
    st.session_state.check_bill_show = False

if "added_services" not in st.session_state:
    st.session_state.added_services = []

if "added_services_prices" not in st.session_state:
    st.session_state.added_services_prices = []

if "added_services_points" not in st.session_state:
    st.session_state.added_services_points = []

st.session_state.mode = 0

hours = datetime.now().hour
today_date = datetime.now().strftime('%Y-%m-%d') 
if 5 <= hours < 12:
    greeting = "Good Morning ☀️"
elif 12 <= hours < 17:
    greeting = "Good Afternoon 🌤️"
elif 17 <= hours < 21:
    greeting = "Good Evening 🌆"
else:
    greeting = "Good Night 🌙"

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{greeting}** <span style='color:red'></span>", unsafe_allow_html=True)

with col2:
    st.markdown(f"**Date:** <span style='color:#ff3a9d'>{today_date}</span>", unsafe_allow_html=True)

st.markdown(
    "<span style='color:#ff3a9d; font-size:55px; font-weight:bold'>Welcome to Saloon</span>", 
    unsafe_allow_html=True
)



customer_data = (1, '-', '-', '-','-')


cursor.execute("SELECT Mobile FROM customer")
data = cursor.fetchall()
mobiles = []
for row in data:
    mobiles.append(row[0])
    
customer_mobile = st.selectbox("Select Customer Mobile", mobiles)
col1, col2 = st.columns([1,2])
with col1:
    customer_btn = st.button(":blue[Select this customer]")
with col2:
    new_customer_btn = st.button(":red[Clear]")
    if new_customer_btn:
        st.session_state.added_services_prices = []
        st.session_state.added_services_points = []
        st.session_state.added_services = []
        discount_read = "NO"
        st.session_state.bill_total = 0
        st.session_state.bill_total_points = 0
        st.session_state.cusMob = ""
        st.session_state.cusMobShow = 0
        st.session_state.customer_data = 0
        st.session_state.discount = False
        

if customer_btn:
    st.session_state.cusMob = customer_mobile
    cursor.execute("SELECT * from customer WHERE Mobile = %s",(customer_mobile,)) 
    st.session_state.customer_data = cursor.fetchone()
    st.session_state.cusMobShow = 1

if st.session_state.cusMobShow == 1:
    if st.session_state.customer_data[3] == "Male": gender = "He" 
    else: gender = "She"
    st.write(f"Customer is :green-background[{st.session_state.customer_data[1]}].  {gender} has :green-background[{st.session_state.customer_data[4]}] points")
    if st.session_state.customer_data[4] >= DISCOUNTAVAIABLE:
        st.session_state.discount = True
        st.markdown("### 🎉 <span style='color:green; font-weight:bold;'>Discount Available!</span>", unsafe_allow_html=True)
    # col1,col2,col3 = st.columns([1,1,3])
    # with col1:
    #     st.write(f"Name")
    #     st.write(f"Gender")
    #     st.write(f"Points")
    # with col2:
    #     st.write(":")
    #     st.write(":")
    #     st.write(":")
    # with col3:
    #     st.write(customer_data[1])
    #     st.write(customer_data[3])
    #     st.write(str(customer_data[4]))

st.divider()
col1,col2 = st.columns([2,2])
with col1:
    cursor.execute("SELECT Service,Price FROM services")
    data = cursor.fetchall()
    services = []
    for row in data:
        services.append(row[0]+" : RS."+str(row[1])+"/-")
        
    services_list = st.selectbox("Select Service", services)
    add_btn = st.button(":blue[Add Service]")
    if add_btn:
        st.session_state.added_services.append(str(services_list))
        completed(str(services_list) + " is added",2)

with col2:
    added_services = []
    for ser in st.session_state.added_services:
        added_services.append(ser)
    added_services_list = st.selectbox("Select Service to :red[DELETE]", added_services)
    dlt_add_btn = st.button(":red[Delete Service]")
    if dlt_add_btn:
        if len(st.session_state.added_services) > 0:
            st.session_state.added_services.remove(str(added_services_list))
            err(str(added_services_list) + " is removed",2)
        else:
            err("No service selected",2)
st.divider()    
    
check_btn = st.button("Check Bill")
if check_btn:
    st.session_state.check_bill_show = True
if st.session_state.check_bill_show:
    if len(st.session_state.added_services) > 0:
        st.session_state.bill_total = 0
        st.session_state.bill_total_points = 0

        st.markdown("## :green[Bill Summary]")

        # Use a table-like layout with columns
        col1, col2,col3 = st.columns([3, 1,1])

        with col1:
            st.markdown("**Service**")
        with col2:
            st.markdown("**Price (LKR)**")
        with col3:
            st.markdown("**Points**")

        for service in st.session_state.added_services:
            service_now = service.split(":")[0].strip()

            cursor.execute("SELECT Price,Point FROM services WHERE Service = %s", (service_now,))
            result = cursor.fetchone()

            if result:
                price = result[0]
                st.session_state.bill_total += price
                st.session_state.bill_total_points += result[1]

                col1, col2,col3 = st.columns([3, 1,1])
                with col1:
                    st.write(service_now)
                with col2:

                    st.write(f"{price:,}")  # Format price with commas (1,200)
                with col3:

                    st.write(f"{result[1]}")
            else:
                st.error(f"❌ Price not found for: {service_now}")

        col1, col2,col3 = st.columns([3, 1,1])

        with col1:
            pass
        with col2:
            st.write(f":orange[{st.session_state.bill_total}]")
        with col3:
            st.write(f":orange[{st.session_state.bill_total_points}]")
        
        # Separator line and total amount
        st.markdown("---")
        st.markdown(f"Total: :red[RS. {st.session_state.bill_total:,}"+"/-]")
        # st.markdown(f"Points: :red[{st.session_state.bill_total_points}]")
        discount_read = "NO"
        if st.session_state.discount:
            dis = st.checkbox("Apply Discount")
            if dis:
                discount_read = "YES"
                price_tot = st.session_state.bill_total - st.session_state.bill_total*DISPOINTVALUERATE
                st.write(f"New Total: :red[{st.session_state.bill_total}] - :green[{st.session_state.bill_total*DISPOINTVALUERATE}] = :orange[{price_tot}]")
        add_bill = st.button(":green[Add Bill]")

        if add_bill:
            st.session_state.added_services_prices = []
            st.session_state.added_services_points = []
            for service in st.session_state.added_services:
                service_now = service.split(":")[0].strip()

                cursor.execute("SELECT Price,Point FROM services WHERE Service = %s", (service_now,))
                result = cursor.fetchone()
                st.session_state.added_services_prices.append(result[0])
                st.session_state.added_services_points.append(result[1])
            if discount_read == "YES":
                st.session_state.bill_total = st.session_state.bill_total*DISPOINTVALUERATE
                st.session_state.bill_total_points = st.session_state.bill_total_points-DISPOINTVALUE
                
            if st.session_state.cusMobShow == 1:
                cursor.execute("INSERT INTO bills (Date,Name,Mobile,Total,Services,Prices,Points,Discount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(today_date,str(st.session_state.customer_data[1]),str(st.session_state.customer_data[2]),str(st.session_state.bill_total),str(st.session_state.added_services),str(st.session_state.added_services_prices),str(st.session_state.added_services_points),discount_read))
                conn.commit()
                completed("Bill added",2)
                cursor.execute("UPDATE customer SET Points = %s WHERE Mobile = %s", (st.session_state.bill_total_points+st.session_state.customer_data[4], st.session_state.cusMob))
                st.session_state.added_services_prices = []
                st.session_state.added_services_points = []
                st.session_state.added_services = []
                discount_read = "NO"
                st.session_state.bill_total = 0
                st.session_state.bill_total_points = 0
                st.session_state.cusMob = ""
                st.session_state.cusMobShow = 0
                st.session_state.customer_data = 0
                st.session_state.discount = False
            else:
                err("No customer selected",2)
    else:
        err("No services added", 2)
