# 🌾 KrishiMap AI

### AI Farm Intelligence

KrishiMap AI is a full-stack agriculture intelligence platform that combines **GIS mapping, weather intelligence, AI-powered crop recommendations, farm planning, and task management** into a single farmer-focused dashboard.

The platform allows farmers to create and manage multiple farms, draw their farm boundaries directly on an interactive map, calculate farm area, monitor weather conditions, receive AI-based crop recommendations, and organize agricultural activities through a farm calendar.

---

## 🚀 Core Idea

Traditional agricultural applications often provide weather, crop information, or farm management as separate features.

**KrishiMap AI connects them into one workflow:**

```text
Farmer
   ↓
Authentication
   ↓
Multiple Farms
   ↓
Draw Farm Boundary
   ↓
GeoJSON Farm Data
   ↓
Weather + Terrain Intelligence
   ↓
AI Crop Recommendation
   ↓
Crop Planning
   ↓
Farm Calendar
   ↓
AI Farm Assistant
```

The goal is to provide **location-aware and farm-specific agricultural intelligence** rather than generic crop advice.

---

## ✨ Features

### 🔐 Authentication

* Farmer registration
* Secure login
* JWT-based authentication
* Password hashing using Argon2
* Protected dashboard routes
* User profile and location data

### 🗺️ GIS Farm Mapping

* Interactive OpenStreetMap map
* Leaflet-based mapping
* Leaflet-Geoman farm boundary drawing
* Polygon-based farm boundaries
* Automatic farm area calculation
* Area conversion to acres
* Farm center calculation
* GeoJSON polygon storage
* Current-location marker
* Multiple farm support

### 🌦️ Weather Intelligence

Powered by **Open-Meteo**.

* Current temperature
* Humidity
* Rainfall
* Precipitation probability
* Wind speed
* Weather condition
* Seven-day forecast
* Farm-specific weather data
* Elevation information

### 🤖 AI Crop Recommendation

KrishiMap AI combines deterministic agricultural scoring with a large language model.

The recommendation engine considers:

* Rainfall suitability
* Temperature suitability
* Soil-data availability
* Seasonal suitability
* Vegetation information
* Terrain/elevation
* Seven-day weather forecast
* Existing/current crop

The system generates:

* Recommended crop
* Recommendation score
* Suitability breakdown
* Crop comparison
* Weather risks
* Farm insights
* Terrain insights
* Farmer advice
* Crop lifecycle schedule

### 📊 Farm Analysis

The analysis dashboard provides a farm-level intelligence view containing:

* Overall farm condition
* Vegetation indicators
* Weather suitability
* Irrigation requirement
* Farm location
* Spatial farm overview
* AI-generated farm insights
* Current crop recommendation

### 📅 Farm Calendar

Farmers can organize agricultural activities through a persistent calendar.

Supported activities:

* Irrigation
* Fertilizer
* Monitoring
* Harvest
* Other farm activities

Tasks are stored in PostgreSQL and remain available across sessions.

### 🌐 Multilingual Interface

The dashboard supports:

* 🇬🇧 English
* 🇮🇳 Hindi
* 🇮🇳 Bengali

The language preference is maintained on the client side and is also passed to the AI recommendation system for localized responses.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       Farmer        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Next.js Frontend  │
                    │                     │
                    │ Dashboard           │
                    │ GIS Map             │
                    │ Weather             │
                    │ Analysis            │
                    │ Calendar             │
                    │ AI Interface        │
                    └──────────┬──────────┘
                               │
                         REST API / JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │                     │
                    │ Authentication      │
                    │ Farms               │
                    │ Weather             │
                    │ Recommendations     │
                    │ Tasks               │
                    └───────┬─────┬───────┘
                            │     │
                 ┌──────────┘     └──────────┐
                 ▼                           ▼
       ┌─────────────────┐         ┌─────────────────┐
       │   PostgreSQL    │         │ External APIs   │
       │                 │         │                 │
       │ Users           │         │ Open-Meteo      │
       │ Farms           │         │                 │
       │ Farm Tasks      │         └─────────────────┘
       └─────────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │      Groq LLM       │
                  │                     │
                  │ AI explanations     │
                  │ Farmer advice       │
                  │ Crop reasoning      │
                  └─────────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Next.js        | React web framework           |
