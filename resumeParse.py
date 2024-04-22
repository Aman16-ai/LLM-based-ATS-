import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image

def parseResumeFromPdf(resume_file):
    if resume_file is not None:
        images = pdf2image.convert_from_bytes(resume_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
    else:
        raise FileNotFoundError("No file uploaded")