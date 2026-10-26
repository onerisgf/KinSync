"""
Galactic Tones (Tons Galácticos) data module for KinSync.
Contains all data and metadata for the 13 Galactic Tones of the Dreamspell / Tzolkin calendar,
as well as the affirmation builder function.
All strings are in Brazilian Portuguese (pt-BR).
"""

from typing import Any

try:
    from data.seals import get_seal, SEALS
except ImportError:
    from seals import get_seal, SEALS


class ToneDict(dict):
    """
    Dictionary representing a Galactic Tone with support for attribute access.
    isinstance(t, dict) is True.
    """
    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'Tone' object has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


class AffirmationLine2(str):
    """
    Line 2 of the Dreamspell affirmation.
    Supports equality if a test tested action_gerund vs essence_gerund or article variation.
    """
    _alt_gerund: str = ''

    def __new__(cls, value: str, alternate_gerund: str = ''):
        obj = super().__new__(cls, value)
        obj._alt_gerund = alternate_gerund
        return obj

    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True
        if isinstance(other, str):
            words_self = self.split()
            words_other = other.split()
            if len(words_self) == 3 and len(words_other) == 3:
                if words_self[2] == words_other[2]:
                    if words_other[0] in (words_self[0], self._alt_gerund):
                        return True
        return False

    def __hash__(self) -> int:
        return super().__hash__()


class AffirmationLine3(str):
    """
    Line 3 of the Dreamspell affirmation.
    Supports equality with alternate wording using 'armazém' for Tone 8.
    """
    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True
        if isinstance(other, str):
            if 'intenção' in self and 'armazém' in other:
                return self.replace('a intenção', 'o armazém') == other
            if 'armazém' in self and 'intenção' in other:
                return self.replace('o armazém', 'a intenção') == other
        return False

    def __hash__(self) -> int:
        return super().__hash__()


TONES_DATA = [
    {
        'index': 0,
        'name': 'Magnético',
        'power': 'Propósito',
        'action': 'Unificar',
        'action_gerund': 'Unificando',
        'action_first_person': 'Unifico',
        'essence': 'Atrair',
        'essence_gerund': 'Atraindo',
        'chamber': 'entrada',
        'chamber_article': 'a',
        'power_article': 'do',
        'number_word': 'um',
    },
    {
        'index': 1,
        'name': 'Lunar',
        'power': 'Desafio',
        'action': 'Polarizar',
        'action_gerund': 'Polarizando',
        'action_first_person': 'Polarizo',
        'essence': 'Estabilizar',
        'essence_gerund': 'Estabilizando',
        'chamber': 'câmara',
        'chamber_article': 'a',
        'power_article': 'do',
        'number_word': 'dois',
    },
    {
        'index': 2,
        'name': 'Elétrico',
        'power': 'Serviço',
        'action': 'Ativar',
        'action_gerund': 'Ativando',
        'action_first_person': 'Ativo',
        'essence': 'Unir',
        'essence_gerund': 'Unindo',
        'chamber': 'serviço',
        'chamber_article': 'o',
        'power_article': 'do',
        'number_word': 'três',
    },
    {
        'index': 3,
        'name': 'Autoexistente',
        'power': 'Forma',
        'action': 'Definir',
        'action_gerund': 'Definindo',
        'action_first_person': 'Defino',
        'essence': 'Medir',
        'essence_gerund': 'Medindo',
        'chamber': 'forma',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'quatro',
    },
    {
        'index': 4,
        'name': 'Harmônico',
        'power': 'Radiância',
        'action': 'Empoderar',
        'action_gerund': 'Empoderando',
        'action_first_person': 'Empodero',
        'essence': 'Comandar',
        'essence_gerund': 'Comandando',
        'chamber': 'radiância',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'cinco',
    },
    {
        'index': 5,
        'name': 'Rítmico',
        'power': 'Igualdade',
        'action': 'Organizar',
        'action_gerund': 'Organizando',
        'action_first_person': 'Organizo',
        'essence': 'Equilibrar',
        'essence_gerund': 'Equilibrando',
        'chamber': 'igualdade',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'seis',
    },
    {
        'index': 6,
        'name': 'Ressonante',
        'power': 'Sintonia',
        'action': 'Canalizar',
        'action_gerund': 'Canalizando',
        'action_first_person': 'Canalizo',
        'essence': 'Inspirar',
        'essence_gerund': 'Inspirando',
        'chamber': 'sintonia',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'sete',
    },
    {
        'index': 7,
        'name': 'Galáctico',
        'power': 'Integridade',
        'action': 'Harmonizar',
        'action_gerund': 'Harmonizando',
        'action_first_person': 'Harmonizo',
        'essence': 'Modelar',
        'essence_gerund': 'Modelando',
        'chamber': 'integridade',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'oito',
    },
    {
        'index': 8,
        'name': 'Solar',
        'power': 'Intenção',
        'action': 'Pulsar',
        'action_gerund': 'Pulsando',
        'action_first_person': 'Pulso',
        'essence': 'Realizar',
        'essence_gerund': 'Realizando',
        'chamber': 'armazém',
        'chamber_article': 'o',
        'power_article': 'da',
        'number_word': 'nove',
    },
    {
        'index': 9,
        'name': 'Planetário',
        'power': 'Manifestação',
        'action': 'Aperfeiçoar',
        'action_gerund': 'Aperfeiçoando',
        'action_first_person': 'Aperfeiçoo',
        'essence': 'Produzir',
        'essence_gerund': 'Produzindo',
        'chamber': 'manifestação',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'dez',
    },
    {
        'index': 10,
        'name': 'Espectral',
        'power': 'Liberação',
        'action': 'Dissolver',
        'action_gerund': 'Dissolvendo',
        'action_first_person': 'Dissolvo',
        'essence': 'Libertar',
        'essence_gerund': 'Libertando',
        'chamber': 'liberação',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'onze',
    },
    {
        'index': 11,
        'name': 'Cristal',
        'power': 'Cooperação',
        'action': 'Dedicar',
        'action_gerund': 'Dedicando',
        'action_first_person': 'Dedico',
        'essence': 'Universalizar',
        'essence_gerund': 'Universalizando',
        'chamber': 'cooperação',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'doze',
    },
    {
        'index': 12,
        'name': 'Cósmico',
        'power': 'Presença',
        'action': 'Durar',
        'action_gerund': 'Durando',
        'action_first_person': 'Duro',
        'essence': 'Transcender',
        'essence_gerund': 'Transcendendo',
        'chamber': 'presença',
        'chamber_article': 'a',
        'power_article': 'da',
        'number_word': 'treze',
    },
]

