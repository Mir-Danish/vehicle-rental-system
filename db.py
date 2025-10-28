#import mysql.connector as sql
#from mysql.connector import Error
from nt import rename
from textwrap import fill
import pymysql
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


#root = Tk()
#root.title("Car Rental Management System")
#root.geometry("400x400+300+300")

root = Tk()
root.title("Vehicle Rental System")
root.geometry("500x500+300+300")




'''print("connecting")

def connect_to_database():
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
    connect_db = connect_to_database().cursor()
    connect_db.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(50),
        model VARCHAR(100),
        rent_per_day FLOAT,
        available VARCHAR(10)
    )''')
    connect_db.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )''')
    connect_db.execute('''CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_id INT,
        customer_id INT,
        rent_date DATE,
        return_date DATE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')
    connect_db.commit()
    connect_db.close()


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

        run_query = connect_to_database().cursor()
        run_query.execute("INSERT INTO vehicles (type, model, rent_per_day, available) VALUES (%s, %s, %s, 'Yes')",(vtype, model, rent))
        run_query.commit()
        run_query.close()
        
        messagebox.showinfo("Success", "Vehicle added successfully!", parent=form_window)
        form_window.destroy()

    Button(form_window, text="Save Vehicle",command=save_Vehicle, bg="blue", fg="white").place(x=150,y=120)
    


    
def view_vehicles():
    view_window = tk.Toplevel(root)
    view_window.title("View Vehicles")
    view_window.geometry("400x400+300+300")

    cols = ("ID", "Type", "Model", "Rent/Day", "Available")
    tree = ttk.Treeview(view_window, columns=cols, show="headings")
    
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

   

    connecttodb = connect_to_database()
    connectDB = connecttodb.cursor()
    connectDB.execute("SELECT * FROM vehicles")
    for row in connectDB.fetchall():
        tree.insert("",tk.END, values=row)
    connectDB.close()

    view_window.mainloop()




#main window
def rent_vehicle_window():
    win = Toplevel()
    win.title("Rent Vehicle")
    win.geometry("400x400")

    Label(win, text="Vehicle ID:").pack(pady=5)
    vehicle_entry = Entry(win)
    vehicle_entry.pack()

    Label(win, text="Customer Name:").pack(pady=5)
    name_entry = Entry(win)
    name_entry.pack()

    Label(win, text="Phone:").pack(pady=5)
    phone_entry = Entry(win)
    phone_entry.pack()




    def rent_vehicle():
        vid = vehicle_entry.get()
        name = name_entry.get()
        phone = phone_entry.get()
        if not (vid and name and phone):
            messagebox.showwarning("Input Error", "All fields required!", parent=win)
            return
     



        cursor = connect_to_database().cursor()
        # Check availability
        cursor.execute("SELECT available FROM vehicles WHERE vehicle_id=%s", (vid,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Error", "Invalid vehicle ID.", parent=win)
            cursor.close()
            return
        if row[0] == 'No':
            messagebox.showwarning("Unavailable", "Vehicle already rented.", parent=win)
            cursor.close()
            return
        # Add customer rental information
        cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
        cid = cursor.lastrowid
        cursor.execute("INSERT INTO rentals (vehicle_id, customer_id, rent_date, return_date) VALUES (%s, %s, %s, NULL)",
                  (vid, cid, date.today()))
        cursor.execute("UPDATE vehicles SET available='No' WHERE vehicle_id=%s", (vid,))
        cursor.commit()
        cursor.close()
        messagebox.showinfo("Success", "Vehicle rented successfully!", parent=win)
        win.destroy()

    Button(win, text="Confirm Rent", command=rent_vehicle, bg="green", fg="white").pack(pady=15)
   

def return_vehicle_window():
    win = Toplevel()
    win.title("Return Vehicle")
    win.geometry("400x200")

    Label(win, text="Rental ID:").pack(pady=5)
    rental_entry = Entry(win)
    rental_entry.pack()

    def return_vehicle():
        rid = rental_entry.get()
        if not rid:
            messagebox.showwarning("Input Error", "Enter rental ID.", parent=win)
            return


        #conn = connect_db()
        connecttodb = connect_to_database().cursor()
        connecttodb.execute("SELECT vehicle_id FROM rentals WHERE rental_id=%s", (rid,))
        row = connecttodb.fetchone()
        if not row:
            messagebox.showerror("Error", "Invalid rental ID.", parent=win)
            connecttodb.close()
            return
        vid = row[0]
        connecttodb.execute("UPDATE rentals SET return_date=%s WHERE rental_id=%s", (date.today(), rid))
        connecttodb.execute("UPDATE vehicles SET available='Yes' WHERE vehicle_id=%s", (vid,))
        connecttodb.commit()
        connecttodb.close()
        messagebox.showinfo("Success", "Vehicle returned successfully!", parent=win)
        win.destroy()

    Button(win, text="Return Vehicle", command=return_vehicle, bg="orange", fg="white").pack(pady=15)


def exit():
    root.destroy()



#main code
w = Label(root, text="Vehicle Rental System", font=("Arial",16,"bold"))
w.pack(pady=20)


b1 = Button(root, text="Add Vehicle",bg="black", fg="white", activeforeground="blue", activebackground="blue",command=open_rent_car, width=20, height=2)
b1.pack(pady=18)

b2 = Button(root, text="View Vehicles", bg="black", fg="white", command=view_vehicles, width=20, height=2)
b2.pack(pady=18)
b2 = Button(root, text="Rent Vehicle", bg="black", fg="white", command=rent_vehicle_window, width=20, height=2)
b2.pack(pady=18)
b2 = Button(root, text="Return Vehicle", bg="black", fg="white", command=return_vehicle_window, width=20, height=2)
b2.pack(pady=18)


b3 = Button(root, text="Exit", bg="red", fg="white", command=exit,width=18, height=2)
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
