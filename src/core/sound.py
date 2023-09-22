import asyncio
from typing import Optional

from pygame import mixer


class Sound():
    # Dictionnaire de sons chargés
    all: dict[str, mixer.Sound]
    channels: dict[str, mixer.Channel]
    instance: Optional['Sound'] = None

    # Initialiser le mixer
    def __init__(self):
        mixer.init()
        mixer.set_num_channels(64)
        Sound.all = {}
        Sound.channels = {}

    # Supprimer tous les sons de la classe et quitter le mixer
    def __del__(self):
        Sound.all.clear()
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
            Sound.all[name] = mixer.Sound(self.get_snd_path(name))
        except FileNotFoundError:
            pass

    # Jouer un son 
    def play(self, name):
        if name not in Sound.all:
            self.load(name)
        Sound.all[name].play()

    async def play_with_delay(self, name, delay):
        await asyncio.sleep(delay)
        self.play(name)

    def add_channel(self, name):
        if name not in Sound.channels:
            Sound.channels[name] = mixer.Channel(len(Sound.channels))

    def loop_sound_in_channel(self, name):
        self.load(name)
        self.add_channel(name)
        Sound.channels[name].play(Sound.all[name], -1)

    def stop_channel(self, name):
        if name in Sound.channels and Sound.channels[name].get_busy():
            Sound.channels[name].stop()
