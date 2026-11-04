# 🧠 InsightAI
### Dual-Mode Data Analytics Platform | Streamlit + Local AI (Ollama)

**InsightAI** is a dual-mode data analytics platform that transforms raw CSV datasets into meaningful insights through interactive dashboards, data investigation, visualizations, and AI-assisted analysis.

The project provides two distinct editions:

- **Analytics Edition:** A publicly accessible Streamlit dashboard that works without Ollama.
- **AI Edition:** An interactive web application powered by locally running Ollama models for AI-assisted data exploration.

Both editions are built using free and open-source technologies.

---

## 🌐 Live Demos

| Edition | Live Website | Requirements |
|---|---|---|
| 📊 **Analytics Edition** | [Launch Dashboard](https://insightai-dataanalyst.streamlit.app/) | Browser only |
| 🤖 **AI Edition** | [Launch AI Edition](https://shambhavi614.github.io/InsightAI/) | Local Ollama for AI features |

> **Important:** The AI Edition is hosted on GitHub Pages as a frontend-only application. To use the AI Copilot, users must have Ollama installed and running locally. The Analytics Edition works without Ollama.

---

## 📸 Project Screenshots

### 📊 Analytics Edition — Without Ollama

![InsightAI Analytics Dashboard](screenshots/analytics-edition.png)

**Live Demo:** https://insightai-dataanalyst.streamlit.app/

### 🤖 AI Edition — With Ollama

![InsightAI AI Edition Dashboard](screenshots/ai-edition.png)

**Live Demo:** https://shambhavi614.github.io/InsightAI/

### 🧠 AI Copilot — Local LLM Integration

![InsightAI AI Copilot](screenshots/ai-copilot.png)

*AI-assisted analysis using a locally running Llama 3.2 model through Ollama.*

---

## ✨ Features

### 📊 Analytics Edition (Without Ollama)

Built with Python and Streamlit for accessible, interactive data analysis.

- Upload CSV datasets
- Explore dataset summaries and statistics
- Visualize trends using interactive Plotly charts
- Investigate changes across categories and time periods
- Generate downloadable PDF reports
- Access the dashboard directly from a browser
- No local AI installation required

**Technology:** Python, Streamlit, Pandas, NumPy, Plotly, ReportLab

**Deployment:** Streamlit Community Cloud

### 🤖 AI Edition (With Ollama)

A browser-based analytics experience with optional local AI-powered assistance.

- Upload and explore CSV datasets
- Interactive charts and visualizations
- Investigation Lab for data exploration
- AI Copilot for natural-language questions
- Streaming AI-generated responses
- Evidence-grounded prompts using calculated dataset summaries
- Local Llama 3.2 model integration
- Responsive Spatial Glass-inspired user interface

**Technology:** HTML5, CSS3, JavaScript, Ollama, Llama 3.2

**Deployment:** GitHub Pages (frontend only)

---

## ⚖️ Edition Comparison

| Feature | Analytics Edition | AI Edition |
|---|---|---|
| CSV Upload | ✅ | ✅ |
| Dataset Exploration | ✅ | ✅ |
| Interactive Charts | ✅ | ✅ |
| Investigation Lab | ✅ | ✅ |
| PDF Report Generation | ✅ | — |
| AI Copilot | ❌ | ✅ |
| Streaming AI Responses | ❌ | ✅ |
| Ollama Required | ❌ | ✅ For AI |
| Hosting | Streamlit Cloud | GitHub Pages |

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python, JavaScript |
| Frontend | HTML5, CSS3, Streamlit |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly |
| AI Integration | Ollama, Llama 3.2 (1B / 3B) |
| PDF Generation | ReportLab |
| Deployment | Streamlit Community Cloud, GitHub Pages |
| Version Control | Git, GitHub |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shambhavi614/InsightAI.git
cd InsightAI
```

### 2. Run the Analytics Edition

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```powershell
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The Streamlit dashboard will open in your browser, usually at `http://localhost:8501`.

For the public demo deployment, Ollama-dependent functionality is disabled through the deployment configuration.

### 3. Run the AI Edition

Install Ollama from:

https://ollama.com/

Download the lightweight Llama 3.2 model:

```bash
ollama pull llama3.2:1b
```

Ensure Ollama is running and accessible on your computer.

Open the AI Edition frontend through a local development server using the files inside the `ai-web` directory, or visit:

https://shambhavi614.github.io/InsightAI/

The AI Copilot communicates with the local Ollama API. Browser access and Ollama origin settings may need configuration depending on the environment.

---

## 🏗️ System Architecture

```text
                        InsightAI
                            |
              +-------------+-------------+
              |                           |
       Analytics Edition              AI Edition
              |                           |
          Streamlit                 HTML / CSS / JS
              |                           |
       CSV Data Upload             CSV Data Upload
              |                           |
       Pandas + NumPy              Data Processing
              |                           |
       Investigation Engine        Investigation Lab
              |                           |
       Plotly Visualizations       Interactive Charts
              |                           |
       PDF Report Generator        Ollama AI Copilot
              |                           |
       Streamlit Cloud             Local Llama 3.2
                                          |
                                     GitHub Pages
                                   (Frontend Hosting)
```

---

## 📁 Project Structure

```text
InsightAI/
│
├── app.py
├── deployment.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── investigation_engine.py
│   ├── insight_narrator.py
│   └── report_generator.py
│
├── utils/
│   └── charts.py
│
├── styles/
│   └── theme.py
│
├── ai-web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── screenshots/
    ├── analytics-edition.png
    ├── ai-edition.png
    └── ai-copilot.png
```

*Simplified project structure showing the primary components and screenshot assets.*

---

## 🔒 Privacy and Deployment

**Analytics Edition:** Data is processed by the Streamlit application running in the cloud. No local Ollama installation is needed.

**AI Edition:** AI inference is performed through a locally running Ollama model rather than a paid cloud AI API. The GitHub Pages deployment does not host the language model.

For sensitive or confidential datasets, users should evaluate the privacy and security implications of their chosen deployment.

---

## 🎯 Project Highlights

- Developed two deployment editions for different user requirements.
- Integrated a local large language model into a browser-based analytics workflow.
- Implemented streaming AI responses for a more responsive user experience.
- Built data investigation and interactive visualization features.
- Added PDF reporting to the Streamlit analytics workflow.
- Deployed both editions using free hosting platforms.
- Troubleshot deployment dependencies and frontend compatibility issues.

---

## 🔮 Future Enhancements

- Optional cloud-hosted AI inference
- Excel and additional dataset formats
- More advanced statistical analysis
- Improved AI-generated insight verification
- Expanded reporting and visualization capabilities

---

## 👩‍💻 Author

**Shambhavi Jha**

B.Tech — Computer Science & Engineering (Artificial Intelligence)

**GitHub:** [shambhavi614](https://github.com/shambhavi614)

---

### ⭐ InsightAI — From Data to Decisions

*Making data exploration more accessible through interactive analytics and local AI.*