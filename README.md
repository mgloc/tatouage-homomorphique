# Projet: Tatouage d’images chiffrées homomorphiquement

## Découpage

- [x] 1. Pré-traitement
- [x] 2. Insertion de la marque dans le domaine en clair
- [x] 3. Insertion de la marque dans le domaine chiffré
- [x] 4. Extraction de la marque dans le domaine en chiffré
- [x] 5. Extraction de la marque dans le domaine en clair

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
# or you can also specify a custom message and image
python main.py --message message --image-path image.png
```

## Principe de fonctionnement

Implémentation de [l'algorithme de tatouage d'images chiffrées homomorphiquement.](docs/Projet_HE_WAT_2024.pdf)
