# 🧠 Creator Pulse – An AI-Powered Newsletter System (LLM Assignment)

Creator Pulse is an **AI-driven newsletter automation platform** built using **Django REST Framework**.  
It curates personalized content, generates styled newsletters, and automates email scheduling — empowering creators to manage topics, styles, and templates with precision.

> 🧩 Built as part of the **100x GenAI Cohort – LLM Engineering Module**

---

## 📌 Features

### 👤 **User Features**
- Personalized **Dashboard** showing credits, topics, newsletters, and reading streaks  
- **Topic Management** – select or deselect topics for curated content  
- **Source Filtering** – filter sources by name, URL, or source type  
- **Style Sample Upload** – influence newsletter tone using custom writing samples  
- **Newsletter Generator** – preview, send, and schedule newsletters (with 10-min cooldown)  
- **Template & Draft Management** – save newsletters, compare versions with inline diff  
- **Newsletter History** – view all sent or attempted newsletters with timestamps  

### 🧑‍💼 **Superadmin Features**
- **Dashboard Analytics** – total users, active sources, sent newsletters  
- **Quick Actions** – manage users and sources  
- **System Overview** – active sources, last sent newsletter, system health  
- **User & Source Management** – activate/deactivate users and add new sources  

---

## ⚙️ Tech Stack

| Tool / Library | Description |
|----------------|-------------|
| **Django 5.2.1** | Web framework |
| **Django REST Framework** | API development |
| **APScheduler** | Background scheduling and cron jobs |
| **Simple JWT** | JSON Web Token Authentication |
| **Resend API** | Transactional email delivery |
| **psycopg2-binary** | PostgreSQL adapter |
| **drf-yasg** | Swagger/OpenAPI schema generation |
| **python-dotenv** | Environment variable management |

> 🖥️ **Frontend Repository:** [Creator Pulse Frontend (React)](https://github.com/TechMaverickHub/100x-LLM-Assignment-CreatorPulse-frontend)

---

## 🚀 Getting Started

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/TechMaverickHub/100x-LLM-Assignment-CreatorPulse.git
cd 100x-LLM-Assignment-CreatorPulse
```

---

### 🐍 2. Create a Virtual Environment

```bash
# Linux/macOS
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
```

---

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=
DATABASE_PORT=
DEBUG=TRUE

GROQ_API_KEY=
RESEND_API_KEY=
```

---

## 🗃️ Database Setup

### 🔧 Make Migrations

```bash
python manage.py makemigrations user
python manage.py makemigrations mail
python manage.py makemigrations newsletter
python manage.py makemigrations role
python manage.py makemigrations sample
python manage.py makemigrations source
python manage.py makemigrations topic
```

### ⚙️ Apply Migrations

```bash
python manage.py migrate
```

### 📥 Load Initial Data

```bash
python manage.py loaddata app/role/fixtures/roles.json
python manage.py loaddata app/source/fixtures/source_types.json
python manage.py loaddata app/topic/fixtures/topic.json
```

---

## 🧪 Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the API at:  
👉 `http://localhost:8000/`

---

## 📚 API Documentation

Interactive Swagger docs available at:  
`http://localhost:8000/swagger/`

---

## 🧠 Assignment Context

This project was developed as part of the **100x GenAI Cohort – LLM Engineering Module**.  
The objective was to integrate **AI-driven personalization**, **task scheduling**, and **content automation** into a production-grade web system using Django and REST APIs.

---

## 🚧 Future Enhancements

- 🤖 Integrate AI summarization and tone adjustment for newsletters  
- 📈 Add advanced analytics dashboards for open/click rates  
- 💬 Enable real-time notifications and activity tracking  
- 🧩 Introduce more user roles (Editor, Subscriber, etc.)  
- 🎨 Support brand customization and newsletter themes  

---

## 🧾 License

This project is part of an educational module and is not licensed for commercial use.  
For learning purposes only under the **100x GenAI Cohort**.
