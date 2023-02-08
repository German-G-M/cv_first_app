import streamlit as st
#import cv2
import numpy as np
import time
from PIL import Image
#import mediapipe as mp

#======Barra de ménu=====

st.sidebar.image("images/Mi foto.JPG",caption="Germán Gutiérrez")
st.sidebar.title("RECONOCIMIENTO DE ACCIÓN HUMANA")
#st.sidebar.subheader("Parámetros")
st.sidebar.button("boton 1")

modo_app=st.sidebar.selectbox('Menú',
['Inicio','Trabajando con imágenes','Trabajando con videos','Pruebas y resultados'])


#==============cuerpo (espacio de trabajo)

if modo_app=='Inicio':
    st.markdown('En esta aplicación utilizamos **MediaPipe** para la detección de movimiento')
    st.markdown('---')
    st.title("VISIÓN POR COMPUTADORA PARA EL RECONOCIMIENTO DE MOVIMIENTO HUMANO INUSUAL EN CÁMARAS DE VIGILANCIA")
    st.markdown('---')
    col1,col2,col3,col4=st.columns([2,3,3,2])
    with col2:
        resultadoboton1=st.button("Cámara Web",help="Reconocimiento de acción humana utilizando una cámara web",type="primary")
    with col3:
        resultadoboton2=st.button("Cámara de Vigilancia",help="Reconocimiento de acción humana utilizando una cámara de vigilancia",type="primary")
    
    if resultadoboton1:
        st.write("hicieron click en cámara web")
    if resultadoboton2:
        st.write("hicieron click en cámara de vigilancia")
    st.markdown('''
    <a href="/Cámara_Web"> Cámara Wweb</a>
    
    ''',
    unsafe_allow_html=True
    )
    st.video('https://youtu.be/uQkNbitG_1o')

    st.markdown(
        '''
        # Sobre mi \n
        Hola soy Germán Gutiérrez 
        '''
    )
if modo_app=='Trabajando con imágenes':
    st.header("Hola esta es la cabeza")
    st.caption("esto es un caption")
if modo_app=='Trabajando con videos':
    st.title('Interfaz de usuario')
if modo_app=='Pruebas y resultados':
    st.write('Aplicación de Visón por computadora de GERMAN GUTIERREZ MACHICADO')
    st.code("X=2023")

#============funciones
@st.cache()
def recorte_imagen(imagen,anchura=None,altura=None,interpolacion=56):
    return "hola"


