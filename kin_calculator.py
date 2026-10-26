"""
KinSync — Motor de cálculo Dreamspell / Lei do Tempo.

Todas as fórmulas seguem o sistema Dreamspell de José Argüelles.
Referência: 26 de julho de 1987 = Kin 34 (Mago Galáctico Branco).

Convenções internas:
  - Selos: 0-indexed (0..19)  →  0=Dragão … 19=Sol
  - Tons:  0-indexed (0..12)  →  0=Magnético … 12=Cósmico
  - Kins:  1-indexed (1..260)
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class KinInfo:
    """Informações completas de um Kin."""
    kin: int        # 1..260
    seal: int       # 0..19
    tone: int       # 0..12


@dataclass(frozen=True)
class OracleInfo:
    """As 5 posições do Oráculo da Quinta Força."""
    destiny: KinInfo
    analog: int      # seal index 0..19
    antipode: int    # seal index 0..19
    occult: int      # seal index 0..19
    occult_tone: int # tone index 0..12
    guide: int       # seal index 0..19


@dataclass(frozen=True)
class NSSyncDate:
    """Data no formato Novo Sincronário (NS)."""
    year: int       # Ano NS (ex: 39 → NS1.39)
    moon: int       # Lua 1..13
    day: int        # Dia 1..28
    is_doot: bool   # Dia Fora do Tempo (25 de julho)
    is_hunab_ku: bool  # 0.0 Hunab Ku (29 de fevereiro)


@dataclass(frozen=True)
class SolarRingInfo:
    """Informações do Anel Solar (Ano Novo Sincronário)."""
    year_number: int            # Ano NS (ex: 39)
    bearer_kin: KinInfo         # Kin de 26/Jul deste ano NS
    bearer_name: str            # ex: "Lua Galáctica Vermelha"
    ns_date: NSSyncDate         # Data NS correspondente


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_REF_DATE = date(1987, 7, 26)
_REF_KIN = 34  # Kin de 26/Jul/1987

# Cores: 0=Vermelho, 1=Branco, 2=Azul, 3=Amarelo
SEAL_COLORS = [0, 1, 2, 3] * 5  # color of each seal (seal_index % 4)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_leap_year(year: int) -> bool:
    """Retorna True se *year* é bissexto no calendário gregoriano."""
    return calendar.isleap(year)


def _count_feb29_between(start: date, end: date) -> int:
    """
    Conta quantos dias 29 de fevereiro existem no intervalo entre start e end.
    Se start <= end: intervalo (start, end] — exclusivo à esquerda, inclusivo à direita.
    Se start > end: intervalo (end, start) — exclusivo a ambos.

    No Dreamspell, 29/Fev é "0.0 Hunab Ku" e não avança o Kin.
    """
    if start <= end:
        count = 0
        y_start = start.year
        y_end = end.year
        for y in range(y_start, y_end + 1):
            if not _is_leap_year(y):
                continue
            feb29 = date(y, 2, 29)
            if start < feb29 <= end:
                count += 1
        return count
    else:
        count = 0
        y_start = end.year
        y_end = start.year
        for y in range(y_start, y_end + 1):
            if not _is_leap_year(y):
                continue
            feb29 = date(y, 2, 29)
            if end < feb29 < start:
                count += 1
        return count


# ---------------------------------------------------------------------------
# Kin Calculation
# ---------------------------------------------------------------------------

def calculate_kin(target: date) -> KinInfo:
    """
    Calcula o Kin Dreamspell para uma data gregoriana.

    Algoritmo:
      1. Conta dias entre a data de referência (26/Jul/1987 = Kin 34) e a data alvo.
      2. Ajusta pelos 29/Fev que caem no intervalo (regra 0.0 Hunab Ku):
         - Se target >= _REF_DATE: subtrai os 29/Fev em (_REF_DATE, target].
         - Se target < _REF_DATE: soma os 29/Fev em (target, _REF_DATE).
      3. kin = ((Δ + base_kin - 1) mod 260) + 1
      4. seal = (kin - 1) mod 20
      5. tone = (kin - 1) mod 13
    """
    raw_days = (target - _REF_DATE).days
    leap_days = _count_feb29_between(_REF_DATE, target)

    if target >= _REF_DATE:
        delta = raw_days - leap_days
    else:
        delta = raw_days + leap_days

    kin = ((delta + _REF_KIN - 1) % 260) + 1
    seal = (kin - 1) % 20
    tone = (kin - 1) % 13

    return KinInfo(kin=kin, seal=seal, tone=tone)


# ---------------------------------------------------------------------------
# Oracle Calculation
# ---------------------------------------------------------------------------

def _guide_offset(seal: int, tone: int) -> int:
    """
    Calcula o offset do selo-guia baseado no tom e na cor do selo.

    A cor determina se o selo pertence ao grupo Vermelho/Azul (pares)
    ou Branco/Amarelo (ímpares).
    O tom (1-indexed) determina o grupo de offset.
    """
    color = seal % 4   # 0=Red, 1=White, 2=Blue, 3=Yellow
    is_red_blue = color in (0, 2)
    tone_1 = tone + 1  # converter para 1-indexed

    if tone_1 in (1, 6, 11):
        return 0  # Auto-guiado
    elif tone_1 in (2, 7, 12):
        return 12 if is_red_blue else 8
    elif tone_1 in (3, 8, 13):
        return 16 if is_red_blue else 4
    elif tone_1 in (4, 9):
        return 4 if is_red_blue else 16
    elif tone_1 in (5, 10):
        return 8 if is_red_blue else 12
    else:
        return 0  # fallback


def calculate_oracle(kin_info: KinInfo) -> OracleInfo:
    """
    Calcula o Oráculo da Quinta Força para um Kin.

    Fórmulas (0-indexed seals):
      - Análogo:  (17 - seal) mod 20 (Soma dos selos = 19 em 1-indexed)
      - Antípoda: (seal + 10) mod 20 (+10 no ciclo de 20)
      - Oculto:   19 - seal (Soma dos selos = 21 em 1-indexed)
      - Guia:     baseado no tom e cor (mesma cor/família)

    Tons do oráculo:
      - Análogo, Antípoda, Guia: mesmo tom do destino
      - Oculto: 12 - tone (Soma dos tons = 14 em 1-indexed)
    """
    s = kin_info.seal
    t = kin_info.tone

    analog_seal = (17 - s) % 20
    antipode_seal = (s + 10) % 20
    occult_seal = 19 - s
    occult_tone = 12 - t
    guide_seal = (s + _guide_offset(s, t)) % 20

    return OracleInfo(
        destiny=kin_info,
        analog=analog_seal,
        antipode=antipode_seal,
        occult=occult_seal,
        occult_tone=occult_tone,
        guide=guide_seal,
    )


# ---------------------------------------------------------------------------
# Wavespell (Onda Encantada)
# ---------------------------------------------------------------------------

def get_wavespell(kin_info: KinInfo) -> List[KinInfo]:
    """
    Retorna os 13 Kins da Onda Encantada à qual o Kin pertence.

    A Onda começa no Kin de Tom 1 (Magnético) e segue por 13 kins
    consecutivos. O Tom 1 da onda é: kin_number - tone (0-indexed).
    """
    start_kin = kin_info.kin - kin_info.tone
    if start_kin < 1:
        start_kin += 260

    result = []
    for i in range(13):
        k = start_kin + i
        if k > 260:
            k -= 260
        seal = (k - 1) % 20
        tone = (k - 1) % 13
        result.append(KinInfo(kin=k, seal=seal, tone=tone))

    return result


def get_wavespell_name_seal(kin_info: KinInfo) -> int:
    """Retorna o índice do selo (0-indexed) que dá nome à Onda Encantada."""
    start_kin = kin_info.kin - kin_info.tone
    if start_kin < 1:
        start_kin += 260
    return (start_kin - 1) % 20


def find_date_for_kin(target_kin: int, ref_date: Optional[date] = None) -> date:
    """
    Encontra a data gregoriana mais próxima de *ref_date* correspondente ao Kin *target_kin*.
    Se *ref_date* for None, utiliza a data de hoje.
    """
    if ref_date is None:
        ref_date = date.today()
    cur_kin = calculate_kin(ref_date).kin
    if cur_kin == target_kin:
        return ref_date
    diff = (target_kin - cur_kin) % 260
    if diff > 130:
        diff -= 260
    step = 1 if diff > 0 else -1
    d = ref_date
    while calculate_kin(d).kin != target_kin:
        d += timedelta(days=step)
    return d


def get_wavespell_dates(target_date: date) -> List[date]:
    """
    Retorna as 13 datas gregorianas correspondentes aos 13 Kins da Onda
    Encantada ativa na target_date (do Tom 1 / Magnético ao Tom 13 / Cósmico).
    Respeita automaticamente a regra 0.0 Hunab Ku (29/Fev).
    """
    d = target_date
    while calculate_kin(d).tone != 0:
        d -= timedelta(days=1)
    base_date = d

    dates = []
    d = base_date
    for tone in range(13):
        while calculate_kin(d).tone != tone:
            d += timedelta(days=1)
        dates.append(d)
        d += timedelta(days=1)
    return dates


# Nomes em português para formatação de datas gregorianas
WEEKDAYS_PT = [
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo"
]

MONTHS_PT = [
    "", "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]


def format_date_pt(d: date, include_year: bool = True) -> str:
    """Retorna data por extenso em português: ex: 'segunda-feira, 19 de outubro de 2026'."""
    weekday = WEEKDAYS_PT[d.weekday()]
    month = MONTHS_PT[d.month]
    if include_year:
        return f"{weekday}, {d.day} de {month} de {d.year}"
    return f"{weekday}, {d.day} de {month}"


# ---------------------------------------------------------------------------
# NS Date (Novo Sincronário / 13 Luas de 28 Dias)
# ---------------------------------------------------------------------------

def _ns_year_start(ns_year: int) -> date:
    """Retorna a data gregoriana do primeiro dia do ano NS dado."""
    greg_year = 1987 + ns_year
    return date(greg_year, 7, 26)


def calculate_ns_date(target: date) -> NSSyncDate:
    """
    Converte uma data gregoriana para o formato Novo Sincronário.

    Estrutura do ano NS:
      - Ano NS começa em 26 de julho (gregoriano)
      - NS1.0 = 26/Jul/1987 a 25/Jul/1988
      - 13 Luas de 28 dias cada = 364 dias
      - Dia Fora do Tempo (DFT) = 25 de julho (365º dia)
      - Em anos bissextos: 29/Fev = 0.0 Hunab Ku (não conta)
    """
    # Dia Fora do Tempo: 25 de julho
    if target.month == 7 and target.day == 25:
        # O DFT pertence ao ano NS que está terminando
        ns_year = target.year - 1987 - 1
        return NSSyncDate(year=ns_year, moon=0, day=0,
                          is_doot=True, is_hunab_ku=False)

    # 0.0 Hunab Ku: 29 de fevereiro
    if target.month == 2 and target.day == 29:
        # Pertence ao ano NS corrente (que começou em Jul do ano anterior)
        ns_year = target.year - 1987 - 1
        return NSSyncDate(year=ns_year, moon=0, day=0,
                          is_doot=False, is_hunab_ku=True)

    # Determinar o ano NS
    # Se target >= 26/Jul/target.year → ano NS = target.year - 1987
    # Se target < 26/Jul/target.year  → ano NS = target.year - 1987 - 1
    jul26 = date(target.year, 7, 26)
    if target >= jul26:
        ns_year = target.year - 1987
    else:
        ns_year = target.year - 1987 - 1

    year_start = _ns_year_start(ns_year)

    # Contar dias desde o início do ano NS, pulando dias especiais
    day_count = 0
    current = year_start
    while current < target:
        current += timedelta(days=1)
        # Pular 29/Fev (0.0 Hunab Ku)
        if current.month == 2 and current.day == 29:
            continue
        # Pular DFT (25/Jul) — já tratado acima, mas por segurança
        if current.month == 7 and current.day == 25:
            continue
        day_count += 1

    # day_count é o número de dias decorridos desde 26/Jul (0-indexado: 0 a 363)
    moon = (day_count // 28) + 1
    day = (day_count % 28) + 1

    # Sanitizar
    if moon > 13:
        moon = 13
        day = 28

    return NSSyncDate(year=ns_year, moon=moon, day=day,
                      is_doot=False, is_hunab_ku=False)


def date_from_ns_date(ns_year: int, moon: int, day: int) -> date:
    """
    Converte uma coordenada do Sincronário (ano NS, lua 1..13, dia 1..28)
    para a respectiva data gregoriana.
    Leva em consideração o início do ano em 26/Jul e o dia bissexto 29/Fev (0.0 Hunab Ku).
    """
    if moon < 1 or moon > 13 or day < 1 or day > 28:
        raise ValueError(f"Lua ({moon}) ou dia ({day}) inválidos.")

    target_day_index = (moon - 1) * 28 + (day - 1)
    current = _ns_year_start(ns_year)
    days_count = 0
    while days_count < target_day_index:
        current += timedelta(days=1)
        # 29/Fev é 0.0 Hunab Ku e não conta nos 364 dias das 13 Luas
        if current.month == 2 and current.day == 29:
            continue
        days_count += 1
    return current


# ---------------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------------

def kin_for_today() -> KinInfo:
    """Retorna o Kin do dia atual."""
    return calculate_kin(date.today())


def format_kin_name_gender(kin_or_seal: KinInfo | int, tone: Optional[int] = None) -> str:
    """
    Retorna o nome completo com flexão de gênero gramatical correta em português:
    ex: 'Lua Galáctica Vermelha', 'Semente Ressonante Amarela', 'Macaco Cristal Azul',
    'Mão Planetária Azul', 'Terra Ressonante Vermelha'.

    Aceita KinInfo ou (seal_idx, tone_idx).
    """
    from data.seals import get_seal
    from data.tones import get_tone

    if isinstance(kin_or_seal, KinInfo):
        seal_idx = kin_or_seal.seal
        tone_idx = kin_or_seal.tone
    else:
        seal_idx = int(kin_or_seal)
        tone_idx = int(tone) if tone is not None else 0

    seal_data = get_seal(seal_idx)
    tone_data = get_tone(tone_idx)
    seal_name = seal_data['name_short']
    tone_name = tone_data['name']
    color_name = seal_data['color_name']

    # Selos gramaticalmente femininos em português:
    # 2: Noite, 3: Semente, 4: Serpente, 6: Mão, 7: Estrela, 8: Lua, 14: Águia, 16: Terra, 18: Tormenta
    FEMININE_SEALS = {2, 3, 4, 6, 7, 8, 14, 16, 18}

    if seal_idx in FEMININE_SEALS:
        if tone_name.endswith('o'):
            tone_name = tone_name[:-1] + 'a'
        if color_name.endswith('o'):
            color_name = color_name[:-1] + 'a'

    return f"{seal_name} {tone_name} {color_name}"


def full_kin_name(kin_info: KinInfo) -> str:
    """
    Retorna o nome completo do Kin com flexão de gênero gramatical correta em português:
    ex: 'Lua Galáctica Vermelha', 'Mão Planetária Azul', 'Terra Ressonante Vermelha'.
    """
    return format_kin_name_gender(kin_info)


def format_ns_date(ns: NSSyncDate) -> str:
    """Formata a data NS: 'NS1.39.6.18' ou textos especiais para DFT/HK."""
    if ns.is_doot:
        return f"NS1.{ns.year} — Dia Fora do Tempo"
    if ns.is_hunab_ku:
        return f"NS1.{ns.year} — 0.0 Hunab Ku"
    return f"NS1.{ns.year}.{ns.moon}.{ns.day}"


def get_solar_ring(target: date) -> SolarRingInfo:
    """Calcula o Anel Solar (ano e portador do ano) para uma data alvo."""
    ns = calculate_ns_date(target)
    start_date = _ns_year_start(ns.year)
    bearer_kin = calculate_kin(start_date)
    bearer_name = format_kin_name_gender(bearer_kin)
    return SolarRingInfo(
        year_number=ns.year,
        bearer_kin=bearer_kin,
        bearer_name=bearer_name,
        ns_date=ns
    )


def get_crono_psi(target: date) -> Optional[KinInfo]:
    """Retorna o KinInfo da Unidade Crono-Psi para uma data alvo (ou None para DFT)."""
    from data.crono_psi import get_crono_psi_kin
    ns = calculate_ns_date(target)
    kin_num = get_crono_psi_kin(ns.moon, ns.day, is_doot=ns.is_doot)
    if kin_num is None:
        return None
    seal = (kin_num - 1) % 20
    tone = (kin_num - 1) % 13
    return KinInfo(kin=kin_num, seal=seal, tone=tone)


def get_moon_for_date(target: date) -> Optional[dict]:
    """Retorna as informações da Lua atual para a data alvo."""
    from data.moons import get_moon
    ns = calculate_ns_date(target)
    if ns.is_doot or ns.is_hunab_ku or ns.moon < 1:
        return None
    return get_moon(ns.moon)


def get_plasma_for_date(target: date) -> Optional[dict]:
    """Retorna o plasma radial para a data alvo."""
    from data.plasmas import get_plasma_for_day
    ns = calculate_ns_date(target)
    if ns.is_doot or ns.is_hunab_ku or ns.day < 1:
        return None
    return get_plasma_for_day(ns.day)
