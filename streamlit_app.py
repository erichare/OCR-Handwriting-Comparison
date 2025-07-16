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


def main():
    # Load external CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(f'<h1 style="color:#09a5ff">OCR Handwriting Comparison <img src="data:image/png;base64,{base64_image}" alt="logo" width="30"></h1>', unsafe_allow_html=True)
    st.sidebar.header("OCR Algorithm")
    with st.sidebar.expander("Instructions"):
        st.markdown("""
        1. Select OCR Algorithm  
        2. Select comparison mode  
        3. Upload two images  
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

        # Image upload section with columns for better aesthetics
        image_extensions = ["png", "jpg", "jpeg", "webp"]
        col1, col2 = st.columns(2)

        file_path_1 = None
        file_path_2 = None

        with col1:
            st.subheader("Image 1")
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

                # Delete temporary files
                os.unlink(file_path_1)
                os.unlink(file_path_2)


if __name__ == "__main__":
    main()
