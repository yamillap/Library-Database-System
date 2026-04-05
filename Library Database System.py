import tkinter as tk
from tkinter import ttk
import oracledb
from tkinter import messagebox

def connectDB():
    user = entry_username.get()  
    password = entry_password.get()  
    sid = entry_service.get()  
   
    connect_string = "localhost:1521/xe"

    try:
       
        connection = oracledb.connect(
            user=user,
            password=password,
            dsn=connect_string
        )
        result.config(text="Connected to the database!", fg="green")
        messagebox.showinfo("Success", "Connected to the database!")
        openNewWindow(connection) 
        return connection
    except oracledb.DatabaseError as e:
        error_message = str(e)
        result.config(text="Connection failed!", fg="red")
        messagebox.showerror("Error", f"Failed to connect: {error_message}")
        return None

def on_button_click(button_id, connection):
    if button_id == 2:  
        create_table(connection)
    if button_id == 1:
        drop_table(connection)
    if button_id == 3:  
        populate_table(connection)
    if button_id == 4:
        query(connection)
    if button_id == 6:  
        search_records(connection)
    if button_id == 5:  
        root.destroy()    
    if button_id == 7:  
        read_update_delete_records(connection)

def openNewWindow(connection):
    qwindow = tk.Toplevel(root)
    qwindow.title("Database Operations")
    qwindow.geometry("400x500")

    button1 = tk.Button(qwindow, text="Drop tables", command=lambda: on_button_click(1, connection))
    button1.pack(pady=5)  

    button2 = tk.Button(qwindow, text="Create tables", command=lambda: on_button_click(2, connection))
    button2.pack(pady=5)

    button3 = tk.Button(qwindow, text="Populate tables", command=lambda: on_button_click(3, connection))
    button3.pack(pady=5)

    button4 = tk.Button(qwindow, text="Query tables", command=lambda: on_button_click(4, connection))
    button4.pack(pady=5)

    button5 = tk.Button(qwindow, text="Exit", command=lambda: on_button_click(5, connection))
    button5.pack(pady=5)

    button6 = tk.Button(qwindow, text="Search records", command=lambda: on_button_click(6, connection))
    button6.pack(pady=5)

    button7 = tk.Button(qwindow, text="Read/Update/Delete Records", command=lambda: on_button_click(7, connection))
    button7.pack(pady=5)

