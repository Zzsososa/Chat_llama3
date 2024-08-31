from itertools import chain
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Inicializa el modelo de Llama 3 utilizando Ollama
llm = Ollama(model="llama3")

def main():
    st.title("Chat con Llama 3")
    bot_name = st.text_input("Nombre del asistente virtual", value="IA")
    prompt = f"""Eres un asistente virtual te llamas {bot_name}, respondes preguntas con respuetas simples, tambien debes preguntarle cosas basicas al usuario para conocerlo"""
    bot_description = st.text_area("Descripcion del asistente virtual:", value= prompt)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


    prompt_template = ChatPromptTemplate.from_messages(

        [

            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),

        ]


    )

    chat = prompt_template | llm

    user_input = st.text_input("Escribe tu pregunta:", key="user_input")

    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.stop
        else: 
            response = llm(prompt_template.format(input=user_input, chat_history=st.session_state["chat_history"]))
            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            st.session_state["chat_history"].append(AIMessage(content=response))


        
    chat_display = ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"Humano: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_display += f"{bot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_display, height=400, key="chat_area") 
            
    




if __name__ == "__main__":
    main()