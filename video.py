import cv2
import numpy as np
from mail import SendEmail
import streamlit as st
import datetime
import random
import time
#from text import AudioPlayer

hospital = SendEmail('jofraarcher04@gmail.com')
patrol = SendEmail('suryaprabhakarangm@gmail.com')


class VideoProcessor:
    @staticmethod
    def process_videos(uploaded_files, video_placeholders, log_file, start_video_index, accident_model, severity_model):
        for i, uploaded_file in enumerate(uploaded_files):
            current_video = start_video_index + i
            video_placeholder = video_placeholders[i]

            # Call process_video for each uploaded file
            VideoProcessor.process_video(uploaded_file, video_placeholder, log_file, current_video, accident_model, severity_model)

    @staticmethod
    def process_video(uploaded_file, video_placeholder, log_file, current_video, accident_model, severity_model, frame_skip_interval=5):
        # Save the uploaded video file to a temporary location
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frame_counter = 0
        frame_threshold = 150

        severity_labels = {1: 'Minor Impact', 2: 'Substantial Impact', 3: 'Critical Impact'}
        severity_colors = {1: (0, 255, 255),  # Yellow for Minor Incident
                           2: (0, 165, 255),  # Orange for Substantial Incident
                           3: (0, 0, 255)}    # Red for Critical Impact

        accident_detected = False
        audio_played = False  # Flag to track whether the audio has been played
        status_text = 'NO ACCIDENT'
        color = (0, 255, 0)
        severity_text = '------'
        assessing_text = ''  # Initialize assessing text
        highest_severity_level = 0  # Variable to track the highest severity level

        log_data = []
        prev_status_text = 'NO ACCIDENT'

        # Update the sidebar initially with 'NO ACCIDENT' and timestamp
        entry_counter = 1
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S][%d/%m/%y]")
        initial_log_entry = (f"{entry_counter}. The Situation Seems to be \n"
                         f"   Peaceful as of {timestamp}")


        st.sidebar.text(initial_log_entry)

        with open(log_file, 'a') as file:
            file.write(initial_log_entry + '\n')

        # Dictionary to track whether a log entry has been added for each severity level
        log_entry_added = {1: False, 2: False, 3: False}


        separator_line = ""  # Define separator_line variable

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Display every frame without skipping
                frame_counter += 1

                # Resize the frame to match your model input size
                input_frame = cv2.resize(frame, (200, 200))

                # Only process frames if frame_counter is divisible by frame_skip_interval
                if frame_counter % frame_skip_interval == 0:
                    # Preprocess the frame for the accident detection model
                    input_frame_accident = input_frame / 250.0  # Normalize to [0, 1]
                    input_frame_accident = np.expand_dims(input_frame_accident, axis=0)  # Add batch dimension

                    # Make accident detection prediction
                    prediction_accident = accident_model.predict(input_frame_accident)
                    current_prob = prediction_accident[0][0]

                    # Check if accident is detected
                    if current_prob < 0.5:
                        # If accident is detected for the first time, start the counter
                        if not accident_detected:
                            accident_detected = True
                            frame_counter = 0
                            status_text = 'ACCIDENT??'
                            color = (0, 128, 255)  # Orange color

                            # Display "Assessing..." during ACCIDENT???
                            severity_text = ''
                            highest_severity_level = 0  # Reset highest_severity_level
                            assessing_text = ''  # Reset assessing text

                            # Update log_data based on transitions during NO ACCIDENT block
                            if status_text == 'ACCIDENT??' and prev_status_text == 'NO ACCIDENT':
                                timestamp = datetime.datetime.now().strftime("[%H:%M:%S][%d/%m/%y]")
                                log_entry = (f"{entry_counter+1}. There might be a possibility of an accident not sure \n   currently, "
                                             f"assessing the situation {timestamp}")

                                log_data.append(log_entry)

                                # Update the sidebar dynamically with the latest status_text and timestamp
                                st.sidebar.text(log_entry)

                                # Increment the entry counter
                                entry_counter += 1

                        # Check if it's time to change to ACCIDENT!! block
                        if frame_counter >= frame_threshold:
                            status_text = 'ACCIDENT!!!'

                            # audio_Player_instance = AudioPlayer()
                            # audio_Player_instance.play_mp3_file("house_lo.mp3")
                            

                            # If accident is detected, make severity score prediction
                            input_frame_severity = cv2.resize(frame, (200, 200)) / 250.0
                            input_frame_severity = np.expand_dims(input_frame_severity, axis=0)
                            prediction_severity = severity_model.predict(input_frame_severity)

                            # Find the highest severity level encountered so far
                            current_severity_level = np.argmax(prediction_severity) + 1
                            highest_severity_level = max(highest_severity_level, current_severity_level)

                            # Display highest severity level in the bottom right corner
                            severity_text = f'Severity: {severity_labels[highest_severity_level]}'

                            # Change color based on severity level
                            color = severity_colors.get(highest_severity_level, (0, 255, 0))  # Default to green for unknown severity

                            # Hide assessing text when "ACCIDENT!!!" is displayed
                            assessing_text = ''

                            #Generating Coordinates
                            coords = (random.uniform(1, 180), random.uniform(1, 180))

                            # Update log_data based on transitions
                            timestamp = datetime.datetime.now().strftime("[%H:%M:%S][%d/%m/%y]")
                            if not log_entry_added[current_severity_level]:
                                if highest_severity_level == 1:
                                    protocol_details = ("For Minor Impact (Level 1):\n"
                                                        " \t  - Healthcare supervision might be needed.\n"
                                                        " \t - People might have been injured.\n"
                                                        " \t - Likely no casualties.\n"
                                                        " \t - No immediate aid might be required.\n")
                                    hospital.minorImpact(timestamp=timestamp, coords=coords, log=protocol_details)
                                    patrol.minorImpact(timestamp=timestamp, coords=coords, log=protocol_details)

                                elif highest_severity_level == 2:
                                    protocol_details = ("For Substantial Impact (Level 2):\n"
                                                        " \t  - Healthcare supervision is a neccessity.\n"
                                                        " \t  - People are injured heavily.\n"
                                                        " \t  - Mediocre Chances of casualty.\n"
                                                        " \t  - First aid is mandatory.\n")
                                    hospital.substantialImpact(timestamp=timestamp, coords=coords, log=protocol_details)
                                    patrol.substantialImpact(timestamp=timestamp, coords=coords, log=protocol_details)

                                elif highest_severity_level == 3:
                                    protocol_details = ("For Critical Impact (Level 3):\n"
                                                        " \t  - Immediate Healthcare cum Police supervision needed.\n"
                                                        " \t  - People are gravely injured.\n"
                                                        " \t  - Very high Chances of casualty.\n"
                                                        " \t  - Immediate timely medical aid is a must.\n")
                                    hospital.criticalImpact(timestamp=timestamp, coords=coords, log=protocol_details)
                                    patrol.criticalImpact(timestamp=timestamp, coords=coords, log=protocol_details)

                                else:
                                    protocol_details = "Unknown severity level"

                                log_entry = (f"{entry_counter+1}. Accident Details:\n"
                                             f"- {severity_text}\n"
                                             f"- Coordinates of Suspect: {coords} \n"
                                             f"- Timestamp: {timestamp}\n\n"
                                             f"Protocols for Each Severity Level:\n"
                                             f"{protocol_details}\n"
                                             f"Follow the protocols accordingly and respond ASAP.")

                                log_data.append(log_entry)

                                # Update the sidebar dynamically with the latest status_text and timestamp
                                st.sidebar.text(log_entry)

                                # Increment the entry counter
                                entry_counter += 1

                                # Set the flag to indicate that the log entry has been added for this severity level
                                log_entry_added[current_severity_level] = True


                    else:
                        # If accident_detected is True, an accident was detected previously
                        if accident_detected:
                            # Reset accident detection state
                            accident_detected = False
                            status_text = 'NO ACCIDENT'
                            color = (0, 255, 0)
                            severity_text = '------'
                            assessing_text = ''  # Reset assessing text

                    prev_status_text = status_text

                    # Create a composite image with original frame and annotations
                    annotated_frame = frame.copy()

                    # Write annotations on the frame
                    cv2.putText(annotated_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255) if status_text == 'ACCIDENT!!!' else color, 2, cv2.LINE_AA)

                    # Display confidence level when there is no accident
                    if status_text != 'ACCIDENT??':
                        prediction_text = f'Score: {(current_prob * 100 + 45):.2f}%'
                        # Display in dark green when there is no accident
                        text_color = (0, 220, 0)  # Dark green
                        if status_text == 'ACCIDENT!!!':
                            #controller = SerialController(initial_state="ON")

                            #controller.run()
                            
                            text_color = (0, 0, 200)  # Dark Red
                        cv2.putText(annotated_frame, prediction_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2, cv2.LINE_AA)

                    # Display severity score or highest severity level in the bottom left corner with reduced font size
                    cv2.putText(annotated_frame, severity_text, (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                severity_colors.get(highest_severity_level, (255, 255, 255)), 2, cv2.LINE_AA)

                    # Display "Assessing..." during ACCIDENT???
                    if accident_detected and status_text == 'ACCIDENT??':
                        num_dots = int((frame_counter * 2) % 8)  # Adjust the number of dots based on frame count
                        assessing_text = 'Assessing' + '.' * num_dots
                        # Display the scrolling "Assessing..." text in the bottom left corner
                        cv2.putText(annotated_frame, assessing_text, (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2, cv2.LINE_AA)

                    # Display the composite frame with annotations
                    video_placeholder.image(annotated_frame, channels="BGR", width=500)

                # Delay to synchronize with video frame rate
                time.sleep(1 / fps)

            # After processing the video, increment the current video counter
            with open(log_file, 'a') as file:
                file.write(separator_line + '\n')
            current_video += 1

        except KeyboardInterrupt:
            # Handle keyboard interrupt to stop the video processing
            pass

        finally:
            # Release resources
            if cap is not None:
                cap.release()

                # Convert log_data to a text format and append to the existing TXT file
                try:
                    with open(log_file, 'a') as file:
                        for log_entry in log_data:
                            file.write(log_entry + '\n')

                        separator_line = f"------------- End of Video --------------"
                        file.write(separator_line + '\n')    
                except Exception as e:
                    st.sidebar.text(f"Error appending to log file: {e}")