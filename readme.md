# IP Location Service

A simple Flask microservice that retrieves IP geolocation information. Non-intrusive, containerized, and production-ready.

## Code Logic

The application follows a simple request-response flow:

1. **User Request** → Sends GET request to `/get-location`
2. **Get Public IP** → Fetches the user's public IP address from Ipify API
3. **Get Location Data** → Queries IP location data from ip-api.com
4. **Return Response** → Returns geolocation details in JSON format

### Key Files

- **`main.py`** - Flask application with 2 endpoints:
  - `GET /health` - Lightweight health check (no API calls)
  - `GET /get-location` - Returns IP geolocation data

- **`utils/ip_services.py`** - Core logic:
  - `get_public_ip()` - Fetches user's public IP
  - `get_location_data(ip)` - Fetches geolocation for given IP

- **`config.py`** - Configuration via environment variables

## Application Flow

```
┌─────────────────────────────────────────────────────────┐
│                   HTTP Request                          │
│              GET /get-location                          │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Flask App           │
                │  main.py             │
                └──────────┬───────────┘
                           │
                           ▼
         ┌─────────────────────────────────┐
         │  get_public_ip()                │
         │  (IPLocationservice)            │
         │                                 │
         │  Calls Ipify API:               │
         │  ipify.org?format=json          │
         └───────────────┬─────────────────┘
                         │
                         ▼ (IP: 37.114.255.180)
         ┌─────────────────────────────────┐
         │  get_location_data(ip)          │
         │  (IPLocationservice)            │
         │                                 │
         │  Calls ip-api.com:              │
         │  ip-api.com/json/{ip}           │
         └───────────────┬─────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────┐
         │  Parse & Return JSON Response   │
         │                                 │
         │  {                              │
         │    "status": "success",         │
         │    "country": "Iran",           │
         │    "city": "Tehran",            │
         │    "lat": 35.4846,              │
         │    "lon": 51.0829,              │
         │    ...                          │
         │  }                              │
         └──────────────┬────────────────┘
                        │
                        ▼
              ┌──────────────────────┐
              │   HTTP Response      │
              │   Status: 200        │
              └──────────────────────┘
```

## Quick Start

**Build & Run:**
```bash
docker compose up -d
```

**Test:**
```bash
# Health check
curl http://localhost:8001/health

# Get IP location
curl http://localhost:8001/get-location
```

## Configuration

Set environment variables to customize:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEBUG` | `False` | Flask debug mode |
| `PORT` | `8001` | Application port |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `IPIFY_URL` | `https://api.ipify.org?format=json` | Public IP API |
| `IP_API_URL` | `http://ip-api.com/json` | Location API |

## API Endpoints

### Health Check
```
GET /health

Response:
{"status": "ok"}
```

### Get Location
```
GET /get-location

Response (Success):
{
  "status": "success",
  "country": "Iran",
  "city": "Tehran",
  "countryCode": "IR",
  "lat": 35.4846,
  "lon": 51.0829,
  "isp": "ISP Name",
  "timezone": "Asia/Tehran"
}

Response (Error):
{
  "status": "fail",
  "data": "Error message"
}
```

All errors are logged for debugging.