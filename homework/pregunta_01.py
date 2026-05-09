"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    import re
    import pandas as pd

    ruta = "files/input/clusters_report.txt"

    registros = []
    registro_actual = None
    leyendo_datos = False

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip()

            if linea.strip().startswith("---"):
                leyendo_datos = True
                continue

            if not leyendo_datos or not linea.strip():
                continue

            patron = r"^\s*(\d+)\s+(\d+)\s+([\d,\.]+)\s*%\s+(.*)$"
            coincidencia = re.match(patron, linea)

            if coincidencia:
                if registro_actual is not None:
                    registros.append(registro_actual)

                registro_actual = {
                    "cluster": int(coincidencia.group(1)),
                    "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        coincidencia.group(3).replace(",", ".")
                    ),
                    "principales_palabras_clave": coincidencia.group(4).strip(),
                }

            else:
                if registro_actual is not None:
                    registro_actual["principales_palabras_clave"] += (
                        " " + linea.strip()
                    )

    if registro_actual is not None:
        registros.append(registro_actual)

    dT = pd.DataFrame(registros)

    dT["principales_palabras_clave"] = (
        dT["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.strip()
        .str.rstrip(".")
    )

    return dT
