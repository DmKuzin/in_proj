import streamlit as st
from pathlib import Path
import PIL
from ultralytics import YOLO

# Setting page layout
st.set_page_config(
    page_icon=":red_car:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Introduction
st.title("IN - match 3 solver")

# Title


# Sidebar
st.sidebar.header("Model Configuration")

# Model Options
model_type = st.sidebar.radio(
    "--------", ['Object Detection'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

if model_type == 'Object Detection':
    model_path = Path('model/yolov8n.pt')

# Load Pre-trained ML Model
try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

source_img = None
source_img = st.sidebar.file_uploader(
    "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

col1, col2 = st.columns(2)

with col1:
    try:
        if source_img is None:
            default_image_path = str('def_image/def_image.jpg')
            default_image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption="Default Image",
                     use_column_width=True)
        else:
            uploaded_image = PIL.Image.open(source_img)
            st.image(source_img, caption="Uploaded Image",
                     use_column_width=True)
    except Exception as ex:
        st.error("Error occurred while opening the image.")
        st.error(ex)

with col2:
    if source_img is None:

        default_detected_image_path = str('def_image/def_image.jpg')
        default_detected_image = PIL.Image.open(
            default_detected_image_path)
        st.image(default_detected_image_path, caption='Detected Image',
                 use_column_width=True)
    else:
        if st.sidebar.button('Detect Objects'):
            res = model.predict(uploaded_image,
                                conf=confidence
                                )
            boxes = res[0].boxes
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption='Detected Image',
                     use_column_width=True)
            try:
                with st.expander("Detection Results"):
                    for box in boxes:
                        st.write(box.data)
            except Exception as ex:
                st.write("No image is uploaded yet!")