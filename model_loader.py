import os
import cv2
import numpy as np
import streamlit as st
import datetime
from Styles import Style
from tensorflow.keras.models import load_model
import time

class Models:
    @staticmethod
    def load_accident_model():
        return load_model('Accident_Model.h5')

    @staticmethod
    def load_severity_model():
        return load_model('Severity_Model.h5')
