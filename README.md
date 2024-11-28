## **Flask Application with Docker: sequenciador_fixo**

This project demonstrates a distributed Flask application with a preconfigured `Dockerfile` and `requirements.txt` for easy setup and deployment. The project includes separate **frontend** and **backend** directories for a clean architecture.

---

### **Features**
- Modular architecture with distinct frontend and backend.
- Dockerized for seamless setup and deployment.
- Includes a `requirements.txt` to manage Python dependencies.

---

### **Requirements**
Before starting, ensure you have the following installed on your system:
- [Docker](https://www.docker.com/)
- [Python 3.11+](https://www.python.org/downloads/) (if running locally)

---

### **Getting Started**

#### 1. **Clone the Repository**
```bash
git clone https://github.com/gabriel-feltes/sequenciador_fixo.git
cd sequenciador_fixo
```

#### 2. **Run Locally Without Docker**
Install the dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Run the Flask application:
```bash
python server.py
```

The application will be accessible at `http://localhost:5000`.

---

### **Using Docker**

#### 1. **Build the Docker Image**
```bash
docker build -t flask-app .
```

#### 2. **Run the Docker Container**
```bash
docker run -d -p 5000:5000 flask-app
```

#### 3. **Access the Application**
Open your browser and navigate to:
```plaintext
http://localhost:5000
```

---

### **Project Structure**

```
.
├── backend/                 # Backend application code
│   ├── server.py            # Entry point of the Flask application; handles routes and API logic.
│   ├── system_state.db      # SQLite database (auto-created); stores system state, logs, and messages.
│   └── requirements.txt     # Python dependencies required for the backend to run.
│
├── frontend/                # Frontend application files
│   ├── templates/           # HTML templates rendered by Flask.
│   │   └── index.html       # Main frontend template for the application's user interface.
│   └── static/              # Static files like stylesheets and JavaScript.
│       ├── styles.css       # CSS for styling the application.
│       └── app.js           # JavaScript for frontend interactivity and API calls.
│
├── Dockerfile               # Docker configuration to containerize the application.
└── README.md                # Project documentation, including setup and usage instructions.
```

---

### **Dependencies**
The project uses the following Python libraries:
- Flask==3.1.0
- Werkzeug==3.1.3
- Jinja2==3.1.4
- itsdangerous==2.2.0
- click==8.1.7
- blinker==1.9.0
- colorama==0.4.6
- MarkupSafe==3.0.2

These are defined in the `backend/requirements.txt` file.

---

### **Customizing the Application**
You can customize the application by modifying the files in the `frontend/` or `backend/` directories. After making changes, rebuild the Docker image:
```bash
docker build -t flask-app .
```
