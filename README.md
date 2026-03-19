#  SpeedRide Car Rental System (FastAPI Project)

This is a complete backend project built using **FastAPI** as part of my internship training.  
The project simulates a real-world **Car Rental Service** with booking workflows, CRUD operations, and advanced APIs.

---

## 📌 Project Features

### 🔹 Core Features
- REST APIs using FastAPI
- Pydantic validation
- CRUD operations (Create, Read, Update, Delete)
- Car rental booking system
- Return workflow (multi-step process)

### 🔹 Advanced Features
- 🔍 Search functionality
- 🔄 Sorting (price, brand, type)
- 📄 Pagination
- 🧠 Combined browsing API (filter + sort + paginate)

---

## 🧠 Concepts Covered

- GET APIs
- POST APIs with validation
- Helper functions
- CRUD operations
- Multi-step workflow (Rental → Return)
- Search, Sorting, Pagination

---

## 🗂️ Project Structure
fastapi-car-rental/                                                                           
│                                                                                                         
├── main.py                                                                                                    
├── requirements.txt                                                                                           
├── README.md                                                                                               
└── screenshots/                                                                                              

---

## ⚙️ Installation & Run

### 1️⃣ Install dependencies
pip install -r requirements.txt                                         


### 2️⃣ Run server
uvicorn main:app --reload            


### 3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs           


---

## 📊 API Endpoints

### 🚗 Cars APIs
- GET /cars
- GET /cars/{car_id}
- GET /cars/summary
- GET /cars/filter
- GET /cars/search
- GET /cars/sort
- GET /cars/page
- GET /cars/browse
- GET /cars/unavailable
- POST /cars
- PUT /cars/{car_id}
- DELETE /cars/{car_id}

### 📦 Rentals APIs
- GET /rentals
- GET /rentals/{rental_id}
- GET /rentals/active
- GET /rentals/by-car/{car_id}
- GET /rentals/search
- GET /rentals/sort
- GET /rentals/page
- POST /rentals
- POST /return/{rental_id}

---

## 📸 Screenshots

All API outputs are tested in Swagger UI and stored in the `screenshots/` folder.

---

## 🎯 Project Objective

To build a real-world backend system using FastAPI demonstrating:
- API design
- Backend logic
- Data handling
- Workflow implementation

---

## 🙌 Acknowledgment

Grateful for the learning opportunity at **Innomatics Research Labs**.

---

## 🔗 Author

- Name: Gandesri Abhilash                                                     
- Project: FastAPI Application                                             
- Internship: GenAI Internship                                                    
- Guidance under @Innomatics Research Lab                                   