| TypeScript     | Type-safe development         |
| Tailwind CSS   | UI styling                    |
| Leaflet        | Interactive maps              |
| React Leaflet  | React integration for Leaflet |
| Leaflet-Geoman | Farm boundary drawing         |
| Turf.js        | Geospatial calculations       |
| Zustand        | Application state management  |
| Axios          | API communication             |
| Recharts       | Data visualization            |
| Lucide React   | UI icons                      |

## Backend

| Technology      | Purpose               |
| --------------- | --------------------- |
| FastAPI         | REST API              |
| Python          | Backend language      |
| SQLAlchemy      | ORM                   |
| PostgreSQL      | Relational database   |
| JWT             | Authentication        |
| pwdlib + Argon2 | Password hashing      |
| Pydantic        | Data validation       |
| HTTPX           | External API requests |
| LangChain       | LLM integration       |
| Groq            | AI inference          |

## External Services

| Service       | Purpose               |
| ------------- | --------------------- |
| OpenStreetMap | Map tiles             |
| Open-Meteo    | Weather and elevation |
| Groq          | AI inference          |

The current architecture intentionally avoids paid satellite dependencies.

---

# 📁 Project Structure

```text
KrishiMap/
│
├── .gitignore
├── README.md
│
├── frontend/
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── forgot-password/
│   │   │   └── dashboard/
│   │   │       ├── farms/
│   │   │       ├── calendar/
│   │   │       └── analysis/
│   │   │
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   ├── map/
│   │   │   ├── calendar/
│   │   │   └── chat/
│   │   │
│   │   ├── context/
│   │   ├── lib/
│   │   ├── store/
│   │   └── types/
│   │
│   ├── .env.local
│   ├── package.json
│   └── ...
│
└── backend/
    │
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── security.py
    │   │
    │   ├── routers/
    │   │   ├── auth.py
    │   │   ├── users.py
    │   │   ├── farms.py
    │   │   ├── weather.py
    │   │   ├── recommendations.py
    │   │   └── tasks.py
    │   │
    │   └── services/
    │       ├── weather.py
    │       ├── recommendation.py
    │       └── satellite.py
    │
    ├── .env
    ├── requirements.txt
    └── run.py
```

---

# ⚙️ Local Development

## Prerequisites

Install:

* Node.js 20+
* Python 3.11+
* PostgreSQL 15+
* Git

You will also need a Groq API key for AI recommendations.

---

# 🗄️ Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE krishimap;
```

Then configure the backend environment.

---

# 🔑 Backend Environment

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/krishimap

JWT_SECRET_KEY=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast

GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=llama-3.3-70b-versatile

FRONTEND_URL=http://localhost:3000
```

**Never commit this file.**

---

# 🐍 Backend Setup

From the project root:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# ⚛️ Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create:

```text
frontend/.env.local
```

with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

---

# 🔄 API Overview

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

## Users

```text
GET   /api/users/me
PATCH /api/users/me/location
```

## Farms

```text
GET    /api/farms
POST   /api/farms
GET    /api/farms/{farm_id}
```

## Weather

```text
GET /api/weather/{farm_id}
```

## AI Recommendations

```text
POST /api/recommendations/crop/{farm_id}
```

Supported languages:

```text
en
hi
bn
```

## Farm Tasks

```text
GET    /api/farms/{farm_id}/tasks
POST   /api/farms/{farm_id}/tasks
PATCH  /api/farms/{farm_id}/tasks/{task_id}
DELETE /api/farms/{farm_id}/tasks/{task_id}
```

