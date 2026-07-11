# SkyMind.ai ✈️🤖
An explainable flight recommendation dashboard driven by a responsive, high-contrast Cyber-Quantum design system and dynamic multi-variable user profiling.

SkyMind.ai bridges the gap between raw flight data logistics and user-centric decision-making. By analyzing traveler profiles (budget sensitivity vs. convenience priority), the engine automatically aggregates, ranks, and crafts unique human-readable text rationales explaining why specific routes perfectly fit a user's behavioral footprint.

---

## 🚀 Key Features

* **Vibrant Cyber-Quantum Design System:** Glassmorphic layout panels, glowing indicators, responsive UI built natively on the updated Tailwind v4 engine.
* **Dynamic Decision-Logic Engine:** The backend adapts its analytical rationale on-the-fly based on flight ranks, price points, transits, and profile metrics—no rigid templates.
* **Telemetry Prompt Auditing:** Front-and-center parameter logging that displays active search keys directly above flight payload deliveries.
* **Robust Error Pipeline:** Gracefully captures database query misses (404s) and infrastructure network drops without breaking layout constraints.

---

## 🛠️ Project Structure

* skymind-backend/ -> FastAPI Python API Gateway
  * app/engines/ -> Dynamic recommendation core matrix
  * app/schemas/ -> Pydantic data validation layer
  * app/main.py -> API endpoints & CORS middleware configuration
* skymind-frontend/ -> Vite + React + Tailwind v4 Web client
  * src/App.jsx -> Master dashboard core viewport layout
  * src/index.css -> Tailwind directives implementation

---

## ⚙️ Setup & Installation

### 1. Backend Service Configuration (FastAPI)
Navigate to your backend service directory, construct a clean virtual environment, install the modules, and ignite the local server:

cd skymind-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

The backend API documentation will now be available locally at http://127.0.0.1:8000/docs.

### 2. Frontend Interface Configuration (React + Vite)
In a secondary terminal window, configure the runtime Node dependencies and launch the hot-reloading development browser preview:

cd skymind-frontend
npm install
npm run dev

Open http://localhost:5173 in your browser to view the operational dashboard!

---

## 🧪 API Endpoints Reference

### Flight Telemetry Query
* **Endpoint:** POST /api/recommendations
* **Payload Format Requirements:** Requires user_id, origin, and destination text strings.
* **Response Blueprint:** Delivers traveler_name, origin, destination, metrics_applied object, and a ranked recommendations array containing custom AI alignment rationales.

### Engine Diagnostics
* **Endpoint:** GET /api/health
* **Description:** Verifies validation schema constraints and core cluster health status.

---

## 🎨 Styling Architecture Notes
This dashboard uses Tailwind v4. Legacy configuration modules are removed in favor of the high-speed CSS-native compiler engine. Global directives are linked explicitly in your main index CSS file using the new import statement rule: @import "tailwindcss";

To keep the colors popping uniformly, focus classes hook onto indigo, purple, fuchsia, and emerald standard color matrices configured on top of an ultra-deep slate background context.