#import mysql.connector as sql
#from mysql.connector import Error
from nt import rename
import pymysql
from tkinter import *
import tkinter as tk
from tkinter import messagebox


#root = Tk()
#root.title("Car Rental Management System")
#root.geometry("400x400+300+300")

root = Tk()
root.title("Vehicle Rental System")
root.geometry("500x500+300+300")




'''print("connecting")
connectdb = pymysql.connect(
host="localhost",
user="root",
password="tiger123",
database="student"
)
print("Connected")

cursor = connectdb.cursor()

cursor.execute("show databases")
for databases in cursor:
    print(databases[0])

print("Database are shown here")'''


def create_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(50),
        model VARCHAR(100),
        rent_per_day FLOAT,
        available VARCHAR(10)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_id INT,
        customer_id INT,
        rent_date DATE,
        return_date DATE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')
    conn.commit()
    conn.close()


def open_rent_car():
    form_window = tk.Toplevel(root)
    form_window.title("Rent A Car")
    form_window.geometry("400x400+300+300")

    tk.Label(form_window, text="Vehicle Type:",).place(x=30,y=30)
    name_entry = tk.Entry(form_window,width=30).place(x=130,y=30)
  

    tk.Label(form_window, text="Model:").place(x=30,y=60)
    model_entry = tk.Entry(form_window,width=30).place(x=130,y=60)
    

    tk.Label(form_window, text="Rent Per Day:").place(x=30,y=90)
    rent_entry = tk.Entry(form_window,width=30).place(x=130,y=90)


    def save_Vehicle():
        vtype = name_entry.get()
        model = model_entry.get()
        rent = rent_entry.get()

        if not (vtype and model and rent):
            messagebox.showerror("Error", "All fields are required")
            return

        connecttodb = connectdb.cursor()
        connecttodb.execute("INSERT INTO vehicles (type, model, rent_per_day, available) VALUES (%s, %s, %s, 'Yes')",(vtype, model, rent))
        connecttodb.commit()
        connecttodb.close()
        
        messagebox.showinfo("Success", "Vehicle added successfully!", parent=form_window)
        form_window.destroy()

    Button(form_window, text="Save Vehicle",command=save_Vehicle, bg="blue", fg="white").place(x=150,y=120)
    


    
def fun():
    messagebox.showinfo("Hello", "Red Button clicked")

def exit():
    root.destroy()


w = Label(root, text="Vehicle Rental System", font=("Arial",16,"bold"))
w.pack(pady=20)


b1 = Button(root, text="Add Vehicle",bg="red", fg="white", activeforeground="blue", activebackground="blue",command=open_rent_car, width=20, height=2)
b1.pack(pady=18)

b2 = Button(root, text="View Vehicles", bg="black", fg="white", command=fun, width=20, height=2)
b2.pack(pady=18)
b2 = Button(root, text="Rent Vehicle", bg="black", fg="white", command=fun, width=20, height=2)
b2.pack(pady=18)
b2 = Button(root, text="Return Vehicle", bg="black", fg="white", command=fun, width=20, height=2)
b2.pack(pady=18)


b3 = Button(root, text="Exit", bg="black", fg="white", command=exit,width=18, height=2)
b3.pack(pady=18)










root.mainloop()




#query ececutions from here

#cursor.execute("create table s1(Name varchar(255),Roll_no int)")

#print("Table Created")

#insert_query = "insert into s1 values('san',11)"

#cursor.execute(insert_query)
#conn.commit()  # Commit the transaction to save changes
#print("inserted into the table")

# Query the s1 table
#cursor.execute("SELECT * FROM s1")
#fetch_query = cursor.fetchall()
#print("\nData from s1 table:")
#for row in fetch_query:
#    print(row)


    #if conn.is_connected():
        #print("✅ Connected to MySQL database successfully!")
        #db_info = conn.get_server_info()
        #print("MySQL server version:", db_info)

#except Error as e:
    #print("❌ Error:", e)

#finally:
    #if 'conn' in locals() and conn.is_connected():
        #conn.close()
        #print("🔒 Connection closed.")
