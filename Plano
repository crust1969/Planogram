import streamlit as st
import pdfplumber
import cv2
import numpy as np
from PIL import Image
import io

# Funktion zum Extrahieren von Bildern aus dem PDF
def extract_images_from_pdf(pdf_path):
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for img in page.images:
                x0, y0, x1, y1 = img['x0'], img['y0'], img['x1'], img['y1']
                page_image = page.to_image()
                cropped_image = page_image.crop((x0, y0, x1, y1))
                images.append(cropped_image)
    return images

# Funktion zur Verarbeitung der Bilder mit OpenCV
def process_images(images):
    processed_images = []
    for image in images:
        # Konvertieren Sie das Bild in ein OpenCV-Format
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        np_img = np.frombuffer(img_byte_arr, np.uint8)
        cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        
        # Anwenden von Bildverarbeitungstechniken
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Finden von Konturen
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            product_image = cv_img[y:y+h, x:x+w]
            processed_images.append(product_image)
    return processed_images
# Streamlit-Anwendung
st.title("Planogram Image Extraction and Optimization")

# Datei-Upload
uploaded_file = st.file_uploader("Upload a PDF document containing a planogram", type="pdf")

if uploaded_file is not None:
    # Speichern der hochgeladenen Datei
    with open("uploaded_planogram.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extrahieren der Bilder aus dem PDF
    extracted_images = extract_images_from_pdf("uploaded_planogram.pdf")
    
    # Verarbeiten der extrahierten Bilder
    processed_images = process_images(extracted_images)
    
    # Anzeigen der extrahierten Produktbilder
    st.header("Extracted Product Images")
    for i, img in enumerate(processed_images):
        st.image(img, caption=f"Product Image {i+1}", use_column_width=True)

# Hinweis: Die Funktionalität zum Vergleichen der Bilder mit einer Datenbank von Produktmaßen und zur Optimierung der Regalplatzierung ist in diesem Beispiel nicht implementiert.
# Sie können diese Anwendung erweitern, indem Sie die erforderliche Logik für den Datenbankvergleich und die Optimierung hinzufügen.
