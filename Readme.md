🌾 Fasal Sathi

Smart Farm AI is a Django-based web application designed to assist farmers with crop recommendation, plant disease detection, and farm management insights using intelligent rule-based logic.
The system is lightweight, reliable, and deployable without heavy machine learning dependencies.

🚀 Project Overview

The goal of Smart Farm AI is to provide data-driven agricultural support through a user-friendly web interface.
Instead of relying on heavy ML models or paid APIs, the system uses rule-based expert logic, making it efficient, explainable, and stable for real-world usage.

✨ Key Features

User Authentication (Login / Registration)

Crop Recommendation System

Rule-Based Plant Disease Detection

Dashboard for Farmers

Secure Form Handling

Scalable Django Architecture

Deployment Ready (Local & Cloud)

🛠️ Tech Stack

Backend: Python, Django

Frontend: HTML, CSS, JavaScript

Database: SQLite (default)

Logic Engine: Rule-Based Expert System

Deployment: Render / Localhost

⚙️ Setup Instructions (Local)
1️⃣ Clone the Repository
git clone https://github.com/your-username/smart-farm-ai.git
cd smart-farm-ai

2️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Database Migrations
python manage.py migrate

5️⃣ Start Development Server
python manage.py runserver


Access the app at:

http://127.0.0.1:8000/


🧠 Disease Detection Logic

The disease detection module uses a rule-based expert system that evaluates visible symptoms such as:

Leaf color changes

Spots or fungal growth

Wilting patterns

This approach ensures:

High reliability

Zero dependency conflicts

Easy explanation during presentations and viva

🔐 Security Practices

Environment variables used for sensitive data

CSRF protection enabled

Django authentication system implemented

📊 Why Rule-Based Instead of ML?

No dependency on large datasets

Faster execution

Explainable predictions

Easy deployment

Suitable for low-resource environments

🌍 Deployment

The application is compatible with:

Localhost

Render Cloud Platform

Static and dynamic configurations are handled via Django settings.

📌 Future Enhancements

Crop-wise fertilizer recommendation

Weather-based advisory

Mobile-responsive UI

Admin analytics dashboard

👨‍💻 Team & Acknowledgements

Developed as part of an academic project to demonstrate practical applications of AI concepts in agriculture using scalable web technologies.

📄 License

This project is for educational purposes.
