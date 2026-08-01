# (002) Diccionario Fuerza Bruta (Wordlist Profiler)

Generador de diccionarios de contraseñas personalizados, inspirado en herramientas como **CUPP (Common User Passwords Profiler)**. A partir de datos personales de un objetivo (nombre, fechas, apodos, mascotas, etc.), genera un archivo `.txt` con posibles contraseñas para usar en auditorías de seguridad con herramientas como **Hydra**, **John the Ripper** o **Hashcat**.

---

## ⚠️ Uso ético y legal

Esta herramienta fue desarrollada con **fines educativos y de práctica en ciberseguridad ofensiva** (pentesting, CTFs, laboratorios propios).

**No la uses contra sistemas, cuentas o personas sin autorización explícita.** El acceso no autorizado a sistemas informáticos es un delito en la mayoría de los países. El autor no se responsabiliza por el uso indebido de este software.

---

## 🚀 Características

- Recolección interactiva de datos personales del objetivo
- Generación de variantes: mayúsculas, minúsculas, capitalización, leetspeak
- Combinación con años extraídos de fechas de nacimiento
- Inserción de números y símbolos comunes
- Exportación a diccionario `.txt` listo para usar
- Ejemplos de integración directa con Hydra

---

## 📦 Instalación

```bash
git clone https://github.com/tu-usuario/diccionario-fuerza-bruta.git
cd diccionario-fuerza-bruta
pip install -r requirements.txt
```

Requiere Python 3.8 o superior. No tiene dependencias externas por el momento (usa solo librerías estándar de Python).

---

## 🛠️ Uso

Ejecutá el script principal y respondé las preguntas sobre el objetivo:

```bash
python3 src/dict_generator/main.py
```

Ejemplo de sesión:

```
=== Generador de diccionario (estilo CUPP) ===
Completá los datos que conozcas de la persona objetivo.
Podés dejar en blanco lo que no sepas.

Nombre: Juan
Apellido: Perez
Apodo / nickname: juanp
Fecha de nacimiento (DDMMAAAA): 15031995
Nombre de la pareja: Maria
...

[+] Diccionario generado: diccionario.txt
[+] Total de contraseñas candidatas: 842
```

Esto genera un archivo `diccionario.txt` con las contraseñas candidatas.

---

## 🔗 Integración con Hydra

Una vez generado el diccionario, podés usarlo para pruebas de fuerza bruta autorizadas:

```bash
# SSH
hydra -l usuario -P diccionario.txt ssh://IP_OBJETIVO

# Formulario web (login)
hydra -l usuario -P diccionario.txt IP_OBJETIVO http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=incorrect"

# FTP
hydra -l usuario -P diccionario.txt ftp://IP_OBJETIVO
```

También compatible con **John the Ripper** y **Hashcat** en modo diccionario:

```bash
john --wordlist=diccionario.txt hash.txt
hashcat -a 0 -m 0 hash.txt diccionario.txt
```

