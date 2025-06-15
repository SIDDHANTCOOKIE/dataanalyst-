# 📊 Data Analyst Agent

An intelligent multimodal agent that can analyze uploaded documents, answer follow-up questions, and create visualizations — all powered by `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` via Together.ai.

---

## 🔍 Features

- ✅ Upload documents: `.csv`, `.xlsx`, `.txt`, `.pdf`, `.docx`, `.png`, `.jpg`, `.jpeg`
- ✅ Ask questions about the data in natural language
- ✅ Generates direct answers (not just code)
- ✅ Smart visualizations: pie chart, bar chart, line chart (based on keywords)
- ✅ Built with Streamlit for quick testing

---

## 💬 Sample Prompts (For Concise Answers)

Add these directly into the app for better results:

- What is the most sold item? Give a direct answer.
- Which region had the highest revenue?
- What is the total revenue generated?
- Plot a pie chart of revenue by item type
- Give a bar chart of revenue by region
- Show line chart of revenue over time
- Who are the top 3 item types by units sold?
- *Add “Give a short answer, no code” to improve brevity.*

---

## 🚀 Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
