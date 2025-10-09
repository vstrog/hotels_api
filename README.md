# 🏨 Hotels Management API

REST API application for managing hotels, built with FastAPI.

## 📋 Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Test Files](#test-files)
- [API Documentation](#api-documentation)

## ✨ Features

- ✅ Create, Read, Update, and Delete hotels (CRUD)
- ✅ Paginated hotel list
- ✅ Data validation
- ✅ Automatic documentation generation (Swagger/ReDoc)
- ✅ Rating system (1-5 stars)

## 🛠 Technologies

- **Python 3.8+**
- **FastAPI** - modern web framework
- **Uvicorn** - ASGI server
- **Pydantic** - data validation

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hotels-api.git
cd hotels-api
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Start the server

```bash
python main.py
```

Or run directly with uvicorn:

```bash
uvicorn main:app --host localhost --port 8090 --reload
```

The application will be available at: **http://localhost:8090**

## 📡 API Endpoints

### Hotel Controller

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/example/v1/hotels` | Get a list of all hotels (with pagination) |
| `POST` | `/example/v1/hotels` | Create a new hotel |
| `GET` | `/example/v1/hotels/{id}` | Get a hotel by ID |
| `PUT` | `/example/v1/hotels/{id}` | Update hotel data |
| `DELETE` | `/example/v1/hotels/{id}` | Delete a hotel |

### Pagination Parameters

- `page` - page number (default: 0)
- `size` - number of items per page (default: 100)
- `sort` - sorting (optional)

## 💡 Usage Examples

### Create a Hotel

```bash
curl -X POST "http://localhost:8090/example/v1/hotels" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Mod Hasharon",
    "description": "Automation Hotel",
    "name": "Nir Great hotel",
    "rating": 1
  }'
```

**Response:**
```json
{
  "id": 1,
  "city": "Mod Hasharon",
  "description": "Automation Hotel",
  "name": "Nir Great hotel",
  "rating": 1
}
```

### Get All Hotels

```bash
curl -X GET "http://localhost:8090/example/v1/hotels"
```

**Response:**
```json
{
  "content": [],
  "last": true,
  "totalElements": 0,
  "totalPages": 0,
  "size": 100,
  "number": 0,
  "sort": null,
  "numberOfElements": 0,
  "first": true
}
```

### Get Hotel by ID

```bash
curl -X GET "http://localhost:8090/example/v1/hotels/1"
```

### Update a Hotel

```bash
curl -X PUT "http://localhost:8090/example/v1/hotels/1" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "description": "Updated description"
  }'
```

### Delete a Hotel

```bash
curl -X DELETE "http://localhost:8090/example/v1/hotels/1"
```

## 📊 Test Files

The repository includes test files with ratings:

### `rating.json`
```json
[
  {"rating": 1},
  {"rating": 2},
  {"rating": 3}
]
```

### `rating.csv`
```csv
rating
1
2
3
```

These files can be used to import test data.

## 📚 API Documentation

After starting the application, interactive documentation is available:

- **Swagger UI**: http://localhost:8090/docs
- **ReDoc**: http://localhost:8090/redoc
- **OpenAPI JSON**: http://localhost:8090/openapi.json

### Swagger UI

Swagger provides an interactive interface for testing all endpoints:

1. Open http://localhost:8090/docs
2. Select the desired endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## 🧪 Testing with Postman

1. Import the collection using URL: `http://localhost:8090/openapi.json`
2. Create a new environment with variable `baseUrl = http://localhost:8090`
3. Use the ready-made requests from the collection

## 📝 Data Model

### Hotel

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `id` | integer | Unique identifier | No (auto) |
| `city` | string | Hotel location city | Yes |
| `description` | string | Hotel description | Yes |
| `name` | string | Hotel name | Yes |
| `rating` | integer | Rating (1-5 stars) | Yes |

## 🔧 Configuration

By default, the application runs on:
- **Host**: localhost
- **Port**: 8090

To change settings, edit the last line in `main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## ⚠️ Important Notes

- Current implementation uses **in-memory storage** (data is not persisted after restart)
- For production use, it's recommended to connect a database (PostgreSQL, MongoDB, etc.)
- Don't forget to add authentication and authorization for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Your Name - [@vstrog](https://github.com/vstrog)

## 🙏 Acknowledgments

- FastAPI documentation
- Python community
