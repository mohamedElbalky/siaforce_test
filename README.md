# Django & React Credential Management Dashboard

This project is a web application that combines a Django backend with a React frontend to manage and display stored credentials. The application allows users to log in, view, filter, and search through credentials stored in a NoSQL database.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [Backend](#backend)
  - [Frontend](#frontend)

## Features

- User authentication (login/logout)
- Display stored credentials in a user-friendly dashboard
- Filter and search functionality for quick access to credentials

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: React, Redux Toolkit, Reeact router dom
- **Database**: MongoDB
- **Others**: Docker (if applicable), Axios (for API requests)

## Installation

### Backend Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

4. Apply migrations and run the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the required npm packages:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm run dev
   ```

## Usage

### Backend

- The Django server will run at `http://localhost:8000/`.
- API endpoints will be available for the frontend to interact with.

### Frontend

- The React application will run at `http://localhost:5173/`.
- Access the dashboard to manage and view credentials.


