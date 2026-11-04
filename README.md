# 🧠 InsightAI
### Dual-Mode Data Analytics Platform | Streamlit + Local AI (Ollama)

**InsightAI** is a data analytics platform that transforms raw CSV datasets into meaningful insights through interactive dashboards, visualizations, investigation tools, and AI-assisted analysis.

The project offers **two distinct editions**: a cloud-hosted analytics dashboard that works without AI installation, and an AI-powered web edition that integrates with locally running Ollama models.

## 🌐 Live Demos

| Edition | Live Website | AI Requirement |
|---|---|---|
| 📊 **Analytics Edition** | [Launch Streamlit Dashboard](https://insightai-dataanalyst.streamlit.app/) | No Ollama required |
| 🤖 **AI Edition** | [Launch AI Web App](https://shambhavi614.github.io/InsightAI/) | Local Ollama required for AI |

> **Note:** Both editions are accessible through a browser. The AI Edition's GitHub Pages deployment hosts only the frontend; AI inference requires Ollama running on the user's computer.

---

## ✨ Key Features

### 📊 Analytics Edition — Without Ollama

Built using **Python and Streamlit**, this edition focuses on accessible, interactive data analysis.

- CSV upload and dataset exploration
- Dataset summaries and statistical insights
- Interactive charts and visualizations
- Investigation of trends and category-level changes
- PDF report generation
- Cloud deployment without local AI dependencies

**Tech Stack:** Python, Streamlit, Pandas, NumPy, Plotly, ReportLab

**Hosting:** Streamlit Community Cloud

### 🤖 AI Edition — With Ollama

Built using **HTML, CSS, and JavaScript**, this edition combines interactive analytics with a locally hosted language model.

- CSV upload and data exploration
- Interactive visualizations and Investigation Lab
- AI Copilot for natural-language analytical questions
- Streaming AI responses
- Evidence-grounded prompts with calculated data summaries
- Local Llama 3.2 integration
- Responsive Spatial Glass user interface

**Tech Stack:** HTML, CSS, JavaScript, Ollama, Llama 3.2

**Hosting:** GitHub Pages (frontend only)

---

## ⚖️ Edition Comparison

| Capability | Analytics Edition | AI Edition |
|---|---|---|
| CSV Upload | ✅ | ✅ |
| Data Exploration | ✅ | ✅ |
| Interactive Charts | ✅ | ✅ |
| Investigation Lab | ✅ | ✅ |
| PDF Report Generation | ✅ | — |
| Natural-Language AI Copilot | ❌ | ✅ |
| Streaming AI Responses | ❌ | ✅ |
| Ollama Installation | Not required | Required for AI |
| Deployment | Streamlit Cloud | GitHub Pages |

---

## 🛠️ Technology Stack

**Frontend:** HTML5, CSS3, JavaScript, Streamlit

**Backend & Analytics:** Python, Pandas, NumPy

**Visualization:** Plotly

**AI Integration:** Ollama, Llama 3.2 (1B/3B)

**Reporting:** ReportLab

**Deployment:** Streamlit Community Cloud, GitHub Pages

**Version Control:** Git, GitHub

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shambhavi614/InsightAI.git
cd InsightAI
```

### 2. Run the Analytics Edition

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

### 3. Run the AI Edition

Install [Ollama](https://ollama.com/) and download a supported model:

```bash
ollama pull llama3.2:1b
```

Ensure the Ollama service is running.

Open `ai-web/index.html` through a local development server, or visit the [AI Edition](https://shambhavi614.github.io/InsightAI/).

The AI Copilot requires the browser to be able to access the local Ollama API. Depending on the environment, Ollama's allowed origins may need configuration.

---

## 🏗️ Project Architecture

```text
                       InsightAI
                           |
             +-------------+-------------+
             |                           |
      Analytics Edition              AI Edition
             |                           |
         Streamlit                 HTML/CSS/JS
             |                           |
      Pandas + NumPy              CSV Processing
             |                           |
      Data Investigation          Investigation Lab
             |                           |
       Plotly Charts              Local Ollama API
             |                           |
       PDF Reporting              Llama 3.2 Model
             |                           |
       Streamlit Cloud              GitHub Pages
```

## 📁 Project Structure

```text
InsightAI/
├── app.py
├── deployment.py
├── requirements.txt
├── core/
│   ├── investigation_engine.py
│   ├── insight_narrator.py
│   └── report_generator.py
├── utils/
│   └── charts.py
├── styles/
│   └── theme.py
└── ai-web/
    ├── index.html
    ├── style.css
    └── app.js
```

*Simplified structure showing the primary application components.*

---

## 🔒 Privacy & Deployment

The Analytics Edition processes uploaded data within its Streamlit application environment and does not require an AI service.

The AI Edition uses a local Ollama instance for language-model inference. Its AI functionality is not hosted on GitHub Pages and does not require a paid AI API.

Users should avoid uploading confidential datasets to public cloud applications unless the deployment's data-handling practices meet their requirements.

---

## 🔮 Future Enhancements

- Optional cloud-hosted AI inference
- Excel and additional file format support
- Advanced statistical analysis
- Improved automated insight verification
- Expanded reporting and visualization options

---

## 👩‍💻 Developed By

**Shambhavi Jha**

B.Tech — Computer Science & Engineering (Artificial Intelligence)

Galgotias College of Engineering and Technology

**GitHub:** [shambhavi614](https://github.com/shambhavi614)

---

### ⭐ InsightAI — From Data to Decisions

*Making data exploration more accessible through interactive analytics and local AI.*