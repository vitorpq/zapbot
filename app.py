# %%
import streamlit as st
import requests
import json
import pandas as pd
import time

URL = "http://localhost:3000/api/"

# %% Set up Streamlit app
st.set_page_config(page_title="ZapBot", page_icon=":robot_face:", layout="wide")
st.title("ZapBot - WhatsApp Bot")
st.markdown("This is a simple WhatsApp bot that can send messages to a phone number.")
st.sidebar.header("Configuration")
SESSION_NAME = "default"

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])
message = st.sidebar.text_area(
    "Message",
    placeholder="Digite sua mensagem aqui. Você pode usar a formatação do WhatsApp: *negrito*, _itálico_, ~riscado~, ```monoespaçado```.",
    height=200
)

# %% Function to check if a phone number exists
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Data from Excel:")
    st.dataframe(df)

    if st.sidebar.button("Send Messages from Excel"):
        if message:
            if 'nome' in df.columns and 'celular' in df.columns:
                for index, row in df.iterrows():
                    nome = row['nome'].capitalize()
                    phone_number = str(row['celular'])
                    phone_number = phone_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                    # Check if phone number starts with 55 (Brazil country code)
                    if not phone_number.startswith('55'):
                        phone_number = '55' + phone_number

                    # Check if phone number exists
                    url_check = URL + f"contacts/check-exists?phone={phone_number}&session={SESSION_NAME}"
                    response_check = requests.get(url_check)
                    if response_check.status_code == 200:
                        contact_info = response_check.json()
                        if contact_info.get('numberExists'):
                            chat_id = contact_info.get('chatId')
                            if chat_id:
                                # Send Message
                                send_url = URL + "sendText"
                                payload = {
                                    "session": SESSION_NAME,
                                    "chatId": chat_id,
                                    "text": f"Boa noite, {nome}! \n {message}"
                                }
                                response = requests.post(send_url, json=payload)

                                # Check for any 2xx status code to indicate success
                                if 200 <= response.status_code < 300:
                                    # Displaying part of the response can be helpful, but the full JSON might be too verbose for a success message.
                                    st.success(f"Message processed for {nome} ({phone_number}). API Status: {response.status_code}. Ack: {response.json().get('ack', 'N/A')}")
                                else:
                                    st.error(f"Error sending message to {nome} ({phone_number}). Status: {response.status_code}, Response: {response.text}")
                            else:
                                st.warning(f"Could not retrieve chat ID for {phone_number} ({nome}) even though number exists.")
                        else:
                            st.warning(f"Phone number {phone_number} does not exist for {nome}.")
                    else:
                        st.error(f"Error checking phone number for {nome} ({phone_number}). Response: {response_check.text}")

                    time.sleep(30)  # Wait 30 seconds

                st.success("All messages sent (or attempted)!")
            else:
                st.error("The Excel file must contain columns named 'nome' and 'celular'.")
        else:
            st.warning("Please enter a message to send.")
else:
    st.info("Please upload an Excel file with 'nome' and 'celular' columns.")
# %%
# This code is a simple Streamlit app that allows users to check if a WhatsApp phone number exists and send messages to it.
# It uses the requests library to interact with a local API that handles WhatsApp messaging.
# The app has a sidebar for configuration where users can input a phone number and a message.
# The main area displays the status of the phone number and allows sending messages if the number exists.
# The app is designed to be user-friendly and provides feedback on the actions taken.
# The code is structured to handle user input, API requests, and display results in a clear manner.
# The app is intended for use with a WhatsApp bot backend that supports the specified API endpoints.
# The app is built using Streamlit, a popular framework for creating web applications in Python.
# The app is designed to be run locally and requires the backend API to be running on port 8000.
# The app is a demonstration of how to integrate WhatsApp messaging capabilities into a web application using Python.
# The app can be extended with additional features such as message history, error handling, and user authentication.
# The app is a starting point for building more complex WhatsApp bot applications.
# The app can be deployed to a web server or cloud platform for wider accessibility.
# The app is open-source and can be modified to suit specific use cases or requirements.
# The app is a practical example of using Streamlit for building interactive web applications with Python.
# The app is a useful tool for developers and businesses looking to integrate WhatsApp messaging into their workflows.
# The app can be used for customer support, notifications, and automated messaging.
# The app is a simple yet effective way to demonstrate the capabilities of WhatsApp bots.
# The app is a great starting point for anyone interested in building WhatsApp bots with Python.
# The app is designed to be easy to use and requires minimal setup.
# The app is a practical example of how to use Streamlit for building web applications that interact with external APIs.