# crear entorno virtual
pip install virtualenv
# Abrir entorno virtual
virtualenv venv
# activar entorno virtual
cd venv/Scripts
activate
cd ../../

# Ejecutar los requirimientos del sistema:
pip install -r requirements.txt

# Ruta descargar pyaudio para windows 
* Nota si no funciona el comando pip install PyAudio, podemos descargarlo de la siguiente página y ejecutarlo de manera independiente
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# Página de iconos
* Si desean pueden descargar los iconos de esta página
https://www.flaticon.com/

# correr la aplicación:
app.py

# Crear el archivo ejecutable
pip install pyinstaller
pyinstaller app.py
pyi-makespec app.py  -> si no existe el archivo, crear el archivo

open file app.spec -> en data
    datas=[], -> agregar rutas de los archivos estaticos
    datas=[
        ('./recorder/icons/*.png', 'recorder/icons/'),
        ('./recorder/database/.audios.csv', 'recorder/database/'),
        ('./recorder/audio_recordings/*.wav', 'recorder/audio_recordings'),
        ('./recorder/audio_texts/*.txt', 'recorder/audio_texts/')
    ],

pyinstaller app.spec 

# Abrir ejecutable
* carpeta dist/app, se encuentra el ejecutable, doble clic para abrir.