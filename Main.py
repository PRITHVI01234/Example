import os
import cv2
import numpy as np
import streamlit as st
import datetime
from Styles import Style
from tensorflow.keras.models import load_model
import time
from UI import UIComponents
from video import VideoProcessor
from model_loader import Models
from log_writer import LogHandler


# Streamlit app
def main():
    # UI setup
    UIComponents.apply_background()
    UIComponents.apply_sidebar_style()

    # Load models
    accident_model = Models.load_accident_model()
    severity_model = Models.load_severity_model()

    # UI components
    st.markdown("<h1 class='main-title'>RoadGuard.V.1</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-heading'>Accident Detection and Severity Assessment</h2>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Choose video files", accept_multiple_files=True, type=["mp4", "avi"])
    st.sidebar.title("Log:")
    log_file_path = "log.txt"

    if st.sidebar.button("Clear Log"):
        LogHandler.clear_log(log_file_path)

    start_video_index = 1

    if uploaded_files:
        video_placeholders = [st.empty() for _ in range(len(uploaded_files))]
        VideoProcessor.process_videos(uploaded_files, video_placeholders, log_file_path, start_video_index, accident_model, severity_model)

    with open(log_file_path, 'r') as file:
        log_contents = file.readlines()
        for log_entry in log_contents:
            st.sidebar.text(log_entry.strip())

if __name__ == "__main__":
    main()