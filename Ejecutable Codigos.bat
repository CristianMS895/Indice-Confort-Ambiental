@echo off
echo Activando entorno Conda y lanzando geovisores...

REM Cambiar a la unidad D
D:
cd "GOOGLE DRIVE\X\1.TRABAJO DE GRADO\Objeto Creación\EJECUTABLE"

REM Activar el entorno Conda (asegúrate de que 'base' sea el entorno correcto)
CALL "C:\Users\CRISTIAN\anaconda3\Scripts\activate.bat" base

REM Ejecutar cada script Python en una nueva ventana de cmd
start cmd /k python indice_calidad_aire.py
start cmd /k python indice_confort_termico.py
start cmd /k python indice_ruido_ambiental.py
start cmd /k python indice_confort_ambiental.py

echo Todos los geovisores han sido iniciados.
pause