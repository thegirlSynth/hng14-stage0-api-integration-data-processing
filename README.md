# Gender Classifier API

A simple FastAPI service that predicts gender from a name using the Genderize API.  
It processes the API response and returns a cleaned, structured result.

---

## Features

- Accepts a name via query parameter
- Calls the Genderize API
- Processes and reformats the response
- Adds confidence calculation
- Returns structured JSON output
- Handles basic error cases

---

## Endpoint

### GET `/api/classify`

### Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | The name to classify |

---

## Example Request

```http
GET /api/classify?name=john
```

**Response:**
```
{
    "status": "success",
    "data": {
        "name": "john",
        "gender": "male",
        "probability": 1.0,
        "sample_size": 2692560,
        "is_confident": true,
        "processed_at": "2026-04-12T12:53:56Z"
    }
}
