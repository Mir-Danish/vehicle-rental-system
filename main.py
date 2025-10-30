#import mysql.connector as sql
#from mysql.connector import Error
from nt import rename
from textwrap import fill
import pymysql
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

root = Tk()
root.title("Vehicle Rental System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.configure(bg="#E8F0FE")

print("connecting")
def connect_to_database():
    connectdb = pymysql.connect(
        host="localhost",
        user="root",
        password="tiger123",
        database="vehicle_records"
    )
    print("Connected to database")
    return connectdb
connectdb = connect_to_database()

def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(50),
        model VARCHAR(100),
        rent_per_day FLOAT,
        available VARCHAR(10)
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_id INT,
        customer_id INT,
        rent_date DATE,
        return_date DATE,
        services VARCHAR(255),
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )''')
    conn.commit()
    cursor.close()
    conn.close()

def open_rent_car():
    form_window = tk.Toplevel(root)
    form_window.title("Rent A Car")
    form_window.geometry("800x400+300+300")

    center_frame = Frame(form_window)
    center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    tk.Label(center_frame, text="Vehicle Type:", font=("Segoe UI", 10)).grid(row=0, column=0, pady=10, padx=10, sticky=E)
    name_entry = tk.Entry(center_frame, width=30, font=("Segoe UI", 10))
    name_entry.grid(row=0, column=1, pady=10, padx=10)
    tk.Label(center_frame, text="Model:", font=("Segoe UI", 10)).grid(row=1, column=0, pady=10, padx=10, sticky=E)
    model_entry = tk.Entry(center_frame, width=30, font=("Segoe UI", 10))
    model_entry.grid(row=1, column=1, pady=10, padx=10)
    tk.Label(center_frame, text="Rent Per Day:", font=("Segoe UI", 10)).grid(row=2, column=0, pady=10, padx=10, sticky=E)
    rent_entry = tk.Entry(center_frame, width=30, font=("Segoe UI", 10))
    rent_entry.grid(row=2, column=1, pady=10, padx=10)
    
    def save_Vehicle():
        vtype = name_entry.get()
        model = model_entry.get()
        rent = rent_entry.get()
        if not (vtype and model and rent):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vehicles (type, model, rent_per_day, available) VALUES (%s, %s, %s, 'Yes')",(vtype, model, rent))
            conn.commit()
            messagebox.showinfo("Success", "Vehicle added successfully!", parent=form_window)
            form_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add vehicle: {str(e)}", parent=form_window)
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    Button(center_frame, text="Save Vehicle", command=save_Vehicle, bg="blue", fg="white", font=("Segoe UI", 10)).grid(row=3, column=0, columnspan=2, pady=20)
    print("Vehicle Added Successfully!")


def view_vehicles():
    view_window = tk.Toplevel(root)
    view_window.title("View Vehicles")
    view_window.geometry("800x400+300+300")

    cols = ("ID", "Type", "Model", "Rent/Day", "Status")
    tree = ttk.Treeview(view_window, columns=cols, show="headings")
    column_widths = {
        "ID": 50,
        "Type": 100,
        "Model": 150,
        "Rent/Day": 100,
        "Status": 100
    }
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths.get(col, 100), anchor='center')
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True, padx=10, pady=5)
    def load_vehicles():
        conn = None
        cursor = None
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    v.vehicle_id, 
                    v.type, 
                    v.model, 
                    v.rent_per_day,
                    CASE 
                        WHEN v.available = 'Yes' THEN 'Available'
                        ELSE 'Rented'
                    END as status
                FROM vehicles v
                ORDER BY v.available DESC, v.vehicle_id
            ''')
            for item in tree.get_children():
                tree.delete(item)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row, 
                          tags=('rented' if row[4] == 'Rented' else 'available'))
            tree.tag_configure('rented', background='#ffdddd')
            tree.tag_configure('available', background='#ddffdd')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vehicles: {str(e)}", parent=view_window)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    load_vehicles()
    view_window.mainloop()



