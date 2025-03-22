from flask import Flask, render_template, request, send_file, Response
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import base64

app = Flask(__name__)

def create_qr_with_text(code):
    # Create the full URL
    url = f"https://world.org/join/{code}"
    
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
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), code, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + (text_height - 30) // 2
    
    # Draw text
    draw.text((text_x, text_y), code, fill='black', font=font)
    
    # Convert to base64 string
    buffered = BytesIO()
    new_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    error = None
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        if code:
            try:
                qr_image = create_qr_with_text(code)
            except Exception as e:
                error = f"Error generating QR code: {str(e)}"
        else:
            error = "Please enter a code"
    
    return render_template('index.html', qr_image=qr_image, error=error)

@app.route('/download/<code>')
def download(code):
    # Create QR code image
    img_str = create_qr_with_text(code)
    img_data = base64.b64decode(img_str)
    img_io = BytesIO(img_data)
    
    return send_file(
        img_io,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'qr_code_{code}.png'
    )

if __name__ == '__main__':
    app.run(debug=True) 