"""
Módulo de dados dos 7 Plasmas Radiais do Sincronário (Dreamspell / Lei do Tempo).
Contém os nomes, chakras associados, cores e afirmações dos 7 plasmas
que regem os 7 dias de cada semana (heptal).
"""

PLASMAS = [
    {
        "index": 0,
        "number": 1,
        "name": "Dali",
        "code": "DALI",
        "chakra": "Coronário",
        "color": "#fabc3c",  # Amarelo
        "quality": "Térmico",
        "action": "Focaliza",
        "affirmation": "Meu pai é a consciência intrínseca, eu sinto o calor.",
    },
    {
        "index": 1,
        "number": 2,
        "name": "Seli",
        "code": "SELI",
        "chakra": "Raiz",
        "color": "#d93829",  # Vermelho
        "quality": "Lumínico",
        "action": "Flui",
        "affirmation": "Minha mãe é a esfera primordial, eu vejo a luz.",
    },
    {
        "index": 2,
        "number": 3,
        "name": "Gama",
        "code": "GAMA",
        "chakra": "Terceiro Olho",
        "color": "#f5f6fa",  # Branco
        "quality": "Térmico-Lumínico",
        "action": "Pacificador",
        "affirmation": "Minha linhagem é a união da consciência intrínseca e da esfera primordial.",
    },
    {
        "index": 3,
        "number": 4,
        "name": "Kali",
        "code": "KALI",
        "chakra": "Sexual",
        "color": "#2980b9",  # Azul
        "quality": "Catalisador",
        "action": "Estabelece",
        "affirmation": "Meu nome é o nascido glorioso do lótus, eu cataliso a luz e o calor intrínsecos.",
    },
    {
        "index": 4,
        "number": 5,
        "name": "Alfa",
        "code": "ALFA",
        "chakra": "Laríngeo",
        "color": "#fabc3c",  # Amarelo
        "quality": "Eletrônico",
        "action": "Libera",
        "affirmation": "Meu país é a esfera não nascida, eu libero o elétron duplo no polo sul.",
    },
    {
        "index": 5,
        "number": 6,
        "name": "Limi",
        "code": "LIMI",
        "chakra": "Plexo Solar",
        "color": "#d93829",  # Vermelho
        "quality": "Mental",
        "action": "Purifica",
        "affirmation": "Eu consumo pensamentos duais como alimento, eu purifico o elétron mental no polo norte.",
    },
    {
        "index": 6,
        "number": 7,
        "name": "Silio",
        "code": "SILIO",
        "chakra": "Cardíaco",
        "color": "#f5f6fa",  # Branco
        "quality": "Telepático",
        "action": "Descarga",
        "affirmation": "Meu papel é realizar as ações de Buda, eu descarrego o elétron neutro no centro da Terra.",
    },
]


def get_plasma_for_day(day_of_moon: int) -> dict:
    """Retorna o plasma radial correspondente ao dia da lua (1..28)."""
    idx = (day_of_moon - 1) % 7
    return PLASMAS[idx]
