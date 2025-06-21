# 🏥 E-Hospitality – Django-Based Hospital Management System

**E-Hospitality** is a full-stack web-based hospital management system built with Django. It allows patients and doctors to securely manage appointments, prescriptions, medical data, and billing in a streamlined and intuitive platform.

---

## 🚀 Features

### 👨‍⚕️ Doctor Module
- Doctor registration & login
- View only your appointments
- View patients linked through appointments
- Add prescriptions & diagnosis
- Custom doctor admin panel

### 🧑‍💼 Patient Module
- Patient registration & login
- Book appointments dynamically with available doctors
- View prescriptions & medical history
- Manage payments and view billing
- Custom patient admin panel

### 🛠 Admin Capabilities
- Separate admin dashboards for doctors and patients
- Add/edit/delete doctor/patient records
- Full control over appointments and data

### 💳 Payments (Stripe Integration)
- Secure payment gateway using Stripe
- Billing section to manage invoices and payment status

---

## 🧱 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Payment Gateway:** Stripe
- **Environment Management:** `.env` with `python-decouple`

---

## 🔐 Security

- All secret keys and API tokens are stored in a `.env` file and excluded from the repo.
- Doctors can only access data of patients who booked an appointment with them.
- Session-based login authentication for both doctors and patients.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Ihlasnj007/Ehospitality.git
cd Ehospitality
