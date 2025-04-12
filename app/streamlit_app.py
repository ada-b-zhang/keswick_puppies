import streamlit as st
import os
from PIL import Image
from tf_style_transfer import stylize_image

PET_DIR = "app/pets"
STYLE_DIR = "app/styles"
OUTPUT_DIR = "app/output"

st.set_page_config(layout="wide")

# 🎨 Centered Title & Description
st.markdown("<h1 style='text-align: center;'>Keswick Puppies Style Transfer 🐕🐶🐶</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center; font-size: 18px;'>
    Welcome to Keswick Puppies, a style transfer app that turns photos of puppies Lucy, Gracie, and Frankie into stylized works of art using famous painting styles or your own uploads.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("### &nbsp;") 

# 🧱 Layout: [pet] [space] [style] [space] [output]
col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

# 🐶 PET SELECTION
with col1:
    st.header("1. Pick a Puppy!")
    pet_names = [d for d in os.listdir(PET_DIR) if os.path.isdir(os.path.join(PET_DIR, d))]
    selected_pet = st.selectbox("Pet:", pet_names)

    pet_folder = os.path.join(PET_DIR, selected_pet)
    pet_imgs = [f for f in os.listdir(pet_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    selected_img = st.selectbox("Photo:", pet_imgs)
    pet_img_path = os.path.join(pet_folder, selected_img)
    st.image(pet_img_path, caption="Your Pet", use_container_width=True)

# 🎨 STYLE SELECTION
with col2:
    st.header("2. Pick a Style!")
    style_option = st.radio("Style source:", ["Pick from existing", "Upload your own"])

    style_img_pil = None
    if style_option == "Pick from existing":
        available_styles = [f for f in os.listdir(STYLE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        selected_style = st.selectbox("Choose a style:", available_styles)
        style_img_path = os.path.join(STYLE_DIR, selected_style)
        style_img_pil = Image.open(style_img_path)
        st.image(style_img_pil, caption="Selected Style", use_container_width=True)
    else:
        style_file = st.file_uploader("Upload style image", type=["jpg", "jpeg", "png"])
        if style_file:
            style_img_pil = Image.open(style_file)
            st.image(style_img_pil, caption="Uploaded Style", use_container_width=True)

# 🖼️ OUTPUT
with col3:
    st.header("3. Stylize!")
    if style_img_pil and st.button("Generate Portrait"):
        output_path = os.path.join(OUTPUT_DIR, f"{selected_pet}_{selected_img.split('.')[0]}_styled.jpg")
        with st.spinner("Painting your pet..."):
            final_path = stylize_image(pet_img_path, style_img_pil, output_path)

        st.success("Done!")
        st.image(final_path, caption="Stylized Portrait", use_container_width=True)
        st.download_button("Download Image", open(final_path, "rb"), file_name=os.path.basename(final_path))
