import streamlit as st
from tinydb import TinyDB, Query

# Configuração do banco de dados
db = TinyDB("config.json")
config_table = db.table("config")
prompts_table = db.table("prompts")

# Configuração da página
st.set_page_config(page_title="Configuração", page_icon="⚙️")

# Título da página
st.title("Configuração ⚙️")

# Configuração da Chave de API
st.subheader("Chave de API da OpenAI")
config = config_table.get(doc_id=1)
api_key = config["api_key"] if config else ""

new_api_key = st.text_input("Insira sua chave de API da OpenAI:", value=api_key, type="password")

if st.button("Salvar Chave de API"):
    if config:
        config_table.update({"api_key": new_api_key}, doc_ids=[1])
    else:
        config_table.insert({"api_key": new_api_key}, doc_id=1)
    st.success("Chave de API salva com sucesso!")

# Gerenciamento de Prompts
st.subheader("Gerenciamento de Prompts")

# Listar prompts existentes
prompts = prompts_table.all()
if prompts:
    for prompt in prompts:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{prompt['name']}**")
        with col2:
            if st.button(f"Editar", key=f"edit_{prompt.doc_id}"):
                st.session_state.edit_prompt = prompt
        with col3:
            if st.button(f"Excluir", key=f"delete_{prompt.doc_id}"):
                prompts_table.remove(doc_ids=[prompt.doc_id])
                st.rerun()

# Adicionar ou Editar Prompt
if "edit_prompt" in st.session_state:
    st.subheader("Editar Prompt")
    prompt_name = st.text_input("Nome do Prompt", value=st.session_state.edit_prompt["name"])
    prompt_text = st.text_area("Texto do Prompt", value=st.session_state.edit_prompt["text"])
    if st.button("Salvar Alterações"):
        prompts_table.update({"name": prompt_name, "text": prompt_text}, doc_ids=[st.session_state.edit_prompt.doc_id])
        del st.session_state.edit_prompt
        st.success("Prompt atualizado com sucesso!")
        st.rerun()
else:
    st.subheader("Adicionar Novo Prompt")
    prompt_name = st.text_input("Nome do Prompt")
    prompt_text = st.text_area("Texto do Prompt")
    if st.button("Adicionar Prompt"):
        # Verificar se já existe um prompt com o mesmo nome
        existing_prompt = prompts_table.get(Query().name == prompt_name)
        if existing_prompt:
            st.warning(f"Já existe um prompt com o nome '{prompt_name}'.")
        else:
            prompts_table.insert({"name": prompt_name, "text": prompt_text})
            st.success("Prompt adicionado com sucesso!")
            st.rerun()