#main window
def rent_vehicle_window():
    top = Toplevel()
    top.title("Rent Vehicle")
    top.geometry("500x450+400+200")

    center_frame = Frame(top)
    center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    Label(center_frame, text="Vehicle ID:", font=("Segoe UI", 10)).grid(row=0, column=0, pady=10, padx=10, sticky=E)
    vehicle_entry = Entry(center_frame, width=25, font=("Segoe UI", 10))
    vehicle_entry.grid(row=0, column=1, pady=10, padx=10)
    Label(center_frame, text="Customer Name:", font=("Segoe UI", 10)).grid(row=1, column=0, pady=10, padx=10, sticky=E)
    name_entry = Entry(center_frame, width=25, font=("Segoe UI", 10))
    name_entry.grid(row=1, column=1, pady=10, padx=10)
    Label(center_frame, text="Phone:", font=("Segoe UI", 10)).grid(row=2, column=0, pady=10, padx=10, sticky=E)
    phone_entry = Entry(center_frame, width=25, font=("Segoe UI", 10))
    phone_entry.grid(row=2, column=1, pady=10, padx=10)
    Label(center_frame, text="Additional Services:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=(15, 5))
    insurance_var = IntVar()
    gps_var = IntVar()
    child_seat_var = IntVar()
    Checkbutton(center_frame, text="Insurance (+$10/day)", variable=insurance_var, font=("Segoe UI", 9)).grid(row=4, column=0, columnspan=2, sticky=W, padx=40)
    Checkbutton(center_frame, text="GPS Navigation (+$5/day)", variable=gps_var, font=("Segoe UI", 9)).grid(row=5, column=0, columnspan=2, sticky=W, padx=40)
    Checkbutton(center_frame, text="Child Seat (+$3/day)", variable=child_seat_var, font=("Segoe UI", 9)).grid(row=6, column=0, columnspan=2, sticky=W, padx=40)

    def rent_vehicle():
        vid = vehicle_entry.get()
        name = name_entry.get()
        phone = phone_entry.get()
        if not (vid and name and phone):
            messagebox.showwarning("Input Error", "All fields required!", parent=top)
            return
        
        # Get selected services
        services = []
        if insurance_var.get():
            services.append("Insurance")
        if gps_var.get():
            services.append("GPS")
        if child_seat_var.get():
            services.append("Child Seat")
        
        conn = None
        cursor = None
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT available FROM vehicles WHERE vehicle_id=%s", (vid,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Invalid vehicle ID.", parent=top)
                return 
            if row[0] == 'No':
                messagebox.showwarning("Unavailable", "Vehicle already rented.", parent=top)
                return
            cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
            cid = cursor.lastrowid
            # Convert services list to comma-separated string
            services_str = ', '.join(services) if services else 'None'
            cursor.execute("""
                INSERT INTO rentals (vehicle_id, customer_id, rent_date, return_date, services) 
                VALUES (%s, %s, CURDATE(), NULL, %s)
            """, (vid, cid, services_str))
            cursor.execute("UPDATE vehicles SET available='No' WHERE vehicle_id=%s", (vid,))
            conn.commit()
            
            # Show success message with selected services
            services_msg = f" with services: {', '.join(services)}" if services else ""
            messagebox.showinfo("Success", f"Vehicle rented successfully{services_msg}!", parent=top)
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rent vehicle: {str(e)}", parent=top)
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    Button(center_frame, text="Confirm Rent", command=rent_vehicle, bg="green", fg="white", 
           width=20, font=("Segoe UI", 10)).grid(row=7, column=0, columnspan=2, pady=20)
    print("Vehicle rented successfully!")
   


