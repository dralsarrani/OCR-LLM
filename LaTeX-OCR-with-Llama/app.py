import streamlit as st 
import base64
from PIL import Image 
from groq import Groq

st.set_page_config( 
    page_title= 'LaTeX OCR with Llama 4 Scout',
    page_icon= '📝', 
    layout= 'centered', 
    initial_sidebar_state= 'expanded',
)

st.title('📝 LaTeX OCR with Llama 4 Scout')

col1, col2 = st.columns([6,1])
with col2:
    if st.button('Clear'):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun() 

st.markdown('<p style="margin-top: -20px;">Extract LaTeX from images using Groq + Llama 4 Scout!</p>',
unsafe_allow_html=True
)
st.markdown('---')

with st.sidebar:
    st.header('Upload your Image')
    uploaded_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg'])
    groq_api_key = st.text_input('Groq API Key', type='password')
    
    if groq_api_key:
        client = Groq(api_key=groq_api_key)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption= 'Uploaded Image', use_container_width=True)

        if st.button('Extract LaTeX', type= 'primary'):
            if not groq_api_key:
                st.error("Please enter your Groq API Key in the sidebar.")
            else:
                with st.spinner('Extracting LaTeX with Llama 4 Scout...'):
                    try:
                        # Convert image to base64 for Groq API
                        img_bytes = uploaded_file.getvalue()
                        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                        img_data_url = f"data:image/jpeg;base64,{img_b64}"

                        response = client.chat.completions.create(
                            model='meta-llama/llama-4-scout-17b-16e-instruct',
                            messages=[{
                                'role': 'user',
                                'content': [
                                    {"type": "text", "text": """Understand the mathematical equation in the provided image and output the corresponding LaTeX code.
Here are some guidelines you MUST follow or you will be penalized:
- NEVER include any additional text or explanation.
- DON'T add dollar signs ($) around the LaTeX code.
- DO NOT extract simplified versions of the equation.
- NEVER add documentclass, packages or begindocument.
- DO NOT explain the symbols used in the equation.
- Output only the LaTeX code corresponding to the mathematical equation in the image."""},
                                    {"type": "image_url", "image_url": {"url": img_data_url}}
                                ]
                            }],

                        )
                        st.session_state['ocr_result'] = response.choices[0].message.content
                    except Exception as e: 
                        import traceback
                        st.error(f"Error processing image: {str(e)}")
                        st.code(traceback.format_exc())

if 'ocr_result' in st.session_state:
    st.markdown('### LaTeX Code')
    st.code(st.session_state['ocr_result'], language='latex')

    st.markdown('### LaTeX Rendered') 

    cleaned_latex = st.session_state['ocr_result'].replace(r"\[","").replace(r"\]","") 
    st.latex(cleaned_latex)

else: 
    st.info("Upload an image and click 'Extract LaTeX' to see the result here.")

st.markdown("---")