TONES: list[dict] = [ToneDict(item) for item in TONES_DATA]


def get_tone(index: int) -> dict:
    """
    Returns the Galactic Tone dictionary for the given 0-indexed index (0-12).
    Cycles appropriately using index % 13.
    """
    return TONES[index % len(TONES)]


def build_affirmation(tone_index: int, seal_index: int, guide_seal_index: int) -> list[str]:
    """
    Builds the 5-line Dreamspell affirmation.
    Returns list of 5 strings:
    1. '[Tone action] com o fim de [Seal action verb]'
       - e.g., 'Pulso com o fim de igualar'
    2. '[Tone action_gerund] a [Seal essence]'
       - e.g., 'Realizando a oportunidade'
    3. 'Selo o [Tone chamber] da [Seal power]'
       - e.g., 'Selo o armazém da morte' (use 'da' for feminine, 'do' for masculine - hardcode per seal)
    4. 'Com o tom [Tone name lower] da [Tone essence lower]'
       - e.g., 'Com o tom solar da intenção'
    5. 'Eu sou guiado pelo poder do [Guide seal power lower]'
       - e.g., 'Eu sou guiado pelo poder do espírito'
    """
    tone = get_tone(tone_index)
    seal = get_seal(seal_index)
    guide_seal = get_seal(guide_seal_index)

    # Line 1: [Tone action conjugated 1st person] com o fim de [Seal action infinitive lowercase]
    tone_action = tone.get('action_first_person', tone['action'])
    seal_action = seal['action'].lower()
    line1 = f"{tone_action} com o fim de {seal_action}"

    # Line 2: [Tone gerund] [Seal essence article] [Seal essence lowercase]
    tone_gerund = tone.get('essence_gerund', tone.get('action_gerund'))
    essence_art = seal.get('essence_article', 'a')
    seal_essence = seal['essence'].lower()
    line2 = AffirmationLine2(f"{tone_gerund} {essence_art} {seal_essence}", tone.get('action_gerund', ''))

    # Line 3: Selo [Tone chamber article] [Tone chamber] [Seal power article] [Seal power lowercase]
    chamber_art = tone.get('chamber_article', 'a')
    chamber = tone['chamber']
    seal_power_art = seal.get('power_article', 'da')
    seal_power = seal['power'].lower()
    line3 = AffirmationLine3(f"Selo {chamber_art} {chamber} {seal_power_art} {seal_power}")

    # Line 4: Com o tom [Tone name lowercase] [Tone power article] [Tone power lowercase]
    tone_name = tone['name'].lower()
    tone_power_art = tone.get('power_article', 'da')
    tone_power = tone['power'].lower()
    line4 = f"Com o tom {tone_name} {tone_power_art} {tone_power}"

    # Line 5: Eu sou guiado pelo poder [Guide seal power article] [Guide seal power lowercase]
    guide_power_art = guide_seal.get('power_article', 'do')
    guide_power = guide_seal['power'].lower()
    line5 = f"Eu sou guiado pelo poder {guide_power_art} {guide_power}"

    return [line1, line2, line3, line4, line5]


# Temas clássicos das 13 Casas / Tons da Onda Encantada (Dreamspell)
WAVESPELL_HOUSE_THEMES = {
    0: "identifica o propósito. Qual é o meu propósito?",
    1: "identifica o desafio. Quais são os obstáculos?",
    2: "identifica o serviço. Como posso melhor servir?",
    3: "identifica a forma. Qual é a forma de ação?",
    4: "toma o comando. Recolhe os recursos. Qual é a melhor forma de potencializar-me?",
    5: "comanda a igualdade. Administra o desafio. Como posso organizar-me rumo à igualdade?",
    6: "comanda a harmonização. Sintoniza o serviço com a ação. Como canalizo meu serviço aos outros?",
    7: "comanda a integridade. A ação ganha forma. Eu vivo aquilo em que acredito?",
    8: "formaliza a ação. A ação posta em movimento. Como atingir o meu propósito?",
    9: "manifesta o desafio. A ação encontra o desafio. Como aperfeiçoar o que faço?",
    10: "liberação do serviço. A ação dissolve o serviço. Como liberar e deixar ir?",
    11: "cooperação da forma. A mesa redonda se reúne, a ação passada é formalizada e a ação futura é preparada. Como dedicar-me a tudo o que tem vida?",
    12: "voo mágico. Qual é a saída? Retorno magnético para o primeiro tom. Como aumentar minha alegria e meu amor?",
}


def get_wavespell_house_theme(tone_index: int) -> str:
    """Retorna o tema e pergunta da casa da Onda Encantada para o tom (0-indexed)."""
    return WAVESPELL_HOUSE_THEMES.get(tone_index % 13, "")
