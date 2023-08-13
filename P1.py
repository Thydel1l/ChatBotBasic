import string  # librería para trabajar con operaciones en cadenas de caracteres
import random  # librería para generar números aleatorios
import nltk  # librería de procesamiento de lenguaje natural
import warnings  # librería para gestionar advertencias
from sklearn.feature_extraction.text import TfidfVectorizer  # librería para vectorizar texto
from sklearn.metrics.pairwise import cosine_similarity  # función para calcular similitud del coseno
from nltk.corpus import stopwords  # palabras de parada para filtrar en el texto

# Descargar recursos de NLTK si no están presentes
nltk.download('punkt')  # Tokenización de palabras y frases
nltk.download('wordnet')  # Lemmatization
nltk.download('stopwords')  # Palabras de parada (stop words)
nltk.download('omw-1.4')  # Open Multilingual WordNet (OMW)

# Restaurar advertencias después de la descarga de NLTK
warnings.resetwarnings()

# Importar módulos adicionales
from gtts import gTTS  # Librería para convertir texto a voz
import time  # Librería para manejar intervalos de tiempo
import os  # Librería para interactuar con el sistema operativo
#------------------
archivo = open('C:/Users/HP/Desktop/Proyectos/Vs.Code/chatbotpp/corpus.txt','r', encoding='utf-8', errors='ignore')
raw = archivo.read()

# Preprocesamiento del texto del corpus
raw = raw.lower()  # Convertir a minúsculas
sent_tokens = nltk.sent_tokenize(raw)  # Dividir el corpus en oraciones
word_tokens = nltk.word_tokenize(raw)  # Dividir el corpus en palabras
lemmer = nltk.stem.WordNetLemmatizer()  # Objeto para lematización
# -- Función para generar lista de tokens lematizados
def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]

# -- Recuperar como un diccionario los signos de puntuación a remover
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# -- Función de lematización removiendo los signos de puntuación
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
#-------------------------------
def preprocesamiento_texto_usuario(user_response):
  # robo_response = ''
  sent_tokens.append(user_response) # -- Añade al final del CORPUS la respuesta del usuario
  TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words = stopwords.words('spanish'), token_pattern=None)
  tfidf = TfidfVec.fit_transform(sent_tokens)
  return tfidf
#-------------------------------
# -- Función para determinar la similitud del texto insertado y el CORPUS
def response(user_response):
  robo_response = ''  # respuesta del robot
  tfidf = preprocesamiento_texto_usuario(user_response) # Vecotirza la entrada del usuario junto con el corpus
  # 3 Evaluar similitud de coseno entre mensaje de usuario (tfidf[-1]) y el CORPUS (tfidf)
  vals = cosine_similarity(tfidf[-1], tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]

  if (req_tfidf == 0):
    robo_response = "Lo siento, no te entendí. Póngase en contacto con el personal asistencial"
  else:
    robo_response = ProcesarRespuesta(idx)
  return robo_response

def ProcesarRespuesta(idx):
  # Procesar respuesta de tipo lista
  if sent_tokens[idx].find('$') != -1:
    lista = sent_tokens[idx].split('$')
    respuesta = lista[0].capitalize() + '\n'
    for i in range(1,len(lista)):
      respuesta += str(i) + ". " + lista[i].capitalize() + '\n'
    return respuesta
  # Procesar respuesta normal (parrafo)
  else:
    return sent_tokens[idx] 
# Definición de palabras de saludo y respuestas correspondientes
SALUDOS_INPUTS = ("hola","buenas", "saludos", "qué tal", "hey", "buenos días")
SALUDOS_OUTPUTS = ["Hola", "Hola, ¿Qué tal?", "Hola, ¿Cómo te puedo ayudar?", "Hola, encantado de hablar contigo"]

def saludos(sentence):
  for word in sentence.split():
    if word.lower() in SALUDOS_INPUTS:
      return random.choice(SALUDOS_OUTPUTS)
#---------------
"""def reproducir(texto):
  lenguaje = "es"
  gtts_object = gTTS(text = texto, lang = lenguaje)
  gtts_object.save("mensaje.mp3")
  audio = Audio("mensaje.mp3", autoplay=True, )
  display(audio)"""
def reproducir(texto):
    lenguaje = "es"
    gtts_object = gTTS(text=texto, lang=lenguaje)
    gtts_object.save("mensaje.mp3")
    os.system("start mensaje.mp3")
# -- PROGRAMA PRINCIPAL -- Bucle de conversación
flag = True
# Iniciar conversación con mensajes de bienvenida
reproducir('Hola, contestaré a tus preguntas acerca de todos los tramites que puedes realizar en la escuela profesional.')
time.sleep(6)
reproducir('Si ya no deseas continuar, escribe salir, adios o chau')
time.sleep(4)
# Bucle de conversación
while (flag == True):
  # -- Solicitar que el usuario ingrese algún texto
  user_response = input()
  user_response = user_response.lower() # -- Convertir a minúsculas
  # Verificar si el usuario desea salir
  if (user_response != 'salir') and (user_response != 'adios') and (user_response != 'chau'):
    if (user_response=='gracias' or user_response=='muchas gracias'):
      flag = True
      print('No hay de qué')
      reproducir('No hay de qué')
      time.sleep(2)
    else:
      if (saludos(user_response) != None):
        saludo_texto = saludos(user_response)
        print(saludo_texto)
        #reproducir(saludos(user_response))
        reproducir(saludo_texto)
        time.sleep(2)
      else:
        respuesta_texto = response(user_response)
        reproducir(respuesta_texto)
        print(respuesta_texto)
        #reproducir(response(user_response))
        time.sleep(2)
        sent_tokens.remove(user_response) # -- Para eliminar del CORPUS la respuesta del usuario y volver a evaluar con el CORPUS limpio
  else:
    flag = False
    print('Nos vemos pronto, ¡Cuídate!')
    reproducir('Nos vemos pronto, ¡Cuídate!')
    time.sleep(2)
