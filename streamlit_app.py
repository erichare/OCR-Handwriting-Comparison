import base64
import os
from tempfile import NamedTemporaryFile

import streamlit as st

import pytesseract_letter
import pytesseract_word
import easyocr_letter
import easyocr_word


# Path to your local image file (replace with your actual path)
image_path = os.path.join(os.path.dirname(__file__), "images", "omniacsdao_logo.png")

# Read the image file in binary mode
with open(image_path, "rb") as image_file:
    # Encode the binary data to Base64 and decode to a string
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Default sample images paths - replace with your actual sample images
DEFAULT_IMAGE_1 = os.path.join(os.path.dirname(__file__), "images", "Author0.png")
DEFAULT_IMAGE_2 = os.path.join(os.path.dirname(__file__), "images", "Author1.png")


def load_default_images():
    """Load default sample images if they exist"""
    default_images = {}
    
    if os.path.exists(DEFAULT_IMAGE_1):
        default_images['image1'] = DEFAULT_IMAGE_1
    
    if os.path.exists(DEFAULT_IMAGE_2):
        default_images['image2'] = DEFAULT_IMAGE_2
    
    return default_images


def ocr_comparison_tab():
    """Main OCR comparison functionality"""
    st.sidebar.header("OCR Algorithm")
    with st.sidebar.expander("Instructions"):
        st.markdown("""
        1. Select OCR Algorithm  
        2. Select comparison mode  
        3. Upload two images (or use default samples)
        4. Click the button to create a juxtaposed collage
        """)
    
    options = st.sidebar.selectbox("Select the OCR Algorithm",
                                   ["Pytesseract", "EasyOCR"])

    if options:
        st.header(f"{options} Algorithm")

        mode = st.radio("Select comparison mode",
                        ["letters", "words"], horizontal=True)

        # Determine the module based on options and mode
        if options == "Pytesseract":
            if mode == "letters":
                module = pytesseract_letter
            else:
                module = pytesseract_word
        elif options == "EasyOCR":
            if mode == "letters":
                module = easyocr_letter
            else:
                module = easyocr_word

        extract_func = module.extract_text_and_boxes
        create_func = module.create_juxtaposed_collage
        collage_filename = f"juxtaposed_{mode[:-1]}_collage_final.png"  # letters -> letter, words -> word
        button_label = f"Create juxtaposed {mode[:-1]} collage"
        success_msg = f"Juxtaposed {mode[:-1]} collage created successfully!"

        # Load default images
        default_images = load_default_images()
        
        # Image upload section with columns for better aesthetics
        image_extensions = ["png", "jpg", "jpeg", "webp"]
        col1, col2 = st.columns(2)

        # Initialize file paths
        file_path_1 = None
        file_path_2 = None

        with col1:
            st.subheader("Image 1")
            
            # Check if we should use default image
            use_default_1 = st.checkbox("Use sample image 1", value=True, key=f"default_1_{options}_{mode}")
            if use_default_1 and 'image1' in default_images:
                st.image(default_images['image1'], use_column_width=True)
                file_path_1 = default_images['image1']
            else:
                image_path_1 = st.file_uploader("Upload image 1", type=image_extensions, key="uploader1")
                if image_path_1:
                    show_image_1 = st.checkbox("Show image 1", key=f"checkbox_1_{options}_{mode}")
                    if show_image_1:
                        st.image(image_path_1, use_column_width=True)
                    with NamedTemporaryFile(delete=False) as temp_file_1:
                        temp_file_1.write(image_path_1.getvalue())
                        file_path_1 = temp_file_1.name

        with col2:
            st.subheader("Image 2")
            
            # Check if we should use default image
            use_default_2 = st.checkbox("Use sample image 2", value=True, key=f"default_2_{options}_{mode}")
            
            if use_default_2 and 'image2' in default_images:
                st.image(default_images['image2'], use_column_width=True)
                file_path_2 = default_images['image2']
            else:
                image_path_2 = st.file_uploader("Upload image 2", type=image_extensions, key="uploader2")
                if image_path_2:
                    show_image_2 = st.checkbox("Show image 2", key=f"checkbox_2_{options}_{mode}")
                    if show_image_2:
                        st.image(image_path_2, use_column_width=True)
                    with NamedTemporaryFile(delete=False) as temp_file_2:
                        temp_file_2.write(image_path_2.getvalue())
                        file_path_2 = temp_file_2.name

        if file_path_1 and file_path_2:
            st.write("")  # Add some space
            if st.button(button_label, use_container_width=True):
                with st.spinner(f"Creating {mode[:-1]} collage..."):
                    image_data_1 = extract_func(file_path_1)
                    image_data_2 = extract_func(file_path_2)
                    create_func(image_data_1, image_data_2, file_path_1, file_path_2)
                st.success(success_msg)

                # Show juxtaposed collage image
                st.subheader("Resulting Collage")
                st.image(collage_filename, use_column_width=True)

                # Delete temporary files (only if they're not default images)
                if file_path_1 != default_images.get('image1') and file_path_1.startswith('/tmp'):
                    os.unlink(file_path_1)
                if file_path_2 != default_images.get('image2') and file_path_2.startswith('/tmp'):
                    os.unlink(file_path_2)


def video_analysis_tab():
    """Static walkthrough video tab"""
    st.header("How to Use OCR Comparison Tool")
    
    # Path to walkthrough video - replace with your actual video path
    video_path = os.path.join(os.path.dirname(__file__), "images", "ocr_handwriting_walkthrough_20250718.mp4")
    
    # Check if video exists and display it
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        # Placeholder for when video doesn't exist yet
        st.info("📹 Walkthrough video will be displayed here once uploaded to `videos/walkthrough.mp4`")
        
        # Add a placeholder video container
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 100px; text-align: center; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #666;">Walkthrough Video</h3>
            <p style="color: #888;">Step-by-step guide to using the OCR comparison tool</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("What You'll Learn")
    st.markdown("""
    📋 **Step-by-step walkthrough covering:**
    
    - How to select the appropriate OCR algorithm
    - Choosing between letter and word comparison modes
    - Uploading and comparing handwriting samples
    - Interpreting the juxtaposed collage results
    - Best practices for forensic handwriting analysis
    """)
    
    st.subheader("Quick Start Guide")
    with st.expander("📖 Text Instructions"):
        st.markdown("""
        1. **Select OCR Algorithm**: Choose between Pytesseract or EasyOCR in the sidebar
        2. **Choose Comparison Mode**: Select 'letters' for character-level analysis or 'words' for word-level analysis
        3. **Upload Images**: Use the sample images or upload your own handwriting samples
        4. **Generate Collage**: Click the button to create a side-by-side comparison
        5. **Analyze Results**: Review the highlighted text regions and compare similarities/differences
        """)
    
    st.info("💡 **Tip**: Start with the sample images to see how the tool works, then try your own handwriting samples!")


def main():
    # Load external CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Title in sidebar
    st.sidebar.markdown(f'<h1 style="color:#09a5ff">OCR Handwriting Comparison <img src="data:image/png;base64,{base64_image}" alt="logo" width="30"></h1>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["OCR Comparison", "Video Tutorial"])
    
    with tab1:
        ocr_comparison_tab()
    
    with tab2:
        video_analysis_tab()

    # Footer in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.8em; color: #666; line-height: 1.3;">
        Advancing forensic science as a public good — powered by $IACS.<br>
        <strong>Support:</strong> 0x46e69Fa9059C3D5F8933CA5E993158568DC80EBf (Base)
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
