# Secure User Management & Authentication API

A modern, production-ready User Management Web API built with **FastAPI**, **SQLAlchemy ORM**, and **Pydantic v2**. This microservice focuses heavily on backend application security, cryptographic password hashing, and strict input validation.

## 🚀 Key Features

- **Advanced Password Strength Validation:** Integrates the **zxcvbn** algorithm (Dropbox's realistic password strength estimator) inside a Pydantic `@field_validator` to reject weak passwords with dynamic, actionable user feedback.
- **Cryptographic Password Hashing:** Implements secure, one-way password hashing via **Bcrypt** (`passlib`), ensuring passwords are never stored in plaintext within the database.
- **Robust Schema Validation:** Utilizes **Pydantic v2** with dedicated data transfer schemas (`CreateUser`, `UserResponse`, `UserLogIn`, `UserUpdate`, `ChangePassword`) and semantic validation using `EmailStr`.
- **Dynamic Object Mutation:** Features efficient, dynamic attribute updates via Python's `setattr` mapping inside update routes, adhering to clean code standards for scalable partial updates.
- **Transactional Consistency:** Leverages SQLAlchemy session management isolated per HTTP request using the native FastAPI Dependency Injection pattern (`Depends(get_db)`) enclosed in a safe `try/finally` lifecycle.

---

## 🛠️ System Architecture

The project maintains a strict Separation of Concerns (SoC) layout:
- **`main.py` (API Layer):** Exposes RESTful endpoints, handles HTTP routing, and raises clean web exceptions natively via `HTTPException`.
- **`models.py` (Validation & Registry Layer):** Houses database entity models mapping to a PostgreSQL/SQLite system and handles real-time data serialization schemas.
- **`security.py` (Cryptographic Layer):** Abstracts the logic for password encryption and secure verification.
- **`db.py` (Infrastructure Layer):** Controls backend database engine lifecycles and transactional rollbacks.

### Tech Stack
* **Framework:** FastAPI
* **Validation:** Pydantic v2 & zxcvbn
* **ORM:** SQLAlchemy
* **Database Engine:** SQLite / PostgreSQL Ready

*  Go to **`http://localhost:5000`** to access the interactive **Swagger UI** to test registrations, logins, and the password strength validator.