def create_table(connection):
    try:
        cursor = connection.cursor()

        sql_create_table_book = """
        CREATE TABLE Book (
            Genre VARCHAR2(25) NOT NULL,
            Title VARCHAR2(30) NOT NULL,
            Author VARCHAR2(30) NOT NULL,
            Book_ID INT NOT NULL,
            Book_Language VARCHAR2(15) NOT NULL,
            PRIMARY KEY (Book_ID)
        )
        """
        cursor.execute(sql_create_table_book)

        sql_create_table_customer = """
        CREATE TABLE Customer (
            Email VARCHAR2(70) NOT NULL,
            Member_ID INT NOT NULL,
            First_Name VARCHAR2(15) NOT NULL,
            Last_Name VARCHAR2(15) NOT NULL,
            Address VARCHAR2(50) NOT NULL,
            Book_Loan_ID INT NOT NULL,
            Fee_Due_Date DATE NOT NULL,
            PRIMARY KEY (Member_ID)
        )
        """
        cursor.execute(sql_create_table_customer)

        sql_create_table_member_fine_info = """
        CREATE TABLE Member_Fine_Info (
            Member_ID INT NOT NULL,
            Fine_ID INT UNIQUE NOT NULL,
            Pay_Date DATE NOT NULL,
            Amount DECIMAL(4, 2) DEFAULT 1.50,
            PRIMARY KEY (Member_ID, Fine_ID),
            FOREIGN KEY (Member_ID) REFERENCES Customer(Member_ID)
        )
        """
        cursor.execute(sql_create_table_member_fine_info)

        sql_create_table_fees_info = """
        CREATE TABLE Fees_Info (
            Fees_ID INT UNIQUE NOT NULL,
            Fine_Status INT NOT NULL,
            FOREIGN KEY (Fees_ID) REFERENCES Member_Fine_Info(Fine_ID)
        )
        """
        cursor.execute(sql_create_table_fees_info)

        sql_create_table_book_fine_info = """
        CREATE TABLE Book_Fine_Info (
            Pay_Date DATE NOT NULL,
            Fine_Due DATE,
            Book_ID INT NOT NULL,
            Member_ID INT NOT NULL,
            Fine_Status INT NOT NULL, -- 0 = Not Paid, 1 = Paid
            PRIMARY KEY (Book_ID, Member_ID),
            FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID),
            FOREIGN KEY (Member_ID) REFERENCES Customer(Member_ID)
        )
        """
        cursor.execute(sql_create_table_book_fine_info)

        sql_create_table_book_loan = """
        CREATE TABLE Book_Loan (
            Member_ID INT NOT NULL,
            Book_ID INT NOT NULL,
            Book_Time_Length INT NOT NULL,
            Num_Of_Copies INT NOT NULL,
            PRIMARY KEY (Book_ID, Member_ID),
            FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID),
            FOREIGN KEY (Member_ID) REFERENCES Customer(Member_ID)
        )
        """
        cursor.execute(sql_create_table_book_loan)

        sql_create_table_publisher = """
        CREATE TABLE Publisher (
            Publisher_Name VARCHAR2(25),
            Publication_Date DATE NOT NULL,
            Book_ID INT NOT NULL,
            PRIMARY KEY (Book_ID, Publisher_Name),
            FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID)
        )
        """
        cursor.execute(sql_create_table_publisher)

        connection.commit()

        result.config(text="Tables created successfully!", fg="green")
        messagebox.showinfo("Success", "Tables created successfully!")

    except oracledb.DatabaseError as e:
        error_message = str(e)
        result.config(text=f"Error creating table: {error_message}", fg="red")
        messagebox.showerror("Error", f"Error creating table: {error_message}")

def drop_table(connection):
    try:
        cursor = connection.cursor()

        tables = [
            "Publisher",
            "Book_Loan",
            "Book_Fine_Info",
            "Fees_Info",
            "Member_Fine_Info",
            "Customer",
            "Book"
        ]

        for table in tables:
            try:
                sql_drop_table = f"DROP TABLE {table} CASCADE CONSTRAINTS"

                cursor.execute(sql_drop_table)

                connection.commit()

                result.config(text=f"Table '{table}' dropped successfully!", fg="green")
                messagebox.showinfo("Success", f"Table '{table}' dropped successfully!")

            except oracledb.DatabaseError as e:
                error_message = str(e)
                result.config(text=f"Error dropping table '{table}': {error_message}", fg="red")
                messagebox.showerror("Error", f"Error dropping table '{table}': {error_message}")

    except oracledb.DatabaseError as e:
        error_message = str(e)
        result.config(text=f"Error dropping tables: {error_message}", fg="red")
        messagebox.showerror("Error", f"Error dropping tables: {error_message}")

