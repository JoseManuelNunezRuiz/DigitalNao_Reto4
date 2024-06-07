import csv

# Datos de ejemplo
correos = [
    {"nombre": "Sonia Martinez", "email": "soniamjofre@gmail.com", "mensaje": "Hola Sonia, ¡esperamos que tengas un gran inicio de semana!"},
    {"nombre": "Sebastian Lopez", "email": "muhjiddin@gmail.com", "mensaje": "Hola Sebastian, ¡esperamos que tengas un gran inicio de semana!"},
    {"nombre": "Manu Ruiz", "email": "mannunezruiz@gmail.com", "mensaje": "Hola Manu, ¡esperamos que tengas un gran inicio de semana!"},
]

# Crear el archivo CSV
with open('correos.csv', mode='w', newline='') as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=["nombre", "email", "mensaje"])
    escritor.writeheader()
    for correo in correos:
        escritor.writerow(correo)

print("Archivo CSV creado con éxito.")