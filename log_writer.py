import os
import cv2
import numpy as np
import streamlit as st
import datetime
from Styles import Style
from tensorflow.keras.models import load_model
import time


class LogHandler:
    @staticmethod
    def write_log_entry(log_file, entry):
        with open(log_file, 'a') as file:
            file.write(entry + '\n')

    @staticmethod
    def clear_log(log_file):
        with open(log_file, 'w') as file:
            file.write("\n")