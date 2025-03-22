import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_qr_with_text(url, output_filename="qr_code.png"):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to RGB mode if necessary
    if qr_image.mode != 'RGB':
        qr_image = qr_image.convert('RGB')
    
    # Calculate dimensions for the new image with space for text
    qr_width, qr_height = qr_image.size
    text_height = 50  # Height for text area
    new_height = qr_height + text_height
    
    # Create a new white image with space for text
    new_image = Image.new('RGB', (qr_width, new_height), 'white')
    
    # Paste QR code at the top
    new_image.paste(qr_image, (0, 0))
    
    # Add text at the bottom
    draw = ImageDraw.Draw(new_image)
    
    # Try to use Arial font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Get the code ID for display
    code_id = url.split('/')[-1]
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), code_id, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + (text_height - 30) // 2
    
    # Draw text
    draw.text((text_x, text_y), code_id, fill='black', font=font)
    
    # Save the image
    new_image.save(output_filename)
    print(f"QR code with text saved as {output_filename}")

# List of URLs
urls = [
    "https://world.org/join/GRONH35",
    "https://world.org/join/P6YEHN1",
    "https://world.org/join/FWDVWJF",
    "https://world.org/join/98JMYZF",
    "https://world.org/join/NQG86UJ",
    "https://world.org/join/K4FFLZD",
    "https://world.org/join/TH1YPW1",
    "https://world.org/join/Y7PEZI4",
    "https://world.org/join/9QIMPH4",
    "https://world.org/join/OJ0GOYP",
    "https://world.org/join/W07JA1Z",
    "https://world.org/join/9VKFKLA",
    "https://world.org/join/1VP33XO"
]

# Generate QR codes for each URL
for i, url in enumerate(urls, 1):
    code_id = url.split('/')[-1]
    output_filename = f"qr_code_{code_id}.png"
    create_qr_with_text(url, output_filename)
