# -*- Coding: utf-8 -*-
import speech_recognition as sr
import pyaudio
import wave
import time
# Utiles
from .utils import directory_exists, file_exists, random_name, write_file, remove_file
from .models import Audio
from .services import AudioService
from .config import Routes, Settings
from functools import partial 

class Record():
    """ Clase de grabación de audio. """
    def __init__(self, interface):
        self.routes = Routes()
        self.interface = interface
        self.listAudios()

    def saveAudio(self, filename, audio, text):
        """ Método para guardar registro de audios. """
        # Guardar archivos
        write_file(
            self.routes.base_audio_url, filename + ".wav", audio.get_wav_data()
        )
        write_file(
            self.routes.base_text_audio_url, filename + ".txt", text.encode()
        )
        # Guardar registros
        audio = Audio(filename, text[:20])
        audio_service = AudioService(self.routes.table_name)
        audio_service.create_audio(audio)
        # Refrescar vista
        self.listAudios()
        self.interface.showMessageInfo("Audio guardado en el sistema.")


    def listAudios(self):
        """ Método para listar grabaciones. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        i_audios = []
        for audio in audios:
            audio = audio.update(
                dict(
                    methods=[
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_delete),
                            action=self.deleteAudio
                        ),
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_play),
                            action=self.playAudio
                        )
                    ]
                )
            )

        self.interface.updateTable(
            headers=Audio.schema() + ["Acciones"],
            data=audios, 
        )

    def getAudio(self, uid):
        """ Método para obtener un audio por UID. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        audio = [audio for audio in audios if audio['uid'] == uid]
        if audio == []:
            return None
        return audio[0]


    def recordAudio(self):
        """ Método para grabar audio. """
        try:
            # Proceso de grabación
            record = sr.Recognizer()
            with sr.Microphone() as resource:
                audio = record.listen(resource)
                try:
                    text = str(record.recognize_google(audio, language=Settings.language))
                    self.interface.updateInfoBox("Has dicho: \n{}".format(text))
                    self.saveAudio(filename=random_name("record"), audio=audio, text=text)
                except Exception as e:
                    self.interface.showMessageInfo("Lo siento no entendi.")
        except:
            self.interface.showMessageInfo("Error de grabación.") 
            

    def deleteAudio(self, uid):
        """ Método para eliminar audio. """
        audio_service = AudioService(self.routes.table_name)
        audio = self.getAudio(uid)
        if audio:
            audio_service.delete_audio(audio["uid"])
            remove_file(self.routes.base_audio_url + audio["filename"] + ".wav" )
            remove_file(self.routes.base_text_audio_url + audio["filename"] + ".txt" )
            self.listAudios()
            self.interface.showMessageInfo("Audio eliminado del sistema.") 
        else:
            self.interface.showMessageInfo("El uid no existe en el sistema.") 


    def playAudio(self, uid):
        """ Método para reproducir audio. """
        try:
            audio = self.getAudio(uid)
            if audio:
                chunk = 1024 
                audio_url = self.routes.base_audio_url + audio["filename"] + ".wav" 
                if file_exists(audio_url):
                    f = wave.open(audio_url, "rb")
                    # reproducimos audio
                    #INICIAMOS PyAudio.
                    p = pyaudio.PyAudio()  
                    #ABRIMOS STREAM
                    stream = p.open(
                        format=p.get_format_from_width(f.getsampwidth()),  
                        channels=f.getnchannels(),  
                        rate=f.getframerate(),  
                        output=True
                    )
                    #LEEMOS INFORMACIÓN  
                    data = f.readframes(chunk)  
                    #REPRODUCIMOS "stream"  
                    while data:  
                        stream.write(data)  
                        data = f.readframes(chunk)  
                    #PARAMOS "stream".  
                    stream.stop_stream()  
                    stream.close()  

                    #FINALIZAMOS PyAudio  
                    p.terminate()
                else:
                    self.interface.showMessageInfo("Audio no encontrado.")
            else:
                self.interface.showMessageInfo("Audio no seleccionado.")

        except Exception as e:
            self.interface.showMessageInfo("No se puede reproducir el Audio.")