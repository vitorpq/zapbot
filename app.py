# %%
import streamlit as st  # Para criar a interface web interativa
import requests         # Para fazer requisições HTTP para a API do WhatsApp
import json             # Para trabalhar com dados JSON (embora não usado explicitamente para dumps/loads nesta versão, requests.post(json=payload) o utiliza internamente)
import pandas as pd     # Para ler e manipular dados de arquivos Excel
import time             # Para adicionar pausas entre as mensagens

# URL base da API do WhatsApp. Substitua se sua API estiver em um endereço diferente.
URL = "http://localhost:3000/api/"

# %% Configuração inicial do aplicativo Streamlit
# Define o título da aba do navegador, o ícone e o layout da página.
st.set_page_config(page_title="ZapBot", page_icon=":robot_face:", layout="wide")
# Título principal exibido na página
st.title("ZapBot - WhatsApp Bot")
# Descrição breve do aplicativo
st.markdown("WhatsApp Bot criado para minhas tarefas diárias.")

# Cabeçalho para a seção de configuração na barra lateral
st.sidebar.header("Configuration")
# Nome da sessão a ser usada nas chamadas da API. Pode ser configurável se necessário.
SESSION_NAME = "default"

# Componente para upload de arquivo na barra lateral, aceitando apenas arquivos .xlsx
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])
# Área de texto na barra lateral para o usuário digitar a mensagem
message = st.sidebar.text_area(
    "Message",
    placeholder="Digite sua mensagem aqui. Você pode usar a formatação do WhatsApp: *negrito*, _itálico_, ~riscado~, ```monoespaçado```.",
    height=200  # Define a altura da caixa de texto em pixels
)
# Componente para selecionar o intervalo de tempo na barra lateral
interval_options = {
    "10 segundos": 10,
    "20 segundos": 20,
    "30 segundos": 30,
}
# Componente para selecionar o intervalo de tempo na barra lateral usando botões de rádio
selected_interval_label = st.sidebar.radio(
    "Intervalo entre mensagens:",
    options=list(interval_options.keys()),
    index=2  # Padrão para "30 segundos"
)
interval_seconds = interval_options[selected_interval_label]

# %% Lógica principal: processamento do arquivo e envio de mensagens
# Verifica se um arquivo foi carregado pelo usuário
if uploaded_file is not None:
    # Lê o arquivo Excel para um DataFrame do pandas
    df = pd.read_excel(uploaded_file)
    st.write("Data from Excel:")  # Exibe um título antes da tabela
    st.dataframe(df)  # Exibe o conteúdo do DataFrame na interface

    # Botão na barra lateral para iniciar o envio das mensagens
    if st.sidebar.button("Send Messages from Excel"):
        # Verifica se o campo de mensagem não está vazio
        if message:
            # Verifica se as colunas 'nome' e 'celular' existem no DataFrame
            if 'nome' in df.columns and 'celular' in df.columns:
                # Itera sobre cada linha do DataFrame
                for index, row in df.iterrows():
                    # Extrai o nome e capitaliza a primeira letra
                    nome = str(row['nome']).capitalize()
                    # Extrai o número de celular e converte para string
                    phone_number = str(row['celular'])
                    # Limpa o número de telefone removendo caracteres comuns
                    phone_number = phone_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

                    # Adiciona o código do país (55 para Brasil) se não estiver presente
                    if not phone_number.startswith('55'):
                        phone_number = '55' + phone_number

                    # Monta a URL para verificar a existência do contato na API
                    url_check = URL + f"contacts/check-exists?phone={phone_number}&session={SESSION_NAME}"
                    try:
                        # Faz a requisição GET para verificar o contato
                        response_check = requests.get(url_check, timeout=10) # Adicionado timeout
                        # Verifica se a requisição foi bem-sucedida (status code 200)
                        if response_check.status_code == 200:
                            contact_info = response_check.json()
                            # Verifica se o número existe e se o chatId foi retornado
                            if contact_info.get('numberExists'):
                                chat_id = contact_info.get('chatId')
                                if chat_id:
                                    # Monta a URL para enviar a mensagem de texto
                                    send_url = URL + "sendText"
                                    # Prepara o payload (dados) da mensagem em formato JSON
                                    payload = {
                                        "session": SESSION_NAME,
                                        "chatId": chat_id,
                                        "text": f"Boa noite, {nome}! \n {message}" # Mensagem personalizada
                                    }
                                    try:
                                        # Faz a requisição POST para enviar a mensagem
                                        response = requests.post(send_url, json=payload, timeout=15) # Adicionado timeout

                                        # Verifica se a API processou a mensagem com sucesso (status code 2xx)
                                        if 200 <= response.status_code < 300:
                                            response_data = response.json()
                                            st.success(f"Message processed for {nome} ({phone_number}). API Status: {response.status_code}. Ack: {response_data.get('ack', 'N/A')}")
                                        else:
                                            st.error(f"Error sending message to {nome} ({phone_number}). Status: {response.status_code}, Response: {response.text}")
                                    except requests.exceptions.RequestException as e:
                                        st.error(f"Request failed for sending message to {nome} ({phone_number}): {e}")
                                else:
                                    st.warning(f"Could not retrieve chat ID for {phone_number} ({nome}) even though number exists.")
                            else:
                                st.warning(f"Phone number {phone_number} does not exist for {nome}.")
                        else:
                            st.error(f"Error checking phone number for {nome} ({phone_number}). Status: {response_check.status_code}, Response: {response_check.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Request failed for checking phone {nome} ({phone_number}): {e}")


                    # Pausa por 30 segundos entre o envio de cada mensagem para evitar bloqueios/sobrecarga
                    time.sleep(interval_seconds)

                st.success("All messages sent (or attempted)!") # Mensagem final após o loop
            else:
                # Aviso se as colunas necessárias não forem encontradas no Excel
                st.error("The Excel file must contain columns named 'nome' and 'celular'.")
        else:
            # Aviso se o campo de mensagem estiver vazio
            st.warning("Please enter a message to send.")
else:
    # Informação para o usuário caso nenhum arquivo tenha sido carregado
    st.info("Please upload an Excel file with 'nome' and 'celular' columns.")


# %% Sidebar infos

st.sidebar.header("Developer")
st.sidebar.markdown(
    ":o: [Vitor Em.](https://github.com/vitorpq)"
)
st.sidebar.header("Tech stack")

st.sidebar.markdown(
    ":violet-badge[Python] :red-badge[Streamlit] :blue-badge[Docker] :green-badge[WAHA API] :gray-badge[Requests] :orange-badge[Pandas]"
)
