```
  __   __ ___            _ _    _                                 _           
 /  \ /  \_  )  ___   __| (_)__| |_    __ _ ___ _ _  ___ _ _ __ _| |_ ___ _ _ 
| () | () / /  |___| / _` | / _|  _|  / _` / -_) ' \/ -_) '_/ _` |  _/ _ \ '_|
 \__/ \__/___|       \__,_|_\__|\__|__\__, \___|_||_\___|_| \__,_|\__\___/_|  
                                  |___|___/                                   
```

Generador de diccionarios de contraseñas personalizados, inspirado en herramientas como **CUPP (Common User Passwords Profiler)**. A partir de datos personales de un objetivo (nombre, fechas, apodos, mascotas, etc.), genera archivos `.txt` con miles de posibles contraseñas para usar en auditorías de seguridad con herramientas como **Hydra**, **John the Ripper** o **Hashcat**.

---

## ⚠️ Uso ético y legal

Esta herramienta fue desarrollada con **fines educativos y de práctica en ciberseguridad ofensiva** (pentesting, CTFs, laboratorios propios).

**No la uses contra sistemas, cuentas o personas sin autorización explícita.** El acceso no autorizado a sistemas informáticos es un delito en la mayoría de los países. El autor no se responsabiliza por el uso indebido de este software.

---

## 🚀 Funcionalidades

- Recolección interactiva de datos personales del objetivo (nombre, apellido, apodo, fechas, pareja, hijo/a, mascota, hobby, palabra clave, números especiales)
- Soporte completo para **ñ** y caracteres especiales
- **3 variantes de leetspeak** por palabra (reemplazo total, reemplazo alternativo con símbolos, y reemplazo parcial de una sola letra)
- Extracción automática de **día, mes y año** desde las fechas de nacimiento ingresadas
- Rango extendido de números: 0-99 y años de 1980 a 2026
- Combinación con símbolos comunes (`! # @ . _ - $ % & *` y combinaciones dobles) en distintas posiciones
- **Combinaciones cruzadas** entre distintas palabras (ej: nombre + mascota + número)
- Filtro de **longitud mínima de 8 caracteres**, sin límite máximo
- Exportación en **dos archivos separados**:
  - `"<nombre> (minimo).txt"` → contraseñas de 8 a 10 caracteres
  - `"<nombre> (maximo).txt"` → contraseñas de más de 10 caracteres
- Comandos de ejemplo listos para usar con Hydra al finalizar

---

## 📦 Instalación

```bash
git clone https://github.com/tu-usuario/diccionario-fuerza-bruta.git
cd diccionario-fuerza-bruta
pip install pyfiglet tqdm
```

## 🛠️ Uso

Ejecutá el script principal y respondé las preguntas sobre el objetivo:

```bash
python3 dict_generator.py
```

Ejemplo de sesión:

```
  __   __ ___            _ _    _                                 _           
 /  \ /  \_  )  ___   __| (_)__| |_    __ _ ___ _ _  ___ _ _ __ _| |_ ___ _ _ 
| () | () / /  |___| / _` | / _|  _|  / _` / -_) ' \/ -_) '_/ _` |  _/ _ \ '_|
 \__/ \__/___|       \__,_|_\__|\__|__\__, \___|_||_\___|_| \__,_|\__\___/_|  
                                  |___|___/                                   

    -------------------------------------------------
     Generador de diccionarios estilo CUPP
     Autor: bsec  |  Version: 1.0
     Uso exclusivo en auditorias autorizadas
    -------------------------------------------------

=== Generador de diccionario (estilo CUPP) ===
Completá los datos que conozcas de la persona objetivo.
Podés dejar en blanco lo que no sepas.

Nombre: Juan
Apellido: Perez
Apodo / nickname: juanp
Fecha de nacimiento (DDMMAAAA): 15031995
...
Nombre base para los archivos de salida (sin extensión): juan

[+] Archivo generado: juan (minimo).txt (249262 contraseñas, hasta 10 caracteres)
[+] Archivo generado: juan (maximo).txt (257051 contraseñas, más de 10 caracteres)
[+] Total combinado: 506313 contraseñas (longitud mínima: 8)
```

---

## 🔗 Integración con herramientas de fuerza bruta

Una vez generados los diccionarios, podés usarlos en pruebas autorizadas:

```bash
# Hydra - SSH
hydra -l usuario -P "juan (minimo).txt" ssh://IP_OBJETIVO

# Hydra - formulario web (login)
hydra -l usuario -P "juan (maximo).txt" IP_OBJETIVO http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=incorrect"

# John the Ripper
john --wordlist="juan (minimo).txt" hash.txt

# Hashcat
hashcat -a 0 -m 0 hash.txt "juan (maximo).txt"
```
