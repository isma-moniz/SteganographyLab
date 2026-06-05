# Steganography Lab

Welcome! The practical and theoretical pdf files contain the walkthrough and theoretical background of this lab.

File structure:

.
├── assets
│   ├── challenge.jpg
│   ├── duck.jpg
│   ├── duck.png
│   ├── gnu.jpg
│   ├── metadata1.jpg
│   ├── metadata2.jpg
│   ├── penguins.jpg
│   └── penguins.png
├── labsetup
│   ├── attacker
│   │   ├── Dockerfile
│   │   ├── duck.png
│   │   ├── embed.py
│   │   └── payload.sh
│   ├── docker-compose.yml
│   ├── solutions
│   │   ├── analysis.py
│   │   ├── embed.py
│   │   └── extractor.py
│   ├── victim
│   │   ├── Dockerfile
│   │   ├── extractor.py
│   │   └── imv_fake.sh
│   └── volumes
│       ├── challenge.jpg
│       ├── metadata1.jpg
│       └── metadata2.jpg
├── README.md
├── SSI Project Proposal - G1 - Steganography Lab.pdf
└── THIRD_PARTY_ASSETS.md

The solutions directory contains the 3 main python scripts' solution
proposals.

Inside the labsetup folder: 

The attacker and victim directories set up the respective Docker images.

The volumes contains useful shared files between host and containers.

Assets contains the source and modified images we fetched from the internet (corresponding credit in THIRD_PARTY_ASSETS.md)

## Asset Attribution

Some images used in this repository are third-party assets using Public Domain or Creative Commons licenses.
This project is not endorsed by the creators. Modifications for the purpose of steganography have been made to
the images. More licensing and credit information can be found in `THIRD_PARTY_ASSETS.md`.

## Maintainer

Ismael Moniz - hismamoniz@gmail.com
