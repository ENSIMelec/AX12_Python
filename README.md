# AX12_Python

Vous retrouverez ici tous les codes concernant la programmation de l'AX12 pour les panneaux solaires, les pinces et ascenseur

## Setup la raspberry

Suivez en premier lieu le tuto pour setup votre raspberry si ce n'est pas fait [Setup a new rasp](https://www.notion.so/ensim-elec/Setting-up-a-new-rasp-1121a751840546299e4f7144cff6ced2?pvs=4)

## Installation

1. Installer `Visual Studio Code` comme IDE. Puis, installer l'extension `Remote - SSH` qui vous permettra de coder sur votre raspberry Pi.
2. Une fois connecté à la rasp, ouvez un terminal et créer un environnement virtuel:
  ```python
      python3 -m venv "nom_du_venv"`
  ```  
4. Activez-le avec:
  ```python
      source "nom_du_venv"/bin/activate
  ```
5. Vous pouvez maintenant installer Dynamixel-sdk avec la commande:
  ```python
      pip install dynamixel-sdk
  ```
