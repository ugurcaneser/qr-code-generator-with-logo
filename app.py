import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="QR Code Generator (with Logo)", layout="centered")
st.title("QR Code Generator with Logo")

st.markdown("""
With this app, you can generate a QR code from any text or link and add your logo to its center.
""")

qr_text = st.text_input("QR Code Content (Text or URL)")
logo_file = st.file_uploader("Upload Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
qr_btn = st.button("Generate QR Code")

if qr_btn and qr_text:
    # Generate QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
        # Do not set version, let qrcode auto-select a valid version
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    if logo_file is not None:
        logo = Image.open(logo_file)
        # Resize logo
        qr_width, qr_height = img_qr.size
        factor = 4  # Logo covers about 1/4 of the QR code
        logo_size = qr_width // factor
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        # Paste logo at the center
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img_qr.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    buf = io.BytesIO()
    img_qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Generated QR Code", use_container_width=True)
    st.download_button(
        label="Download QR Code",
        data=buf.getvalue(),
        file_name="qr_code.png",
        mime="image/png"
    )
