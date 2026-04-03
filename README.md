# 📄 AI Contract Risk Analyzer

## 🚀 Overview

An AI-powered NLP system that analyzes legal contracts and detects risky or unfair clauses.

---

## 🎯 Features

* Upload PDF contracts
* Clause classification
* Risk detection (High/Medium/Safe)
* Risk scoring system
* Named Entity Recognition

---

## 🧠 Tech Stack

* Python
* NLP (spaCy, Scikit-learn)
* Streamlit
* Machine Learning

---

## 📂 Project Structure

* app/ → frontend
* src/ → NLP modules
* models/ → trained models

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app/app.py
```

---

## 📊 Output

* Risk score (0–100)
* Highlighted risky clauses
* Explanation for each risk

---

## 🔥 Future Improvements

* Legal-BERT integration
* Better dataset (CUAD)
* Explainable AI

---

## 👨‍💻 Author

Om Singh
