#!/bin/bash

# Ejecutar saludos cada lunes a las 8 AM
schedule_cron="0 8 * * 1"
python3 enviar_felicitaciones.py &
croncmd_saludos="python3 enviar_felicitaciones.py"
cronjob_saludos="$schedule_cron $croncmd_saludos"
(crontab -l | grep -v -F "$croncmd_saludos"; echo "$cronjob_saludos") | crontab -

# Ejecutar felicitaciones por cumpleaños todos los días a las 8 AM
schedule_cron_diario="0 8 * * *"
croncmd_cumpleanos="python3 enviar_felicitaciones.py"
cronjob_cumpleanos="$schedule_cron_diario $croncmd_cumpleanos"
(crontab -l | grep -v -F "$croncmd_cumpleanos"; echo "$cronjob_cumpleanos") | crontab -

# Salida de confirmación
echo "Configuración de cron completada para enviar saludos los lunes y felicitaciones diarias por cumpleaños."

# Descargar el script en Python en GitHub
curl -O https://raw.githubusercontent.com/JoseManuelNunezRuiz/DigitalNao_Reto4/main/enviar_correo.py

# Ejecutar el script de Python que envía el correo de saludo
python3 enviar_correo.py
