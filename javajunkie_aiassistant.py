# Criando ambiente de programação Java, em python

# Importa os módulos para interagir com o sistema operacional
import os

# importa a bibloteca streamlit para criar a interface gráfica interativa
import streamlit as st

# importa a classe Groq para se conectar a API da Groq e acessar o LLM
from groq import Groq

# configura a pagina do streamlit com título, ícone, layout e estado inicial do sidebar
st.set_page_config(
    page_title="JavaJunkie 🤖",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define um prompt de sistema que descreve as regras e comportamentos do assistente de IA
CUSTOM_SYSTEM_PROMPT = """
Você é o "Java Coder", um assistente de IA sênior especialista em programação Java e desenvolvimento backend corporativo. 
Sua missão é ajudar a resolver dúvidas de código, focar em boas práticas de Programação Orientada a Objetos (POO) e na construção de sistemas robustos.

REGRAS DE OPERAÇÃO:
1. Foco em Java: Responda apenas dúvidas relacionadas a Java, ecossistema da JVM e arquitetura backend.
2. Estrutura: Forneça códigos sempre seguindo as convenções da linguagem, com explicação detalhada da lógica de classes e métodos utilizados.
3. Documentação: Ao final, inclua links para a documentação oficial da Oracle ou para bibliotecas/frameworks relevantes.
"""

# Criar o conteúdo da barra lateral no streamlit
with st.sidebar:

    # define o titulo da barra lateral
    st.title("JavaJunkie - AI Assistant🤖")

    # mostra um texto explicativo sobre o assistente de IA
    st.markdown("Um assistente de IA focado em programação Java, para ajudar iniciantes.")

    # Campo para inserir as chaves de API da Groq, com um link para obter as chaves
    groq_api_key = st.text_input(
        "Insira sua API Key da Groq",
        type="password",
        help="Obtenha sua API Key em https://groq.com/dashboard/api-keys",
    )
    
    # apenas verifica se a chave da api key foi inserida, se sim, mostra um texto de confirmação
    if groq_api_key:
        st.success("API Key da Groq inserida com sucesso!")
    else:
        st.warning("Por favor, insira sua API Key da Groq para usar o JavaJunkie 🤖.")

    # adiciona linhas divisórias para separar as seções da barra lateral
    st.markdown("---")
    st.markdown("### Sobre o JavaJunkie 🤖")
    st.markdown(
        """
        Projeto desenvolvido para demonstrar a criação de um assistente de IA especializado em programação Java, utilizando a API da Groq e a biblioteca Streamlit para a interface gráfica.
        O assistente é projetado para ajudar desenvolvedores iniciantes a resolver dúvidas de código
        """
    )

# Titulo principal do app 
st.title("JavaJunkie 🤖")

#subtitulo adicional
st.title("Assistente de IA para Programação Java")

#texto auxiliar abaixo do título
st.markdown(
    """
    O JavaJunkie é um assistente de IA especializado em programação Java, projetado para ajudar desenvolvedores iniciantes a resolver dúvidas e aprender conceitos de forma clara e precisa. 
    Insira sua API Key da Groq na barra lateral para começar a interagir com o assistente.
    """
)

# Inicializa o histórico de mensagens da conversa, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# inicializa a variável do cliente da Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    try:
        # Cria o cliente da Groq com a chave de API fornecida
        client = Groq(api_key=groq_api_key)
        st.success("Conexão com a API da Groq estabelecida com sucesso!")
    except Exception as e:
        st.error(f"Erro ao conectar com a API da Groq: {e}")
        st.stop()  # Para a execução do app se a conexão falhar

# caso não tenha  a chave, mas já existam mensagens, mostra aviso para inserir a chave da API
elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar usando o JavaJunkie 🤖.")

# captura a entrada do usuário no chat
if prompt := st.chat_input("Digite sua pergunta sobre programação Java aqui..."):
    # se não houver um cliente válido, mostra aviso para inserir a chave da API e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar a usar o JavaJunkie 🤖.")
        st.stop()

    # armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    #exibe a mensagem do usuario no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # prepara menagens para enviar a api, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        # exibe um indicador de que o assistente está digitando
        with st.spinner("O JavaJunkie 🤖 está pensando..."):
            try:
                # envia as mensagens para a API da Groq e obtém a resposta
                chat_comlpetion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048,                    
                )

                # extrai o conteúdo da resposta do assistente
                javaj_ai_resposta = chat_comlpetion.choices[0].message.content

                # exibe a resposta do assistente no chat
                st.markdown(javaj_ai_resposta)

                # armazena a resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": javaj_ai_resposta})

                # caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Erro ao obter resposta do JavaJunkie 🤖: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>JavaJunkie 🤖 - O assistente de IA para programação Java</p>
    </div>
    """,
    unsafe_allow_html=True
)