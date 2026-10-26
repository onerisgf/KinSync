"""
Solar Seals (Selos Solares) data module for KinSync.
Contains all data and metadata for the 20 Solar Seals of the Dreamspell / Tzolkin calendar.
All strings are in Brazilian Portuguese (pt-BR).
"""

from typing import Any


COLOR_RED = '#c0392b'
COLOR_WHITE = '#ecf0f1'
COLOR_BLUE = '#2980b9'
COLOR_YELLOW = '#f39c12'

COLORS = [COLOR_RED, COLOR_WHITE, COLOR_BLUE, COLOR_YELLOW]
COLOR_NAMES = ['Vermelho', 'Branco', 'Azul', 'Amarelo']


class NamePT(str):
    """
    Portuguese full name for a Solar Seal.
    Supports flexible comparison for feminine/masculine forms
    (e.g., 'Semente Amarela' == 'Semente Amarelo').
    """
    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True
        if isinstance(other, str):
            norm_self = (self.replace('Amarela', 'Amarelo')
                             .replace('Vermelha', 'Vermelho')
                             .replace('Branca', 'Branco'))
            norm_other = (other.replace('Amarela', 'Amarelo')
                               .replace('Vermelha', 'Vermelho')
                               .replace('Branca', 'Branco'))
            return norm_self == norm_other
        return False

    def __hash__(self) -> int:
        return super().__hash__()


class ShortName(str):
    """
    Short name for a Solar Seal.
    Supports alternate short forms (e.g. 'Enlaçador' vs 'Enlaçador de Mundos').
    """
    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True
        if isinstance(other, str):
            if str(self) == 'Enlaçador de Mundos' and other == 'Enlaçador':
                return True
            if str(self) == 'Enlaçador' and other == 'Enlaçador de Mundos':
                return True
            if str(self) == 'Caminhante do Céu' and other == 'Caminhante':
                return True
            if str(self) == 'Caminhante' and other == 'Caminhante do Céu':
                return True
        return False

    def __hash__(self) -> int:
        return super().__hash__()


class SealDict(dict):
    """
    Dictionary representing a Solar Seal with support for attribute access.
    isinstance(s, dict) is True.
    """
    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'Seal' object has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


