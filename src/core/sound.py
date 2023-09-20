from pygame import mixer
from typing import Optional

class Sound():
    # Dictionnaire de sons chargés
    all: dict[str, mixer.Sound]
    instance: Optional['Sound'] = None

    # Initialiser le mixer
    def __init__(self):
        mixer.init()
        self.all = {}

    # Supprimer tous les sons de la classe et quitter le mixer
    def __del__(self):
        self.all.clear()
        mixer.quit()

    @staticmethod
    def get():
        if Sound.instance is None:
            Sound.instance = Sound()
        return Sound.instance

    # Former le chemin relatif vers le fichier son auquel on souhaite accéder
    def get_snd_path(self, name):
        return "assets/snd/{}.ogg".format(name)

    # Arrêter le morceau en cours
    def stop_music(self):
        if mixer.music.get_busy():
            mixer.music.stop()
            mixer.music.unload()

    # Jouer un moceau indéfiniment
    def loop_music(self, name):
        self.stop_music()
        try:
            mixer.music.load(self.get_snd_path(name))
            mixer.music.play(-1)
        except FileNotFoundError:
            pass

    # Charger un son dans la classe
    def load(self, name):
        try:
            self.all[name] = mixer.Sound(self.get_snd_path(name))
        except FileNotFoundError:
            pass

    # Jouer un son 
    def play(self, name):
        if name not in self.all:
            self.load(name)
        self.all[name].play()
>>>>>>> main

