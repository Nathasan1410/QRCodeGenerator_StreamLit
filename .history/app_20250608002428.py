import streamlit as st

import qrcode

from PIL import Image

import io



# --- App Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---

st.set_page_config(

    page_title="QR Code Generator",

    layout="centered",

    initial_sidebar_state="expanded"

)



# --- Hard-coded CSS for VS Code Dark+ Theme ---

# This block of CSS will be injected into the app to force the dark theme.

def apply_dark_theme():

    dark_theme_css = """

        <style>

        /* Main page background */

        .stApp {

            background-color: #1E1E1E;

        }



        /* Main text color */

        body, .stApp, .stButton>button, .stTextInput>div>div>input, .stSelectbox>div>div, .stSlider>div>div, .stFileUploader>div, .stDownloadButton>a {

            color: #D4D4D4;

            font-family: monospace;

        }

       

        /* Titles and headers */

        h1, h2, h3, h4, h5, h6 {

            color: #D4D4D4;

            font-family: monospace;

        }



        /* Sidebar background */

        [data-testid="stSidebar"] {

            background-color: #252526;

        }

       

        /* Sidebar text */

        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stSlider {

            color: #D4D4D4;

        }



        /* Widget backgrounds (text input, buttons) */

        .stTextInput>div>div>input, .stSelectbox>div>div, .stFileUploader>div {

            background-color: #3C3C3C;

            border-color: #3C3C3C;

        }



        /* Primary button style */

        .stButton>button {

            background-color: #3B82F6;

            color: white;

            border: none;

        }

        .stButton>button:hover {

            background-color: #2563EB;

            color: white;

            border: none;

        }

        .stDownloadButton>a {

            background-color: #006400; /* A dark green for download */

            color: white !important;

            border: none;

            padding: 0.5rem 1rem;

            border-radius: 0.25rem;

            text-decoration: none;

            display: inline-block;

            text-align: center;

        }

        .stDownloadButton>a:hover {

            background-color: #008000;

        }

        </style>

    """

    st.markdown(dark_theme_css, unsafe_allow_html=True)



# --- Apply the theme (Now that page config is set) ---

apply_dark_theme()



# --- QR Code Generation Function ---

def generate_qr_code(data, error_correction, box_size, border, fill_color, back_color):

    if not data: return None

    error_map = {'Low (L)': qrcode.constants.ERROR_CORRECT_L, 'Medium (M)': qrcode.constants.ERROR_CORRECT_M, 'Quartile (Q)': qrcode.constants.ERROR_CORRECT_Q, 'High (H)': qrcode.constants.ERROR_CORRECT_H}

    qr = qrcode.QRCode(version=1, error_correction=error_map[error_correction], box_size=box_size, border=border)

    qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    buf = io.BytesIO()

    img.save(buf, format="PNG")

    buf.seek(0)

    return buf



# --- Floating Button ---

def add_floating_button(url):

    button_style = """

    <style>

        .floating-button {

            position: fixed; width: 60px; height: 60px; bottom: 40px; right: 40px;

            background-color: #3B82F6; color: white; border-radius: 50px; text-align: center;

            font-size: 24px; box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4); z-index: 100;

            display: flex; align-items: center; justify-content: center; text-decoration: none;

            transition: all 0.3s ease;

        }

        .floating-button:hover { background-color: #2563EB; transform: scale(1.1); color: white; }

        @media screen and (max-width: 768px) {

            .floating-button { width: 50px; height: 50px; bottom: 20px; right: 20px; font-size: 20px; }

        }

    </style>

    """

    button_html = f'<a href="{url}" target="_blank" class="floating-button">🌐</a>'

    st.markdown(button_html, unsafe_allow_html=True)



# --- Main Streamlit App UI ---

add_floating_button("https://your-portfolio-url.com")

st.title("QR Code Generator `// Dark+`")

st.write("Enter data to encode and customize your QR code in the sidebar.")



if 'qr_code_image' not in st.session_state: st.session_state.qr_code_image = None



st.sidebar.header("`Settings`")

col1, col2 = st.sidebar.columns(2)

fill_color = col1.color_picker("Fill color", "#FFFFFF")

back_color = col2.color_picker("BG color", "#1E1E1E")



st.sidebar.subheader("`Advanced`")

error_correction = st.sidebar.select_slider('Error Correction', options=['Low (L)', 'Medium (M)', 'Quartile (Q)', 'High (H)'], value='Low (L)')

box_size = st.sidebar.slider("Box Size", min_value=1, max_value=20, value=10)

border = st.sidebar.slider("Border", min_value=1, max_value=10, value=4)



data_to_encode = st.text_input("Data to encode", "https://streamlit.io", label_visibility="collapsed")



if st.button("Generate QR Code", use_container_width=True, type="primary"):

    if data_to_encode:

        st.session_state.qr_code_image = generate_qr_code(data_to_encode, error_correction, box_size, border, fill_color, back_color)

    else:

        st.warning("Please enter some data to generate a QR code.")

        st.session_state.qr_code_image = None



if st.session_state.qr_code_image:

    st.image(st.session_state.qr_code_image, use_container_width=True)

    st.download_button(label="Download as PNG", data=st.session_state.qr_code_image, file_name="qr_code.png", mime="image/png", use_container_width=True)