def view_rented_vehicles():
    rented_window = tk.Toplevel(root)
    rented_window.title("Rented Vehicles")
    rented_window.geometry("1000x400+250+300")

    # Create Treeview with columns
    cols = ("Rental ID", "Vehicle ID", "Type", "Model", "Customer Name", "Phone", "Rent Date", "Services")
    tree = ttk.Treeview(rented_window, columns=cols, show="headings")
    column_widths = {
        "Rental ID": 70,"Vehicle ID": 70,"Type": 100,"Model": 120,"Customer Name":120,"Phone": 100,"Rent Date": 100,"Services": 150
    }
    
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths.get(col, 100), anchor='center')
    scrollbar = ttk.Scrollbar(rented_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True, padx=10, pady=5)

    def load_rented_vehicles():
        conn = None
        cursor = None
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.rental_id, v.vehicle_id, v.type, v.model, 
                       c.name, c.phone, r.rent_date, r.services
                FROM rentals r
                JOIN vehicles v ON r.vehicle_id = v.vehicle_id
                JOIN customers c ON r.customer_id = c.customer_id
                WHERE r.return_date IS NULL
                ORDER BY r.rent_date DESC
            ''')
            for item in tree.get_children():
                tree.delete(item)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load rented vehicles: {str(e)}", parent=rented_window)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    load_rented_vehicles()
    print("Rented vehicles loaded successfully!")
    rented_window.mainloop()


def return_vehicle_window():
    return_window = Toplevel()
    return_window.title("Return Vehicle")
    return_window.geometry("500x300+400+250")
    center_frame = Frame(return_window)
    center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    Label(center_frame, text="Rental ID:", font=("Segoe UI", 12)).grid(row=0, column=0, pady=15, padx=15, sticky=E)
    rental_entry = Entry(center_frame, width=30, font=("Segoe UI", 12))
    rental_entry.grid(row=0, column=1, pady=15, padx=15)

    def return_vehicle():
        rid = rental_entry.get()
        if not rid:
            messagebox.showwarning("Input Error", "Please enter rental ID.", parent=return_window)
            return
        conn = None
        cursor = None
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT vehicle_id 
                FROM rentals 
                WHERE rental_id = %s AND return_date IS NULL
            """, (rid,))

            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Invalid or already returned rental ID.", parent=return_window)
                return
            vehicle_id = result[0]
            cursor.execute("""
                UPDATE rentals 
                SET return_date = CURDATE() 
                WHERE rental_id = %s
            """, (rid,))
            cursor.execute("""
                UPDATE vehicles 
                SET available = 'Yes' 
                WHERE vehicle_id = %s
            """, (vehicle_id,))
            conn.commit()
            messagebox.showinfo("Success", "Vehicle returned successfully!", parent=return_window)
            return_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return vehicle: {str(e)}", parent=return_window)
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    Button(center_frame, text="Return Vehicle", command=return_vehicle, 
           bg="#4CAF50", fg="white", width=25, font=("Segoe UI", 11, "bold")).grid(row=1, column=0, columnspan=2, pady=20)
    print("Vehicle returned successfully!")


def exit():
    root.destroy()



#main code
photo =PhotoImage(file="p1 (2).png")
p = Button(root, text="click me", image=photo).pack(pady=18)

button_frame1 = Frame(root, bg="#E8F0FE")
button_frame1.pack(pady=10)

b1 = Button(button_frame1, text="Add Vehicle", font=("segeo",10,"bold"),bg="#2196F3", fg="white", activeforeground="white", 
activebackground="#1E88E5", command=open_rent_car, width=20, height=2)
b1.pack(side=LEFT, padx=20, pady=5)

b2 = Button(button_frame1, text="View Vehicles", font=("segeo",10,"bold"),bg="#2196F3", fg="white", activeforeground="white",
activebackground="#1E88E5", command=view_vehicles, width=20, height=2)
b2.pack(side=LEFT, padx=20, pady=5)

button_frame2 = Frame(root, bg="#E8F0FE")
button_frame2.pack(pady=10)

b3 = Button(button_frame2, text="Rent Vehicle", font=("segeo",10,"bold"),bg="#4CAF50", fg="white", activeforeground="white",activebackground="#45a049", command=rent_vehicle_window, width=20, height=2)
b3.pack(side=LEFT, padx=20, pady=5)

b_return = Button(button_frame2, text="Return Vehicle", font=("segeo",10,"bold"),
bg="#404040", fg="white", activeforeground="white",activebackground="#2C2C2C", command=return_vehicle_window, width=20, height=2)
b_return.pack(side=LEFT, padx=20, pady=5)

button_frame3 = Frame(root, bg="#E8F0FE")
button_frame3.pack(pady=10)
b_rented = Button(button_frame3, text="Rented Vehicles", font=("segeo",10,"bold"),bg="#4CAF50", fg="white", activeforeground="white",activebackground="#45a049", command=view_rented_vehicles, width=20, height=2)
b_rented.pack(side=LEFT, padx=20, pady=5)

b_exit = Button(button_frame3, text="Exit", font=("segeo",10,"bold"),
bg="#f44336", fg="white", activeforeground="white",activebackground="#B22222", command=root.destroy, width=20, height=2)
b_exit.pack(side=LEFT, padx=20, pady=5)


root.mainloop()



