import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import fitz  # PyMuPDF
import docx
from PIL import Image
import pytesseract
import io
import together
import os

# Load your environment variables
load_dotenv()

# Get the API key from the .env file
together.api_key = os.getenv("TOGETHER_API_KEY")

model_name = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"


def ask_llm(prompt):
    response = together.Complete.create(
        prompt=prompt,
        model=model_name,
        max_tokens=512,
        temperature=0.7,
        top_k=50,
        top_p=0.7,
        repetition_penalty=1.1,
        stop=["User:", "AI:"]
    )
    return response['choices'][0]['text'].strip()

def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    if ext == 'csv':
        df = pd.read_csv(file)
        return df, df.to_string()
    elif ext in ['xls', 'xlsx']:
        df = pd.read_excel(file)
        return df, df.to_string()
    elif ext == 'txt':
        content = file.read().decode('utf-8')
        return None, content
    elif ext == 'pdf':
        pdf_text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                pdf_text += page.get_text()
        return None, pdf_text
    elif ext == 'docx':
        doc = docx.Document(file)
        fullText = '\n'.join([para.text for para in doc.paragraphs])
        return None, fullText
    elif ext in ['png', 'jpg', 'jpeg']:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return None, text
    else:
        return None, "❌ Unsupported file type"

st.set_page_config(page_title="Data Analyst Agent", layout="wide")
st.title("📊 Data Analyst Agent")
st.markdown("Upload a file (CSV, Excel, PDF, DOCX, TXT, Image) and ask questions about its data.")

uploaded_file = st.file_uploader("Upload your document", type=['csv', 'xlsx', 'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    df, content = extract_text(uploaded_file)

    st.subheader("📄 Extracted Data Preview")
    if df is not None:
        st.dataframe(df)
    else:
        st.text_area("Extracted Text", content, height=300)

    query = st.text_input("🔎 Ask a question about the data:")

    if query:
        with st.spinner("Thinking..."):
            try:
                prompt = f"Here is the data:\n{content}\n\nQuestion: {query}\nAnswer:"
                answer = ask_llm(prompt)
                st.success("✅ Answer:")
                st.markdown(answer)
            except Exception as e:
                st.error(f"⚠️ Error from LLM: {e}")

        # 🔍 Try simple chart render based on keywords
        if df is not None:
            if "pie chart" in query.lower():
                if 'Item Type' in df.columns and 'Total Revenue' in df.columns:
                    pie_data = df.groupby('Item Type')['Total Revenue'].sum().reset_index()
                    fig, ax = plt.subplots()
                    ax.pie(pie_data['Total Revenue'], labels=pie_data['Item Type'], autopct='%1.1f%%')
                    ax.set_title("Total Revenue by Item Type")
                    st.pyplot(fig)

            elif "bar chart" in query.lower():
                if 'Region' in df.columns and 'Total Revenue' in df.columns:
                    bar_data = df.groupby('Region')['Total Revenue'].sum().reset_index()
                    fig, ax = plt.subplots()
                    ax.bar(bar_data['Region'], bar_data['Total Revenue'])
                    ax.set_xlabel("Region")
                    ax.set_ylabel("Total Revenue")
                    ax.set_title("Bar Chart: Revenue by Region")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

            elif "line chart" in query.lower():
                if 'Order Date' in df.columns and 'Total Revenue' in df.columns:
                    try:
                        df['Order Date'] = pd.to_datetime(df['Order Date'])
                        line_data = df.groupby('Order Date')['Total Revenue'].sum().reset_index()
                        fig, ax = plt.subplots()
                        ax.plot(line_data['Order Date'], line_data['Total Revenue'])
                        ax.set_title("Total Revenue Over Time")
                        ax.set_xlabel("Date")
                        ax.set_ylabel("Revenue")
                        st.pyplot(fig)
                    except Exception as e:
                        st.warning("Could not parse dates or plot line chart.")
# Sample Prompts  (concise answers, no code expected):
# - "What is the most sold item? Give a direct answer."
# - "Which region had the highest total revenue? Just the region name."
# - "Summarize the sales performance in one line."
# - "What is the total revenue from electronics?"
# - "Which item type generated the least revenue?"
# - "Tell me the month with the highest sales, answer directly."
#
#  Tip: Adding 'Give a direct answer' or 'Do not include code' at the end of your prompt 
# often helps the agent skip showing Python code and focus on a clean, human-readable answer.
