import streamlit as st
import qrcode
from PIL import Image
import io

# --- QR Code Generation Function ---
def generate_qr_code(data):
    """Generates a QR code and returns it as a BytesIO buffer."""
    if not data:
        return None
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# --- Streamlit App UI ---
st.set_page_config(page_title="QR Code Generator", layout="centered")

st.title("QR Code Generator generating_qr_codes_with_python_and_streamlit/2_app_ui.webp")

st.write("Enter the text or URL you want to encode into a QR code below.")

# Input field for the data
data_to_encode = st.text_input("Enter data:", "https://www.google.com")

if st.button("Generate QR Code"):
    if data_to_encode:
        # Generate the QR code
        qr_code_image = generate_qr_code(data_to_encode)

        # Display the generated QR code
        st.image(qr_code_image, caption="Here is your QR Code", use_column_width=True)

        # Provide a download button
        st.download_button(
            label="Download QR Code",
            data=qr_code_image,
            file_name="qr_code.png",
            mime="image/png"
        )
    else:
        st.warning("Please enter some data to generate a QR code.")