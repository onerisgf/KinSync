"""
Módulo de dados do Crono-Psi (Unidade Psi-Crono) para o KinSync.
Contém a tabela oficial de 365 dias do Banco Psi (Lei do Tempo / Noosfera)
alinhada aos 364 dias das 13 Luas mais o Dia Fora do Tempo (25 de Julho).
"""

from typing import Optional

# Tabela oficial de 365 dias do Banco Psi (13 Luas x 28 dias = 364 dias + 1 Dia Fora do Tempo)
# Cada elemento é o número do Kin (1..260) ou None para o Dia Fora do Tempo (dia 365).
CRONO_PSI_TABLE = [
    # Lua 1 (Magnética)
    1, 1, 1, 20, 20, 20, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 241, 241, 241, 260, 260, 260,
    # Lua 2 (Lunar)
    22, 22, 22, 39, 39, 39, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 222, 222, 222, 239, 239, 239,
    # Lua 3 (Elétrica)
    43, 43, 43, 58, 58, 58, 36, 37, 38, 40, 41, 42, 44, 45, 46, 47, 48, 49, 52, 53, 54, 55, 203, 203, 203, 218, 218, 218,
    # Lua 4 (Autoexistente)
    50, 50, 50, 51, 51, 51, 56, 57, 59, 60, 61, 62, 63, 65, 66, 67, 68, 70, 71, 73, 74, 75, 210, 210, 210, 211, 211, 211,
    # Lua 5 (Harmônica)
    64, 64, 64, 77, 77, 77, 76, 78, 79, 80, 81, 82, 83, 84, 86, 87, 89, 90, 91, 92, 94, 95, 184, 184, 184, 197, 197, 197,
    # Lua 6 (Rítmica)
    69, 69, 69, 72, 72, 72, 97, 98, 99, 100, 101, 102, 103, 104, 105, 116, 117, 118, 119, 120, 121, 122, 189, 189, 189, 192, 192, 192,
    # Lua 7 (Ressonante)
    85, 85, 85, 96, 96, 96, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 165, 165, 165, 176, 176, 176,
    # Lua 8 (Galáctica)
    88, 88, 88, 93, 93, 93, 139, 140, 141, 142, 143, 144, 145, 156, 157, 158, 159, 160, 161, 162, 163, 164, 168, 168, 168, 173, 173, 173,
    # Lua 9 (Solar)
    106, 106, 106, 115, 115, 115, 166, 167, 169, 170, 171, 172, 174, 175, 177, 178, 179, 180, 181, 182, 183, 185, 146, 146, 146, 155, 155, 155,
    # Lua 10 (Planetária)
    107, 107, 107, 114, 114, 114, 186, 187, 188, 190, 191, 193, 194, 195, 196, 198, 199, 200, 201, 202, 204, 205, 147, 147, 147, 154, 154, 154,
    # Lua 11 (Espectral)
    108, 108, 108, 113, 113, 113, 206, 207, 208, 209, 212, 213, 214, 215, 216, 217, 219, 220, 221, 223, 224, 225, 148, 148, 148, 153, 153, 153,
    # Lua 12 (Cristal)
    109, 109, 109, 112, 112, 112, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 240, 242, 243, 149, 149, 149, 152, 152, 152,
    # Lua 13 (Cósmica)
    110, 110, 110, 111, 111, 111, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 150, 150, 150, 151, 151, 151,
    # Dia Fora do Tempo (25 de Julho)
    None
]


def get_crono_psi_kin(moon: int, day: int, is_doot: bool = False) -> Optional[int]:
    """
    Retorna o número do Kin (1..260) do Crono-Psi para um dia de uma Lua (1..13, 1..28).
    Para o Dia Fora do Tempo (is_doot=True), retorna None.
    """
    if is_doot:
        return None
    if moon < 1 or moon > 13 or day < 1 or day > 28:
        return None
    day_of_year = (moon - 1) * 28 + day
    idx = day_of_year - 1
    if 0 <= idx < len(CRONO_PSI_TABLE):
        return CRONO_PSI_TABLE[idx]
    return None
