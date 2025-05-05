import streamlit as st
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io
import pandas as pd

def extract_images_from_pdf(pdf_file):
    images = []
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image.convert("RGB"))
    return images

def detect_products(image):
    # Dummy-Erkennung: Schneidet die Seiten in 4 gleich große Kacheln
    width, height = image.size
    detected = []
    for i in range(2):
        for j in range(2):
            crop = image.crop((i*width/2, j*height/2, (i+1)*width/2, (j+1)*height/2))
            detected.append(crop)
    return detected

def match_products_to_database(detected_images, product_db):
    # Dummy-Zuordnung: Alle Produktbilder dem ersten Eintrag zuordnen
    matched = []
    for img in detected_images:
        matched.append({
            "Produkt": product_db.iloc[0]["Produkt"],
            "Breite_cm": product_db.iloc[0]["Breite_cm"],
            "Höhe_cm": product_db.iloc[0]["Höhe_cm"],
            "Bild": img
        })
    return matched

def calculate_placement(matched_products, regal_breite_cm, regal_hoehe_cm):
    total_breite = 0
    plazierte = []
    for p in matched_products:
        if total_breite + p["Breite_cm"] <= regal_breite_cm:
            plazierte.append(p)
            total_breite += p["Breite_cm"]
    return plazierte

# --- Streamlit UI ---
st.title("Planogram Optimierer")

uploaded_pdf = st.file_uploader("Lade ein Planogramm (PDF)", type=["pdf"])
uploaded_csv = st.file_uploader("Lade Produktdatenbank (CSV)", type=["csv"])

regal_breite = st.number_input("Regalbreite (cm)", min_value=10, max_value=500, value=100)
regal_hoehe = st.number_input("Regalhöhe (cm)", min_value=10, max_value=500, value=50)

if uploaded_pdf and uploaded_csv:
    product_db = pd.read_csv(uploaded_csv)
    images = extract_images_from_pdf(uploaded_pdf)

    all_detected = []
    for img in images:
        all_detected.extend(detect_products(img))

    matched = match_products_to_database(all_detected, product_db)
    platzierung = calculate_placement(matched, regal_breite, regal_hoehe)

    st.header("Optimale Platzierung")
    for i, p in enumerate(platzierung):
        st.image(p["Bild"], caption=f"{p['Produkt']} ({p['Breite_cm']}x{p['Höhe_cm']} cm)", width=150)
