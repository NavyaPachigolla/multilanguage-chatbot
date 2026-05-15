import os

from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader

from pdf2image import convert_from_path

import pytesseract


# Set tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def load_pdfs(uploaded_files):

    documents = []

    os.makedirs("uploaded_docs", exist_ok=True)

    for file in uploaded_files:

        try:

            temp_path = os.path.join(
                "uploaded_docs",
                file.name
            )

            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())

            # Try normal PDF extraction first
            loader = PyPDFLoader(temp_path)

            pages = loader.load()

            valid_text = False

            for page in pages:

                if page.page_content.strip():

                    valid_text = True

                    page.metadata["source"] = file.name

                    documents.append(page)

            # If no text found → OCR
            if not valid_text:

                images = convert_from_path(temp_path)

                for i, image in enumerate(images):

                    text = pytesseract.image_to_string(image)

                    if text.strip():

                        doc = Document(
                            page_content=text,
                            metadata={
                                "source": file.name,
                                "page": i + 1
                            }
                        )

                        documents.append(doc)

        except Exception as e:

            print(f"Error processing {file.name}: {e}")

    return documents
