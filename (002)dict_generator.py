import itertools
import re

try:
    import pyfiglet
    TIENE_PYFIGLET = True
except ImportError:
    TIENE_PYFIGLET = False

# ---------------------------------------------------------
# Colores ANSI (si la terminal no los soporta, simplemente
# se ven como texto plano, no rompe nada)
# ---------------------------------------------------------

class Color:
    ROJO = '\033[91m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    CIAN = '\033[96m'
    GRIS = '\033[90m'
    NEGRITA = '\033[1m'
    FIN = '\033[0m'


def mostrar_banner():
    titulo = "002 - dict_generator"

    if TIENE_PYFIGLET:
        arte = pyfiglet.figlet_format(titulo, font='small', width=200)
    else:
        # Respaldo simple por si no está instalado pyfiglet
        arte = f"=== {titulo} ===\n"

    print(f"{Color.CIAN}{Color.NEGRITA}{arte}{Color.FIN}")
    print(f"{Color.GRIS}    -------------------------------------------------")
    print(f"     Generador de diccionarios para bruteforce")
    print(f"     Autor: bsec  |  Version: 1.0")
    print(f"     Uso exclusivo en auditorias autorizadas")
    print(f"    -------------------------------------------------{Color.FIN}\n")


# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------

def limpiar(texto: str) -> str:
    """Quita espacios raros pero conserva letras, números y ñ."""
    return re.sub(r'[^a-zA-Z0-9ñÑ]', '', texto.strip())


def leet_variantes(palabra: str) -> set:
    """Genera varias variantes leetspeak de una palabra (no solo una)."""
    mapa = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'b': ['8'],
        'g': ['9'],
        'l': ['1'],
        'ñ': ['n'],
    }

    base = palabra.lower()
    variantes = {base}

    # Variante 1: reemplazo simple (una sola sustitución por letra, todas juntas)
    simple = list(base)
    for i, ch in enumerate(simple):
        if ch in mapa:
            simple[i] = mapa[ch][0]
    variantes.add(''.join(simple))

    # Variante 2: reemplazo alternativo (usa la segunda opción si existe)
    alterna = list(base)
    for i, ch in enumerate(alterna):
        if ch in mapa and len(mapa[ch]) > 1:
            alterna[i] = mapa[ch][1]
        elif ch in mapa:
            alterna[i] = mapa[ch][0]
    variantes.add(''.join(alterna))

    # Variante 3: solo la primera vocal reemplazada (mutación parcial, típica de contraseñas reales)
    for i, ch in enumerate(base):
        if ch in mapa:
            parcial = base[:i] + mapa[ch][0] + base[i + 1:]
            variantes.add(parcial)
            break

    return variantes


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
    """De una fecha DDMMAAAA extrae variantes de año, día y mes."""
    piezas = []
    if len(fecha) == 8 and fecha.isdigit():
        dia, mes, anio_completo = fecha[0:2], fecha[2:4], fecha[4:]
        anio_corto = anio_completo[2:]
        piezas.extend([anio_completo, anio_corto, dia, mes, dia + mes, mes + anio_corto])
    return piezas


