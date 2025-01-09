from speech import speech
from random import choice, randint
import time

# Niveles de dificultad
levels = {
    "easy": ["agenda", "ami", "souris"],
    "medium": ["ordinateur", "algorithme", "développeur"],
    "hard": ["réseau neuronal", "apprentissage automatique", "intelligence artificielle"]
}

def play_game(level):
    words = levels.get(level, [])  # Seleccionar las palabras en función del nivel de dificultad
    if not words:
        print("Nivel de dificultad incorrecto.")
        return

    score = 0
    num_attempts = 3  # Número de intentos por palabra

    for _ in range(len(words)):
        random_word = choice(words)
        print(f"Por favor, pronuncie la palabra {random_word}")
        recog_word = speech()
        print(recog_word)
        
        if random_word == recog_word:
            print("¡Eso es correcto!")
            score += 1
        else:
            print(f"Algo va mal. La palabra es: {random_word}")

        time.sleep(2)  # Pausa entre palabras
        
    print(f"¡Se acabó el juego! Tu puntuación es: {score}/{len(words)}")

# Seleccione el nivel de dificultad
selected_level = input("Seleccione el nivel de dificultad (easy/medium/hard): ").lower()
play_game(selected_level)