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

# --- Session State & Query Param Handling for Theme Switching ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark' # Default to dark theme

query_params = st.query_params
if 'theme' in query_params:
    st.session_state.theme = query_params['theme']
    st.query_params.clear()


# --- Hard-coded CSS Themes ---
def apply_dark_theme():
    """Injects CSS for a hard-coded VS Code Dark+ theme."""
    st.markdown("""
        <style>
            .stApp { background-color: #1E1E1E; }
            body, .stApp, .stButton>button, .stTextInput>div>div>input, .stDownloadButton>a { color: #D4D4D4; font-family: monospace; }
            h1 { color: #D4D4D4 !important; font-family: monospace; }
            [data-testid="stSidebar"] { background-color: #252526; }
            .stTextInput>div>div>input { background-color: #3C3C3C; border-color: #3C3C3C; }
            .stButton>button { background-color: #3B82F6; color: white; border: none; }
            .stDownloadButton>a { background-color: #006400; color: white !important; border:none; padding: 0.5rem 1rem; border-radius: 0.25rem; text-decoration: none; display: inline-block; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

def apply_light_theme():
    """Injects CSS for a hard-coded VS Code Light+ theme."""
    st.markdown("""
        <style>
            .stApp { background-color: #FFFFFF; }
            body, .stApp, .stButton>button, .stTextInput>div>div>input, .stDownloadButton>a { color: #333333; font-family: monospace; }
            h1 { color: #00008B !important; font-family: monospace; }
            [data-testid="stSidebar"] { background-color: #F5F5F5; }
            .stTextInput>div>div>input { background-color: #F5F5F5; border-color: #CCCCCC; }
            .stButton>button { background-color: #007ACC; color: white; border: none; }
            .stDownloadButton>a { background-color: #28a745; color: white !important; border:none; padding: 0.5rem 1rem; border-radius: 0.25rem; text-decoration: none; display: inline-block; text-align: center; }
        </style>
    """, unsafe_allow_html=True)


# --- NEW Clickable Title Function with Pill Button ---
def create_clickable_title():
    """Creates a custom title where the theme comment is a clickable, styled button."""
    current_theme = st.session_state.theme
    if current_theme == 'dark':
        next_theme = 'light'
        button_text = '// Dark+'
        bg_color, text_color, hover_bg_color = "#0A0A0A", "#23D18B", "#202020"
    else:
        next_theme = 'dark'
        button_text = '// Light+'
        bg_color, text_color, hover_bg_color = "#E0E0E0", "#005a9e", "#CECECE"

    title_html = f"""
        <style>
            .title-container {{
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: -15px;
            }}
            h1.main-title {{
                font-size: 2.5rem;
                font-weight: 600;
                margin: 0;
            }}
            .theme-switcher-button {{
                display: inline-block;
                padding: 8px 16px;
                background-color: {bg_color};
                color: {text_color} !important;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 1.2rem;
                font-weight: bold;
                text-decoration: none;
                transition: background-color 0.3s ease;
                line-height: 1;
            }}
            .theme-switcher-button:hover {{
                background-color: {hover_bg_color};
                text-decoration: none;
                color: {text_color} !important;
            }}
        </style>
        <div class="title-container">
            <h1 class="main-title">QR Code Generator</h1>
            <a href="?theme={next_theme}" target="_self" class="theme-switcher-button">{button_text}</a>
        </div>
        """
    st.markdown(title_html, unsafe_allow_html=True)

# --- Floating Portfolio Button ---
def add_floating_button(url):
    st.markdown(f"""
    <style>
        .floating-button {{
            position: fixed; width: 60px; height: 60px; bottom: 40px; right: 40px;
            background-color: #007ACC; color: white; border-radius: 50px; text-align: center;
            font-size: 24px; box-shadow: 2px 2px 3px #999; z-index: 100;
            display: flex; align-items: center; justify-content: center; text-decoration: none;
            transition: all 0.3s ease;
        }}
        .floating-button:hover {{ background-color: #005f9e; transform: scale(1.1); }}
        @media screen and (max-width: 768px) {{
            .floating-button {{ width: 50px; height: 50px; bottom: 20px; right: 20px; font-size: 20px; }}
        }}
    </style>
    <a href="{url}" target="_blank" class="floating-button">🌐</a>
    """, unsafe_allow_html=True)

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

# --- Main App UI ---
if st.session_state.theme == 'dark':
    apply_dark_theme()
else:
    apply_light_theme()

add_floating_button("https://your-portfolio-url.com")
create_clickable_title()
st.write("") # Add a little space after the title
st.write("Enter data to encode and customize your QR code in the sidebar.")

if 'qr_code_image' not in st.session_state: st.session_state.qr_code_image = None

st.sidebar.header("`Settings`")
col1, col2 = st.sidebar.columns(2)
fill_color = col1.color_picker("Fill color", "#000000" if st.session_state.theme == 'light' else "#FFFFFF")
back_color = col2.color_picker("BG color", "#FFFFFF" if st.session_state.theme == 'light' else "#1E1E1E")

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