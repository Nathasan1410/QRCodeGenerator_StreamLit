import streamlit as st
import qrcode
from PIL import Image
import io

# --- QR Code Generation Function ---
def generate_qr_code(data, fill_color="black", back_color="white"):
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
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Save image to a buffer to be displayed in Streamlit
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)  # Rewind the buffer to the beginning
    return buf

# --- Floating Button CSS and HTML ---
def add_floating_button(url):
    """Adds a responsive floating button to the bottom right of the page."""
    button_style = """
    <style>
        .floating-button {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 40px;
            right: 40px;
            background-color: #007bff;
            color: white;
            border-radius: 50px;
            text-align: center;
            font-size: 24px;
            box-shadow: 2px 2px 3px #999;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .floating-button:hover {
            background-color: #0056b3;
            transform: scale(1.1);
            color: white;
        }
        
        /* Media query for mobile responsiveness */
        @media screen and (max-width: 768px) {
            .floating-button {
                width: 50px;
                height: 50px;
                bottom: 20px;
                right: 20px;
                font-size: 20px;
            }
        }
    </style>
    """
    # Remember to change the link to your actual portfolio!
    button_html = f'<a href="{url}" target="_blank" class="floating-button">🌐</a>'
    
    st.markdown(button_style, unsafe_allow_html=True)
    st.markdown(button_html, unsafe_allow_html=True)


# --- Streamlit App UI ---
st.set_page_config(page_title="QR Code Generator", layout="centered")

# Add the floating button. IMPORTANT: Change the URL to your portfolio!
add_floating_button("https://your-portfolio-url.com")

st.title("QR Code Generator")
st.write("Enter the text or URL you want to encode into a QR code below.")

# --- Session State to hold the generated image ---
if 'qr_code_image' not in st.session_state:
    st.session_state.qr_code_image = None

# Input field for the data
data_to_encode = st.text_input("Enter data:", "https://streamlit.io")

# --- UI for Customization in Sidebar ---
# On mobile, this sidebar will collapse into a menu.
st.sidebar.header("Customize Your QR Code")
fill_color = st.sidebar.color_picker("Fill color", "#000000")
back_color = st.sidebar.color_picker("Background color", "#FFFFFF")

# Generate Button
if st.button("Generate QR Code"):
    if data_to_encode:
        # Generate the QR code and store it in session state
        st.session_state.qr_code_image = generate_qr_code(data_to_encode, fill_color, back_color)
    else:
        st.warning("Please enter some data to generate a QR code.")
        st.session_state.qr_code_image = None

# --- Display and Download Area ---
if st.session_state.qr_code_image:
    st.image(
        st.session_state.qr_code_image,
        caption="Here is your QR Code",
        use_container_width=True
    )

    # Provide a download button
    st.download_button(
        label="Download QR Code",
        data=st.session_state.qr_code_image,
        file_name="qr_code.png",
        mime="image/png"
    )