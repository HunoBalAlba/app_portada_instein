"""
Utilidades auxiliares para manipulación de colores.
"""


def invertir_color_hexadecimal(color_hexadecimal: str) -> str:
    """
    Invierte un color hexadecimal (ej: '#9ebae4' → '#61451b').

    Args:
        color_hexadecimal: Color en formato #RRGGBB.

    Returns:
        Color invertido en el mismo formato.

    Raises:
        ValueError: Si el color no tiene 6 dígitos hexadecimales.
    """
    codigo = color_hexadecimal.strip().lstrip("#")
    if len(codigo) != 6:
        raise ValueError("Se esperaba un color de 6 dígitos como #RRGGBB")

    rojo = 255 - int(codigo[0:2], 16)
    verde = 255 - int(codigo[2:4], 16)
    azul = 255 - int(codigo[4:6], 16)
    return f"#{rojo:02x}{verde:02x}{azul:02x}"
