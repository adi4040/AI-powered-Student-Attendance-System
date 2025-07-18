import csv
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import re
from datetime import datetime
from tkinter import messagebox, ttk, END

# Set the theme and color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AnimatedGIFLabel(ctk.CTkLabel):
    def __init__(self, master, filename, width, height, delay=100):
        self.image = Image.open(filename)
        self.width = width
        self.height = height
        self.delay = delay
        self.frames = [ImageTk.PhotoImage(self.image.resize((width, height)))]

        ctk.CTkLabel.__init__(self, master, image=self.frames[0])

        self.idx = 0
        self.after(self.delay, self.update)

    def update(self):
        self.idx += 1
        try:
            self.image.seek(self.idx)
            self.frames.append(ImageTk.PhotoImage(self.image.resize((self.width, self.height))))
            self.configure(image=self.frames[-1])
        except EOFError:
            self.idx = 0
            self.image.seek(self.idx)
            self.frames = [ImageTk.PhotoImage(self.image.resize((self.width, self.height)))]

        self.after(self.delay, self.update)

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")

        self.db_password = 'Iamadam4040'

        #***************Text Variables****************
        self.var_id = ctk.StringVar()
        self.var_name = ctk.StringVar()
        self.var_roll = ctk.StringVar()
        self.var_dep = ctk.StringVar()
        self.var_date = ctk.StringVar()
        self.var_timein = ctk.StringVar()
        self.var_timeout = ctk.StringVar()
        self.fromEntry = ctk.StringVar()
        self.toEntry = ctk.StringVar()

        # Configure grid for root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame with padding
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure main frame grid
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title with increased padding
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Attendance Management",
            font=("Helvetica", 35, "bold"),
            text_color="#00ff9f"
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Create container frame
        self.container_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.container_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.container_frame.grid_columnconfigure(0, weight=1)

        # Create content frame with explicit size
        self.content_frame = ctk.CTkFrame(self.container_frame, 
                                        fg_color="#1a1a1a", 
                                        corner_radius=10,
                                        width=1400,
                                        height=600)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_propagate(False)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Configure grid for horizontal layout
        self.content_frame.grid_columnconfigure(0, weight=1)  # Left frame
        self.content_frame.grid_columnconfigure(1, weight=2)  # Right frame

        # Left frame - Attendance Details
        self.left_frame = ctk.CTkFrame(self.content_frame,
                                     fg_color="#2d2d2d",
                                     corner_radius=8,
                                     width=400,
                                     height=700)
        self.left_frame.grid(row=0, column=0, pady=50, padx=20)
        self.left_frame.grid_propagate(False)

        # Student ID & Roll Number
        id_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        id_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(id_frame, text="Student ID:", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(id_frame, textvariable=self.var_id, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        ctk.CTkLabel(id_frame, text="Roll No:", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(id_frame, textvariable=self.var_roll, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)

        # Name & Department
        name_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(name_frame, text="Name:", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(name_frame, textvariable=self.var_name, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        ctk.CTkLabel(name_frame, text="Department:", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        dep_combo = ctk.CTkComboBox(name_frame, values=["Select Department", "Computer", "IT", "Civil", "Mechanical"],
                                  variable=self.var_dep, width=150, font=("Helvetica", 12))
        dep_combo.pack(side="left", padx=5)

        # Date & Time
        time_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(time_frame, text="Date:", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(time_frame, textvariable=self.var_date, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        ctk.CTkLabel(time_frame, text="Time(In):", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(time_frame, textvariable=self.var_timein, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)

        # Time Out
        timeout_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        timeout_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(timeout_frame, text="Time(Out):", font=("Helvetica", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(timeout_frame, textvariable=self.var_timeout, width=150, font=("Helvetica", 12)).pack(side="left", padx=5)

        # Animated GIF
        gif_path = r"image_assets/face-scan.gif"
        gif_label = AnimatedGIFLabel(self.left_frame, gif_path, width=130, height=130)
        gif_label.pack(pady=20)

        # Button Frame
        btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)

        # Action Buttons
        ctk.CTkButton(btn_frame, text="Save", command=self.add_data, width=100, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Update", command=self.update_data, width=100, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_data, width=100, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Reset", command=self.reset_data, width=100, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        # Additional Buttons Frame
        additional_btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        additional_btn_frame.pack(fill="x", padx=20, pady=5)

        # Additional Buttons with consistent styling
        button_style = {
            "width": 150,
            "font": ("Helvetica", 12, "bold"),
            "fg_color": "#1a1a1a",
            "hover_color": "#2d2d2d",
            "text_color": "#00ff9f",
            "corner_radius": 10
        }

        ctk.CTkButton(additional_btn_frame, text="Reset Timings", command=self.reset_timings, **button_style).pack(pady=3)
        ctk.CTkButton(additional_btn_frame, text="Export CSV File", command=self.export_csv, **button_style).pack(pady=3)
        ctk.CTkButton(additional_btn_frame, text="Append Data", command=self.append_data, **button_style).pack(pady=3)

        # Right frame - Information
        self.right_frame = ctk.CTkFrame(self.content_frame,
                                      fg_color="#2d2d2d",
                                      corner_radius=8,
                                      width=800,
                                      height=600)
        self.right_frame.grid(row=0, column=1, pady=50, padx=20)
        self.right_frame.grid_propagate(False)

        # Search frame
        search_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=20)

        # Date search
        ctk.CTkLabel(search_frame, text="From:", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, textvariable=self.fromEntry, width=120, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        ctk.CTkLabel(search_frame, text="To:", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, textvariable=self.toEntry, width=120, font=("Helvetica", 12)).pack(side="left", padx=5)
        
        # Department filter
        ctk.CTkLabel(search_frame, text="Department:", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        self.dep_var = ctk.StringVar()
        self.dep_combo = ctk.CTkComboBox(search_frame, values=["All Departments","IoT", "Computer", "IT", "Civil", "Mechanical", "AIML", "AIDS"],
                                       variable=self.dep_var, width=150, font=("Helvetica", 12))
        self.dep_combo.pack(side="left", padx=5)
        self.dep_combo.set("All Departments")

        # Action buttons
        ctk.CTkButton(search_frame, text="Sort", command=self.sort_by_date, width=80, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Unsort", command=self.fetch_data, width=80, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Reset List", command=self.reset_list, width=80, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        # Table frame
        table_frame = ctk.CTkFrame(self.right_frame, fg_color="#000000", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create a frame to hold the table and scrollbars
        table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True)

        # Create Treeview with custom style
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure main treeview style
        style.configure(
            "Treeview",
            background="#000000",  # Black background
            foreground="white",    # White text
            fieldbackground="#000000",  # Black field background
            borderwidth=0,
            rowheight=25,
            font=('Helvetica', 11)
        )
        
        # Configure heading style
        style.configure(
            "Treeview.Heading",
            background="#1a1a1a",  # Dark gray header background
            foreground="white",    # White header text
            relief="flat",
            font=('Helvetica', 12, 'bold'),
            borderwidth=0
        )
        
        # Configure selected row style
        style.map('Treeview',
            background=[('selected', '#2d2d2d')],  # Dark gray for selected rows
            foreground=[('selected', 'white')]     # White text for selected rows
        )
        
        # Configure scrollbar style
        style.configure(
            "Vertical.TScrollbar",
            background="#1a1a1a",
            troughcolor="#000000",
            bordercolor="#000000",
            arrowcolor="white"
        )
        
        style.configure(
            "Horizontal.TScrollbar",
            background="#1a1a1a",
            troughcolor="#000000",
            bordercolor="#000000",
            arrowcolor="white"
        )

        # Create scrollbars
        scroll_y = ttk.Scrollbar(table_container, style="Vertical.TScrollbar")
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", style="Horizontal.TScrollbar")

        # Create the treeview with scrollbars
        self.student_table = ttk.Treeview(table_container, 
                                        columns=("ID", "Name", "Roll No", "Dep", "Date", "Time(In)", "Time(out)"),
                                        show="headings",
                                        style="Treeview",
                                        yscrollcommand=scroll_y.set,
                                        xscrollcommand=scroll_x.set)
        
        # Configure columns
        self.student_table.heading("ID", text="ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Roll No", text="Roll No")
        self.student_table.heading("Dep", text="Dep")
        self.student_table.heading("Date", text="Date")
        self.student_table.heading("Time(In)", text="Time(In)")
        self.student_table.heading("Time(out)", text="Time(out)")

        # Set column widths
        for col in ("ID", "Name", "Roll No", "Dep", "Date", "Time(In)", "Time(out)"):
            self.student_table.column(col, width=100)

        # Configure scrollbars
        scroll_y.config(command=self.student_table.yview)
        scroll_x.config(command=self.student_table.xview)

        # Grid layout for table and scrollbars
        self.student_table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Bind events
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        
        # Fetch initial data
        self.fetch_data()

    #***************Fetching data*********************
    def fetch_data(self):
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM attendancetb")
                data = my_cursor.fetchall()

                if len(data) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for row in data:
                        self.student_table.insert("", END, values=row)
                    conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)


    #****************getting cursor**********************
    def get_cursor(self,event=""):
        
        #focus the cursor on student table:
        cursor_focus = self.student_table.focus() 
        
        #get content of the item on which cursor is focussed:
        content = self.student_table.item(cursor_focus) 
        data = content["values"]

        #set the data from student_table into respective fields:
       
        self.var_id.set(data[0]),
        self.var_name.set(data[1]),
        self.var_roll.set(data[2]),
        self.var_dep.set(data[3])
        self.var_date.set(data[4]),
        self.var_timein.set(data[5]),
        self.var_timeout.set(data[6]),

    #**************Adding Data**********************
    def add_data(self):

        if not self.validating_fields():
            return

        #validating the empty fields
        if self.var_id.get()=="":
            messagebox.showerror("Error","Atleast Enter ID!",parent=self.root) #show box on same window
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into attendancetb values(%s,%s,%s,%s,%s,%s,%s)",( 
                                                                                                self.var_id.get(),
                                                                                                self.var_name.get(),
                                                                                                self.var_roll.get(),
                                                                                                self.var_dep.get(),
                                                                                                self.var_date.get(),
                                                                                                self.var_timein.get(),
                                                                                                self.var_timeout.get(),

                                                                                              ))          
                conn.commit()
                self.fetch_data() #as soon as save button is clicked, this function is called
                conn.close()
                messagebox.showinfo("Success","Student details have been added successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)



    #****************Updating data************************
    def update_data(self):

        if not self.validating_fields():
            return

        if self.var_dep.get()=="Select Department" or self.var_id.get()=="":
            messagebox.showerror("Error","Atleast Enter ID!",parent=self.root) #show box on same window
        else:
            try:
                Update = messagebox.askyesno("Update","Are you sure?",parent=self.root)
                if Update>0: 
                    conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update attendancetb set Name=%s, `Roll No`=%s,Dep=%s,Date=%s,`Status (In)`=%s,`Status (out)`=%s where ID = %s" ,(
                                                                                          
                                                                                            self.var_name.get(),
                                                                                            self.var_roll.get(),                                                                                            
                                                                                            self.var_dep.get(),                                                                                            
                                                                                            self.var_date.get(),
                                                                                            self.var_timein.get(),
                                                                                            self.var_timeout.get(),
                                                                                            self.var_id.get()
                                                                                            
                    ))
                else:
                    if not Update: #if user selects "No" it'll stay on the page
                        return
                messagebox.showinfo("success","Details Updated",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Unsuccessful attempt due to: {str(es)}",parent=self.root)


    #************Reset Data*******************
    def reset_data(self):
        self.var_dep.set("Select Department")       
        self.var_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_date.set("")
        self.var_timein.set("")
        self.var_timeout.set("")

    #************Delete Data******************
    def delete_data(self):
        if self.var_id.get()=="": 
            messagebox.showerror("Error","Student ID Required!",parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete Data","Are you Sure?",parent=self.root)
                if delete>0:
                   conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                   my_cursor = conn.cursor() 
                   sql = "delete from attendancetb where ID=%s"
                   val = (self.var_id.get(),)
                   my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                    
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Deleted Successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Unsuccessful attempt due to: {str(es)}",parent=self.root)
    
    #******************Reset In and Out Timing of all students************************
    def reset_timings(self,event=""):
            try:
                Update = messagebox.askyesno("Update","Are you sure?",parent=self.root)
                if Update>0:
                   conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                   my_cursor = conn.cursor()     
                   my_cursor.execute("UPDATE attendancetb SET `Status (In)` = '';")
                   my_cursor.execute("UPDATE attendancetb SET `Status (out)` = '';")
                   conn.commit()
                   self.fetch_data()
                   conn.close()
                   messagebox.showinfo("Delete","Timings Reset Successful!",parent=self.root)
                else:
                    if not Update: #if user selects "No" it'll stay on the page
                        return
            except Exception as es:
                messagebox.showerror("Error",f"Unsuccessful attempt due to: {str(es)}",parent=self.root)            

    #*******************Exporting CSV File***********************************
    def export_csv(self, event=""):
        try:
            # Fetching data from the student_table widget
            data = []
            for row in self.student_table.get_children():
                item = self.student_table.item(row)["values"]
                data.append(item)

            # Specify the path for the CSV file
            csv_file_path = "attendance.csv"

            # Open the CSV file in write mode
            with open(csv_file_path, 'w', newline='') as csv_file:
                # Create a CSV writer object
                csv_writer = csv.writer(csv_file, delimiter=';')

                # Write the header row
                header = ["ID", "Name", "Roll No", "Dep", "Date", "Time(In)", "Time(out)"]
                csv_writer.writerow(header)

                # Write the data rows
                csv_writer.writerows(data)

            messagebox.showinfo("Success", "Data exported successfully!", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)
 


    def validating_fields(self):
        # Validating Student ID
        student_id = self.var_id.get()
        if not student_id.isdigit():
            messagebox.showerror("Error", "ID should only contain numbers", parent=self.root)
            return False
            

        # Validating name
        name = self.var_name.get()
        if not name:
            messagebox.showerror("Error", "Name not entered", parent=self.root)
            return False

        if not re.match(r"^[A-Za-z\-\'\s]+$", name):
            messagebox.showerror("Error", "Invalid name", parent=self.root)
            return False

        return True

    def append_data(self):
        try:
            # Fetching data from the right frame's table
            data = []
            for row in self.student_table.get_children():
                item = self.student_table.item(row)["values"]
                # Skip the first column (ID) and append the rest of the columns
                data.append(item[1:])  

            # Establishing a connection to the database
            conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
            my_cursor = conn.cursor()

            # Inserting data into the append_data table
            for item in data:
                name, roll, dep, date, timein, timeout = item
                my_cursor.execute("INSERT INTO appended_data (Name, RollNo, Dep, Date, `Time(In)`, `Time(Out)`) VALUES (%s, %s, %s, %s, %s, %s)", (name, roll, dep, date, timein, timeout))

            # Committing the changes and closing the connection
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Data appended to 'append_data' table successfully!", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)

    
    def sort_by_date(self):
        try:
            # Clear previous data in the student_table
            self.student_table.delete(*self.student_table.get_children())

            # Get the entered from date, to date, and selected department
            from_date = self.fromEntry.get()
            to_date = self.toEntry.get()
            selected_dep = self.dep_var.get()

            # Validate the entered dates
            if not from_date or not to_date:
                messagebox.showerror("Error", "Please enter both from and to dates", parent=self.root)
                return

            # Establish connection to the database
            conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
            my_cursor = conn.cursor()

            # Base query
            query = "SELECT `Name`, `RollNo`, `Dep`, `Date`, `Time(In)`, `Time(Out)` FROM appended_data WHERE `Date` BETWEEN %s AND %s"
            params = [from_date, to_date]

            # Add department filter if not "All Departments"
            if selected_dep != "All Departments":
                query += " AND `Dep` = %s"
                params.append(selected_dep)

            # Execute query
            my_cursor.execute(query, params)
            data = my_cursor.fetchall()

            if len(data) != 0:
                # Insert the fetched data into the student_table
                for row in data:
                     self.student_table.insert("", END, values=[""] + list(row))
                conn.commit()
            else:
                messagebox.showinfo("Info", "No records found for the selected criteria", parent=self.root)

            # Close the database connection
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)

    def reset_list(self):
        try:
            # Clear the date entries and department selection
            self.fromEntry.set("")
            self.toEntry.set("")
            self.dep_var.set("All Departments")
            self.dep_combo.current(0)
            
            # Clear the table
            self.student_table.delete(*self.student_table.get_children())
            
            # Fetch all records again
            self.fetch_data()
            
            messagebox.showinfo("Success", "List has been reset successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error resetting list: {str(es)}", parent=self.root)






        


if __name__ == "__main__":
    root = ctk.CTk()
    obj = Attendance(root)
    root.mainloop()