import xml.etree.ElementTree as ET
from PIL import Image
import fitz  # PyMuPDF
import io
import base64

def extract_photo_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Check if this is Aadhaar OKY format
    if root.tag == 'OKY':
        # Extract photo from 'i' attribute (Base64 encoded)
        photo_attr = root.get('i')
        if photo_attr:
            try:
                photo_data = base64.b64decode(photo_attr)
                return Image.open(io.BytesIO(photo_data))
            except Exception as e:
                print(f"Error decoding Aadhaar photo: {e}")
                return None
    else:
        # Fallback to Pht element for other XML formats
        photo_elem = root.find('.//Pht')
        if photo_elem is not None:
            photo_data = base64.b64decode(photo_elem.text)
            return Image.open(io.BytesIO(photo_data))
    
    return None

def extract_photo_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image['image']
            return Image.open(io.BytesIO(image_bytes))
    return None 