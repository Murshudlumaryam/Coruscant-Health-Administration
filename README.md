# Welcome to Coruscant Health Administration
***

## Task
This project focuses on rebuilding the Coruscant Health Administration Medical Management System using Python and Django technologies.
The objective is to develop a robust, secure, and scalable platform that connects multiple healthcare stakeholders — including patients, doctors, administrators, departments, and emergency services.
A key challenge of this project is implementing a role-based system that ensures secure access, supports real-time data exchange, and provides safe handling of sensitive medical information.

## Description
The Coruscant Health Administration system is a comprehensive full-stack application designed to simulate a modern healthcare environment.

It supports multiple user roles, each with specific responsibilities:

## Patient
Registers in the system after administrator approval
Uploads health-related data from wearable devices
Accesses personal medical history and records
Reviews prescriptions and recommendations from doctors

## Doctor
Registers with administrator authorization
Accesses and analyzes patient health information
Tracks patient progress and condition
Creates prescriptions and medical reports
Requests medical services from departments

## Department
Receives and processes service requests from doctors
Performs required medical procedures
Uploads diagnostic results and reports to the system

## Administrator
Approves and manages patient and doctor accounts
Maintains and updates the system database
Oversees overall system operations
Emergency Services
Handles urgent patient registrations
Provides quick access to the system during emergencies
## Features
Multi-role authentication system (Patient, Doctor, Admin, Emergency)
Continuous tracking of patient health data
Interaction system between doctors and patients
Generation and management of medical reports
Medical service request and execution system
Secure file upload with encryption
Responsive and user-friendly interface

## Security
All sensitive files are encrypted before being stored
Secret keys are managed using environment variables
Role-based access control ensures data protection
Secure authentication mechanisms are implemented

## Installation
### 1. Clone repository
git clone https: https://github.com/xatirealiyeva/cha_project
cd cha-project

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate      

1. Clone the repository
git clone https://github.com/xatirealiyeva/cha_project
cd cha-project
2. Set up a virtual environment
python -m venv venv

Activate the environment:
On macOS/Linux:
source venv/bin/activate
On Windows:
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
python manage.py migrate

### 5. Start server
python manage.py runserver

## Usage
Open the application in your browser:

http://127.0.0.1:8000/

Workflow:
1. Admin registers doctors and patients  
2. Patient uploads health data  
3. Doctor reviews patient data  
4. Doctor writes reports and prescriptions  
5. Department processes medical orders  
6. Patient receives feedback  

---

## Deployment
The project is deployed on a cloud platform.

URL is stored in:
my_coruscant_health_administration_url.txt

---

## Testing
Run tests using:
python manage.py test

```
./my_project argument1 argument2
```

### The Core Team
murshudl_m
liyeva_x

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>
