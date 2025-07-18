import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import re
from tkinter import messagebox, ttk, END

# Set the theme and color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student Details")

        self.db_password = 'Iamadam4040'

        #********************Text Variables*************************
        self.var_dep = ctk.StringVar()
        self.var_course = ctk.StringVar()
        self.var_year = ctk.StringVar()
        self.var_std_id = ctk.StringVar()
        self.var_std_name = ctk.StringVar()
        self.var_div = ctk.StringVar()
        self.var_roll = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_phone = ctk.StringVar()
        self.searchCombo = ctk.StringVar()
        self.searchEntry = ctk.StringVar()
        self.var_radio1 = ctk.StringVar()

        # Configure grid for root window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame with padding
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        
        # Configure main frame grid
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title with increased padding
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Student Management",
            font=("Helvetica", 35, "bold"),
            text_color="#00ff9f"
        )
        title_label.grid(row=0, column=0, pady=(0, 40))

        # Create container frame for left and right sections with padding
        self.container_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.container_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        self.container_frame.grid_columnconfigure(0, weight=5)  # Left frame gets more weight
        self.container_frame.grid_columnconfigure(1, weight=1)  # Right frame gets less weight

        # Left Frame with increased width
        self.left_frame = self.create_left_frame()
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(30, 10))  # Increased left padding

        # Right Frame with adjusted padding
        self.right_frame = self.create_right_frame()
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 40))  # Increased right padding

        # Fetch initial data
        self.fetch_data()

    def create_left_frame(self):
        frame = ctk.CTkFrame(self.container_frame, fg_color="#1a1a1a", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        
        # Current Course Information with increased padding
        course_frame = ctk.CTkFrame(frame, fg_color="#2d2d2d", corner_radius=8)
        course_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)  # Increased horizontal padding
        
        # Configure grid weights for course_frame
        for i in range(4):
            course_frame.grid_columnconfigure(i, weight=1, uniform='cols')

        ctk.CTkLabel(
            course_frame,
            text="Current Course Details",
            font=("Helvetica", 16, "bold"),
            text_color="#00ff9f"
        ).grid(row=0, column=0, columnspan=4, pady=10)

        # Department with adjusted spacing
        ctk.CTkLabel(
            course_frame,
            text="Department",
            font=("Helvetica", 12),
            text_color="white"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        dep_combo = ctk.CTkComboBox(
            course_frame,
            values=["Select Department", "IoT", "Computer", "IT", "Civil", "Mechanical", "AIDS", "ENTC", "AIML", "SE"],
            variable=self.var_dep,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            button_color="#000000",
            button_hover_color="#1a1a1a",
            width=180
        )
        dep_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Course with adjusted spacing
        ctk.CTkLabel(
            course_frame,
            text="Course",
            font=("Helvetica", 12),
            text_color="white"
        ).grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        course_combo = ctk.CTkComboBox(
            course_frame,
            values=["Select Course", "1st Year", "2nd Year", "3rd Year", "4th Year"],
            variable=self.var_course,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            button_color="#000000",
            button_hover_color="#1a1a1a",
            width=180
        )
        course_combo.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        # Year with adjusted spacing
        ctk.CTkLabel(
            course_frame,
            text="Year",
            font=("Helvetica", 12),
            text_color="white"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        year_combo = ctk.CTkComboBox(
            course_frame,
            values=["Select Year", "2022-23", "2023-24", "2024-25", "2025-26"],
            variable=self.var_year,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            button_color="#000000",
            button_hover_color="#1a1a1a",
            width=180
        )
        year_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Class Student Information with adjusted padding
        student_frame = ctk.CTkFrame(frame, fg_color="#2d2d2d", corner_radius=8)
        student_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=15)
        
        # Configure grid weights for student_frame
        for i in range(4):
            student_frame.grid_columnconfigure(i, weight=1, uniform='cols')

        ctk.CTkLabel(
            student_frame,
            text="Class Student Information",
            font=("Helvetica", 16, "bold"),
            text_color="#00ff9f"
        ).grid(row=0, column=0, columnspan=4, pady=10)

        # Student ID
        ctk.CTkLabel(
            student_frame,
            text="Student ID:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        ctk.CTkEntry(
            student_frame,
            textvariable=self.var_std_id,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f",
            width=180
        ).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Student Name
        ctk.CTkLabel(
            student_frame,
            text="Student Name:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        ctk.CTkEntry(
            student_frame,
            textvariable=self.var_std_name,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f",
            width=180
        ).grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        # Class Division
        ctk.CTkLabel(
            student_frame,
            text="Class Division:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        div_combo = ctk.CTkComboBox(
            student_frame,
            values=["Select Division", "1", "2", "3"],
            variable=self.var_div,
            font=("Helvetica", 10),
            fg_color="#1a1a1a",
            button_color="#000000",
            button_hover_color="#1a1a1a",
            width=180
        )
        div_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Roll Number
        ctk.CTkLabel(
            student_frame,
            text="Roll Number:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=2, column=2, padx=10, pady=5, sticky="nsew")

        ctk.CTkEntry(
            student_frame,
            textvariable=self.var_roll,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f",
            width=180
        ).grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        # Email
        ctk.CTkLabel(
            student_frame,
            text="Email:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        ctk.CTkEntry(
            student_frame,
            textvariable=self.var_email,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f",
            width=180
        ).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Phone Number
        ctk.CTkLabel(
            student_frame,
            text="Phone Number:",
            font=("Helvetica", 10),
            text_color="white",
            width=120
        ).grid(row=3, column=2, padx=10, pady=5, sticky="nsew")

        ctk.CTkEntry(
            student_frame,
            textvariable=self.var_phone,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f",
            width=180
        ).grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Radio Buttons
        radio_frame = ctk.CTkFrame(student_frame, fg_color="transparent")
        radio_frame.grid(row=4, column=0, columnspan=4, pady=10)

        ctk.CTkRadioButton(
            radio_frame,
            text="Take Photo Sample",
            variable=self.var_radio1,
            value="Yes",
            font=("Helvetica", 12),
            fg_color="#00ff9f",
            hover_color="#00cc7f"
        ).pack(side="left", padx=10)

        ctk.CTkRadioButton(
            radio_frame,
            text="Don't Take Photo Sample",
            variable=self.var_radio1,
            value="No",
            font=("Helvetica", 12),
            fg_color="#00ff9f",
            hover_color="#00cc7f"
        ).pack(side="left", padx=10)

        # Buttons Frame
        btn_frame = ctk.CTkFrame(student_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=4, pady=20)

        # Configure grid columns to distribute buttons evenly
        for col in range(4):
            btn_frame.grid_columnconfigure(col, weight=1)



        # Create buttons with consistent style
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "fg_color": "#1a1a1a",
            "hover_color": "#2d2d2d",
            "text_color": "#00ff9f",
            "corner_radius": 10,
            "width": 120,
            "height": 35
        }

        ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self.add_data,
            **button_style
        ).grid(row=0, column=0, padx=5, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Update",
            command=self.update_data,
            **button_style
        ).grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            **button_style
        ).grid(row=0, column=2, padx=5, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            **button_style
        ).grid(row=0, column=3, padx=5, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Take Photo Sample",
            command=self.generate_dataset,
            **button_style
        ).grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        return frame

    def create_right_frame(self):
        frame = ctk.CTkFrame(self.container_frame, fg_color="#1a1a1a", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        
        # Search Frame with adjusted padding
        search_frame = ctk.CTkFrame(frame, fg_color="#2d2d2d", corner_radius=8)
        search_frame.grid(row=0, column=0, sticky="nsew", padx=(30, 20), pady=20)  # Adjusted horizontal padding
        
        ctk.CTkLabel(
            search_frame,
            text="Search System",
            font=("Helvetica", 16, "bold"),
            text_color="#00ff9f"
        ).grid(row=0, column=0, columnspan=5, pady=15)

        ctk.CTkLabel(
            search_frame,
            text="Search by:",
            font=("Helvetica", 12),
            text_color="white"
        ).grid(row=1, column=0, padx=15, pady=8)

        search_combo = ctk.CTkComboBox(
            search_frame,
            values=["Select", "Roll", "Name"],
            variable=self.searchCombo,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            button_color="#000000",
            button_hover_color="#1a1a1a"
        )
        search_combo.grid(row=1, column=1, padx=15, pady=8)

        ctk.CTkEntry(
            search_frame,
            textvariable=self.searchEntry,
            font=("Helvetica", 12),
            fg_color="#1a1a1a",
            border_color="#00ff9f"
        ).grid(row=1, column=2, padx=15, pady=8)

        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "fg_color": "#1a1a1a",
            "hover_color": "#2d2d2d",
            "text_color": "#00ff9f",
            "corner_radius": 10,
            "width": 120,
            "height": 35
        }

        ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_system,
            **button_style
        ).grid(row=1, column=3, padx=15)

        ctk.CTkButton(
            search_frame,
            text="Search All",
            command=self.fetch_data,
            **button_style
        ).grid(row=1, column=4, padx=15)

        # Table Frame with increased padding
        table_frame = ctk.CTkFrame(frame, fg_color="#000000", corner_radius=8)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

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

        # Create Treeview widget
        self.student_table = ttk.Treeview(
            table_frame,
            columns=("Dep", "Course", "Year", "Id", "Name", "Div", "RollNo", "Email", "PhoneNo"),
            show="headings",
            style="Treeview"
        )

        # Configure scrollbars with dark theme
        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.student_table.xview,
            style="Horizontal.TScrollbar"
        )
        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview,
            style="Vertical.TScrollbar"
        )

        # Grid layout
        self.student_table.grid(row=0, column=0, sticky="nsew")
        scroll_x.grid(row=1, column=0, sticky="ew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        # Configure headings with white text
        headings = {
            "Dep": ("Department", 120),
            "Course": ("Course", 100),
            "Year": ("Year", 100),
            "Id": ("ID", 80),
            "Name": ("Name", 150),
            "Div": ("Division", 100),
            "RollNo": ("Roll No", 100),
            "Email": ("Email", 200),
            "PhoneNo": ("Phone No", 120)
        }

        for col, (heading, width) in headings.items():
            self.student_table.heading(col, text=heading, anchor="w")
            self.student_table.column(col, width=width, minwidth=width, anchor="w")

        # Configure tag for selected rows
        self.student_table.tag_configure('selected', background='#2d2d2d')  # Dark gray for selection

        # Bind click event
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        return frame
    #*********************Functions for adding data to database****************************
    
    def add_data(self):
        if not self.validating_fields():
            return

        if self.var_dep.get()=="Select Department" or self.var_std_id.get()=="" or self.var_std_name.get()=="":
            messagebox.showerror("Error","Fill all the fields!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
                my_cursor = conn.cursor()
                
                # Check if student ID already exists
                my_cursor.execute("SELECT * FROM student WHERE Student_id=%s", (self.var_std_id.get(),))
                existing = my_cursor.fetchone()
                
                if existing:
                    messagebox.showerror("Error", "Student ID already exists", parent=self.root)
                    return

                # Insert into student table
                student_query = """
                    INSERT INTO student (Dep, Course, Year, Student_id, Name, Division, Roll, Email, Phone, PhotoSample)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                student_data = (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_radio1.get()
                )
                my_cursor.execute(student_query, student_data)

                # Insert into attendancetb table
                attendance_query = """
                    INSERT INTO attendancetb (ID, Name, `Roll No`, Dep)
                    VALUES (%s, %s, %s, %s)
                """
                attendance_data = (
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_roll.get(),
                    self.var_dep.get()
                )
                my_cursor.execute(attendance_query, attendance_data)

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student details have been added successfully",parent=self.root)
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error",f"Database error: {err}",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    #**************************Fetching data******************************
    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password=self.db_password,  # Using password variable
            database="face_recognizer"
        )
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student ORDER BY CAST(Student_id AS UNSIGNED)")
        data = my_cursor.fetchall()

        if len(data)!=0:  #if some data is fetched 
            self.student_table.delete(*self.student_table.get_children()) #delete the already displayed data 
            for i in data: #insert new data 
                self.student_table.insert("",END,values=i)
                conn.commit() #so that data gets added
        conn.close()


    # get cursor function (so that when user clicks on any entry in table, its details will be filled in the fields and user will be able to update it!)
    def get_cursor(self,event=""):
        
        #focus the cursor on student table:
        cursor_focus = self.student_table.focus() 
        
        #get content of the item on which cursor is focussed:
        content = self.student_table.item(cursor_focus) 
        data = content["values"]

        #set the data from student_table into respective fields:
        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_std_id.set(data[3]),
        self.var_std_name.set(data[4]),
        self.var_div.set(data[5]),
        self.var_roll.set(data[6]),
        self.var_email.set(data[7]),
        self.var_phone.set(data[8]),
        self.var_radio1.set(data[9]),

    
    #**************Update Function*******************
    def update_data(self):

        if not self.validating_fields():
            return

        if self.var_dep.get() == "Select Department" or self.var_std_id.get() == "" or self.var_std_name.get() == "":
            messagebox.showerror("Error", "Fill all the fields!", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update", "Are you sure?", parent=self.root)
                if Update:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password=self.db_password,
                        database="face_recognizer"
                    )
                    my_cursor = conn.cursor()

                    # Update the student table
                    my_cursor.execute("""
                        UPDATE student 
                        SET Dep=%s, Course=%s, Year=%s, Student_id=%s, Name=%s, Division=%s, Roll=%s, Email=%s, Phone=%s, PhotoSample=%s 
                        WHERE Student_id=%s
                    """, (
                                                                                            self.var_dep.get(),
                                                                                            self.var_course.get(),
                                                                                            self.var_year.get(),                                                                                            
                                                                                            self.var_std_id.get(),                                                                                            
                                                                                            self.var_std_name.get(),
                                                                                            self.var_div.get(),
                                                                                            self.var_roll.get(),
                                                                                            self.var_email.get(),
                                                                                            self.var_phone.get(),
                                                                                            self.var_radio1.get(),
                                                                                            self.var_std_id.get()    
                    ))

                    # Update the attendancetb table
                    my_cursor.execute("""
                        UPDATE attendancetb 
                        SET Name=%s, `Roll No`=%s, Dep=%s 
                        WHERE ID=%s
                    """, (
                        self.var_std_name.get(),
                        self.var_roll.get(),
                        self.var_dep.get(),
                        self.var_std_id.get()
                    ))

                    conn.commit()
                    self.fetch_data()
                    conn.close() 
                    messagebox.showinfo("Success", "Details Updated", parent=self.root)
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)


    #***********Delete Function**************************
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete Data", "Are you Sure?", parent=self.root)
                if delete:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password=self.db_password,
                        database="face_recognizer"
                    )
                    my_cursor = conn.cursor() 

                    # Delete from student table
                    sql = "DELETE FROM student WHERE Student_id=%s"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)

                    # Delete from attendancetb table
                    sql_attendance = "DELETE FROM attendancetb WHERE ID=%s"
                    my_cursor.execute(sql_attendance, val)
                    
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Delete", "Deleted Successfully", parent=self.root)
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)
 

    #*************Reset Data Fields***********************
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_radio1.set("")


    #************Generate data set and take photo samples********************
    
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_id.get() == "" or self.var_std_name.get() == "":
            messagebox.showerror("Error", "Fill all the fields!", parent=self.root)
        else:
            try:
                # Get the selected student ID from the table
                selected_id = self.var_std_id.get()

                #**************Load Predefined data on face frontals from opencv***************
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray,1.3,5)

                    for(x,y,w,h) in faces:
                        face_cropped = img[y:y+h,x:x+w]
                        return face_cropped

                cap = cv2.VideoCapture(0)
                img_id = 0

                while True:
                    ret, my_frame=cap.read()
                    cropped_face = face_cropped(my_frame)
                    if cropped_face is not None:
                        img_id += 1
                        face = cv2.resize(cropped_face,(450,450))
                        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        # Use the selected student ID for the file name
                        file_name_path = f"Data/user.{selected_id}.{img_id}.jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(my_frame,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",my_frame)

                        if cv2.waitKey(1) == 13 or int(img_id)==500:
                            break
                    # Display the resulting frame (without cropping)
                    cv2.imshow('frame', my_frame)
                    # Break the loop if 'q' key is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating dataset completed !!")
                    
            except Exception as es:
                messagebox.showerror("Error",f"Unsuccessful attempt due to: {str(es)}",parent=self.root) 

    def search_system(self):
        conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
        my_cursor = conn.cursor()

        comboSelection = self.searchCombo.get()  # Get the selected search criteria from the combobox
        entry = self.searchEntry.get()

        try:
            if comboSelection == "Roll":
                my_cursor.execute("Select * from student where Roll = %s", (entry,))
                data = my_cursor.fetchall()

                if len(data) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("", END, values=i)
                        conn.commit()

            elif comboSelection == "Name":
                my_cursor.execute("Select * from student where Name = %s", (entry,))
                data = my_cursor.fetchall()

                if len(data) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("", END, values=i)
                        conn.commit()
                        print('hey')
            else:
                messagebox.showerror("Error", "No Selection", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Unsuccessful attempt due to: {str(es)}", parent=self.root)

        conn.close()


    def validating_fields(self):
        # Validating Student ID
        student_id = self.var_std_id.get()
        if not student_id.isdigit():
            messagebox.showerror("Error", "ID should only contain numbers", parent=self.root)
            return False
            
        # Validating email address
        email = self.var_email.get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address", parent=self.root)
            return False

        # Validating phone number
        phone_number = self.var_phone.get()
        pattern = r"^\+?[0-9]{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,10}$"
        if not re.match(pattern, phone_number) or len(phone_number) != 10:
            messagebox.showerror("Error", "Invalid phone number", parent=self.root)
            return False

        # Validating name
        name = self.var_std_name.get()
        if not name:
            messagebox.showerror("Error", "Name not entered", parent=self.root)
            return False

        if not re.match(r"^[A-Za-z\-\'\s]+$", name):
            messagebox.showerror("Error", "Invalid name", parent=self.root)
            return False

        return True





if __name__ == "__main__":
    root = ctk.CTk()
    obj = Student(root)
    root.mainloop()
