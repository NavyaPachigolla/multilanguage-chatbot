from langchain_core.documents import Document

from PyPDF2 import PdfReader

from pdf2image import convert_from_path
import easyocr
import numpy as np


import pytesseract

import tempfile

import os


# TESSERACT PATH

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\SAMA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def extract_text_normal(pdf_path):

    documents = []

    reader = PdfReader(pdf_path)

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():


            documents.append(

                Document(

                    page_content=text,

                    metadata={

                        "source": os.path.basename(pdf_path),

                        "page": page_num + 1
                    }
                )
            )

    return documents


def extract_text_ocr(pdf_path):

    print("OCR Started...")

    documents = []

    images = convert_from_path(
        pdf_path,
        dpi=300,
        thread_count=4
    )

    print(f"Total Pages: {len(images)}")

    for page_num, image in enumerate(images):

        print(f"\nProcessing Page {page_num + 1}")
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(
            image,
            lang="eng",
            config=custom_config
        )

        print("\n========== OCR TEXT ==========")
        print(text[:1000])
        print("==============================")

        print(f"Completed Page {page_num + 1}")

        if text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": os.path.basename(pdf_path),
                        "page": page_num + 1
                    }
                )
            )

    print("OCR Finished")

    return documents

def extract_text_easyocr(pdf_path):

    print("EasyOCR Started...")

    documents = []

    reader = easyocr.Reader(
        ['en'],
        gpu=False
    )

    images = convert_from_path(
        pdf_path,
        dpi=300
    )

    print(f"Total Pages: {len(images)}")

    for page_num, image in enumerate(images):

        print(f"Processing Page {page_num + 1}")

        image_np = np.array(image)

        results = reader.readtext(
            image_np,
            detail=0,
            paragraph=True
        )

        text = "\n".join(results)

        print(text[:500])

        if text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": os.path.basename(pdf_path),
                        "page": page_num + 1
                    }
                )
            )

    print("EasyOCR Finished")

    return documents

def load_pdfs(uploaded_files):

    all_documents = []

    for uploaded_file in uploaded_files:

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".pdf"

        ) as temp_file:

            temp_file.write(

                uploaded_file.read()
            )

            temp_pdf_path = temp_file.name


        # NORMAL PDF EXTRACTION

        documents = extract_text_normal(
            temp_pdf_path
        )


        # OCR FALLBACK

        if len(documents) == 0:

            print(
                "Using EasyOCR..."
            )

            documents = extract_text_easyocr(
                temp_pdf_path
            )


        all_documents.extend(
            documents
        )

        os.remove(temp_pdf_path)

    return all_documents