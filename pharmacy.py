import streamlit as st
import pandas as pd
from PIL import Image
#from drug_db import *
import random
from datetime import date
from streamlit_option_menu import option_menu

## SQL DATABASE CODE
import time
import mysql.connector
conn = mysql.connector.connect(user='root',password='Rohan@2387',host='localhost',database='hr1')
c = conn.cursor()

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.vecteezy.com/system/resources/previews/009/748/976/non_2x/coronavirus-vaccine-shield-and-human-hand-on-a-dark-background-in-low-poly-style-the-concept-of-creating-a-medicine-saving-and-protecting-humanity-from-the-virus-stock-illustration-vector.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


def get_email(username):
    c.execute('''select C_Email from Customers where C_Name = %s''',(username))
    ge = c.fetchall()
    return ge



def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_Address VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL,
                    C_Pin int not null 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, CAddress,Cnumber,CPin):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_Address, C_Number,C_Pin) VALUES(%s,%s,%s,%s,%s,%s)''', (Cname,Cpass,Cemail,CAddress,Cnumber,CPin))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number =%s WHERE C_Email = %s''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")

def customer_update_add(cust_email,cust_add):
    c.execute(''' UPDATE Customers SET C_Address =%s WHERE C_Email = %s''', (cust_add,cust_email,))
    conn.commit()  


def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = %s''', (Cemail,))
    conn.commit()

def amount_update(am):
    c.execute('update amt set amount=(amount+%s) where id = 1;',(am,))
    conn.commit()

def amount_deduct(am):
    c.execute('update amt set amount=(amount-%s) where id = 1;',(am,))
    conn.commit()

def amount_reset():
    c.execute('update amt set amount=0 where id = 1;')
    c.execute('update amt set last_amt=0 where id = 1;')
    conn.commit()
    


def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL,
                Amount int not null,
                Order_Date date,
                Status Varchar(100) default "Pending")
    ''')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = %s''', (Oid,))
    conn.commit()
