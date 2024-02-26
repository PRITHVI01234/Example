import os
import cv2
import numpy as np
import streamlit as st
import datetime
from Styles import Style
from tensorflow.keras.models import load_model
import time

class UIComponents:
    @staticmethod
    def apply_background():
        adding_gif_background = Style(f"""
        <style>
        .stApp {{
            background-image: url("https://giffiles.alphacoders.com/209/209037.gif");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """)
        adding_gif_background.run()

    @staticmethod
    def apply_sidebar_style():
        sidebar_style = Style("""
        <style>
        .sidebar .sidebar-content {
            font-family: 'Arial', sans-serif; /* Change 'Arial' to the desired font family */
        }
        </style>
        """)
        sidebar_style.run()