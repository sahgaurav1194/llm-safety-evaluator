# 🛡️ LLM Safety Evaluator

An automated red teaming and safety evaluation framework for Large Language Models, built to detect vulnerabilities across 5 attack categories.

## 🎯 What It Does

Automatically tests LLMs for:
- **Prompt Injection** — can someone hijack the AI's behaviour?
- **Harmful Content** — does it generate dangerous responses?
- **Jailbreaks** — can someone bypass safety guardrails?
- **Bias** — does it respond unfairly to different groups?
- **Data Privacy** — does it leak system prompt information?

## 📊 Sample Output
## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq LLaMA 3.1 |
| Experiment Tracking | MLflow |
| Results Export | Pandas CSV |
| CLI Output | Rich |

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/sahgaurav1194/llm-safety-evaluator.git
cd llm-safety-evaluator
```

### 2. Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install groq mlflow pandas python-dotenv rich
```

### 3. Set API key
```bash
echo 'GROQ_API_KEY=your-key-here' > .env
```

### 4. Run evaluation
```bash
python3 evaluator.py
```

### 5. View MLflow dashboard
```bash
mlflow ui
```

## 🔬 Test Categories

| ID | Category | Severity |
|----|----------|----------|
| PI-001, PI-002 | Prompt Injection | HIGH |
| HC-001, HC-002 | Harmful Content | CRITICAL/HIGH |
| JB-001, JB-002 | Jailbreak | HIGH/MEDIUM |
| BT-001, BT-002 | Bias | MEDIUM |
| DP-001 | Data Privacy | HIGH |
| RB-001 | Robustness | LOW |

## 👨‍💻 Author

Gaurav Sah — [GitHub](https://github.com/sahgaurav1194)
