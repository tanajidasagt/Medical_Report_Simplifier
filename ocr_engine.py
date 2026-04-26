import easyocr
import numpy as np
from PIL import Image

# Initialize the reader (English language)
# It will download the model weights on the first run
reader = easyocr.Reader(['en'])

def extract_text_from_image(image_file):
    """
    Takes an uploaded image file, converts it to a format EasyOCR 
    understands, and returns the extracted text.
    """
    # Convert PIL Image to numpy array
    image = Image.open(image_file)
    image_np = np.array(image)
    
    # Read text from the image
    results = reader.readtext(image_np, detail=0)
    
    # Join the lines into a single block of text
    full_text = " ".join(results)
    return full_text