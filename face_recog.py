import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import face_recognition
import xml.etree.ElementTree as ET
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import wx
import time
import os

# Set the theme and color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition")

        self.constant = 0
        self.db_password = 'Iamadam4040'
        self.setup_ui()
            
    def setup_ui(self):
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
            text="Face Recognition",
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
        self.content_frame.grid_columnconfigure(0, weight=2)  # Recognition display
        self.content_frame.grid_columnconfigure(1, weight=1)  # Recognition button

        # Middle frame - Recognition Display
        self.middle_frame = ctk.CTkFrame(self.content_frame,
                                       fg_color="#2d2d2d",
                                       corner_radius=8,
                                       width=800,
                                       height=600)
        self.middle_frame.grid(row=0, column=0, pady=50, padx=20)
        self.middle_frame.grid_propagate(False)

        # Recognition display label
        self.recognition_label = ctk.CTkLabel(
            self.middle_frame,
            text="Recognition Display",
            font=("Helvetica", 24, "bold"),
            text_color="#00ff9f"
        )
        self.recognition_label.grid(row=0, column=0, pady=30)

        # Create a container frame for the recognition display
        self.display_container = ctk.CTkFrame(
            self.middle_frame,
            fg_color="transparent",
            width=700,
            height=400
        )
        self.display_container.grid(row=1, column=0, pady=20)
        self.display_container.grid_propagate(False)
        self.display_container.grid_columnconfigure(0, weight=1)
        self.display_container.grid_rowconfigure(0, weight=1)

        # Recognition display image label
        self.display_label = ctk.CTkLabel(
            self.display_container,
            text="",
            text_color="white"
        )
        self.display_label.grid(row=0, column=0, sticky="nsew")

        # Right frame - Recognition Button and Status
        self.right_frame = ctk.CTkFrame(self.content_frame,
                                      fg_color="#2d2d2d",
                                      corner_radius=8,
                                      width=400,
                                      height=600)
        self.right_frame.grid(row=0, column=1, pady=50, padx=20)
        self.right_frame.grid_propagate(False)

        # Recognition icon
        recognize_Icon = Image.open(r"image_assets/recog_icon.png")
        recognize_Icon = recognize_Icon.resize((200, 200), Image.LANCZOS)
        self.recog_photo = ImageTk.PhotoImage(recognize_Icon)

        # Recognition button
        self.recognize_button = ctk.CTkButton(
            self.right_frame,
            image=self.recog_photo,
            text="",
            command=self.face_recog,
            fg_color="transparent",
            hover_color="#1a1a1a",
            width=200,
            height=200
        )
        self.recognize_button.grid(row=0, column=0, pady=40)

        # Recognition label
        ctk.CTkLabel(
            self.right_frame,
            text="Click to Start Recognition",
            font=("Helvetica", 20, "bold"),
            text_color="#00ff9f"
        ).grid(row=1, column=0, pady=(0, 30))

        # Status label
        self.status_label = ctk.CTkLabel(
            self.right_frame,
            text="Ready to recognize",
            font=("Helvetica", 18),
            text_color="white"
        )
        self.status_label.grid(row=2, column=0, pady=20)

        # Add Mark Attendance button
        self.mark_attendance_btn = ctk.CTkButton(
            self.right_frame,
            text="Mark Attendance",
            command=self.confirm_attendance,
            font=("Helvetica", 16, "bold"),
            fg_color="#00ff9f",
            hover_color="#00cc7f",
            width=180,
            height=40,
            state="disabled"
        )
        self.mark_attendance_btn.grid(row=3, column=0, pady=20)



        # Add a label to show recognized student details
        self.recognized_details_label = ctk.CTkLabel(
            self.right_frame,
            text="",
            font=("Helvetica", 14),
            text_color="white",
            wraplength=350
        )
        self.recognized_details_label.grid(row=5, column=0, pady=10)

        # Store current recognized student details
        self.current_student = None

    # ********************Marking Attendance**************
    def mark_attendance_in(self,id,name):
        
       #getting data to be displayed
        now = datetime.now() #display date and time
        date = now.strftime("%d/%m/%Y") #date format
        time = now.strftime("%H:%M:%S") #time format 
        
        conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT `Status (In)` FROM attendancetb WHERE ID = %s", (id,))
        time_in = my_cursor.fetchone()
        
        
        my_cursor.execute("SELECT `Status (out)` FROM attendancetb WHERE ID = %s",(id,))
        time_out = my_cursor.fetchone()
        

        if not time_in or not time_in[0]:
            #Database Connectivity
            try:
                    
                    my_cursor.execute("update attendancetb set `Status (In)`=%s where ID=%s",(time,id))
                    my_cursor.execute("update attendancetb set Date = %s where ID = %s",(date,id))    
                    app = wx.App(False)
                    wx.MessageBox("Marked the attendance for {} (IN)!".format(name), "Info", wx.OK | wx.ICON_INFORMATION)
                    self.constant = 1

            except Exception as es:
                    messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)  

        elif not time_out or not time_out[0]:
            try:
                    
                    my_cursor.execute("update attendancetb set `Status (out)`=%s where ID=%s",(time,id))
                    app = wx.App(False)
                    wx.MessageBox("Marked the attendance for {} (OUT)!".format(name), "Info", wx.OK | wx.ICON_INFORMATION)
                    self.constant = 1
                    

            except Exception as es:
                    messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

        else :
            #  messagebox.showerror("Error","Can't change the out timing") 
            app = wx.App(False)
            wx.MessageBox("Can't mark OUT attendance for {} again!".format(name), "Info", wx.OK | wx.ICON_INFORMATION)
            self.constant = 1      

     

        conn.commit()
        conn.close()    
            
        

              
            

    #****************Face Recognition*********************

    def face_recog(self):
        # Load known faces encodings and ids from the XML file
        known_encodings, known_ids = self.load_known_faces()

        def recognize(img):
            try:
                if img is None:
                    print("Error: No frame captured")
                    return
                    
                # Start timing for overall system response
                start_time = time.time()
                
                # Face detection using Haar Cascade
                haar_start = time.time()
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                haar_faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                haar_time = (time.time() - haar_start) * 1000  # Convert to milliseconds
                
                # Face detection using HOG
                hog_start = time.time()
                face_locations = face_recognition.face_locations(img)
                hog_time = (time.time() - hog_start) * 1000  # Convert to milliseconds
                
                # Face encoding
                encoding_start = time.time()
                face_encodings = face_recognition.face_encodings(img, face_locations)
                encoding_time = (time.time() - encoding_start) * 1000  # Convert to milliseconds
                
                # Calculate overall system response time
                system_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Save metrics
                self.save_metrics(haar_time, hog_time, encoding_time, system_time)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Calculate face distances instead of just comparing
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                    best_match_index = face_distances.argmin()
                    min_distance = face_distances[best_match_index]
                    
                    # Convert distance to confidence percentage (lower distance = higher confidence)
                    confidence = (1 - min_distance) * 100
                    
                    # Format confidence to 2 decimal places
                    confidence_text = f"{confidence:.2f}%"
                    
                    id = ""
                    name = ""
                    roll = ""
                    dep = ""
                    
                    # Use a threshold for matching (0.4 is the default in face_recognition)
                    if min_distance < 0.4:
                        student_id = known_ids[best_match_index]

                        # Fetch student details using the student ID which is matched
                        details = self.fetch_student_details(student_id)

                        if details:
                            name, roll, dep, id = details
                            
                            # Store current student details
                            self.current_student = (id, name)
                            
                            # Update UI with student details
                            details_text = f"Recognized Student:\nID: {id}\nName: {name}\nRoll: {roll}\nDepartment: {dep}\nConfidence: {confidence_text}"
                            self.recognized_details_label.configure(text=details_text)
                            self.mark_attendance_btn.configure(state="normal")
                        
                        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
                        cv2.putText(img, id, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, name, (left, top - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, roll, (left, top - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, dep, (left, top - 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        
                        # Display confidence below the face
                        cv2.putText(img, f"Confidence: {confidence_text}", (left, bottom + 25), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    else:
                        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown Face", (left, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        # Display confidence for unknown face
                        cv2.putText(img, f"Confidence: {confidence_text}", (left, bottom + 25), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        
                        # Reset UI for unknown face
                        self.mark_attendance_btn.configure(state="disabled")
                        self.recognized_details_label.configure(text="")
                        self.current_student = None

                # Convert OpenCV image to PIL Image for display
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_pil.thumbnail((500, 400), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage instead of PhotoImage
                img_tk = ctk.CTkImage(
                    light_image=img_pil,
                    dark_image=img_pil,
                    size=(500, 400)
                )
                self.display_label.configure(image=img_tk)
                self.display_label.image = img_tk  # Keep a reference
                self.root.update()

            except Exception as e:
                print(f"Error during face recognition: {e}")
                messagebox.showerror("Error", f"Error during face recognition: {e}")

        # Set up video capture with retry logic
        max_retries = 3
        retry_count = 0
        video_cap = None
        
        while retry_count < max_retries:
            try:
                video_cap = cv2.VideoCapture(0)
                if not video_cap.isOpened():
                    raise Exception("Failed to open video capture device")
                    
                # Test if we can read a frame
                ret, test_frame = video_cap.read()
                if not ret or test_frame is None:
                    raise Exception("Failed to read frame from video capture device")
                    
                break  
                
            except Exception as e:
                retry_count += 1
                if video_cap is not None:
                    video_cap.release()
                if retry_count == max_retries:
                    messagebox.showerror("Error", f"Failed to initialize camera after {max_retries} attempts: {str(e)}")
                    return
                print(f"Retrying video capture (attempt {retry_count}/{max_retries})")
                time.sleep(1)  

        self.status_label.configure(text="Recognition in progress...")

        while True:
            ret, img = video_cap.read()
            if not ret or img is None:
                print("Error: Failed to capture frame")
                continue
                
            recognize(img)

            if self.constant == 1:
                self.constant = 0
                break

            if cv2.waitKey(1) == 13:
                break

        # Release video capture and close OpenCV windows
        if video_cap is not None:
            video_cap.release()
        cv2.destroyAllWindows()
        self.status_label.configure(text="Ready to recognize")

    def load_known_faces(self, xml_file="classifier.xml"):
        try:
            # Parse XML file for known faces encodings and ids
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Store known faces encodings and ids in class variables
            self.known_encodings = []
            self.known_ids = []

            for encoding_elem in root.find("encodings"):
                encoding_str = encoding_elem.text
                encoding = [float(value) for value in encoding_str.split(",")]
                self.known_encodings.append(encoding)

            for id_elem in root.find("ids"):
                face_id = id_elem.text
                self.known_ids.append(face_id)

            return self.known_encodings, self.known_ids

        except Exception as e:
            print(f"Error loading known faces from {xml_file}: {e}")
            messagebox.showerror("Error", f"Error loading known faces from {xml_file}: {e}")
            return [], []

    def fetch_student_details(self, student_id):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password=self.db_password, database="face_recognizer")
            my_cursor = conn.cursor()

            my_cursor.execute("SELECT Student_id FROM student WHERE Student_id=" + str(student_id))
            id = my_cursor.fetchone()
            id = "+".join(id) if id else "Unknown"

            my_cursor.execute("SELECT Name FROM student WHERE Student_id=" + str(student_id))
            name = my_cursor.fetchone()
            name = "+".join(name) if name else "Unknown"

            my_cursor.execute("SELECT Roll FROM student WHERE Student_id=" + str(student_id))
            roll = my_cursor.fetchone()
            roll = "+".join(roll) if roll else "Unknown"

            my_cursor.execute("SELECT Dep FROM student WHERE Student_id=" + str(student_id))
            dep = my_cursor.fetchone()
            dep = "+".join(dep) if dep else "Unknown"

            conn.close()

            return name, roll, dep, id

        except Exception as e:
            print(f"Error fetching student details: {e}")
            messagebox.showerror("Error", f"Error fetching student details: {e}")
            return None

    def confirm_attendance(self):
        if self.current_student:
            id, name = self.current_student
            self.mark_attendance_in(id, name)
            # Reset UI after marking attendance
            self.mark_attendance_btn.configure(state="disabled")
            self.recognized_details_label.configure(text="")
            self.current_student = None

 
    def save_metrics(self, haar_time, hog_time, encoding_time, system_time):
        try:
            # Load existing metrics
            if os.path.exists('performance_metrics.xml'):
                tree = ET.parse('performance_metrics.xml')
                root = tree.getroot()
            else:
                root = ET.Element("metrics")
                tree = ET.ElementTree(root)

            # Update detection time data
            detection_elem = root.find('detection_time')
            if detection_elem is None:
                detection_elem = ET.SubElement(root, "detection_time")
                ET.SubElement(detection_elem, "haar").text = str(haar_time)
                ET.SubElement(detection_elem, "hog").text = str(hog_time)
            else:
                haar_elem = detection_elem.find('haar')
                hog_elem = detection_elem.find('hog')
                if haar_elem is None:
                    ET.SubElement(detection_elem, "haar").text = str(haar_time)
                else:
                    haar_elem.text = f"{haar_elem.text},{haar_time}"
                if hog_elem is None:
                    ET.SubElement(detection_elem, "hog").text = str(hog_time)
                else:
                    hog_elem.text = f"{hog_elem.text},{hog_time}"

            # Update encoding time data
            encoding_elem = root.find('encoding_time')
            if encoding_elem is None:
                encoding_elem = ET.SubElement(root, "encoding_time")
                encoding_elem.text = str(encoding_time)
            else:
                encoding_elem.text = f"{encoding_elem.text},{encoding_time}"

            # Update system response time data
            response_elem = root.find('system_response')
            if response_elem is None:
                response_elem = ET.SubElement(root, "system_response")
                response_elem.text = str(system_time)
            else:
                response_elem.text = f"{response_elem.text},{system_time}"

            # Save updated metrics
            tree.write('performance_metrics.xml')

        except Exception as e:
            print(f"Error saving metrics: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    obj = FaceRecognition(root)
    root.mainloop()
