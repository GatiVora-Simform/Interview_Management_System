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

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/auth/token/` | POST | Obtain JWT token | Anyone |
| `/api/auth/token/refresh/` | POST | Refresh JWT token | Authenticated user |


### User Management

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/users/` | GET | List all users | Admin |
| `/api/users/create` | POST | Register user | Anyone |
| `/api/users/<id>/` | GET, PUT, DELETE | View, update or delete user | Admin |
| `/api/users/me/` | GET, PUT | View or update current user profile | Authenticated user |


### Jobs

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/jobs/` | GET, POST | List all jobs, Create new job | Admin  |
| `/api/jobs/<id>/` | GET, PUT, DELETE | Retrieve, update or delete job | Admin |
| `/api/jobs/open/` | GET | List all open jobs | Authenticated users |
| `/api/jobs/<id>/applications/` | GET | List applications for a job | Admin |
| `/api/jobs/application-counts/` | GET | Get jobs with application counts | Admin |

### Applications

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/applications/` | GET, POST | List all applications, Create application | Admin (GET), Candidate (POST) |
| `/api/applications/<id>/` | GET, PUT, DELETE | Retrieve, update or delete application | Admin |
| `/api/applications/<id>/select/` | PUT | Select a candidate for a job | Admin |
| `/api/applications/me/` | GET | List current user's applications | Candidate |

### Interview Rounds

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/interview-rounds/` | GET, POST | List/create interview round types | Admin |
| `/api/applications/<id>/rounds/` | GET, POST | List/create rounds for an application | Admin  |
| `/api/application-rounds/<id>/` | GET, PUT, DELETE | Manage a specific application round | Admin |

### Feedback

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/application-rounds/<id>/feedback/` | POST | Create feedback for an interview round | Interviewer |
| `/api/feedback/me/` | GET | Get feedback for the logged-in candidate | Candidate |

### Interviews

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/interviews/upcoming/` | GET | List upcoming interviews | Admin, Interviewer |
| `/api/interviews/me/` | GET | List interviews for the logged-in interviewer | Interviewer |


## 🔒 Rate Limiting

The system implements role-based throttling:
- Admins: 100 requests per minute
- Interviewers: 50 requests per minute
- Candidates: 10 requests per minute
- Unauthenticated users: 10 requests per minute

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