def order_add_data(O_Name,O_Items,O_Qty,O_id,Amount,Order_Date):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id,Amount,Order_Date) VALUES(%s,%s,%s,%s,%s,%s)''',
              (O_Name,O_Items,O_Qty,O_id,Amount,Order_Date))
    conn.commit()

def view_order_date(ord_date):
    c.execute('SELECT * FROM ORDERS where Order_Date=%s',(ord_date,))
    order_all_data = c.fetchall()
    return order_all_data


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name = %s',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data

def order_update(ord_id):
    c.execute('update ORDERS set Status = "Completed" Where O_id = %s',(ord_id,))
    conn.commit()

def get_amount():
    c.execute('select amount from amt;')
    get_a = c.fetchall()
    return get_a

def get_last_amount():
    c.execute('select last_amt from amt;')
    get_a = c.fetchall()
    return get_a

def amount_last(am):
    c.execute('update amt set last_amt=%s where id = 1;',(am,))
    conn.commit()

#__________________________________________________________________________________






def admin():


    st.title("Pharmacy Database Dashboard")
    menu = ["Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)



    ## DRUGS
    


    ## CUSTOMERS
    if choice == "Customers":

        menu = ["View", "Delete","Update"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number","Pin"])
                st.dataframe(cust_clean_df)
        

        

    elif choice == "Orders":

        menu = ["View","Update Order Status"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID","Amount","Order_Date","Status",])
                st.dataframe(order_clean_df)

            ord_date = st.text_area("Order Date")
            if st.button(label="View Orders By Date"):
                date_result = view_order_date(ord_date)
                with st.expander("View All Order Data"):
                    order_clean_df1 = pd.DataFrame(date_result, columns=["Name", "Items","Qty" ,"ID","Amount","Order_Date","Status",])
                    st.dataframe(order_clean_df1)


        elif choice == "Update Order Status":
            order_result = order_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID","Amount","Order_Date","Status"])
                st.dataframe(order_clean_df)
            st.subheader("Update Order Status")
            ord_id = st.text_area("Order_id")
            if st.button(label="Update TO Completed"):
                order_update(ord_id)

    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Ritika Patil,Rohan bagawade, Rohit Andhale,Ritwik Meshram,Rutwik Powar,Sachin Satale")


def getauthenicate(username, password):
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = %s', (username,))
    cust_password = c.fetchall()
    if cust_password[0][0] == password:
        return True
    else:
        return False

###################################################################

def customer(username, password):
    
    #st.write(str(amounta))
    if getauthenicate(username, password):
        print("In Customer")
        st.title("Welcome to Pharmacy Store")

        menu = ["Order", "Delete","Update"]
        choice = st.sidebar.selectbox("Menu", menu)
        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        # st.write(cust_result)


        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID","Amount","Status","Order_Date"])
            st.dataframe(order_clean_df)
        

        Amoxillyn_Tablets = 0
        Anti_Fungle_Cream = 0
        Zandu_Pancharishta = 0
        Volini_Spray = 0
        Sinarest_Tablets = 0
        Bendril = 0
        Azithromycin_Tablet_500mg = 0
        Ceralac = 0
        Dettol = 0
        Whisper = 0
        Cold_And_Cough_Syrup = 0
        hair_Colour_Dark_Brown = 0
        Throat_Calm_Tablet = 0
        Teething_Relief_Drop = 0
        Leg_Cramps_Tablet = 0
        Weight_Gain_It = 0
        Diabetes_Tablet = 0
        Weight_Loss_Tablet = 0
        BOROPLUS = 0
        Tonner = 0
        Sunscreen = 0
        Lipcare = 0
        Serum = 0
        Facewash = 0
        Anti_aging_cream = 0
        Glow_n_lovely = 0
        Scrubber = 0
        Ear_Care_Antiseptic_spray_lotion = 0
        Ear_Cleaner_bamboo_cotton_swab = 0
        Ear_Cleaning_Tool_Kit = 0
        Ear_drop = 0
        Eye_Creame = 0
        Eye_drop = 0
        Eye_Ointment_Eye_Care = 0
        Eye_wash_lotion = 0
        sound_voice_amplifier_machine = 0
        #if choice == 'Order':

            #selected = 

        ##option = st.sidebar.selectbox('Select Category',('----Select----','Medicines & Drugs', 'Baby Care', 'Natural & Homeopathic Products','Daily Essentials'))

        ##st.write('You selected:', option)

        option = option_menu(
            menu_title=None,
            options=["Medicines & Drugs", "Baby Care", "Natural & Homeopathic Products","Daily Essentials"],
            # icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
            orientation="horizontal")







        
        if option == 'Medicines & Drugs':
            st.info("Azithromycin Tablet 500mg(3 tabs)")
            img = Image.open('images/Az.png')
            st.image(img, width=100, caption="Rs. 280/-")
            Azithromycin_Tablet = st.slider(label="Quantity",min_value=0, max_value=20, key= 1)
            # st.info("When to USE: " + str(drug_result[0][2]))
            #amt1+=(a*280)

            st.info("Bendril Syrup")
            img = Image.open('images/bendril.JPG')
            st.image(img, width=100 , caption="Rs. 114/-")
            Bendril = st.slider(label="Quantity",min_value=0, max_value=20, key= 2)
            # st.info("When to USE: " + str(drug_result[1][2]))
            #amt1+=(b*114)

            st.info("Sinarest Tablets")
            img = Image.open('images/sin.jpeg')
            st.image(img, width=100, caption="Rs. 15/- Per Tab")
            Sinarest_Tablets = st.slider(label="Quantity",min_value=0, max_value=20, key=5)
            #st.info("When to USE: " + str(drug_result[2][2]))
            #amt1+=(e*15)

            st.info("Volini Spray")
            img = Image.open('images/volini_spray.webp')
            st.image(img, width=100, caption="Rs. 110/-")
            Volini_Spray = st.slider(label="Quantity",min_value=0, max_value=5, key=6)
            #amt1+=(f*110)

            st.info("Zandu Pancharishta")
            img = Image.open('images/zandu_pancharishta.JPG')
            st.image(img, width=100, caption="Rs. 100/-")
            Zandu_Pancharishta = st.slider(label="Quantity",min_value=0, max_value=20, key=8)
            #amt1+=(h*100)

            st.info("Anti Fungle Cream 20gm")
            img = Image.open('images/Antifungle.webp')
            st.image(img, width=100, caption="Rs. 100/-")
            Anti_Fungle_Cream = st.slider(label="Quantity",min_value=0, max_value=20, key=9)
            #amt1+=(i*100)

            st.info("Amoxillyn Tablets")
            img = Image.open('images/amox.jpeg')
            st.image(img, width=100, caption="Rs. 12/-Per Tab")
            Amoxillyn_Tablets = st.slider(label="Quantity",min_value=0, max_value=20, key=10)
            #amt1+=(j*12)

            
            amounta = ((int(Azithromycin_Tablet)*280)+(int(Bendril)*114)+(int(Sinarest_Tablets)*15)+(int(Volini_Spray)*110)+(int(Zandu_Pancharishta)*100)+(int(Anti_Fungle_Cream)*100)+(int(Amoxillyn_Tablets)*12))
            if st.checkbox(label="Add To Cart"):
                #l[0] = amounta
                amount_update(amounta)
                amount_last(amounta)
                st.success("Added To Cart", icon="✅")
                ##st.info("Your Cart Amount")
                ##a = get_amount()
                ##st.info(a[0][0])

        if option == "Baby Care":
                

            st.info("Ceralac")
            img = Image.open('images/Cerelac.JPG')
            st.image(img, width=100, caption="Rs. 190/-")
            Ceralac = st.slider(label="Quantity",min_value=0, max_value=20, key=3)
            #st.info("When to USE: " + str(drug_result[2][2]))
            #amt2+=(c*190)

            st.info("Dettol 500 ML")
            img = Image.open('images/Dettol.JPG')
            st.image(img, width=100, caption="Rs. 240/-")
            Dettol = st.slider(label="Quantity",min_value=0, max_value=10, key=4)
            #st.info("When to USE: " + str(drug_result[2][2]))
            #amt2+=(d*240)
                

            st.info("PAMPERS")
            img = Image.open('images/Whisper.JPG')
            st.image(img, width=100, caption="Rs. 100/-")
            Whisper = st.slider(label="Quantity",min_value=0, max_value=20, key=7)
                
            amountb = ((int(Ceralac)*190)+(int(Dettol)*240)+(int(Whisper)*100))
            if st.checkbox(label="Add To Cart",key=20):
                #global amounta
                    
                #l[1] = amountb+l[0]
                amount_update(amountb)
                amount_last(amountb)
                st.success("Added To Cart")
                ##st.info("Your Cart Amount")
                ##a = get_amount()
                ##st.info(a[0][0])
        
        if option == "Natural & Homeopathic Products":
            st.info("Weight Loss Tablet(120 tabs)")
            img = Image.open('images/Weight_Loss_Tablet.jfif')
            st.image(img, width=100, caption="Rs. 2280/-")
            Weight_Loss_Tablet= st.slider(label="Quantity",min_value=0, max_value=20, key= 30)
            # st.info("When to USE: " + str(drug_result[0][2]))


            st.info("Diabetes Tablet(60)")
            img = Image.open('images/Diabetes_Tablet.jfif')
            st.image(img, width=100 , caption="Rs. 1140/-")
            Diabetes_Tablet= st.slider(label="Quantity",min_value=0, max_value=20, key= 31)
            # st.info("When to USE: " + str(drug_result[1][2]))

            st.info("Weight Gain It(500 Mg)(120 Tablet)")
            img = Image.open('images/Weight_Gain_It.jfif')
            st.image(img, width=100, caption="Rs. 1690/-")
            Weight_Gain_It = st.slider(label="Quantity",min_value=0, max_value=20, key=32)
            #st.info("When to USE: " + str(drug_result[2][2]))

            st.info("Leg Cramps Tablet(100 Tablet)")
            img = Image.open('images/Leg_Cramps_Tablet.jfif')
            st.image(img, width=100, caption="Rs. 1799/-")
            Leg_Cramps_Tablet = st.slider(label="Quantity",min_value=0, max_value=10, key=33)
            #st.info("When to USE: " + str(drug_result[2][2]))

            st.info("Teething Relief Drop")
            img = Image.open('images/Teething_Relief_Drop.jfif')
            st.image(img, width=100, caption="Rs. 735/-")
            Teething_Relief_Drop = st.slider(label="Quantity",min_value=0, max_value=20, key=34)
            #st.info("When to USE: " + str(drug_result[2][2]))

            st.info("Throat Calm Tablet(30)")
            img = Image.open('images/Throat_Calm_Tablet.jfif')
            st.image(img, width=100, caption="Rs. 699/-")
            Throat_Calm_Tablet= st.slider(label="Quantity",min_value=0, max_value=5, key=35)

            st.info("hair Colour Dark Brown")
            img = Image.open('images/hair_Colour_Dark_Brown.jfif')
            st.image(img, width=100, caption="Rs. 129/-")
            hair_Colour_Dark_Brown = st.slider(label="Quantity",min_value=0, max_value=20, key=36)

            st.info("Cold And Cough Syrup")
            img = Image.open('images/Cold_And_Cough_Syrup.jfif')
            st.image(img, width=100, caption="Rs. 199/-")
            Cold_And_Cough_Syrup = st.slider(label="Quantity",min_value=0, max_value=20, key=37)       

            amountc = ((int(Weight_Loss_Tablet)*2280)+(int(Diabetes_Tablet)*1140)+(int(Weight_Gain_It)*1690)+(int(Leg_Cramps_Tablet)*1799)+(int(Teething_Relief_Drop)*735)+(int(Throat_Calm_Tablet)*699)+(int(hair_Colour_Dark_Brown)*129)+(int(Cold_And_Cough_Syrup)*199))

            if st.checkbox(label="Add To Cart",key=21):
                
                amount_update(amountc)
                amount_last(amountc)
                st.success("Added To Cart", icon="✅")
                ##st.info("Your Cart Amount")
                ##a = get_amount()
                ##st.info(a[0][0])
        if option =='Daily Essentials':

            st.info("Boroplus")
            img = Image.open('images/BOROPLUS.jpg')
            st.image(img, width=100, caption="Rs. 30/-")
            BOROPLUS = st.slider(label="Quantity",min_value=0, max_value=20, key= 50)
            
            st.info("Tonner")
            img = Image.open('images/Tonner.jpg')
            st.image(img, width=100, caption="Rs. 238/-")
            Tonner = st.slider(label="Quantity",min_value=0, max_value=20, key= 51)
            
            st.info("Sunscreen")
            img = Image.open('images/Sunscreen.jpg')
            st.image(img, width=100, caption="Rs. 149/-")
            Sunscreen = st.slider(label="Quantity",min_value=0, max_value=20, key= 52)
            
            st.info("Lipcare")
            img = Image.open('images/Lipcare.jpg')
            st.image(img, width=100, caption="Rs. 185/-")
            Lipcare = st.slider(label="Quantity",min_value=0, max_value=20, key= 53)
            
            st.info("Serum")
            img = Image.open('images/Serum.jpg')
            st.image(img, width=100, caption="Rs. 645/-")
            Serum = st.slider(label="Quantity",min_value=0, max_value=20, key= 54)
            
            st.info("Facewash")
            img = Image.open('images/Facewash.jpg')
            st.image(img, width=100, caption="Rs. 249/-")
            Facewash = st.slider(label="Quantity",min_value=0, max_value=20, key= 55)
            
            st.info("Anti Aging Cream")
            img = Image.open('images/Anti_aging_cream.jpg')
            st.image(img, width=100, caption="Rs. 699/-")
            Anti_aging_cream = st.slider(label="Quantity",min_value=0, max_value=20, key= 56)
            
            st.info("Glow N Lovely")
            img = Image.open('images/Glow_n_lovely.jpg')
            st.image(img, width=100, caption="Rs. 39/-")
            Glow_n_lovely = st.slider(label="Quantity",min_value=0, max_value=20, key= 57)
            
            st.info("Scrubber")
            img = Image.open('images/Scrubber.jfif')
            st.image(img, width=100, caption="Rs. 145/-")
            Scrubber = st.slider(label="Quantity",min_value=0, max_value=20, key= 58)
            
            
            st.info("Ear Care Antiseptic Spray Lotion")
            img = Image.open('images/Ear_Care_Antiseptic_spray_lotion.jfif')
            st.image(img, width=100, caption="Rs. 499/-")
            Ear_Care_Antiseptic_spray_lotion = st.slider(label="Quantity",min_value=0, max_value=20, key= 59)
            
            st.info("Ear Cleaner Bamboo Cotton Swab")
            img = Image.open('images/Ear_Cleaner_bamboo_cotton_swab.jfif')
            st.image(img, width=100, caption="Rs. 449/-")
            Ear_Cleaner_bamboo_cotton_swab = st.slider(label="Quantity",min_value=0, max_value=20, key= 60)
            
            st.info("Ear Cleaning Tool Kit")
            img = Image.open('images/Ear_Cleaning_Tool_Kit.jfif')
            st.image(img, width=100, caption="Rs. 299/-")
            Ear_Cleaning_Tool_Kit = st.slider(label="Quantity",min_value=0, max_value=20, key= 61)
            
            st.info("Ear Drop")
            img = Image.open('images/Ear_drop.jfif')
            st.image(img, width=100, caption="Rs. 99/-")
            Ear_drop = st.slider(label="Quantity",min_value=0, max_value=20, key= 62)
            
            st.info("Eye Creame")
            img = Image.open('images/Eye_Creame.jfif')
            st.image(img, width=100, caption="Rs. 249/-")
            Eye_Creame = st.slider(label="Quantity",min_value=0, max_value=20, key= 63)
            
            st.info("Eye Drop")
            img = Image.open('images/Eye_drop.jfif')
            st.image(img, width=100, caption="Rs. 199/-")
            Eye_drop = st.slider(label="Quantity",min_value=0, max_value=20, key= 64)
            
            st.info("Eye Ointment Eye Care")
            img = Image.open('images/Eye_Ointment_Eye_Care.jfif')
            st.image(img, width=100, caption="Rs. 299/-")
            Eye_Ointment_Eye_Care = st.slider(label="Quantity",min_value=0, max_value=20, key= 65)
            
            st.info("Eye Wash Lotion")
            img = Image.open('images/Eye_wash_lotion.jfif')
            st.image(img, width=100, caption="Rs. 499/-")
            Eye_wash_lotion = st.slider(label="Quantity",min_value=0, max_value=20, key= 66)
            
            st.info("Sound Voice Amplifier Machine")
            img = Image.open('images/sound_voice_amplifier_machine.jfif')
            st.image(img, width=100, caption="Rs. 145/-")
            sound_voice_amplifier_machine = st.slider(label="Quantity",min_value=0, max_value=20, key= 67)

            amountd = (int(BOROPLUS)*30)+(int(Tonner)*238)+(int(Sunscreen)*150)+(int(Lipcare)*185)+(int(Serum)*645)+(int(Facewash)*249)+(int(Anti_aging_cream)*700)+(int(Glow_n_lovely)*40)+(int(Scrubber)*145)+(int(Ear_Care_Antiseptic_spray_lotion)*499)+(int(Ear_Cleaner_bamboo_cotton_swab)*449)+(int(Ear_Cleaning_Tool_Kit)*299)+(int(Ear_drop)*99)+(int(Eye_Creame)*249)+(int(Eye_drop)*199)+(int(Eye_Ointment_Eye_Care)*299)+(int(Eye_wash_lotion)*499)+(int(sound_voice_amplifier_machine)*145)
            if st.checkbox(label="Add To Cart",key=23):
                
                amount_update(amountd)
                amount_last(amountd)
                st.success("Added To Cart",icon="✅")
                ##st.info("Your Cart Amount")
                ##a = get_amount()
                ##st.info(a[0][0])
    
    if st.sidebar.button(label="Buy now"):
        O_items = ""

        
        if int(Weight_Loss_Tablet) > 0:
            O_items += "Weight_Loss_Tablet,"
        if int(Diabetes_Tablet) > 0:
            O_items += "Diabetes_Tablet,"
        if int(Weight_Gain_It) > 0:
            O_items += "Weight_Gain_It,"
        if int(Leg_Cramps_Tablet) > 0:
            O_items += "Leg_Cramps_Tablet,"
        if int(Teething_Relief_Drop) > 0:
            O_items += "Teething_Relief_Drop,"
        if int(Throat_Calm_Tablet) > 0:
            O_items += "Throat_Calm_Tablet"
        if int(hair_Colour_Dark_Brown) > 0:
            O_items += "hair_Colour_Dark_Brown,"
        if int(Cold_And_Cough_Syrup) > 0:
            O_items += "Cold_And_Cough_Syrup,"

        if int(Azithromycin_Tablet_500mg) > 0:
                O_items += "Azithromycin_Tablet_500mg,"
        if int(Bendril) > 0:
            O_items += "Bendril_Syrup,"
        if int(Ceralac) > 0:
            O_items += "Ceralac,"
        if int(Dettol) > 0:
            O_items += "Dettol_500_ML,"
        if int(Sinarest_Tablets) > 0:
            O_items += "Sinarest_Tablets,"
        if int(Volini_Spray) > 0:
            O_items += "Volini_Spray,"
        if int(Whisper) > 0:
            O_items += "Whisper_Ultra,"
        if int(Zandu_Pancharishta) > 0:
            O_items += "Zandu_Pancharishta,"
        if int(Anti_Fungle_Cream) > 0:
            O_items += "Anti_Fungle_Cream_20gm,"
        if int(Amoxillyn_Tablets) > 0:
            O_items += "Amoxillyn_Tablets,"
        if int(BOROPLUS) > 0:
            O_items += "BOROPLUS,"
        if int(Tonner) > 0:
            O_items += "Tonner,"
        if int(Sunscreen) > 0:
            O_items += "Sunscreen,"
        if int(Lipcare) > 0:
            O_items += "Lipcare,"
        if int(Serum) > 0:
            O_items += "Serum,"
        if int(Facewash) > 0:
            O_items += "Facewash,"
        if int(Anti_aging_cream) > 0:
            O_items += "Anti_aging_cream,"
        if int(Glow_n_lovely) > 0:
            O_items += "Glow_n_lovely,"
        if int(Scrubber) > 0:
            O_items += "Scrubber,"
        if int(Ear_Care_Antiseptic_spray_lotion) > 0:
            O_items += "Ear_Care_Antiseptic_spray_lotion,"
        if int(Ear_Cleaner_bamboo_cotton_swab) > 0:
            O_items += "Ear_Cleaner_bamboo_cotton_swab,"
        if int(Ear_Cleaning_Tool_Kit) > 0:
            O_items += "Ear_Cleaning_Tool_Kit,"
        if int(Ear_drop) > 0:
            O_items += "Ear_drop,"
        if int(Eye_Creame) > 0:
            O_items += "Eye_Creame,"
        if int(Eye_drop) > 0:
            O_items += "Eye_drop,"
        if int(Eye_Ointment_Eye_Care) > 0:
            O_items += "Eye_Ointment_Eye_Care,"
        if int(Eye_wash_lotion) > 0:
            O_items += "Eye_wash_lotion,"
        if int(sound_voice_amplifier_machine) > 0:
            O_items += "sound_voice_amplifier_machine,"

        O_Qty = str(Azithromycin_Tablet_500mg)+str(',') + str(Bendril) + str(",") + str(int(Sinarest_Tablets))+str(',')+str(Volini_Spray)+str(',') + str(Zandu_Pancharishta) + str(",") + str(Anti_Fungle_Cream)+str(',')+str(Amoxillyn_Tablets)+str(",")+str(Weight_Loss_Tablet)+str(',') + str(Diabetes_Tablet) + str(",") + str(Weight_Gain_It)+str(",")+str(Leg_Cramps_Tablet)+str(',') + str(Teething_Relief_Drop) + str(",") + str(Throat_Calm_Tablet)+str(",")+str(hair_Colour_Dark_Brown)+str(',') + str(Cold_And_Cough_Syrup)+str(",")+str(Azithromycin_Tablet_500mg)+str(',')+ str(Ceralac)+ str(",")+str(Dettol)+str(',')+str(Whisper)+str(',') + str(Zandu_Pancharishta) + str(",") + str(BOROPLUS)+str(",")+str(Tonner)+str(",")+str(Sunscreen)+str(",")+str(Lipcare)+str(",")+str(Serum)+str(",")+str(Facewash)+str(",")+str(Anti_aging_cream)+str(",")+str(Glow_n_lovely)+str(",")+str(Scrubber)+str(",")+str(Ear_Care_Antiseptic_spray_lotion)+str(",")+str(Ear_Cleaner_bamboo_cotton_swab)+str(",")+str(Ear_Cleaning_Tool_Kit)+str(",")+str(Ear_drop)+str(",")+str(Eye_Creame)+str(",")+str(Eye_drop)+str(",")+str(Eye_Ointment_Eye_Care)+str(",")+str(Eye_wash_lotion)+str(",")+str(sound_voice_amplifier_machine)+str(",")
	
        O_id = username + "#O" + str(random.randint(0,10000))
        
        lst = get_last_amount()
        last = lst[0][0]
        amount_deduct(last)
        ml = get_amount()
        
        amt1 = ml[0][0]
        d = date.today()
        order_add_data(username, O_items, O_Qty, O_id,int(str(ml[0][0])),d)
        
        st.warning("Your Total Amount:Rs=" + str(amt1))
        amount_reset()
        

    else:
        if choice == 'Delete':
            st.subheader("Delete Your All Details")
            cust_email = st.text_area("Email",key=100)
            if st.button(label="Delete",key = 200):
                customer_delete(cust_email)

        if choice == 'Update':
            st.subheader("Update Your Details")
            cust_email = st.text_input("Email",key=101)
            cust_number = st.text_input("Phone Number",key=102)
            if st.button(label='Update Phone Number',key=103):
                customer_update(cust_email,cust_number)  
                st.success("Your Email Is Updated Successfully",icon="✅") 

            cust_city = st.text_input("Enter Your New Address",key=104)
            if st.button(label='Update Address',key=105):
                customer_update_add(cust_email,cust_city)  
                st.success("Your Address Is Updated Successfully",icon="✅")




if __name__ == '__main__':
    cust_create_table()
    order_create_table()

    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Login", menu)
    

    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            
            customer(username, password)

        

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)

        col1,col2=st.columns(2)
        with col1:
            cust_email = st.text_input("Email ID")
        with col2:
            cust_number=st.text_input("Enter Number", max_chars=10, key= 1002)

        col1,col2,col3=st.columns(3)
        with col1:  
            cust_plot=st.text_input("Plot No.")
        with col2:
            cust_add=st.text_input("Address") 
        with col3:
            cust_pin=st.text_input("Pincode")
            
        cust_area = option = st.selectbox('Select State',('----Select----','Andhra Pradesh', 'Arunachal Pradesh', 'Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal',))

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_add, cust_number,cust_pin)
                st.success("Your Account is Created!")
                with st.spinner('Wait for it...'):
                    time.sleep(2)
                # st.success('Done!')
                st.success('This is a success message!', icon="✅")
                st.snow()
                #st.balloons()
                st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        # if st.sidebar.button("Login"):
        if username == "admin9876" and password == 'dbda23':
            admin()