def populate_table(connection):
    try:
        cursor = connection.cursor()
        

        book_inserts = [
            ('Drama', 'To Kill a Mockingbird', 'Harper Lee', 2839, 'English'),
            ('Coming of Age', 'Catcher in the Rye', 'J.D. Salinger', 462, 'English'),
            ('Fiction', 'The Great Gatsby', 'F. Scott Fitzgerald', 435671, 'English'),
            ('Science Fiction', 'Dune', 'Frank Herbert', 497511, 'English'),
            ('Mystery', 'The Dragon Tattoo', 'Stieg Larsson', 409571, 'Swedish'),
            ('Historical Fiction', 'The Book Thief', 'Markus Zusak', 405411, 'English'),
            ('Drama', 'I Saw The Light', 'Russo Teddy', 8154, 'French'),
            ('Fantasy', 'Harry Potter', 'J.K. Rowling', 485615, 'English')
        ]

        for row in book_inserts:
            cursor.execute("""
            INSERT INTO Book (Genre, Title, Author, Book_ID, Book_Language)
            VALUES (:1, :2, :3, :4, :5)
            """, row)
        connection.commit()

        customer_inserts = [
            ('jim.taney@gmail.com', 73819, 'Jim', 'Taney', '371 Oak Avenue', 3921, '2024-02-11'),
            ('carl.julio@yahoo.ca', 64872, 'Carl', 'Julio', '5638 Ridge Rd E', 47284, '2024-05-26'),
            ('john.doe@example.com', 809375, 'John', 'Doe', '123 Elm St', 1, '9999-12-31'),
            ('jane.smith@example.com', 887777, 'Jane', 'Smith', '456 Oak Ave', 0, '9999-12-31'),
            ('alice.johnson@example.com', 873516, 'Alice', 'Johnson', '789 Maple Dr', 2, '2024-10-15'),
            ('bob.brown@example.com', 811222, 'Bob', 'Brown', '321 Pine Rd', 3, '2024-05-11'),
            ('emily.davis@example.com', 899000, 'Emily', 'Davis', '654 Cedar Blvd', 4, '9999-12-31')
        ]

        for row in customer_inserts:
            cursor.execute("""
            INSERT INTO Customer (Email, Member_ID, First_Name, Last_Name, Address, Book_Loan_ID, Fee_Due_Date)
            VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'))
            """, row)
        connection.commit()

        member_fine_info_inserts = [
            (873516, 2432, '9999-12-31', 20.00),
            (811222, 2112, '9999-12-31', 10.00),
            (64872, 2637, '2024-12-08', 5.60),
            (73819, 37618, '1998-01-01', 74.50),
            (899000, 2719, '2024-12-31', 25.00),
            (811222, 9371, '2021-09-29', 15.50),
            (899000, 57182, '2019-08-15', 9.55)
        ]

        for row in member_fine_info_inserts:
            cursor.execute("""
            INSERT INTO Member_Fine_Info (Member_ID, Fine_ID, Pay_Date, Amount)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)
            """, row)
        connection.commit()

        fees_info_inserts = [
            (37618, 0),
            (2719, 1),
            (2637, 1),
            (2432, 0)
        ]

        for row in fees_info_inserts:
            cursor.execute("""
            INSERT INTO Fees_Info (Fees_ID, Fine_Status)
            VALUES (:1, :2)
            """, row)
        connection.commit()

        book_fine_info_inserts = [
            ('2021-09-29', None, 497511, 811222, 1),
            ('9999-12-31', '2024-05-11', 409571, 811222, 0),
            ('2019-08-15', '2020-08-15', 485615, 873516, 0),
            ('1998-01-01', '1999-01-01', 2839, 73819, 1),
            ('2010-06-15', '2011-06-15', 462, 64872, 0)
        ]

        for row in book_fine_info_inserts:
            cursor.execute("""
            INSERT INTO Book_Fine_Info (Pay_Date, Fine_Due, Book_ID, Member_ID, Fine_Status)
            VALUES (TO_DATE(:1, 'YYYY-MM-DD'), TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5)
            """, row)
        connection.commit()

        book_loan_inserts = [
            (73819, 462, 20, 5),
            (809375, 485615, 14, 4),
            (873516, 405411, 5, 2),
            (811222, 409571, 2, 6),
            (899000, 497511, 20, 1),
            (809375, 2839, 20, 3),
            (899000, 462, 7, 4),
            (809375, 405411, 3, 1)
        ]

        for row in book_loan_inserts:
            cursor.execute("""
            INSERT INTO Book_Loan (Member_ID, Book_ID, Book_Time_Length, Num_Of_Copies)
            VALUES (:1, :2, :3, :4)
            """, row)
        
        publisher_inserts = [
            ('LippinCott', '1960-08-27', 2839),
            ('Knoxknot', '1979-09-26', 462),
            ('Luminous Leaf Publishing', '1999-01-01', 435671),
            ('Luminous Leaf Publishing', '1990-02-15', 497511),
            ('Evergreen Publishing', '2021-05-24', 8154),
            ('Inkspire Press', '2003-12-01', 409571),
            ('Inkspire Press', '2010-05-26', 405411),
            ('Evergreen Publishing', '2001-06-04', 485615)
        ]

        for row in publisher_inserts:
            cursor.execute("""
            INSERT INTO Publisher (Publisher_Name, Publication_Date, Book_ID)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3)
            """, row)
        connection.commit()


        result.config(text="Tables populated successfully!", fg="green")
        messagebox.showinfo("Success", "Tables populated successfully!")

    except oracledb.DatabaseError as e:
        error_message = str(e)
        result.config(text=f"Error populating tables: {error_message}", fg="red")
        messagebox.showerror("Error", f"Error populating tables: {error_message}")


