import streamlit as st
import tempfile
import numpy as np
import time


import cv2
import mediapipe as mp

mp_holistic=mp.solutions.holistic
mp_drawing=mp.solutions.drawing_utils

DEMO_IMAGEN='demo.mp3'
DEMO_VIDEO='images/DEMO.mp4'
st.title("Pagina de la cámara web")

#===side bar
st.sidebar.subheader("Parámetros")
cam_web=st.sidebar.button('Utilizar la cámara web')
grabacion=st.sidebar.checkbox('grabar video')
max_personas=st.sidebar.number_input('máximo número de personas a detectar',min_value=1,max_value=7,value=2)
#st.sidebar.markdown('---')
nivel_confianza_deteccion=st.sidebar.slider('Nivel de confianza para la detección',min_value=0.1,max_value=1.0,value=0.5)
nivel_confianza_seguimiento=st.sidebar.slider('Nivel de confianza para el seguimiento',min_value=0.1,max_value=1.0,value=0.5)
buffer_archivo_video=st.sidebar.file_uploader("cargar un video",type=['mp4','mov','avi','asf'])
st.sidebar.markdown('---')

#====Body
st.set_option('deprecation.showfileUploaderEncoding',False)

if grabacion:
    st.checkbox("Grabando",value=True)
st.markdown('## Salida')

st_cuadro=st.empty()
archivo_temporal=tempfile.NamedTemporaryFile(delete=False)

##obtenemos el archivo de video
if not buffer_archivo_video:
    if cam_web:
        #vid=cv2.VideoCapture(1)
        #vid=cv2.VideoCapture(0)
        vid=cv2.VideoCapture('rtsp://192.168.1.110:554/ch0_0.h264')
    else:
        vid=cv2.VideoCapture(DEMO_VIDEO)
        archivo_temporal.name=DEMO_VIDEO
else:
    archivo_temporal.write(buffer_archivo_video.read())
    vid=cv2.VideoCapture(archivo_temporal.name)

anchura=int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
altura=int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
entrada_fps=int(vid.get(cv2.CAP_PROP_FPS))

##Parte de grabación
#codec=cv2.VideoWriter_fourcc('M','J','P','G')
#salida=cv2.VideoWriter('salida1.mp4',codec,entrada_fps,(anchura,altura))

st.sidebar.text('Video de entrada')
st.sidebar.video(archivo_temporal.name)

fps=0
i=0

#creación de columnas
col1,col2,col3=st.columns(3)
with col1:
    st.markdown("**tasa del cuadro**")
    col1_text=st.markdown("0")
with col2:
    st.markdown("**Cántidad de personas**")
    col2_text=st.markdown("0")
with col3:
    st.markdown("**tamaño de la imagen**")
    col3_text=st.markdown("0")

st.markdown("<hr/>",unsafe_allow_html=True)#otra forma de hacer división

##===========funciones
def mediapipe_detection (imagen, modelo): 
    imagen=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB) #Convertimos a RGB antes de procesar. conversión del color. "cvtColor" es una función que nos permite cambiar los colores
    imagen.flags.writeable=False #esto para mejorar el desempeño, hacer la imagen no escribible. pone el estado de escritura en FALSE. La imagen ya no tien mas permiso de escritura 
    resultados = modelo.process (imagen) #esta linea hace la detección (prediccion) usando mediaPipe. la 'imagen' es un frame de openCV
    imagen.flags.writeable=True #devolvemos la escritura a la imagen. la imagen ahora se puede escribir
    imagen=cv2.cvtColor (imagen,cv2.COLOR_RGB2BGR) # Reconvertimos el color
    return imagen, resultados

def draw_my_own_landmarks(imagen,resultados):#podemos penerle nuestro estilo al mostrar los puntos y las conexiones
    mp_drawing.draw_landmarks(imagen, resultados.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                              mp_drawing.DrawingSpec(color=(80,110,10),thickness=1,circle_radius=1),
                              mp_drawing.DrawingSpec(color=(80,256,121),thickness=1,circle_radius=1)
                              ) 
    mp_drawing.draw_landmarks(imagen, resultados.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(imagen, resultados.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(imagen, resultados.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

def redimension_imagen(imagen,anchura=None,altura=None,interp=cv2.INTER_AREA):
    dimension=None
    (alt,anch)=imagen.shape[:2]
    if anchura is None and altura is None:
        return imagen
    if anchura is None:
        #r=altura/float(anch)
        r=anchura/float(anch)
        dimension=(int(anch*r),altura)
    else:
        #r=anchura/float(alt)
        r=anchura/float(anch)
        dimension=(anchura,int(alt*r))

    #redimencion de la imagen
    redimensionado=cv2.resize(imagen,dimension,interpolation=interp)
    return redimensionado

##===========fin apartado funciones
tiempoAnterior=0
with st_cuadro.container():
    with mp_holistic.Holistic(min_detection_confidence=nivel_confianza_deteccion,min_tracking_confidence=nivel_confianza_seguimiento) as holistic:
        while vid.isOpened():
            ret, frame=vid.read()
            if not ret:
                continue
            #Detección
            imagen,resultados=mediapipe_detection(frame,holistic)
            #dibujo Puntos de referencia
            draw_my_own_landmarks(imagen,resultados)

            ##contador de FPS
            tiempoActual=time.time()
            fps=1/(tiempoActual-tiempoAnterior) #1/(tiempo para procesar el loop)
            tiempoAnterior=tiempoActual

            # if grabacion:
            #     out.write(frame)
        
            ##pantalla principal
            col1_text.write(f"<h2 style='text-align:center; color:green;'>{int(fps)}</h2>",unsafe_allow_html=True)
            col2_text.write(f"<h2 style='text-align:center; color:green;'>{int(fps)}</h2>",unsafe_allow_html=True)
            col3_text.write(f"<h2 style='text-align:center; color:green;'>{int(anchura)}</h2>",unsafe_allow_html=True)

            ##Para mostrar la pantalla en la páginaWeb
            #imagen_recortada=cv2.resize(imagen,(0,0),fx=0.8,fy=0.8)
            #imagen_recortada=redimension_imagen(imagen=imagen_recortada,anchura=900)

            st_cuadro.image(imagen,channels='BGR',use_column_width=True)
            #st_cuadro.image(imagen_recortada,channels='BGR',use_column_width=True)
            time.sleep(0.1)
