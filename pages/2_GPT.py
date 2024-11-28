import streamlit as st
from tinydb import TinyDB, Query
from utils import process_prompt
import os
from datetime import datetime
import re

# Configurações da página
st.set_page_config(page_title="Processamento com ChatGPT", page_icon="🤖")

# Inicializar TinyDB e carregar os prompts
db = TinyDB("config.json")
prompts_table = db.table("prompts")
config_table = db.table("config")

# Diretórios para armazenar arquivos
transcription_dir = "data/transcriptions/"
results_dir = "data/results/"
os.makedirs(transcription_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# Título da página
st.title("Processamento com ChatGPT 🤖")

# Opções de entrada
st.markdown("### Escolha uma opção para processar:")
option = st.radio(
    "Como você deseja fornecer o texto para processamento?",
    ["Selecionar uma transcrição existente", "Fazer upload de um arquivo"]
)

content = None
uploaded_filename = None

if option == "Selecionar uma transcrição existente":
    # Listar transcrições disponíveis
    transcriptions = [f for f in os.listdir(transcription_dir) if f.endswith(".txt")]

    if transcriptions:
        selected_transcription = st.selectbox("Selecione uma transcrição", transcriptions)
        if selected_transcription:
            with open(os.path.join(transcription_dir, selected_transcription), "r") as file:
                content = file.read()
            uploaded_filename = selected_transcription
            st.markdown("### Texto Selecionado")
            st.text_area("Texto", content, height=300)
    else:
        st.warning("Nenhuma transcrição disponível. Faça upload de um arquivo ou vá para a página de transcrição.")

elif option == "Fazer upload de um arquivo":
    # Upload do arquivo de texto
    uploaded_file = st.file_uploader("Envie um arquivo de texto", type=["txt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        uploaded_filename = uploaded_file.name
        sanitized_filename = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", uploaded_filename)
        with open(os.path.join(transcription_dir, sanitized_filename), "w") as f:
            f.write(content)
        st.success(f"Arquivo salvo como: {sanitized_filename}")
        st.markdown("### Texto Carregado")
        st.text_area("Texto", content, height=300)

if content:
    # Seleção do Prompt
    st.markdown("### Seleção do Prompt")
    prompts = prompts_table.all()
    if prompts:
        prompt_names = [prompt["name"] for prompt in prompts]
        selected_prompt_name = st.selectbox("Selecione um Prompt", prompt_names)
        selected_prompt = next((p for p in prompts if p["name"] == selected_prompt_name), None)
        if selected_prompt:
            prompt_template = selected_prompt["text"]
    else:
        st.warning("Nenhum prompt disponível. Vá para a página de Configuração e crie um prompt.")
        st.stop()

    # Checkbox para formato Markdown
    format_markdown = st.checkbox("Formato Markdown")
    if format_markdown:
        prompt_template += "\n\nFaça em formato Markdown."

    # Opções do ChatGPT
    st.markdown("### Configurações do ChatGPT")
    model = st.selectbox("Modelo do ChatGPT", ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"], index=2)
    max_tokens = st.number_input("Máximo de Tokens", min_value=150, max_value=16384, value=8192)
    temperature = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Processar com ChatGPT
    if st.button("Processar com ChatGPT"):
        with st.spinner("Processando..."):
            try:
                result = process_prompt(
                    {"sys_prompt": prompt_template, "content": content},
                    options={
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "api_key": config_table.get(doc_id=1)["api_key"],
                        "model": model
                    }
                )
                # Salvar o resultado
                timestamp = datetime.now().strftime("%y%m%d")
                sanitized_filename = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", uploaded_filename)
                result_filename = f"{timestamp}_{model}_{sanitized_filename}"
                if not result_filename.endswith(".txt"):
                    result_filename += ".txt"
                result_path = os.path.join(results_dir, result_filename)

                with open(result_path, "w") as f:
                    f.write(result)

                st.success(f"Resultado salvo em: {result_filename}")
                st.markdown("### Resultado")
                st.text_area("Texto Gerado", result, height=300)
                st.download_button("Baixar Resultado", result, file_name=result_filename)
            except Exception as e:
                st.error(f"Erro ao processar com ChatGPT: {e}")
