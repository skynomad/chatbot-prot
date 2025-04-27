# FastAPI Math Server

This project is a simple FastAPI application that provides a RESTful API for basic mathematical operations: addition, subtraction, multiplication, and division.

## Project Structure

```
fastapi-math-server
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── routers
│   │   └── operations.py      # API endpoints for mathematical operations
│   └── models
│       └── __init__.py        # Placeholder for data models or schemas
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Requirements

To run this project, you need to have Python installed. The required packages are listed in `requirements.txt`. You can install them using:

```
pip install -r requirements.txt
```

## Running the Application

To start the FastAPI server, navigate to the `app` directory and run the following command:

```
uvicorn main:app --reload
```

This will start the server in development mode, and you can access the API at `http://127.0.0.1:8000`.

## API Endpoints

The following endpoints are available:

- **Addition**: `POST /add`
- **Subtraction**: `POST /subtract`
- **Multiplication**: `POST /multiply`
- **Division**: `POST /divide`

Each endpoint expects a JSON body with two numbers and returns the result of the operation.

## License

This project is licensed under the MIT License.