# ZapBot - WhatsApp Bot

ZapBot é uma aplicação simples construída com Streamlit para enviar mensagens em massa via WhatsApp. Ele permite que os usuários façam upload de um arquivo Excel contendo nomes e números de celular, digitem uma mensagem personalizada e enviem essa mensagem para cada contato listado.

## ToDo
- Modularização de código
    - api_client.py - Funções da API
    - utils.py - clean_phone, formatação de mensagens
    - app.py - stream UI
    - config.py - URL, SESSION_NAME, TIMEOUTS
- Incluir gatilho para eventos 
- Respostas automáticas aos clientes

## Funcionalidades

- **Interface Web Interativa:** Construída com Streamlit para fácil utilização.
- **Upload de Arquivo Excel:** Suporta arquivos `.xlsx` com colunas para `nome` e `celular`.
- **Mensagens Personalizadas:** Permite que o usuário digite uma mensagem que será personalizada com o nome de cada contato.
- **Formatação de Mensagem:** A caixa de texto de mensagem suporta a sintaxe de formatação do WhatsApp (negrito, itálico, etc.).
- **Validação de Número:** Verifica a existência do número de telefone via API antes de tentar enviar a mensagem.
- **Limpeza de Número:** Formata automaticamente os números de telefone (remove espaços, hífens, adiciona código do país '55').
- **Feedback em Tempo Real:** Exibe o status de envio (sucesso/erro) para cada mensagem.
- **Controle de Envio:** Inclui um intervalo entre as mensagens para evitar bloqueios.

## Como Executar

1.  **Pré-requisitos:**
    *   Python 3.8+
    *   Uma API de WhatsApp como a WAHA (WhatsApp HTTP API) ou similar, rodando e acessível (o código está configurado para `http://localhost:3000/api/` por padrão).
    *   As dependências Python listadas em `requirements.txt` (se você criar um). Caso contrário, instale manualmente:
        ```bash
        pip install streamlit requests pandas openpyxl
        ```

2.  **Configuração da API:**
    *   Certifique-se de que sua API do WhatsApp esteja em execução.
    *   Se a URL da sua API for diferente de `http://localhost:3000/api/`, atualize a variável `URL` no arquivo `app.py`.

3.  **Executando o Aplicativo Streamlit:**
    *   Navegue até o diretório do projeto no seu terminal.
    *   Execute o comando:
        ```bash
        streamlit run app.py
        ```
    *   Abra o navegador no endereço fornecido pelo Streamlit (geralmente `http://localhost:8501`).

4.  **Usando o ZapBot:**
    *   Na barra lateral, faça o upload de um arquivo Excel (`.xlsx`) com as colunas `nome` e `celular`.
    *   Digite a mensagem que deseja enviar na caixa de texto "Message".
    *   Clique no botão "Send Messages from Excel".

## Estrutura do Arquivo Excel

O arquivo Excel deve conter pelo menos duas colunas:
- `nome`: O nome do contato.
- `celular`: O número de telefone do contato.

Exemplo:
| nome  | celular        |
|-------|----------------|
| Alice | (11) 98765-4321 |
| Bob   | 71912345678    |

## Tech Stack

:violet-badge[Python] :red-badge[Streamlit] :blue-badge[Docker]\* :green-badge[WAHA API]\* :gray-badge[Requests] :orange-badge[Pandas]

*\*Docker e WAHA API são mencionados com base na sua configuração de "Tech stack" no `app.py`, assumindo que você os utiliza para hospedar a API do WhatsApp.*

## Desenvolvedor

:o: Vitor Em.