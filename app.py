from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# from ats.resumeParse import parseResumeFromPdf
import streamlit as st
import os
import base64
import io
from PIL import Image 
import pdf2image
from pypdf import PdfReader
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY",'noi noi')

def parseResumeFromPdf(resume_file):
    # if resume_file is not None:
    #     images = pdf2image.convert_from_bytes(resume_file.read())
    #     first_page = images[0]

    #     img_byte_arr = io.BytesIO()
    #     first_page.save(img_byte_arr,format='JPEG')
    #     img_byte_arr = img_byte_arr.getvalue()

    #     pdf_parts = [
    #         {
    #             "mime_type": "image/jpeg",
    #             "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
    #         }
    #     ]
    # else:
    #     raise FileNotFoundError("No file uploaded")
    reader = PdfReader(resume_file)
    page = reader.pages[0]
    return page.extract_text()


## streamlit framework
input_prompt = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
Job description is : {jd} and content of candidate resume is : {content}
"""

prompt = PromptTemplate.from_template(input_prompt)
st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

# openAI LLm 
llm=ChatGoogleGenerativeAI(model="gemini-pro")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

# if input_text:
#     st.write(chain.invoke({'content':input_text,'jd':'require a machine learning engineer with skills, python and django'}))

if submit3:
   if uploaded_file is not None and input_text:
       pdf_content = parseResumeFromPdf(uploaded_file)
       st.write(chain.invoke({'content':pdf_content,'jd':input_text}))
    