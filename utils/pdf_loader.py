from langchain_core.documents import Document

from PyPDF2 import PdfReader

from pdf2image import convert_from_path

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

    documents = []

    images = convert_from_path(pdf_path)

    for page_num, image in enumerate(images):

        text = pytesseract.image_to_string(

            image,

            lang="eng"
        )

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
                "Using OCR for scanned PDF..."
            )

            documents = extract_text_ocr(
                temp_pdf_path
            )


        all_documents.extend(
            documents
        )

        os.remove(temp_pdf_path)

    return all_documents