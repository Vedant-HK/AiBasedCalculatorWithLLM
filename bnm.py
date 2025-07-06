import streamlit as st
import numpy as np
import PIL.Image
import google.generativeai as genai
import os
from streamlit_drawable_canvas import st_canvas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def set_streamlit_config():
    st.set_page_config(page_title='Virtual Math Board', layout="wide")
    st.markdown("""
        <style>
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        .block-container { padding-top: 0rem; }
        </style>
    """, unsafe_allow_html=True)
    st.title("📝 Virtual Math Board")

def analyze_with_ai(image=None, text=None):
    if image is None and not text:
        return "No input detected. Please provide an image, draw something, or enter text."
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = "Analyze the input and solve the mathematical problem."
    if text:
        response = model.generate_content([prompt, text])
    else:
        img_pil = PIL.Image.fromarray(image)
        response = model.generate_content([prompt, img_pil])
    
    return response.text

def main():
    set_streamlit_config()
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        st.markdown("### Draw using your mouse or upload an image")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        
        image = None
        if uploaded_image is not None:
            image = PIL.Image.open(uploaded_image)
            image = np.array(image)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        else:
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=5,
                stroke_color="#000000",
                background_color="#FFFFFF",
                height=500,
                width=800,
                drawing_mode="freedraw",
                key="canvas"
            )
            if canvas_result.image_data is not None:
                image = canvas_result.image_data.astype(np.uint8)
    
    with col2:
        st.markdown("### Options")
        text_input = st.text_area("Or enter a word problem here:")

        if st.button("Clear Board 🧹"):
            st.rerun()
        
        if st.button("Analyze with AI 🤖"):
            if uploaded_image is not None or (canvas_result and canvas_result.image_data is not None) or text_input:
                result = analyze_with_ai(image=image, text=text_input)
                st.write("**Result:**", result)
            else:
                st.write("Please upload an image, draw an equation, or enter a word problem.")

if __name__ == "__main__":
    main()
