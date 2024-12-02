# Best Brawl - High Level Design Document

## 1. Introduction

Best Brawl is a web application providing real-time tier lists for Brawl Stars maps and modes. The application updates data hourly via the brawltime.ninja API and presents it through a modern, mobile-friendly interface.

### 1.1 Key Features
- Real-time tier lists for all maps/modes
- Hourly data updates
- Mobile-first design
- Offline support
- Share functionality
- Modern gaming UI
- Fast performance

### 1.2 Target Users
- Brawl Stars players seeking optimal brawler choices
- Competitive players planning team compositions
- Players drafting for matches

## 2. System Architecture

### 2.1 High-Level Overview
```
[React Frontend] <-> [Caddy Server] <-> [Flask API] <-> [JSON Files]
                                       |
                                       v
                                [In-Memory Cache]

[Cron Jobs] -> [Data Updater] -> [JSON Files]
```

### 2.2 Component Architecture

#### Frontend
```
/src
  /components
    /core
      - TierList.tsx         # Tier list grid
      - ModeSelector.tsx     # Mode dropdown
      - MapSelector.tsx      # Map selection
      - BrawlerCard.tsx      # Brawler display
      - ShareButton.tsx      # Share functionality
      - Navigation.tsx       # Mobile navigation
    /layout
      - Header.tsx          # App header
      - Footer.tsx          # App footer
    /pages
      - App.tsx            # Main app
      - Documentation.tsx  # Documentation
  /hooks
    - useMapData.ts       # Data fetching
    - useTierList.ts      # Tier management
  /utils
    - scoring.ts         # Score calculations
    - dataTransforms.ts  # Data transformations
  /types
    - types.ts          # TypeScript types
```

#### Backend
```
/backend
  /api
    __init__.py
    routes.py          # API endpoints
    data.py           # Data management
    models.py         # Data structures
    utils.py          # Helpers
  /services
    brawlapi.py      # BrawlTime integration
    cache.py         # Memory caching
    scoring.py       # Tier calculations
    token.py         # API token management
  /data
    /tierlists       # JSON storage
    /meta            # Config files
```

## 3. Data Management

### 3.1 File Structure
```
/data
  /tierlists
    /{mode}_{map}.json    # Tier lists
  /meta
    - last_updated.json   # Update timestamps
    - modes.json         # Game modes
    - maps.json          # Maps
  /cache
    - api_responses/     # API cache
```

### 3.2 Data Models

#### Tier List JSON
```json
{
  "lastUpdated": "ISO-DATE",
  "mode": "string",
  "map": "string",
  "tiers": {
    "S": [
      {
        "name": "string",
        "winRate": "number",
        "pickRate": "number",
        "score": "number"
      }
    ],
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "F": [],
    "X": []
  },
  "metadata": {
    "totalMatches": "number",
    "averageWinRate": "number",
    "lastCalculated": "ISO-DATE"
  }
}
```

## 4. API Endpoints

### 4.1 Core Endpoints
```
GET /api/modes
    Returns available game modes

GET /api/maps/{mode}
    Returns maps for specified mode

GET /api/tierlist/{mode}/{map}
    Returns tier list for mode/map

GET /api/meta/last-updated
    Returns last update timestamps
```

### 4.2 Response Format
```json
{
  "success": boolean,
  "data": object,
  "error": string|null,
  "timestamp": "ISO-DATE"
}
```

## 5. Frontend Design

### 5.1 UI Components

#### Tier List Grid
```typescript
const TierList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  padding: 1rem;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
`;
```

#### Mobile Navigation
```typescript
const BottomNav = styled.nav`
  position: fixed;
  bottom: 0;
  width: 100%;
  background: rgba(0,0,0,0.8);
  backdrop-filter: blur(10px);
  padding: 1rem;
  
  @media (min-width: 768px) {
    position: static;
  }
`;
```

### 5.2 Theme
```typescript
const theme = {
  colors: {
    background: '#121212',
    surface: '#1E1E1E',
    primary: '#BB86FC',
    secondary: '#03DAC6',
    error: '#CF6679'
  },
  glassmorphism: {
    background: 'rgba(30,30,30,0.8)',
    blur: '10px',
    border: '1px solid rgba(255,255,255,0.1)'
  }
}
```

## 6. Deployment

### 6.1 Server Setup
```bash
# Installation
apt update
apt install -y python3-pip nodejs npm caddy