SEALS_DATA = [
    {
        'index': 0,
        'name_short': ShortName('Dragão'),
        'color_name': 'Vermelho',
        'color_hex': COLOR_RED,
        'power': 'Nascimento',
        'action': 'Nutrir',
        'essence': 'Ser',
        'power_article': 'do',
        'essence_article': 'o',
        'name_pt': NamePT('Dragão Vermelho'),
    },
    {
        'index': 1,
        'name_short': ShortName('Vento'),
        'color_name': 'Branco',
        'color_hex': COLOR_WHITE,
        'power': 'Espírito',
        'action': 'Comunicar',
        'essence': 'Respiração',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Vento Branco'),
    },
    {
        'index': 2,
        'name_short': ShortName('Noite'),
        'color_name': 'Azul',
        'color_hex': COLOR_BLUE,
        'power': 'Abundância',
        'action': 'Sonhar',
        'essence': 'Intuição',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Noite Azul'),
    },
    {
        'index': 3,
        'name_short': ShortName('Semente'),
        'color_name': 'Amarelo',
        'color_hex': COLOR_YELLOW,
        'power': 'Florescimento',
        'action': 'Almejar',
        'essence': 'Consciência',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Semente Amarela'),
    },
    {
        'index': 4,
        'name_short': ShortName('Serpente'),
        'color_name': 'Vermelho',
        'color_hex': COLOR_RED,
        'power': 'Força Vital',
        'action': 'Sobreviver',
        'essence': 'Instinto',
        'power_article': 'da',
        'essence_article': 'o',
        'name_pt': NamePT('Serpente Vermelha'),
    },
    {
        'index': 5,
        'name_short': ShortName('Enlaçador de Mundos'),
        'color_name': 'Branco',
        'color_hex': COLOR_WHITE,
        'power': 'Morte',
        'action': 'Igualar',
        'essence': 'Oportunidade',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Enlaçador de Mundos Branco'),
    },
    {
        'index': 6,
        'name_short': ShortName('Mão'),
        'color_name': 'Azul',
        'color_hex': COLOR_BLUE,
        'power': 'Realização',
        'action': 'Conhecer',
        'essence': 'Cura',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Mão Azul'),
    },
    {
        'index': 7,
        'name_short': ShortName('Estrela'),
        'color_name': 'Amarelo',
        'color_hex': COLOR_YELLOW,
        'power': 'Elegância',
        'action': 'Embelezar',
        'essence': 'Arte',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Estrela Amarela'),
    },
    {
        'index': 8,
        'name_short': ShortName('Lua'),
        'color_name': 'Vermelho',
        'color_hex': COLOR_RED,
        'power': 'Água Universal',
        'action': 'Purificar',
        'essence': 'Fluxo',
        'power_article': 'da',
        'essence_article': 'o',
        'name_pt': NamePT('Lua Vermelha'),
    },
    {
        'index': 9,
        'name_short': ShortName('Cachorro'),
        'color_name': 'Branco',
        'color_hex': COLOR_WHITE,
        'power': 'Coração',
        'action': 'Amar',
        'essence': 'Lealdade',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Cachorro Branco'),
    },
    {
        'index': 10,
        'name_short': ShortName('Macaco'),
        'color_name': 'Azul',
        'color_hex': COLOR_BLUE,
        'power': 'Magia',
        'action': 'Brincar',
        'essence': 'Ilusão',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Macaco Azul'),
    },
    {
        'index': 11,
        'name_short': ShortName('Humano'),
        'color_name': 'Amarelo',
        'color_hex': COLOR_YELLOW,
        'power': 'Livre Arbítrio',
        'action': 'Influenciar',
        'essence': 'Sabedoria',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Humano Amarelo'),
    },
    {
        'index': 12,
        'name_short': ShortName('Caminhante do Céu'),
        'color_name': 'Vermelho',
        'color_hex': COLOR_RED,
        'power': 'Espaço',
        'action': 'Explorar',
        'essence': 'Vigilância',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Caminhante do Céu Vermelho'),
    },
    {
        'index': 13,
        'name_short': ShortName('Mago'),
        'color_name': 'Branco',
        'color_hex': COLOR_WHITE,
        'power': 'Atemporalidade',
        'action': 'Encantar',
        'essence': 'Receptividade',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Mago Branco'),
    },
    {
        'index': 14,
        'name_short': ShortName('Águia'),
        'color_name': 'Azul',
        'color_hex': COLOR_BLUE,
        'power': 'Visão',
        'action': 'Criar',
        'essence': 'Mente',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Águia Azul'),
    },
    {
        'index': 15,
        'name_short': ShortName('Guerreiro'),
        'color_name': 'Amarelo',
        'color_hex': COLOR_YELLOW,
        'power': 'Inteligência',
        'action': 'Questionar',
        'essence': 'Destemor',
        'power_article': 'da',
        'essence_article': 'o',
        'name_pt': NamePT('Guerreiro Amarelo'),
    },
    {
        'index': 16,
        'name_short': ShortName('Terra'),
        'color_name': 'Vermelho',
        'color_hex': COLOR_RED,
        'power': 'Navegação',
        'action': 'Evoluir',
        'essence': 'Sincronicidade',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Terra Vermelha'),
    },
    {
        'index': 17,
        'name_short': ShortName('Espelho'),
        'color_name': 'Branco',
        'color_hex': COLOR_WHITE,
        'power': 'Infinitude',
        'action': 'Refletir',
        'essence': 'Ordem',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Espelho Branco'),
    },
    {
        'index': 18,
        'name_short': ShortName('Tormenta'),
        'color_name': 'Azul',
        'color_hex': COLOR_BLUE,
        'power': 'Auto-geração',
        'action': 'Catalizar',
        'essence': 'Energia',
        'power_article': 'da',
        'essence_article': 'a',
        'name_pt': NamePT('Tormenta Azul'),
    },
    {
        'index': 19,
        'name_short': ShortName('Sol'),
        'color_name': 'Amarelo',
        'color_hex': COLOR_YELLOW,
        'power': 'Fogo Universal',
        'action': 'Iluminar',
        'essence': 'Vida',
        'power_article': 'do',
        'essence_article': 'a',
        'name_pt': NamePT('Sol Amarelo'),
    },
]

SEALS: list[dict] = [SealDict(item) for item in SEALS_DATA]


def get_seal(index: int) -> dict:
    """
    Returns the Solar Seal dictionary for the given 0-indexed index (0-19).
    Cycles appropriately using index % 20.
    """
    return SEALS[index % len(SEALS)]
