import streamlit as st
import qrcode
from PIL import Image
import io

# --- App Configuration and Theming ---
# This is where we set the VS Code Dark+ theme.
# We define the primary color, background, and text colors.
st.set_page_config(
    page_title="QR Code Generator",
    layout="centered",
    initial_sidebar_state="expanded",
    theme={
        "base": "dark",
        "primaryColor": "#3B82F6", # A nice blue for widgets
        "backgroundColor": "#1E1E1E", # VS Code's main background
        "secondaryBackgroundColor": "#252526", # VS Code's sidebar color
        "textColor": "#D4D4D4", # VS Code's primary text color
        "font": "monospace" # Use a monospace font for a code-editor feel
    }
)


# --- QR Code Generation Function ---
def generate_qr_code(data, error_correction, box_size, border, fill_color, back_color):
    """Generates a QR code and returns it as a BytesIO buffer."""
    if not data:
        return None
        
    error_map = {
        'Low (L)': qrcode.constants.ERROR_CORRECT_L,
        'Medium (M)': qrcode.constants.ERROR_CORRECT_M,
        'Quartile (Q)': qrcode.constants.ERROR_CORRECT_Q,
        'High (H)': qrcode.constants.ERROR_CORRECT_H
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_map[error_correction],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# --- Floating Button CSS and HTML (Styled for Dark Theme) ---
def add_floating_button(url):
    """Adds a responsive floating button, styled for the dark theme."""
    button_style = """
    <style>
        .floating-button {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 40px;
            right: 40px;
            background-color: #3B82F6; /* Matches primaryColor */
            color: white;
            border-radius: 50px;
            text-align: center;
            font-size: 24px;
            box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4);
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .floating-button:hover {
            background-color: #2563EB; /* A slightly lighter blue on hover */
            transform: scale(1.1);
            color: white;
        }
        
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
    button_html = f'<a href="{url}" target="_blank" class="floating-button">🌐</a>'
    
    st.markdown(button_style, unsafe_allow_html=True)
    st.markdown(button_html, unsafe_allow_html=True)

# --- Main Streamlit App UI ---
add_floating_button("https://your-portfolio-url.com") # Don't forget to change this!

st.title("QR Code Generator `// Dark+`")
st.write("Enter data to encode and customize your QR code in the sidebar.")

# --- Session State Management ---
if 'qr_code_image' not in st.session_state:
    st.session_state.qr_code_image = None

# --- Sidebar for Customization ---
st.sidebar.header("`Settings`")

# Use columns for a cleaner layout in the sidebar
col1, col2 = st.sidebar.columns(2)
# Sensible defaults for a dark theme
fill_color = col1.color_picker("Fill color", "#FFFFFF")
back_color = col2.color_picker("BG color", "#1E1E1E")

st.sidebar.subheader("`Advanced`")
error_correction = st.sidebar.select_slider(
    'Error Correction',
    options=['Low (L)', 'Medium (M)', 'Quartile (Q)', 'High (H)'],
    value='Low (L)'
)
box_size = st.sidebar.slider("Box Size", min_value=1, max_value=20, value=10)
border = st.sidebar.slider("Border", min_value=1, max_value=10, value=4)

# --- Main Area for Input and Generation ---
data_to_encode = st.text_input("Data to encode", "https://streamlit.io", label_visibility="collapsed")

if st.button("Generate QR Code", use_container_width=True, type="primary"):
    if data_to_encode:
        st.session_state.qr_code_image = generate_qr_code(
            data_to_encode, error_correction, box_size, border, fill_color, back_color
        )
    else:
        st.warning("Please enter some data to generate a QR code.")
        st.session_state.qr_code_image = None

# --- Display and Download Area ---
if st.session_state.qr_code_image:
    st.image(
        st.session_state.qr_code_image,
        use_container_width=True
    )
    st.download_button(
        label="Download as PNG",
        data=st.session_state.qr_code_image,
        file_name="qr_code.png",
        mime="image/png",
        use_container_width=True
    )