---

# 🧠 AI Recommendation Pipeline

The recommendation system intentionally separates **numeric decision logic** from **natural-language generation**.

```text
Farm Boundary
      │
      ▼
Farm Metadata
      │
      ├──────────────► Area
      ├──────────────► Crop
      ├──────────────► Location
      └──────────────► Coordinates
                         │
                         ▼
                   Open-Meteo
                         │
                         ├── Current Weather
                         ├── 7-Day Forecast
                         └── Elevation
                         │
                         ▼
              Deterministic Scoring
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
         Rainfall   Temperature    Season
             │           │           │
             └───────────┼───────────┘
                         │
                         ▼
                  Crop Suitability
                         │
                         ▼
                    Groq LLM
                         │
                         ▼
             Farmer-Facing Explanation
```

This approach helps prevent the LLM from inventing numerical agricultural measurements.

---

# 🌱 Crop Scoring

The recommendation engine currently evaluates:

```text
Rainfall
Temperature
Soil
Season
Vegetation
Terrain
```

The weighted recommendation model uses:

```text
Rainfall       25%
Temperature    30%
Soil           10%
Season         15%
Vegetation     15%
Terrain         5%
```

The scores are intended as **decision-support indicators**, not replacements for professional agronomic or soil-laboratory analysis.

---

# 🛰️ Satellite Data

The architecture includes a satellite-insights layer so that real satellite indicators can be integrated later.

Current implementation uses a safe fallback when satellite data is unavailable:

```text
NDVI  → unavailable
NDMI  → unavailable
BSI   → unavailable
```

The application therefore does not fabricate satellite measurements.

The satellite service can later be replaced with a free/open imagery processing pipeline.

---

# 🔒 Security

KrishiMap AI follows several basic security practices:

* Passwords are hashed using Argon2.
* Passwords are never stored in plaintext.
* Authentication uses JWT access tokens.
* Farm APIs are owner-scoped.
* Users cannot access another user's farm data.
* Environment secrets are excluded from Git.
* API input is validated with Pydantic.
* PostgreSQL is used instead of storing application data in local files.

---

# 🌍 Localization

The interface currently supports:

```text
English
Hindi
Bengali
```

Language selection is available from the dashboard.

The selected language is also passed to the AI recommendation service:

```text
English → en
Hindi   → hi
Bengali → bn
```

This allows the recommendation explanation to be generated for the selected language.

---

# 🧪 Production Build

Frontend type checking and production build:

```bash
cd frontend
npm run build
```

Start the production frontend:

```bash
npm start
```

Backend production example:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# 🎯 Future Roadmap

Potential future improvements include:

* Real satellite imagery processing
* NDVI time-series analysis
* Soil moisture estimation
* Crop disease detection
* Irrigation prediction
* Fertilizer optimization
* Yield prediction
* Farm health anomaly detection
* AI voice assistant
* Odia language support
* Offline/PWA support
* SMS/WhatsApp farmer alerts
* Historical farm analytics
* Crop price intelligence
* Advanced geospatial layers
* IoT sensor integration

---

# 🏆 Why KrishiMap AI?

KrishiMap AI is designed around a simple principle:

> **Agricultural intelligence should be farm-specific, location-aware, explainable, and actionable.**

Instead of showing farmers isolated datasets, the platform combines:

```text
GIS
+
Weather
+
Terrain
+
Agricultural Scoring
+
Generative AI
+
Farm Management
```

into one workflow.

---

# 👨‍💻 Development

This project was developed as an agriculture-focused full-stack and AI/GIS application.

The architecture is designed to demonstrate:

* Full-stack engineering
* REST API development
* Database design
* Authentication
* Geospatial application development
* External API integration
* AI/LLM integration
* Multilingual UX
* Data-driven decision support

---

# 📄 License

This project is currently intended as an educational and prototype application.

Add an appropriate open-source license before public distribution.