# Application setup
mkdir -p /opt/bestbrawl/{frontend,backend,data,logs}
cd /opt/bestbrawl

# Backend
pip install -r backend/requirements.txt
cp backend/systemd/bestbrawl.service /etc/systemd/system/
systemctl enable --now bestbrawl

# Frontend
cd frontend
npm install
npm run build

# Caddy
cp Caddyfile /etc/caddy/
systemctl restart caddy
```

### 6.2 Directory Structure
```
/opt/bestbrawl/
  ├── frontend/        # React build
  ├── backend/         # Flask app
  ├── data/           # JSON files
  ├── logs/           # App logs
  └── scripts/        # Maintenance
```

### 6.3 Caddy Configuration
```caddyfile
bestbrawl.com {
    root * /opt/bestbrawl/frontend/dist
    encode gzip
    try_files {path} /index.html
    
    handle /api/* {
        reverse_proxy localhost:8000
    }
    
    file_server
}
```

### 6.4 Process Management
```bash
# Systemd service
[Unit]
Description=BestBrawl API
After=network.target

[Service]
Type=simple
User=bestbrawl
WorkingDirectory=/opt/bestbrawl/backend
Environment=FLASK_ENV=production
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 7. Data Update Process

### 7.1 Update Flow
1. Hourly cron triggers update
2. Verify/refresh API token
3. Fetch data for all modes/maps
4. Calculate scores and tiers
5. Update JSON files
6. Clear cache

### 7.2 Scoring Logic
```python
def calculate_score(win_rate, pick_rate, avg_win_rate):
    win_rate_diff = win_rate - avg_win_rate
    if win_rate_diff > 0:
        score = 2 * win_rate_diff
    else:
        score = win_rate_diff
    return score * np.log1p(pick_rate)
```

### 7.3 Tier Thresholds
```python
TIER_THRESHOLDS = {
    'S': 20,
    'A': 10,
    'B': 5,
    'C': 0,
    'D': -5,
    'F': float('-inf'),
    'X': 'pick_rate < 1%'
}
```

## 8. Development Guidelines

### 8.1 Tech Stack
- Frontend: React + TypeScript
- Backend: Python Flask
- Storage: JSON + In-memory cache
- Server: Ubuntu 22.04 LTS
- Web Server: Caddy
- Process Manager: Systemd

### 8.2 Code Style
```bash
# Frontend
npx prettier --write "src/**/*.{ts,tsx}"
npx eslint "src/**/*.{ts,tsx}"

# Backend
black backend/
pylint backend/
```

### 8.3 Git Workflow
```bash
main        # Production branch
└── develop # Development branch
    └── feature/* # Feature branches
```

## 9. Performance Optimizations

### 9.1 Frontend
- Code splitting
- Asset preloading
- Image optimization
- Progressive loading
- Service worker caching

### 9.2 Backend
- In-memory caching
- Response compression
- JSON file caching
- Async data fetching
- Request batching

## 10. Monitoring

### 10.1 Health Checks
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'last_update': get_last_update_time(),
        'cache_size': get_cache_size(),
        'uptime': get_uptime()
    }
```

### 10.2 Logging
```python
import logging

logging.basicConfig(
    filename='/opt/bestbrawl/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 11. Security

### 11.1 API Token Management
- Secure token storage
- Automatic token refresh
- Token validation
- Rate limiting

### 11.2 CORS Configuration
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://bestbrawl.com"],
        "methods": ["GET", "OPTIONS"]
    }
})
```

## 12. Documentation

### 12.1 API Documentation
```markdown
# API Documentation
Base URL: https://bestbrawl.com/api

## Endpoints
GET /modes
GET /maps/{mode}
GET /tierlist/{mode}/{map}
...
```

### 12.2 User Guide
- Quick start
- Mode/map selection
- Understanding tiers
- Sharing lists
- Offline usage