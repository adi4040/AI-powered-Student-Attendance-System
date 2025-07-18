import customtkinter as ctk
from PIL import Image, ImageTk
import face_recognition
import os
import numpy as np
import xml.etree.ElementTree as ET
from tkinter import messagebox

# Set the theme and color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Train Data")

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
            text="Train Dataset",
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
        self.content_frame.grid_propagate(False)  # Prevent size changes
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Create main canvas with fixed size
        self.main_canvas = ctk.CTkCanvas(
            self.content_frame,
            bg="#1a1a1a",
            highlightthickness=0,
            width=1350,
            height=550
        )
        self.main_canvas.grid(row=0, column=0, sticky="nsew")

        # Add main scrollbar
        self.main_scrollbar = ctk.CTkScrollbar(
            self.content_frame,
            orientation="vertical",
            command=self.main_canvas.yview
        )
        self.main_scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure main canvas
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # Create scrollable frame with explicit size
        self.scrollable_frame = ctk.CTkFrame(self.main_canvas, 
                                           fg_color="transparent",
                                           width=1350,
                                           height=800)
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure grid for horizontal layout
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=2)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        # Left frame - Training Button
        self.left_frame = ctk.CTkFrame(self.scrollable_frame,
                                     fg_color="#2d2d2d",
                                     corner_radius=8,
                                     width=300,
                                     height=600)
        self.left_frame.grid(row=0, column=0, pady=50, padx=20)
        self.left_frame.grid_propagate(False)

        # Processing icon with verified size
        processing_Icon = Image.open(r"image_assets/face-recognition.png")
        processing_Icon = processing_Icon.resize((200, 200), Image.LANCZOS)
        self.photoImg = ImageTk.PhotoImage(processing_Icon)

        # Process button with verified size
        self.process_button = ctk.CTkButton(
            self.left_frame,
            image=self.photoImg,
            text="",
            command=self.train_classifier,
            fg_color="transparent",
            hover_color="#1a1a1a",
            width=200,
            height=200
        )
        self.process_button.grid(row=0, column=0, pady=40)

        # Training label
        ctk.CTkLabel(
            self.left_frame,
            text="Click to Train Dataset",
            font=("Helvetica", 20, "bold"),
            text_color="#00ff9f"
        ).grid(row=1, column=0, pady=(0, 30))

        # Middle frame - Preview
        self.preview_frame = ctk.CTkFrame(self.scrollable_frame,
                                        fg_color="#2d2d2d",
                                        corner_radius=8,
                                        width=600,
                                        height=600)
        self.preview_frame.grid(row=0, column=1, pady=50, padx=20)
        self.preview_frame.grid_propagate(False)
        
        # Configure grid for preview frame
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(1, weight=1)

        # Preview label
        ctk.CTkLabel(
            self.preview_frame,
            text="Training Preview",
            font=("Helvetica", 24, "bold"),
            text_color="#00ff9f"
        ).grid(row=0, column=0, pady=30)

        # Create a container frame for the preview image
        self.preview_container = ctk.CTkFrame(
            self.preview_frame,
            fg_color="transparent",
            width=500,
            height=400
        )
        self.preview_container.grid(row=1, column=0, pady=20)
        self.preview_container.grid_propagate(False)
        self.preview_container.grid_columnconfigure(0, weight=1)
        self.preview_container.grid_rowconfigure(0, weight=1)

        # Preview image label
        self.preview_label = ctk.CTkLabel(
            self.preview_container,
            text="",
            text_color="white"
        )
        self.preview_label.grid(row=0, column=0, sticky="nsew")

        # Right frame - Status and Progress
        self.right_frame = ctk.CTkFrame(self.scrollable_frame,
                                      fg_color="#2d2d2d",
                                      corner_radius=8,
                                      width=300,
                                      height=600)
        self.right_frame.grid(row=0, column=2, pady=50, padx=20)
        self.right_frame.grid_propagate(False)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.right_frame,
            text="Ready to train",
            font=("Helvetica", 18),
            text_color="white"
        )
        self.status_label.grid(row=0, column=0, pady=(20, 10))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.right_frame,
            width=250,
            height=20,
            corner_radius=10,
            progress_color="#00ff9f",
            fg_color="#1a1a1a"
        )
        self.progress_bar.grid(row=1, column=0, pady=10)
        self.progress_bar.set(0)  # Initialize to 0

        # Configure scroll regions
        self.scrollable_frame.bind("<Configure>", lambda e: self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        ))

    def train_classifier(self):
        try:
            data_dir = "Data"
            if not os.path.exists(data_dir):
                messagebox.showerror("Error", "Data directory not found!", parent=self.root)
                return

            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
            if not path:
                messagebox.showerror("Error", "No images found in Data directory!", parent=self.root)
                return

            known_encodings = []
            known_ids = []

            # Load existing data
            existing_encodings, existing_ids = self.load_existing_data()

            self.status_label.configure(text="Training in progress...")
            self.progress_bar.set(0)  # Reset progress bar
            self.root.update()

            total_images = len(path)
            processed_images = 0

            for image_path in path:
                try:
                    face_id = os.path.split(image_path)[1].split('.')[1]
                    if face_id in existing_ids:
                        continue

                    processed_images += 1
                    progress = processed_images / total_images
                    self.progress_bar.set(progress)
                    self.status_label.configure(text=f"Processing image {processed_images}/{total_images}")
                    self.root.update()

                    image = face_recognition.load_image_file(image_path)
                    face_encoding = face_recognition.face_encodings(image)

                    if face_encoding:
                        known_encodings.append(face_encoding[0])
                        known_ids.append(face_id)

                        # Display preview
                        img = Image.open(image_path)
                        img.thumbnail((900, 700), Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        self.preview_label.configure(image=img_tk)
                        self.preview_label.image = img_tk
                        self.root.update()
                    else:
                        # Silently skip images with no face detected
                        continue

                except Exception as e:
                    # Silently skip errors without showing messagebox
                    continue

            if known_encodings:
                self.save_new_data(known_encodings, known_ids)
                self.status_label.configure(text="Training completed successfully!")
                self.progress_bar.set(1)
                messagebox.showinfo("Success", f"Trained {len(known_encodings)} new images!", parent=self.root)
            else:
                self.status_label.configure(text="No new faces to train")
                self.progress_bar.set(0)
                messagebox.showinfo("Info", "No new faces found for training", parent=self.root)

        except Exception as e:
            self.status_label.configure(text="Training failed")
            self.progress_bar.set(0)
            messagebox.showerror("Error", f"Training failed: {str(e)}", parent=self.root)

    def load_existing_data(self):
        try:
            tree = ET.parse("classifier.xml")
            root = tree.getroot()
            return (
                [np.array(enc.text.split(","), dtype=np.float64) for enc in root.find("encodings")],
                [id_elem.text for id_elem in root.find("ids")]
            )
        except FileNotFoundError:
            return [], []

    def save_new_data(self, new_encodings, new_ids):
        try:
            tree = ET.parse("classifier.xml")
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("root")

        encodings = root.find("encodings") or ET.SubElement(root, "encodings")
        ids = root.find("ids") or ET.SubElement(root, "ids")

        for enc in new_encodings:
            ET.SubElement(encodings, "encoding").text = ",".join(map(str, enc.tolist()))
        
        for fid in new_ids:
            ET.SubElement(ids, "id").text = str(fid)

        ET.ElementTree(root).write("classifier.xml")
        
if __name__ == "__main__":
    root = ctk.CTk()
    obj = Train(root)
    root.mainloop()