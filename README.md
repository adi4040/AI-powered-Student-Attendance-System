# AI-Based Attendance Monitoring System Using Face Recognition

An automated attendance system designed to replace traditional methods in educational institutions using deep learning and facial recognition technology.

---

## Abstract

> The traditional method of taking attendance in schools and colleges has become overwhelming. Artificial Intelligence offers a way to automate these traditional processes. This paper presents an automated attendance system based on deep learning that uses a Convolutional Neural Network (CNN) trained and tested dynamically on student samples. The system is a desktop application built with Python for both frontend and backend development. We present a gap analysis of existing work, detail our development methodology, and conclude with a discussion of the results.

---

## 1. Introduction

The AI-based Attendance Monitoring system aims to eliminate traditional, manual attendance methods. Conventional techniques like calling out names or passing around sheets are time-consuming and susceptible to proxy attendance and errors. As institutions grow, an efficient and automated system is necessary.

Face recognition, powered by AI and deep learning algorithms like Convolutional Neural Networks (CNN), provides a promising solution. Our system uses a pre-trained ResNet model to identify students, streamlining administrative tasks and allowing educators to focus more on teaching instead of paperwork.

---

## 2. Methodology

The system's development follows the **Waterfall Model** to ensure a structured process. The application architecture consists of four main layers: User Interface, Application, Processing, and Data Storage.

<img width="333" height="222" alt="image" src="https://github.com/user-attachments/assets/e1e5c992-e6f7-406d-b710-1c83c90cb00b" />

*Figure 1: The Waterfall Model used for development.*

### Architectural Layers

<img width="623" height="550" alt="image" src="https://github.com/user-attachments/assets/2001429d-c3dd-4707-a653-6facbb2adc9b" />

*Figure 2: The 4-Layer Architecture of the System.*

1.  **User Interface Layer**: This is the entry point for the admin (teacher), who can add student details and upload photo samples. The system captures 500 samples per student, converts them to grayscale, and stores them locally.

2.  **Application Layer**: This layer contains several key modules.
    * **Student Management**: Allows the user to access and manage student data.
    * **Training Module**: Encodes the stored image samples using a pre-trained ResNet model and a Haar Cascade classifier, generating 128-dimensional encodings stored in a `classifier.xml` file.
    * **Face Recognition**: Scans student faces in real-time using a HOG-based detector. It dynamically encodes faces and compares them with the stored encodings.
    * **Attendance Module**: Marks a student as present with an in-time upon successful recognition. A second scan marks the out-time.

---

## 3. Algorithm and Models

### Histogram of Oriented Gradients (HOG)

The HOG descriptor is created using OpenCV's `HOGDescriptor` class.
* **Working Principle**: The HOG algorithm converts an image to grayscale and then computes the gradient magnitude and direction. The image is divided into small cells, and a histogram of gradients is computed for each. These histograms are normalized across larger blocks to handle lighting variations and are finally combined into a single feature vector for classification.

<img width="153" height="311" alt="image" src="https://github.com/user-attachments/assets/f63a3167-9ff5-4185-86b3-0f406347d1fb" />

*Figure 4: The HOG algorithm workflow.*

### Convolutional Neural Network (CNN)

The system uses a standard CNN architecture for binary classification. It begins with a 32-filter, 3x3 convolutional layer with ReLU activation, followed by a MaxPooling2D layer to reduce complexity. This pattern is repeated for more detailed feature extraction. A Flatten layer converts the 2D feature maps into a 1D vector, which is then passed to a Dense layer with 100 neurons (ReLU) and a final Dense layer with a Sigmoid activation for classification. The model is trained using the Adam optimizer.

<img width="255" height="319" alt="image" src="https://github.com/user-attachments/assets/a11ec596-8b07-4b75-aecd-aab70aade31c" />

*Table 1: The CNN Architecture.*

---

## 4. Visual Results and Discussion

The application's user interface consists of four main modules: student management, train data, detect faces, and attendance report. In the student management section, users can add student details and their photo samples.

<img width="340" height="164" alt="image" src="https://github.com/user-attachments/assets/e8be3ec4-db35-4850-b3a0-007a9261ec3e" />

*The Student Management interface for adding details and photos.*

During the recognition phase, the system identifies the student and displays their details. Attendance is marked based on the recognized student ID.

### Performance Analysis

Performance testing was conducted to evaluate the efficiency of the face detectors and encoders used. The system uses two face detection methods: Haar Cascade and a HOG-based detector.

<img width="326" height="311" alt="image" src="https://github.com/user-attachments/assets/940f6e07-1bdc-4221-a702-c20e038e0664" />

*Figure 5: Performance analysis of face detection and encoding times.*

* **Haar Cascade (Training)**: This classifier had an average detection time of **0.1344s**. Although it was initially slower, it became faster in later phases, suggesting optimization.
* **HOG Detector (Recognition)**: This detector maintained a more consistent average detection time of **0.1470s**. Its consistency makes it well-suited for prediction, even though it's comparatively slower than Haar Cascade.
* **ResNet Encoding**: The average encoding time was **0.9767s**. The time fluctuated initially before stabilizing, which likely reflects the deep learning framework allocating resources before achieving an optimal rhythm.

The model demonstrates **60-70% accuracy** even with a pre-trained ResNet model because the data is generated, trained, and tested dynamically within the system.
