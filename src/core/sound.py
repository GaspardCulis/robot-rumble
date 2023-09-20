from pygame import mixer

class Sound():
    # Dictionnaire de sons chargés
    all: dict[str, mixer.Sound]

    # Initialiser le mixer
    def __init__(self):
        mixer.init()
        self.all = {}

    # Supprimer tous les sons de la classe et quitter le mixer
    def __del__(self):
        self.all.clear()
        mixer.quit()

    # Former le chemin relatif vers le fichier son auquel on souhaite accéder
    def get_snd_path(self, name):
        return "asset/snd/{}.ogg".format(name)

    # Arrêter le morceau en cours
    def stop_music(self):
        if mixer.music.get_busy():
            mixer.music.stop()
            mixer.music.unload()

    # Jouer un moceau indéfiniment
    def loop_song(self, name):
        self.stop_music()
        try:
            mixer.music.load(self.get_snd_path(name))
            mixer.music.play(-1)
        except FileNotFoundError:
            pass

    # Charger un son dans la classe
    def load_sound(self, name):
        try:
            self.all[name] = mixer.Sound(self.get_snd_path(name))
        except FileNotFoundError:
            pass

    # Jouer un son 
    def play_sound(self, name):
        if not name in self.all:
            self.load_sound(name)
        self.all[name].play()