def generar_diccionario(datos: dict) -> set:
    palabras_base = set()

    # Números base + rango ampliado de años y números comunes
    numeros = {'', '1', '12', '123', '1234', '12345', '01', '007',
               '69', '99', '00'}
    numeros.update(str(n) for n in range(0, 100))          # 0-99
    numeros.update(str(n) for n in range(1980, 2027))       # años de nacimiento probables

    # Campos de texto a combinar
    campos_texto = ['nombre', 'apellido', 'apodo', 'pareja',
                     'hijo', 'mascota', 'equipo', 'palabra_clave']

    for campo in campos_texto:
        valor = limpiar(datos.get(campo, ''))
        if valor:
            palabras_base.add(valor.lower())
            palabras_base.add(valor.capitalize())
            palabras_base.add(valor.upper())
            palabras_base.update(leet_variantes(valor))

    # Combinaciones entre nombre y apellido
    nombre = limpiar(datos.get('nombre', ''))
    apellido = limpiar(datos.get('apellido', ''))
    if nombre and apellido:
        combos_nombre = [
            (nombre + apellido).lower(),
            (apellido + nombre).lower(),
            (nombre[0] + apellido).lower(),
            (apellido[0] + nombre).lower(),
            (nombre + '.' + apellido).lower(),
            (nombre + '_' + apellido).lower(),
        ]
        for c in combos_nombre:
            palabras_base.add(c)
            palabras_base.update(leet_variantes(c))

    # Años, días y meses extraídos de las fechas
    for campo_fecha in ['fecha_nac', 'fecha_pareja']:
        for pieza in extraer_anios(datos.get(campo_fecha, '')):
            numeros.add(pieza)

    # Números especiales ingresados manualmente
    extras = datos.get('numeros_extra', '')
    if extras:
        for n in extras.split(','):
            n = n.strip()
            if n:
                numeros.add(n)

    # Símbolos y caracteres especiales ampliados
    simbolos = ['', '!', '#', '@', '.', '_', '-', '$', '%', '&', '*', '!!', '??', '.-']

    resultado = set()

    for palabra in palabras_base:
        for numero in numeros:
            for simbolo in simbolos:
                resultado.add(f"{palabra}{numero}{simbolo}")
                resultado.add(f"{palabra}{simbolo}{numero}")
                resultado.add(f"{simbolo}{palabra}{numero}")
                resultado.add(f"{numero}{palabra}{simbolo}")

    # Combinaciones dobles: palabra + palabra (ej: nombre + mascota)
    lista_palabras = list(palabras_base)
    for p1, p2 in itertools.permutations(lista_palabras, 2):
        for numero in list(numeros)[:15]:  # limitar para no explotar demasiado
            resultado.add(f"{p1}{p2}{numero}")
            resultado.add(f"{p1}{numero}{p2}")

    resultado.update(palabras_base)
    resultado.update(n for n in numeros if n)

    return resultado


# ---------------------------------------------------------
# Filtrado y guardado
# ---------------------------------------------------------

def guardar_diccionarios(palabras: set, nombre_base: str, longitud_minima: int = 8,
                          umbral_corte: int = 10):
    """
    Filtra por longitud mínima y separa en dos archivos:
    - "<nombre_base> (minimo).txt"  -> longitud entre longitud_minima y umbral_corte
    - "<nombre_base> (maximo).txt"  -> longitud mayor a umbral_corte
    """
    filtradas = [p for p in palabras if p and len(p) >= longitud_minima]
    filtradas.sort(key=len)

    cortas = [p for p in filtradas if len(p) <= umbral_corte]
    largas = [p for p in filtradas if len(p) > umbral_corte]

    archivo_min = f"{nombre_base} (minimo).txt"
    archivo_max = f"{nombre_base} (maximo).txt"

    with open(archivo_min, 'w', encoding='utf-8') as f:
        for p in cortas:
            f.write(p + '\n')

    with open(archivo_max, 'w', encoding='utf-8') as f:
        for p in largas:
            f.write(p + '\n')

    print(f"\n[+] Archivo generado: {archivo_min} ({len(cortas)} contraseñas, hasta {umbral_corte} caracteres)")
    print(f"[+] Archivo generado: {archivo_max} ({len(largas)} contraseñas, más de {umbral_corte} caracteres)")
    print(f"[+] Total combinado: {len(filtradas)} contraseñas (longitud mínima: {longitud_minima})")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    mostrar_banner()
    datos = recolectar_datos()
    diccionario = generar_diccionario(datos)
    nombre_base = preguntar("\nNombre base para los archivos de salida (sin extensión): ") or "diccionario"
    guardar_diccionarios(diccionario, nombre_base, longitud_minima=8, umbral_corte=10)

    print("\n--- Ejemplo de uso con Hydra (solo en entornos autorizados) ---")
    print(f'hydra -l usuario -P "{nombre_base} (minimo).txt" ssh://IP_OBJETIVO')
    print(f'hydra -l usuario -P "{nombre_base} (maximo).txt" ssh://IP_OBJETIVO')


if __name__ == "__main__":
    main()