# Interview Management System (IMS)

A comprehensive Django REST Framework-based application for managing the end-to-end interview process for organizations.

## 🚀 Features

- **User Management**
  - Role-based access (Admin, Interviewer, Candidate)
  - JWT Authentication
  - User profile management

- **Job Management**
  - Create and manage job listings
  - Filter and search jobs
  - Track application status

- **Interview Process**
  - Structured multi-round interview process
  - Interview scheduling
  - Feedback collection

- **Notifications**
  - Email notifications for interviews
  - Interview reminders via Celery tasks

- **Security**
  - Role-based throttling
  - Permission-based access control
  - Token-based authentication

## 🛠️ Technologies

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (SimpleJWT)
- **Task Queue**: Celery with Redis
- **Scheduled Tasks**: Celery Beat
- **Cross-Origin Support**: CORS headers


## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Interview_Management_System.git
   cd Interview_Management_System
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with the following variables:
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Redis server**
   ```bash
   redis-server
   ```

8. **Start the Celery worker**
   ```bash
   celery -A ims worker --loglevel=info
   ```

9. **Start the Celery beat scheduler**
    ```bash
    celery -A ims beat --loglevel=info
    ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `POST /api/auth/register/` - Register a new user
- `GET /api/auth/users/` - List all users (Admin only)
- `GET /api/auth/users/me/` - Get current user profile
- `PUT /api/auth/users/me/` - Update current user profile
- `GET /api/auth/users/{id}/` - Get user details (Admin only)
- `PUT/PATCH /api/auth/users/{id}/` - Update user (Admin only)
- `DELETE /api/auth/users/{id}/` - Delete user (Admin only)

### Jobs
- `GET/POST /api/jobs/` - List/create jobs
- `GET/PUT/DELETE /api/jobs/{id}/` - Retrieve/update/delete job
- `GET /api/jobs/open/` - List open jobs
- `GET /api/jobs/application-counts/` - List jobs with application counts (Admin only)

### Applications
- `GET/POST /api/applications/` - List/create applications
- `GET/PUT/DELETE /api/applications/{id}/` - Retrieve/update/delete application
- `GET /api/applications/me/` - View candidate's own applications
- `GET /api/jobs/{id}/applications/` - List applications for a job

### Interview Process
- `GET/POST /api/interview-rounds/` - List/create interview rounds
- `GET/POST /api/applications/{id}/rounds/` - List/create rounds for an application
- `GET/PUT/DELETE /api/application-rounds/{id}/` - Retrieve/update/delete application round
- `POST /api/application-rounds/{id}/feedback/` - Create feedback for a round
- `GET /api/feedback/me/` - View candidate's feedback
- `GET /api/interviews/upcoming/` - View upcoming interviews
- `GET /api/interviews/me/` - View interviewer's interviews

## 🔒 Rate Limiting

The system implements role-based throttling:
- Admins: 500 requests per minute
- Interviewers: 200 requests per minute
- Candidates: 100 requests per minute
- Unauthenticated users: 30 requests per minute

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
