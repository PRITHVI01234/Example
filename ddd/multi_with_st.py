import multiprocessing
from mail import SendEmail
import streamlit as st

# Initialize session state
if 'email_process_started' not in st.session_state:
    st.session_state.email_process_started = False

def emailer(emails):
    for email in emails:
        user = SendEmail(email)
        user.criticalImpact('9:00', (15.15, 18.8), 'Log')

def printSending():
    st.write('Sending mail...')

emails = ['suryaprabhakarangm@gmail.com', 'jofraarcher04@gmail.com', 'krithickguru13@gmail.com', 'valantamildasan@gmail.com', 'officialrudhresh@gmail.com']

sendemail = st.button('Send Email')
log = st.button('Log Message')

def main():
    if sendemail and not st.session_state.email_process_started:
        st.session_state.email_process_started = True
        p = multiprocessing.Process(target=emailer, args=(emails,))
        p.start()
        p.join()  # Wait for the process to finish
        st.session_state.email_process_started = False

if log:
    printSending()

if sendemail or log:
    main()
