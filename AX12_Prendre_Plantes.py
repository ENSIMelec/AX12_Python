import time
from AX12_Pinces import AX12_Pinces
from AX12_Ascenseur import AX12_Ascenseur

def prendre_plante():
    # Initialisation des instances des classes AX12_Pinces et AX12_Ascenseur
    ax12_pinces = AX12_Pinces()
    ax12_ascenseur = AX12_Ascenseur()
    
    # Initialiser les moteurs des pinces et de l'ascenseur
    ax12_pinces.initialize_motors()
    ax12_ascenseur.initialize_motors()

    # Ouvrir la pince pour prendre les plantes
    ax12_pinces.open_pince()
    
    # Fermer la pince pour prendre les plantes
    ax12_pinces.close_pince()

    # Monter l'ascenseur
    ax12_ascenseur.elevate()
    
    time.sleep(10)

    # Descendre l'ascenseur
    ax12_ascenseur.lower_for_plant()

    # Ouvrir à nouveau la pince pour déposer les plantes
    ax12_pinces.open_pince_stepbystep()
    
    # Monter l'ascenseur
    ax12_ascenseur.elevate()
    
    # Fermer la pince à nouveau
    ax12_pinces.close_pince()

if __name__ == "__main__":
    # Prendre les plantes
    prendre_plante()

