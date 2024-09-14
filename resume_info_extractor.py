import os
import streamlit as st
import PyPDF2 as pdf
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
import json
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": input}] ,
    n=1
    )
    
    return response.choices[0].message.content
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt_template = """
Extract all possible information from the resume and return it in JSON format. Do not include any additional text.
Here is the resume: {text}
"""


## streamlit app
st.title("Resume Information Extractor")  
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        #st.write(resume_text)
        #st.write(jd)
        input_prompt = input_prompt_template.format(text=resume_text)
        response = get_response(input_prompt)
        st.write(response)
        json_data = json.dumps(response, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="extracted_resume_info.json",
            mime="application/json"
        )