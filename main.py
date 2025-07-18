import customtkinter as ctk
from PIL import Image, ImageTk
from student import Student
from train import Train
from face_recog import FaceRecognition
from attendance import Attendance

# Set the theme and color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Facial_recognition:
    def __init__(self, root, login_window_destroy_callback=None):
        self.root = root
        self.login_window_destroy_callback = login_window_destroy_callback
        self.root.geometry("1530x790+0+0")
        self.root.title("Student Attendance System")

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
            text="AI-based Student Attendance System",
            font=("Helvetica", 35, "bold"),
            text_color="#00ff9f"
        )
        title_label.grid(row=0, column=0, pady=(20, 40))
        
        # Create container frame for buttons with padding
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=(100, 40), pady=40)
        
        # Configure button frame grid
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        # Create a frame to hold all buttons in a 2x2 grid
        self.buttons_container = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        self.buttons_container.grid(row=0, column=0, sticky="nsew", padx=(50, 0))
        self.buttons_container.grid_columnconfigure((0,1), weight=1)
        self.buttons_container.grid_rowconfigure((0,1), weight=1)
        
        # Student Button (top left)
        self.create_button(
            self.buttons_container,
            "Student Details",
            "image_assets/students.gif",
            self.student_details,
            0, 0
        )
        
        # Training Button (top right)
        self.create_button(
            self.buttons_container,
            "Train Data",
            "image_assets/ai.gif",
            self.train_data,
            0, 1
        )
        
        # Detect Button (bottom left)
        self.create_button(
            self.buttons_container,
            "Detect Faces",
            "image_assets/face-scanner.gif",
            self.face_recog,
            1, 0
        )
        
        # Attendance Button (bottom right)
        self.create_button(
            self.buttons_container,
            "Attendance",
            "image_assets/attendance.gif",
            self.attendance_stud,
            1, 1
        )

    def create_button(self, parent, text, image_path, command, row, column):
        # Create container for button and image
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")
        
        # Load and resize image
        img = Image.open(image_path)
        img = img.resize((215, 195), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        # Create image label
        img_label = ctk.CTkLabel(
            container,
            image=photo,
            text=""
        )
        img_label.image = photo
        img_label.pack(pady=(0, 10))
        
        # Create button with hover effect
        btn = ctk.CTkButton(
            container,
            text=text,
            command=command,
            font=("Helvetica", 15, "bold"),
            fg_color="#1a1a1a",
            hover_color="#2d2d2d",
            text_color="#00ff9f",
            height=40,
            width=220,
            corner_radius=10
        )
        btn.pack()
        
        # Bind hover events
        btn.bind("<Enter>", lambda e: btn.configure(fg_color="#2d2d2d"))
        btn.bind("<Leave>", lambda e: btn.configure(fg_color="#1a1a1a"))

    def student_details(self, event=None):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.transient(self.root)  # Make window transient
        self.new_window.grab_set()  # Make window modal
        self.app = Student(self.new_window)

    def train_data(self, event=None):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.transient(self.root)  # Make window transient
        self.new_window.grab_set()  # Make window modal
        self.app = Train(self.new_window)  

    def face_recog(self, event=None):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.transient(self.root)  # Make window transient
        self.new_window.grab_set()  # Make window modal
        self.app = FaceRecognition(self.new_window)

    def attendance_stud(self, event=None):
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.transient(self.root)  # Make window transient
        self.new_window.grab_set()  # Make window modal
        self.app = Attendance(self.new_window)  

if __name__ == "__main__":
    root = ctk.CTk()
    obj = Facial_recognition(root)
    root.mainloop()