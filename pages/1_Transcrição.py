import streamlit as st
from utils import transcribe_audio
import os
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="Transcrição de Áudio", page_icon="🎤")

# Título da página
st.title("Transcrição de Áudio 🎤")

# Diretório para armazenar transcrições
transcription_dir = "data/transcriptions/"
audio_dir = "data/audio/"
os.makedirs(transcription_dir, exist_ok=True)

# Instruções para o usuário
st.markdown("""
Faça o upload de um arquivo de áudio nos formatos MP3, WAV ou M4A para transcrição.
""")

# Seção de upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Salva o arquivo de áudio no diretório especificado
    audio_path = os.path.join(audio_dir, uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

    # Opções de transcrição
    st.markdown("### Opções de Transcrição")
    model = st.selectbox("Selecione o modelo do Whisper", ["tiny", "base", "small", "medium", "large"], index=1)
    language = st.text_input("Idioma do áudio (código ISO 639-1)", value="pt")

    # Botão para iniciar a transcrição
    if st.button("Iniciar Transcrição"):
        with st.spinner("Transcrevendo o áudio..."):
            try:
                # Chama a função de transcrição
                transcription = transcribe_audio(audio_path, options={"model": model, "language": language, "output_dir": transcription_dir})

                # Salva a transcrição em um arquivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                transcription_filename = f"{timestamp}_{os.path.splitext(uploaded_file.name)[0]}.txt"
                transcription_path = os.path.join(transcription_dir, transcription_filename)

                with open(transcription_path, "w") as f:
                    f.write(transcription)

                st.success(f"Transcrição salva em '{transcription_filename}'.")
                st.markdown("### Resultado da Transcrição")
                st.text_area("Texto Transcrito", transcription, height=300)
            except Exception as e:
                st.error(f"Ocorreu um erro durante a transcrição: {e}")
