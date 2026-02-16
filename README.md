# SchemaX

SchemaX is a robust and modern authentication service built with **FastAPI**. It provides a secure foundation for user management, featuring JWT-based authentication, refresh token rotation, and secure password handling using industry standards.

## 🚀 Features

- **FastAPI Powered**: High performance, easy to learn, fast to code, ready for production.
- **Secure Authentication**: Implements OAuth2 password flow with Bearer tokens.
- **JWT Strategy**: Utilizes short-lived access tokens and long-lived refresh tokens for enhanced security.
- **Password Security**: Strong password hashing using `bcrypt` with salt generation.
- **Database ORM**: SQLAlchemy for robust database interactions.
- **Interactive Docs**: Automatic Swagger UI and ReDoc integration.

## 🛠️ Tech Stack & Libraries

This project relies on a modern Python stack:

- **FastAPI**: The core web framework.
- **SQLAlchemy**: SQL toolkit and Object Relational Mapper.
- **PyJWT**: For generating and verifying JSON Web Tokens.
- **Bcrypt**: For secure password hashing.
- **Pydantic**: For data validation and settings management.
- **Uvicorn**: A lightning-fast ASGI server.

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SchemaX
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   Ensure you have configured your environment variables (e.g., `SECRET_KEY`, `DATABASE_URL`) in a `.env` file or your system environment.

## 🏃‍♂️ Running the Project

You can start the server using the provided batch script or directly via Uvicorn.

**Using the batch script (Windows):**
```bash
start.bat
```

**Using Uvicorn directly:**
```bash
uvicorn main:app --reload
```

## 📚 API Documentation

Once the server is running, you can explore the API endpoints:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔐 Authentication Flow

The authentication system is designed with security in mind:

1. **Register**: Create a new account via `POST /auth/register`.
2. **Login**: Authenticate via `POST /auth/login` to receive an `access_token` and `refresh_token`.
3. **Access**: Use the `access_token` in the `Authorization: Bearer <token>` header for protected routes.
4. **Refresh**: When the access token expires, send the `refresh_token` to `POST /auth/refresh` to obtain a new pair.

---

*Generated for SchemaX*
