#!/bin/bash

# Función para enviar saludos cada lunes a las 8:00 AM
function enviar_saludos() {
    python3 enviar_correo.py saludos
}

# Función para enviar felicitaciones por cumpleaños todos los días a las 8:00 AM
function enviar_felicitaciones_cumpleanos() {
    python3 enviar_correo.py cumpleanos
}

# Configurar la tarea programada para enviar saludos cada lunes a las 8:00 AM
schedule_saludos="0 8 * * 1"
croncmd_saludos="enviar_saludos"
cronjob_saludos="$schedule_saludos $croncmd_saludos"
(crontab -l | grep -v -F "$croncmd_saludos"; echo "$cronjob_saludos") | crontab -

# Configurar la tarea programada para enviar felicitaciones por cumpleaños todos los días a las 8:00 AM
schedule_felicitaciones="0 8 * * *"
croncmd_felicitaciones="enviar_felicitaciones_cumpleanos"
cronjob_felicitaciones="$schedule_felicitaciones $croncmd_felicitaciones"
(crontab -l | grep -v -F "$croncmd_felicitaciones"; echo "$cronjob_felicitaciones") | crontab -

# Salida de confirmación
echo "Configuración de cron completada para enviar saludos los lunes y felicitaciones diarias por cumpleaños."

