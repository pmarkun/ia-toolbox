import streamlit as st

# Configurações iniciais da aplicação
st.set_page_config(
    page_title="Transcrição e Processamento de Áudio",
    page_icon="🎙️",
    layout="wide"
)

# Página inicial da aplicação
st.title("Bem-vindo ao Transcritor de Áudio e Processador de Texto 🎙️")
st.markdown("""
Este aplicativo permite que você:
- Transcreva arquivos de áudio usando o Whisper.
- Selecione ou faça upload de novos arquivos para processamento.
- Utilize prompts personalizados com ChatGPT para analisar os textos transcritos.

Use o menu à esquerda para navegar entre as funcionalidades disponíveis:
- **Transcrição de Áudio**: Envie arquivos para transcrição.
- **Processamento de Texto**: Selecione ou envie textos para análise com ChatGPT.
- **Configurações**: Configure sua chave de API do OpenAI e personalize prompts.
""")