def query(connection):
    query_window = tk.Toplevel(root)
    query_window.title("Query Database")
    query_window.geometry("400x300")

    query_label = tk.Label(query_window, text="Enter your SQL query:")
    query_label.pack(pady=10)


    query_entry = tk.Entry(query_window, width=40)
    query_entry.pack(pady=5)


    def execute_query():
        sql_query = query_entry.get()
        try:

            cursor = connection.cursor()


            cursor.execute(sql_query)


            results = cursor.fetchall()


            if not results:
                result_text.insert(tk.END, "No results found.\n")
            else:

                result_text.delete(1.0, tk.END)  
                
                for row in results:
                    result_text.insert(tk.END, str(row) + "\n")


            connection.commit()

        except oracledb.DatabaseError as e:
            error_message = str(e)
            messagebox.showerror("Error", f"Error executing query: {error_message}")


    execute_button = tk.Button(query_window, text="Execute Query", command=execute_query)
    execute_button.pack(pady=10)


    result_text = tk.Text(query_window, height=10, width=50)
    result_text.pack(pady=10)

def read_update_delete_records(connection):
    action_window = tk.Toplevel(root)
    action_window.title("Read/Update/Delete Records")
    action_window.geometry("500x500")

    label = tk.Label(action_window, text="Enter Customer Email, Address or Name You Want to Change")
    label.pack(pady=10)

    entry_field = tk.Entry(action_window)
    entry_field.pack(pady=5)

    label2 = tk.Label(action_window, text="Enter the new Customer Email You Want it Changed to" )
    label2.pack(pady= 10)

    change_email_field = tk.Entry(action_window)
    change_email_field.pack(pady=10)

    label3 = tk.Label(action_window, text="Enter the new Customer Address You Want it Changed to" )
    label3.pack(pady= 10)

    change_address_field = tk.Entry(action_window)
    change_address_field.pack(pady=10)

    label4 = tk.Label(action_window, text="Enter the new Customer First Name and Last Name You Want it Changed to" )
    label4.pack(pady= 10)

    change_fn_field = tk.Entry(action_window)
    change_fn_field.pack(pady=10)

    change_ln_field = tk.Entry(action_window)
    change_ln_field.pack(pady=10)

    label5 = tk.Label(action_window, text="Enter Customer Email to Delete Record" )
    label5.pack(pady= 10)

    del_field = tk.Entry(action_window)
    del_field.pack(pady=10)

    def read_record():
        identifier = entry_field.get()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM Customer WHERE Email = :1
        """, (identifier,))
        record = cursor.fetchone()
        if record:
            result_text = f"Customer Found: {record}"
        else:
            result_text = "No customer found with that email."
        result_label.config(text=result_text)

    def update_record():
        identifier = entry_field.get()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM Customer WHERE Email = :1
        """, (identifier,))
        record = cursor.fetchone()
        if record:
            new_email = change_email_field.get()
            cursor.execute("""
            UPDATE Customer SET Email = :1 WHERE Email = :2
            """, (new_email, identifier))
            connection.commit()
            result_label.config(text="Customer email updated successfully!")
        
        identifier = entry_field.get()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM Customer WHERE Address = :5
        """, (identifier,))
        record = cursor.fetchone()
        if record:
            new_address = change_address_field.get()
            cursor.execute("""
            UPDATE Customer SET Address = :5 WHERE Address = :2
            """, (new_address, identifier))
            connection.commit()
            result_label.config(text="Customer address updated successfully!")
        
        names = identifier.split()
        if len(names) == 2:
            fn = names[0]
            ln = names[1]
            cursor = connection.cursor()

            cursor.execute("""
            SELECT * FROM Customer WHERE First_Name = :3 AND Last_Name = :4
            """, (fn,ln))
            record = cursor.fetchone()
            if record:
                new_fn = change_fn_field.get()
                new_ln = change_ln_field.get()
                cursor.execute("""
                UPDATE Customer SET First_Name = :3 WHERE First_Name = :2
                """, (new_fn, fn))

                cursor.execute("""
                UPDATE Customer SET Last_Name = :4 WHERE Last_Name = :2
                """, (new_ln, ln))
                connection.commit()
                result_label.config(text="Customer Name updated successfully!")
            else:
                result_label.config(text="No customer found with that email, address or name")

    def delete_record():
        identifier = del_field.get() 

        try:
            cursor = connection.cursor()

        
            cursor.execute("SELECT Member_ID FROM Customer WHERE Email = :1", (identifier,))
            result = cursor.fetchone()
            
            if result is None:
                result_label.config(text="No customer found with the provided email.", fg="red")
                return

            member_id = result[0]


            cursor.execute("DELETE FROM Fees_Info WHERE Fees_ID IN (SELECT Fine_ID FROM Member_Fine_Info WHERE Member_ID = :1)", (member_id,))
            cursor.execute("DELETE FROM Member_Fine_Info WHERE Member_ID = :1", (member_id,))
            cursor.execute("DELETE FROM Book_Fine_Info WHERE Member_ID = :1", (member_id,))
            cursor.execute("DELETE FROM Book_Loan WHERE Member_ID = :1", (member_id,))
            cursor.execute("DELETE FROM Customer WHERE Email = :1", (identifier,))

            connection.commit()
            result_label.config(text="Customer and related records deleted successfully!", fg="green")
        except Exception as e:
            connection.rollback()  
            result_label.config(text=f"Error: {str(e)}", fg="red")
        finally:
            cursor.close()

    read_button = tk.Button(action_window, text="Read", command=read_record)
    read_button.pack(pady=5)

    update_button = tk.Button(action_window, text="Update", command=update_record)
    update_button.pack(pady=5)

    delete_button = tk.Button(action_window, text="Delete", command=delete_record)
    delete_button.pack(pady=5)

    result_label = tk.Label(action_window, text="")
    result_label.pack(pady=10)

def search_records(connection):
    search_window = tk.Toplevel(root)
    search_window.title("Search Records")
    search_window.geometry("300x200")

    label = tk.Label(search_window, text="Enter Email (for Customer search):")
    label.pack(pady=10)

    search_entry = tk.Entry(search_window)
    search_entry.pack(pady=5)

    def perform_search():
        email = search_entry.get()
        try:
            cursor = connection.cursor()
            cursor.execute("""
            SELECT * FROM Customer WHERE Email = :1
            """, (email,))
            result_set = cursor.fetchall()
            if result_set:
                display_text = "\n".join([str(row) for row in result_set])
                messagebox.showinfo("Search Results", f"Found record: \n{display_text}")
            else:
                messagebox.showinfo("No Results", "No customer found with that email address.")
        except oracledb.DatabaseError as e:
            error_message = str(e)
            messagebox.showerror("Error", f"Error searching records: {error_message}")

    search_button = tk.Button(search_window, text="Search", command=perform_search)
    search_button.pack(pady=10)


root = tk.Tk()
root.title("Assignment 9")
root.geometry("400x300")  

result = tk.Label(root, text="Enter credentials and connect")
result.pack(pady=10)

entry_username = tk.Label(root, text="Username")
entry_username.pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

entry_password = tk.Label(root, text="Password")
entry_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

entry_service = tk.Label(root, text="Service name OR sid")
entry_service.pack(pady=10)
entry_service = tk.Entry(root)
entry_service.pack(pady=5)

btn_connect = tk.Button(root, text="Connect to DB", command=connectDB)
btn_connect.pack(pady=10)

root.mainloop()