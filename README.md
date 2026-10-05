# Online Examination System for Physically Challenged Students

An AI-enabled Online Examination System developed using **Python Flask** to help physically challenged, especially visually impaired, students appear for online examinations independently through voice assistance and accessibility features.

---

## Project Overview

This project provides an accessible online examination platform with secure login, voice-guided examination, live monitoring, and machine learning-based proctoring.

The system allows students to register, log in, attend exams, receive voice instructions, and view previous exam history.

---

## Features

- Student Registration
- Secure Login
- Student Dashboard
- Student Profile
- Accessibility Settings
- Voice Assistant
- Speech-to-Text Commands
- Text-to-Speech Question Reading
- Online Examination
- Automatic Timer
- Answer Lock Feature
- Exam History
- Result Generation
- Live Camera Monitoring
- Face Detection
- Multiple Face Detection
- No Face Detection
- Object Detection (Mobile Phone / Other Electronic Devices)
- ML-based Suspicious Activity Monitoring

---

## Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask

### Database

- MySQL

### Machine Learning

- OpenCV
- Haar Cascade Face Detection
- Object Detection

### Browser APIs

- Speech Recognition API
- Speech Synthesis API
- Web Camera API

---

## Project Structure

```
online_exam_physically_challenged_ml/

│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── ml/
│   ├── detect_face.py
│   └── object_detection.py
│
├── database.py
├── config.py
├── monitoring.py
├── app.py
└── README.md
```

---

## Modules

### Authentication

- Registration
- Login
- Logout

### Student Module

- Dashboard
- Profile
- Accessibility Settings

### Examination Module

- Instructions
- Online Exam
- Voice Commands
- Timer
- Answer Locking
- Result Generation

### Monitoring Module

- Live Camera Feed
- Face Detection
- Multiple Face Detection
- No Face Detection
- Object Detection
- Warning Generation

### History Module

- Previous Exam Results
- Scores
- Percentage

---

## Voice Commands

The system supports voice interaction for visually impaired students.

Available commands:

- Start Exam
- Option A
- Option B
- Option C
- Option D
- Lock Answer
- Next Question
- Previous Question
- Repeat Question
- Read Options
- Submit Exam
- Yes
- No
- Help

---

## Database Tables

- students
- questions
- history_result

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/online_exam_physically_challenged_ml.git
```

### Install Requirements

```bash
pip install flask
pip install mysql-connector-python
pip install opencv-python
pip install opencv-contrib-python
pip install numpy
```

### Configure Database

Create the MySQL database and import the required tables.

Update your database credentials in:

```
config.py
```

### Run Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- Face Recognition
- YOLO-based Object Detection
- Head Pose Estimation
- Eye Tracking
- Lip Movement Detection
- AI-based Cheating Detection
- Online Video Proctoring
- Admin Dashboard
- Email Notifications
- Performance Analytics

---

## License

This project is developed for academic and educational purposes.
