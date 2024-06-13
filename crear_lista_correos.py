import csv

# Datos de ejemplo con fecha de cumpleaños
correos = [
    {"nombre": "Sonia Martinez", "email": "soniamjofre@gmail.com", "mensaje": "Hola Sonia, ¡esperamos que tengas un gran inicio de semana!", "fecha_cumpleanos": "15-07"},
    {"nombre": "Sebastian Lopez", "email": "muhjiddin@gmail.com", "mensaje": "Hola Sebastian, ¡esperamos que tengas un gran inicio de semana!", "fecha_cumpleanos": "13-06"},
    {"nombre": "Manu Ruiz", "email": "mannunezruiz@gmail.com", "mensaje": "Hola Manu, ¡esperamos que tengas un gran inicio de semana!", "fecha_cumpleanos": "10-05"},
]

# Crear el archivo CSV
with open('correos.csv', mode='w', newline='') as archivo:
    # Definir los nombres de las columnas (fields)
    fieldnames = ["nombre", "email", "mensaje", "fecha_cumpleanos"]
    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)

    # Escribir la fila de encabezado con los nombres de las columnas
    escritor.writeheader()

    # Escribir cada fila de datos
    for correo in correos:
        escritor.writerow(correo)

print("Archivo CSV creado con éxito.")
