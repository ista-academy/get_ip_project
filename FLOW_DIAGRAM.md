# Application Flow Diagram

## Sequence Diagram: Request to Response

```mermaid
sequenceDiagram
    participant User as User/Client
    participant Flask as Flask App
    participant Ipify as Ipify API
    participant IpApi as IP-API.com
    
    User->>Flask: GET /get-location
    
    Flask->>Ipify: GET https://api.ipify.org?format=json
    activate Ipify
    Ipify-->>Flask: {ip: "37.114.255.180"}
    deactivate Ipify
    
    Flask->>IpApi: GET http://ip-api.com/json/37.114.255.180
    activate IpApi
    IpApi-->>Flask: {status: "success", country: "Iran", ...}
    deactivate IpApi
    
    Flask-->>User: HTTP 200 + JSON Response
```

## Component Diagram: Architecture

```mermaid
graph TB
    subgraph Client["Client Layer"]
        A["HTTP Client"]
    end
    
    subgraph Flask["Flask Application"]
        B["main.py<br/>Routes"]
        C["get_location()<br/>get_public_ip()"]
    end
    
    subgraph Services["Service Layer"]
        D["IPLocationservice<br/>ip_services.py"]
        E["get_public_ip()<br/>get_location_data()"]
    end
    
    subgraph Config["Configuration"]
        F["config.py<br/>Environment Variables"]
    end
    
    subgraph APIs["External APIs"]
        G["Ipify API<br/>Public IP"]
        H["IP-API.com<br/>Geolocation"]
    end
    
    A -->|Request| B
    B -->|Uses| D
    D -->|Calls| E
    E -->|Gets Config| F
    E -->|HTTP Requests| G
    E -->|HTTP Requests| H
    B -->|Returns| A
```

## State Diagram: Request States

```mermaid
stateDiagram-v2
    [*] --> RequestReceived: GET /get-location
    
    RequestReceived --> FetchingIP: Start Process
    
    FetchingIP --> IPSuccess: IP Retrieved
    FetchingIP --> IPError: Network Error
    
    IPSuccess --> FetchingLocation: Get Location
    
    FetchingLocation --> LocationSuccess: Data Retrieved
    FetchingLocation --> LocationError: Network Error
    
    LocationSuccess --> Success: Return 200
    
    IPError --> Error: Return 500
    LocationError --> Error: Return 500
    
    Success --> [*]
    Error --> [*]
```

## Data Flow: Request to Response

```mermaid
flowchart LR
    A["Client Request<br/>GET /get-location"] -->|HTTP| B["Flask Route<br/>@app.route"]
    
    B -->|Call| C["get_public_ip()"]
    
    C -->|Request| D["Ipify API"]
    D -->|Response| E["Extract IP<br/>37.114.255.180"]
    
    E -->|Pass IP| F["get_location_data(ip)"]
    
    F -->|Request| G["IP-API.com"]
    G -->|Response| H["Parse Geolocation<br/>JSON"]
    
    H -->|Return| I["jsonify()"]
    
    I -->|HTTP 200| J["Client Response<br/>Geolocation Data"]
    
    style A fill:#e1f5ff
    style J fill:#c8e6c9
    style D fill:#fff9c4
    style G fill:#fff9c4
```

## Class Diagram: Data Structure

```mermaid
classDiagram
    class IPLocationservice {
        -ip_api: str
        -ipify: str
        +get_public_ip() str
        +get_location_data(ip: str) dict
    }
    
    class Config {
        +IP_API_URL: str
        +IPIFY_URL: str
        +DEBUG: bool
        +PORT: int
        +LOG_LEVEL: str
    }
    
    class FlaskApp {
        +health() dict
        +get_location() dict
    }
    
    FlaskApp --> IPLocationservice: uses
    IPLocationservice --> Config: reads
```
