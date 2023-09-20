from pygame import mixer

def load_sound(name):
    mixer.music.load("assets/snd/{}.ogg".format(name))

def loop_song(name):
    load_sound(name)
    mixer.music.play(-1)

def stop_sound():
    mixer.music.stop()
    mixer.music.unload()

