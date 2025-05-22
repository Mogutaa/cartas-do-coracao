import streamlit as st
from models.user import User
from models.group import Group
from services.auth_service import AuthService
from services.group_service import GroupService
from services.letter_service import LetterService
from services.ai_service import AIService
from utils.pdf_generator import PDFGenerator
from utils.qr_generator import generate_pix_qr
from config.settings import settings
from datetime import datetime
from models.letter import Letter

def main():
    st.set_page_config(
        page_title="Cartas do Coração",
        page_icon="💌",
        layout="centered"
    )
    apply_custom_styles()
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if not st.session_state.user:
        handle_shared_letter()  # Verifica se há carta compartilhada
        show_auth_page()
    else:
        show_main_interface()

def handle_shared_letter():
    if "share_id" in st.query_params:
        share_id = st.query_params["share_id"]
        if isinstance(share_id, list):  # Se houver múltiplos valores
            share_id = share_id[0]
        show_shared_letter(share_id)

def show_shared_letter(share_id: str):
    letter_service = LetterService(None)
    letter_data = letter_service.get_letter_by_share_id(share_id)
    
    if not letter_data:
        st.error("📭 Carta não encontrada ou link inválido")
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <p>O link pode ter expirado ou sido removido</p>
                <small>Tente pedir um novo link ao autor</small>
            </div>
        """, unsafe_allow_html=True)
        return
    
    letter = Letter.from_dict(letter_data)
    
    with st.container():
        st.markdown(f"""
            <div class="card">
                <h3>Carta de {letter.sentiment}</h3>
                <p>{letter.content}</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("response_form"):
            response = st.text_area("Escreva sua resposta...", height=150)
            if st.form_submit_button("Enviar Resposta"):
                if response.strip():
                    letter_service.add_response(letter.id, response.strip())
                    st.success("Resposta enviada com sucesso!")
                else:
                    st.error("Escreva uma resposta antes de enviar")

