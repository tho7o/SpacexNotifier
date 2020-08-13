import win10toast
import requests
import json
from datetime import datetime
import time

#DICCIONARIO PARA GUARDAR LISTA DE FECHAS Y ORDENARLAS
schedule = []
# VARIABLE DE PROXIMO LANZAMIENTO
next_launch = ""

#CABECERA DE REQUEST
headers = {'content-type': 'application/json'}
#ENDPOINT API
url = 'https://api.spacexdata.com/v4/launches'
# METODO
r = requests.get(url, headers=headers)

#PASO RESPUESTA DE ARREGLO DE BYTES A TEXT
r = json.loads(r.text)
#RECORRO TODOS LOS JSON BUSCANDO "date_unix"
#Y GENERO UNA NUEVA LISTA
for date in r:
    schedule.append (date["date_unix"])

#ORDENO LA LISTA
schedule.sort()

# COMPARA LA HORA ACTUAL CON LA DE TODOS LOS LAZAMIENTOS RECOLECTADOS
# Y GUARDA EN next_launch EL SIGUIENTE A LA FECHA ACTUAL
# 3600 ES PARA ADELANTAR UNA HORA LA FECHA ACTUAL Y Q ASÍ
# PUEDA SER MAYOR LA FECHA ACTUAL INCLUSIVE EL MISMO DIA
#DEL LANZAMIENTO
for date in schedule:
    if (int(date) + 3600) >= int(time.time()): #time.time() OBTIENE TIMESTAMP ACTUAL
        if next_launch == "":
            next_launch = date

#CONVIERTE TIMESTAMP A FECHA
next_launch = datetime.utcfromtimestamp(int(next_launch)  - 14400 ).strftime('%d-%m-%Y %H:%M:%S')
#PREPARA EL MENSAJE
Message = "Proximo lanzamiento " + str(next_launch)
#INSTANCIA NOTIFIER
toaster=win10toast.ToastNotifier()
#LANZA AVISO
toaster.show_toast('SpaceX', Message, duration=5)

