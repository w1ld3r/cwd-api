# Crypto Wallet Dashboard API (CWD-API)

The Crypto Wallet Dashboard API (CWD-API) is a backend solution designed to allow users to store and manage their cryptocurrency transactions securely. The backend serves as a data store for transactions and user information, while all data consolidation and enrichment are handled on the closed-source frontend dashboard available at [cwd.danjon.xyz](https://cwd.danjon.xyz).

## Features

The CWD-API backend facilitates the following features:

### Data Storage & Management
- Securely store and manage cryptocurrency transactions.
- Maintain user information with secure authentication mechanisms.

## Technology Stack

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** PostgreSQL, managed via [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication:** JSON Web Tokens (JWT) for secure user authentication.

### Deployment
- **Containerization:** Docker and Docker Compose.

## Getting Started

### Prerequisites

Ensure the following are installed on your system:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/cwd-api.git
    cd cwd-api
    ```

2. Build and start the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Access the API documentation:
    - Navigate to `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

### Environment Variables

Configure the `.env` file for the application. An example configuration:

```env
DATABASE_URL=postgresql://user:password@db:5432/cwd
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Usage

Once the backend is up and running, it serves as the foundation for the Crypto Wallet Dashboard.

### API Endpoints

The API includes endpoints for:
- **User Management**: Registration, login, and JWT-based authentication.
- **Transaction Management**: CRUD operations for cryptocurrency transactions.

Refer to the [API Documentation](https://cwd-api.danjon.xyz/docs) for detailed endpoint descriptions.

## Development

### Running Locally

For local development, you can start the application without Docker:

1. Set up a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

4. Access the API documentation:
    - Navigate to `http://127.0.0.1:8000/docs`.

### Database Migrations

Handle database schema changes using Alembic:

1. Generate a new migration:
    ```bash
    alembic revision --autogenerate -m "Your migration message"
    ```

2. Apply the migration:
    ```bash
    alembic upgrade head
    ```

## Testing

Run tests using `pytest`:

```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature description"
    ```
4. Push to your branch:
    ```bash
    git push origin feature-name
    ```
5. Submit a pull request.

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