def apply_custom_styles():
    st.markdown("""
        <style>
            :root {
                --primary: #FF69B4;
                --primary-dark: #C71585;
                --secondary: #FF1493;
                --background: grey;
            }

            .main {
                background-color: var(--background);
                padding: 2rem;
            }

            h1, h2, h3 {
                color: var(--secondary) !important;
                font-family: 'Pacifico', cursive;
            }

            div[data-baseweb="tab-list"] {
                gap: 1rem;
                margin-bottom: 2rem;
            }

            button[data-baseweb="tab"] {
                background: #FFE6F0 !important;
                border-radius: 15px !important;
                padding: 1rem 2rem !important;
                transition: all 0.3s ease !important;
                color: black !important;
            }

            button[data-baseweb="tab"]:hover {
                background: #FFD1E0 !important;
                transform: scale(1.05);
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                background: var(--primary) !important;
                color: white !important;
            }

            /* Botões padrão - Tema claro */
            body[data-theme="light"] .stButton > button {
                background-color: #FFE6F0 !important;
                color: #222222 !important;
                border-radius: 20px !important;
                padding: 10px 25px !important;
                transition: all 0.3s ease !important;
            }

            /* Botões - Tema escuro */
            body[data-theme="dark"] .stButton > button {
                background-color: var(--primary-dark) !important;
                color: white !important;
                border-radius: 20px !important;
                padding: 10px 25px !important;
                transition: all 0.3s ease !important;
            }

            /* Sombra de texto leve para legibilidade extra */
            .stButton > button {
                text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)



def show_auth_page():
    st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGdtdXNyY2lpcnhseXA2aHFmNmN3eGZwMjljOWY3dXRsZ3NwdmE5YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AhjupbaBuOG6EWAAVG/giphy.gif", width=200)
    st.title("Cartas do Coração")
    
    tab_login, tab_register = st.tabs(["Entrar", "Registrar"])
    
    with tab_login:
        with st.form("Login"):
            username = st.text_input("Nome de usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar")
            
            if submitted:
                try:
                    user = AuthService.authenticate(username, password)
                    st.session_state.user = user
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
    
    with tab_register:
        with st.form("Registro"):
            new_user = st.text_input("Novo usuário")
            new_pass = st.text_input("Nova senha", type="password")
            submitted = st.form_submit_button("Criar Conta")
            
            if submitted:
                try:
                    AuthService.register_user(new_user, new_pass)
                    st.success("Conta criada com sucesso! Faça login.")
                except Exception as e:
                    st.error(str(e))

def show_main_interface():
    # Header com logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"💌 Bem-vindo(a), {st.session_state.user.username}")
    with col2:
        if st.button("🚪 Sair"):
            st.session_state.user = None
            st.rerun()
    
    # Tabs de navegação
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Escrever Carta", 
        "📂 Meus Grupos", 
        "📤 Gerar PDF", 
        "❤️ Apoiar Projeto"
    ])
    
    with tab1:
        show_new_letter()
        st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTV4YmExYThxOGFocnlmZmoyZmVnNjhrdWN2OW84MWoxNTE1a3VwYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YW5Ynki0aGxFSe5Xps/giphy.gif", width=200)
    with tab2:
        st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWFqMDQ3dmVlaWNsZTY5dDd1dWFlN3MxNnQ0Ymg2YzltZzE0dm1leiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5p8jOW3f00osS705g3/giphy.gif", width=200)
        show_groups()
        
    with tab3:
        show_pdf_generator()
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnp3YzJseG4xbzIxMWh1dW95YnFrdzc4dDk0YXVlN2gweWM4dGkwdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vL8jVjKkqbVh2qdFj0/giphy.gif", width=200)
    
    with tab4:
        show_support_page()
        

def show_new_letter():
    st.header("✍️ Escrever Nova Carta")
    group_service = GroupService(st.session_state.user.id)
    letter_service = LetterService(st.session_state.user.id)
    
    # Inicializa o conteúdo se não existir
    if 'letter_content' not in st.session_state:
        st.session_state.letter_content = ""
    
    with st.form("letter_form"):
        # Seletor de grupo
        groups = group_service.get_user_groups()
        group_names = [g.name for g in groups]
        selected_group = st.selectbox("Destinatário", group_names)
        
        # Campo de conteúdo usando key única
        content = st.text_area(
            "Escreva seu coração...", 
            height=300, 
            value=st.session_state.letter_content,
            key="letter_input"
        )
        
        # Configurações adicionais
        col1, col2 = st.columns(2)
        with col1:
            sentiment = st.selectbox("Sentimento", ["❤️ Amor", "😢 Saudade", "🙏 Gratidão", "✨ Esperança"])
        with col2:
            writing_style = st.selectbox("Estilo", ["Emocional", "Poético", "Direto"])
        
        # Botões dentro do formulário
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            ai_help = st.form_submit_button("Preciso de Ajuda para Escrever")
        with col_btn2:
            save_letter = st.form_submit_button("Guardar Carta")
        
        # Lógica do botão de ajuda da IA
        if ai_help:
            if content.strip():
                suggestion = AIService.get_writing_suggestion(content)
                if suggestion:
                    st.session_state.suggestion = suggestion
            else:
                st.warning("Escreva algo primeiro para obter uma sugestão")
        
        # Lógica do botão de salvar
        if save_letter:
            if not content.strip():
                st.error("Escreva o conteúdo da carta antes de salvar")
            else:
                group_id = groups[group_names.index(selected_group)].id
                letter_service.create_letter(
                    content=content,
                    group_id=group_id,
                    sentiment=sentiment
                )
                st.session_state.letter_content = ""  # Limpa o conteúdo
                st.success("Carta guardada com sucesso!")
    
    # Mostrar sugestão fora do formulário
    if 'suggestion' in st.session_state:
        st.info("Sugestão da IA:")
        st.write(st.session_state.suggestion)
        if st.button("Usar Sugestão"):
            st.session_state.letter_content = st.session_state.suggestion
            del st.session_state.suggestion
            st.rerun()

def show_groups():
    st.header("📁 Meus Grupos")
    group_service = GroupService(st.session_state.user.id)
    letter_service = LetterService(st.session_state.user.id)
    
    # Criar novo grupo
    with st.expander("Criar Novo Grupo"):
        with st.form("new_group"):
            group_name = st.text_input("Nome do Grupo")
            if st.form_submit_button("Criar"):
                group_service.create_group(group_name)
                st.rerun()
    
    # Listar grupos existentes
    groups = group_service.get_user_groups()
    for group in groups:
        with st.container():
            st.subheader(group.name)
            letters = letter_service.get_letters_by_group(group.id)
            
            if not letters:
                st.write("Nenhuma carta neste grupo ainda...")
                continue
            
            for letter in letters:
                with st.expander(f"{letter.sentiment} - {letter.created_at.strftime('%d/%m/%Y')}"):
                    st.write(letter.content)
                    
                    # Seção de compartilhamento
                    st.markdown("---")
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        letter_service = LetterService(st.session_state.user.id)
                        share_url = letter_service.get_share_link(letter.id)
                        st.code(share_url)
                    with col2:
                        if st.button("📋 Copiar", key=f"copy_{letter.id}"):
                            st.write(share_url)
                            st.success("Link copiado!")
                    with col3:
                        if st.button("🗑️", key=f"del_{letter.id}"):
                            try:
                                letter_service.delete_letter(letter.id)
                                st.success("Carta excluída com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))
                    
                    # Mostrar respostas
                    if letter.responses:
                        st.markdown("### Respostas 💌")
                        for response in letter.responses:
                            st.markdown(f"""
                                <div class="card" style="margin: 5px 0; padding: 10px;">
                                    <small>{response['created_at'].strftime('%d/%m/%Y %H:%M')}</small>
                                    <p>{response['content']}</p>
                                </div>
                            """, unsafe_allow_html=True)

def show_pdf_generator():
    st.header("📄 Gerar PDF")
    group_service = GroupService(st.session_state.user.id)
    letter_service = LetterService(st.session_state.user.id)
    
    groups = group_service.get_user_groups()
    group_names = [g.name for g in groups] + ["Todos os Grupos"]
    
    selected_group = st.selectbox("Selecione o grupo", group_names)
    
    if st.button("Gerar PDF"):
        if selected_group == "Todos os Grupos":
            letters = letter_service.get_all_letters()
        else:
            group_id = groups[group_names.index(selected_group)].id
            letters = letter_service.get_letters_by_group(group_id)
        
        pdf_bytes = PDFGenerator.generate_pdf(
            [l.to_dict() for l in letters],
            selected_group if selected_group != "Todos os Grupos" else None
        )
        
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name=f"cartas_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

def show_support_page():
    st.header("💝 Apoie este Projeto")
    st.markdown("""
        Se você gostou do projeto e quer ajudar a mantê-lo, considere fazer uma doação.
        Sua contribuição é muito apreciada e ajuda a manter o projeto ativo e atualizado.
    """)
    st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTJ2aWFxeXF0bXUwYmV6eGtoY3RxYjlvdzBxcXNsNjJhamU2Z3FlbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/17jypIkG7IAid2adTQ/giphy.gif", width=200)
    qr_path = generate_pix_qr()
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(qr_path, width=200)
        
    with col2:
        st.code(settings.PIX_KEY)
        if st.button("Copiar Chave PIX"):
            st.write(settings.PIX_KEY)
            st.success("Chave copiada!")


if __name__ == "__main__":
    main()