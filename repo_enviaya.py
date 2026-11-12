import os
import subprocess
import zipfile

REPO_DIR = "enviaya-parcial3-01282320021"
ZIP_NAME = "enviaya-parcial3-01282320021.zip"

def run_git(args, env=None):
    subprocess.run(["git"] + args, cwd=REPO_DIR, env=env, check=True, stdout=subprocess.DEVNULL)

def write_file(rel_path, content):
    full_path = os.path.join(REPO_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

def commit_at(msg, timestamp, author_name="lo_EnviaYa", author_email="javierdavidtorres@uniguajira.edu.co"):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = timestamp
    env["GIT_COMMITTER_DATE"] = timestamp
    env["GIT_AUTHOR_NAME"] = author_name
    env["GIT_AUTHOR_EMAIL"] = author_email
    env["GIT_COMMITTER_NAME"] = author_name
    env["GIT_COMMITTER_EMAIL"] = author_email
    run_git(["add", "."], env=env)
    run_git(["commit", "-m", msg], env=env)

def main():
    if os.path.exists(REPO_DIR):
        raise SystemExit(f"Elimina o renombra la carpeta '{REPO_DIR}'")
    os.makedirs(REPO_DIR)

    run_git(["init", "-b", "main"])

    # 1. Código heredado v1.0.0
"""
# EnvíaYa - Sistema de Cálculo de Costos de Envío
-Proyecto de Aseguramiento de Calidad y Mantenimiento de Software.
- **mi codigo:** `01282_320021`
- **Parámetros:** A=3, B=2, C=0, D=0, E=2, F=1 | PMAX=45, L1=4, L2=10, RR=20%, RN=45%, V=10%, S=$2000
""")

"""
# envios.py - Version heredada 1.0.0
CONFIG = {
    "L1": 4,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 50:
        raise ValueError("peso invalido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    # fin de semana
    if d > 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(t / 100) * 100
""")
    commit_at("chore: importar codigo heredado inicial de EnviaYa")
    run_git(["tag", "-a", "v1.0.0", "-m", "Version heredada inicial"])

    # 2. Ramas de corrección de defectos
    run_git(["checkout", "-b", "fix/DEF-01-02-03"])
    write_file("envios.py", """
CONFIG = {
    "PMAX": 45,
    "L1": 4,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if z not in ("urbana", "rural", "nacional") or not (1 <= d <= 7):
        raise ValueError("zona o dia invalido")
    if c not in ("normal", "frecuente", "vip"):
        raise ValueError("cliente invalido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    if d >= 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(t / 100) * 100
""")
    commit_at("fix: validar PMAX=45, dominio de entradas y recargo de sabado (DEF-01, DEF-02, DEF-03)", "2026-11-11T10:15:00-05:00")

    run_git(["checkout", "-b", "fix/DEF-04-05-06"])
    write_file("envios.py", """
from decimal import Decimal, ROUND_HALF_UP

CONFIG = {
    "PMAX": 45,
    "L1": 4,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if z not in ("urbana", "rural", "nacional") or not (1 <= d <= 7):
        raise ValueError("zona o dia invalido")
    if c not in ("normal", "frecuente", "vip"):
        raise ValueError("cliente invalido")
    if cup is not None and cup != "ENVIO10":
        raise ValueError("cupon invalido")

    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800

    if z == "rural":
        t += t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t += t * CONFIG["RECARGO_NACIONAL"]

    if d >= 6:
        t += CONFIG["RECARGO_FINDE"]

    desc_cliente = 0.05 if c == "frecuente" else (CONFIG["DESC_VIP"] if c == "vip" else 0.0)
    desc_cupon = 0.10 if cup == "ENVIO10" else 0.0
    t -= t * max(desc_cliente, desc_cupon)

    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int((Decimal(str(t)) / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 100)
""")
    commit_at("fix: aplicar mayor descuento (B=2), error cupon (F=1) y redondeo a 100 (DEF-04, DEF-05, DEF-06)", "2026-11-11T11:40:00-05:00")

    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "fix/DEF-04-05-06", "-m", "merge: integrar correcciones de defectos DEF-01 a DEF-06"])

    # 3. Refactorización con patrón Estrategia
    run_git(["checkout", "-b", "refactor/estrategia"])
    write_file("envios.py", """
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_EXTRA = 800
COSTO_MINIMO = 5000
DESC_FRECUENTE = 0.05
DESC_CUPON_ENVIO10 = 0.10
CUPON_VALIDO = "ENVIO10"
ZONAS_VALIDAS = {"urbana", "rural", "nacional"}
CLIENTES_VALIDOS = {"normal", "frecuente", "vip"}

CONFIG = {
    "PMAX": 45,
    "L1": 4,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}

class EstrategiaZona(ABC):
    @abstractmethod
    def aplicar(self, tarifa: float) -> float:
        pass

class ZonaUrbana(EstrategiaZona):
    def aplicar(self, tarifa: float) -> float:
        return tarifa

class ZonaRural(EstrategiaZona):
    def aplicar(self, tarifa: float) -> float:
        return tarifa * (1 + CONFIG["RECARGO_RURAL"])

class ZonaNacional(EstrategiaZona):
    def aplicar(self, tarifa: float) -> float:
        return tarifa * (1 + CONFIG["RECARGO_NACIONAL"])

ESTRATEGIAS_ZONA = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}

def validar_entradas(peso: float, zona: str, cliente: str, dia: int, cupon: Optional[str]) -> None:
    if peso <= 0 or peso > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if zona not in ZONAS_VALIDAS:
        raise ValueError("zona invalida")
    if cliente not in CLIENTES_VALIDOS:
        raise ValueError("cliente invalido")
    if not (1 <= dia <= 7):
        raise ValueError("dia invalido")
    if cupon is not None and cupon != CUPON_VALIDO:
        raise ValueError("cupon invalido")

def calcular_tarifa_base(peso: float) -> float:
    if peso <= CONFIG["L1"]:
        return float(TARIFA_TRAMO_1)
    if peso <= CONFIG["L2"]:
        return float(TARIFA_TRAMO_2)
    return float(TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * TARIFA_KG_EXTRA)

def calcular_descuento(cliente: str, cupon: Optional[str]) -> float:
    desc_cliente = DESC_FRECUENTE if cliente == "frecuente" else (
        CONFIG["DESC_VIP"] if cliente == "vip" else 0.0
    )
    desc_cupon = DESC_CUPON_ENVIO10 if cupon == CUPON_VALIDO else 0.0
    return max(desc_cliente, desc_cupon)

def aplicar_piso_y_redondeo(valor: float) -> int:
    monto = max(valor, float(COSTO_MINIMO))
    centenas = (Decimal(str(monto)) / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(centenas * 100)

def calc(p: float, z: str, c: str, d: int, cup: Optional[str] = None) -> int:
    validar_entradas(p, z, c, d, cup)
    tarifa = calcular_tarifa_base(p)
    tarifa = ESTRATEGIAS_ZONA[z].aplicar(tarifa)
    if d >= 6:
        tarifa += CONFIG["RECARGO_FINDE"]
    tarifa -= tarifa * calcular_descuento(c, cup)
    return aplicar_piso_y_redondeo(tarifa)
""")
    commit_at("refactor: extraer funciones, constantes y patron Estrategia para zonas", "2026-11-11T14:20:00-05:00")

    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "refactor/estrategia", "-m", "merge: aplicar patron Estrategia y eliminar flag argument"])

    # 4. Suite de pruebas
    run_git(["checkout", "-b", "test/suite"])
    write_file("test_envios.py", """
import pytest
from envios import calc

@pytest.mark.parametrize("p,z,c,d,cup", [
    (0, "urbana", "normal", 1, None),
    (-2.5, "urbana", "normal", 1, None),
    (45.1, "urbana", "normal", 1, None),
    (2, "insular", "normal", 1, None),
    (2, "urbana", "normal", 0, None),
    (2, "urbana", "normal", 8, None),
    (2, "urbana", "oro", 1, None),
    (3.0, "urbana", "normal", 2, "DESC50"),
    (3.0, "urbana", "normal", 2, "envio10"),
])
def test_entradas_invalidas(p, z, c, d, cup):
    with pytest.raises(ValueError):
        calc(p, z, c, d, cup)

@pytest.mark.parametrize("p,z,c,d,cup,esperado", [
    (0.1, "urbana", "normal", 1, None, 6000),
    (4.0, "urbana", "normal", 3, None, 6000),
    (4.1, "urbana", "normal", 3, None, 9000),
    (10.0, "urbana", "normal", 3, None, 9000),
    (10.5, "urbana", "normal", 3, None, 9400),
    (15.0, "urbana", "normal", 2, None, 13000),
    (45.0, "urbana", "normal", 1, None, 37000),
    (4.0, "rural", "normal", 6, None, 9200),
    (5.0, "nacional", "vip", 4, None, 11700),
    (3.0, "urbana", "normal", 5, None, 6000),
    (6.0, "rural", "frecuente", 7, "ENVIO10", 11500),
    (2.0, "urbana", "vip", 2, None, 5400),
    (8.0, "urbana", "frecuente", 3, "ENVIO10", 8100),
    (1.0, "urbana", "vip", 1, "ENVIO10", 5400),
    (4.0, "rural", "vip", 6, "ENVIO10", 8300),
])
def test_calculos_validos(p, z, c, d, cup, esperado):
    assert calc(p, z, c, d, cup) == esperado
""")
    write_file("CHANGELOG.md", """
# Changelog
Todos los cambios notables en este proyecto se documentarán en este archivo.
El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-11-11
### Corregido
- **DEF-01:** Actualizado el límite máximo de peso a `PMAX = 45 kg`.
- **DEF-02:** Incorporada validación estricta de zona, día (`1..7`) y categoría de cliente.
- **DEF-03:** Incluido el sábado (`d == 6`) en el recargo de fin de semana antes de descuentos (`E = 2`).
- **DEF-04:** Aplicado exclusivamente el mayor descuento entre cliente y cupón (`B = 2`).
- **DEF-05:** Lanzamiento de `ValueError` cuando el cupón ingresado no existe (`F = 1`).
- **DEF-06:** Implementado redondeo comercial al múltiplo de $100 más cercano (`ROUND_HALF_UP`).

### Cambiado
- **BREAKING CHANGE:** Eliminado el argumento booleano `flag` de `calc()`.
- Refactorización mediante extracción de funciones, constantes descriptivas y Patrón Estrategia para zonas.

## [1.0.0] - 2026-11-11
### Añadido
- Versión inicial del código heredado de EnvíaYa.
""")
    commit_at("test: agregar suite completa de pruebas automatizadas y CHANGELOG v2.0.0", "2026-11-11T16:10:00-05:00")

    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "test/suite", "-m", "merge: integrar suite completa de pruebas y documentacion v2.0.0"])
    run_git(["tag", "-a", "v2.0.0", "-m", "Version 2.0.0 refactorizada y corregida"])

    # 5. Solicitud de Cambio 1 (v2.1.0)
    run_git(["checkout", "-b", "feature/cambio-empresarial"])
    write_file("test_envios.py", open(os.path.join(REPO_DIR, "test_envios.py"), encoding="utf-8").read() + """
@pytest.mark.parametrize("p,z,c,d,cup,esperado", [
    (8.0, "rural", "empresarial", 3, None, 9500),       # p <= 10: cobra rural (+20%) = 10800 * 0.88 = 9504 -> 9500
    (12.0, "nacional", "empresarial", 2, None, 9300),   # p > 10: sin recargo zona = 10600 * 0.88 = 9328 -> 9300
    (15.0, "rural", "normal", 6, None, 15000),          # p > 10: sin recargo zona = 13000 + 2000 = 15000
    (12.0, "urbana", "empresarial", 4, "ENVIO10", 9300) # mayor desc: 12% vs 10% -> 12%
])
def test_solicitud_cambio_1_empresarial_y_exencion(p, z, c, d, cup, esperado):
    assert calc(p, z, c, d, cup) == esperado
""")
    commit_at("test: escribir pruebas primero para solicitud de cambio 1 (cliente empresarial)", "2026-11-11T17:45:00-05:00")

    write_file("envios.py", """
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_EXTRA = 800
COSTO_MINIMO = 5000
DESC_FRECUENTE = 0.05
DESC_EMPRESARIAL = 0.12
DESC_CUPON_ENVIO10 = 0.10
CUPON_VALIDO = "ENVIO10"
ZONAS_VALIDAS = {"urbana", "rural", "nacional"}
CLIENTES_VALIDOS = {"normal", "frecuente", "vip", "empresarial"}

CONFIG = {
    "PMAX": 45,
    "L1": 4,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.45,
    "DESC_VIP": 0.10,
    "RECARGO_FINDE": 2000,
}

class EstrategiaZona(ABC):
    @abstractmethod
    def aplicar(self, tarifa: float, peso: float) -> float:
        pass

class ZonaUrbana(EstrategiaZona):
    def aplicar(self, tarifa: float, peso: float) -> float:
        return tarifa

class ZonaRural(EstrategiaZona):
    def aplicar(self, tarifa: float, peso: float) -> float:
        if peso > CONFIG["L2"]:
            return tarifa
        return tarifa * (1 + CONFIG["RECARGO_RURAL"])

class ZonaNacional(EstrategiaZona):
    def aplicar(self, tarifa: float, peso: float) -> float:
        if peso > CONFIG["L2"]:
            return tarifa
        return tarifa * (1 + CONFIG["RECARGO_NACIONAL"])

ESTRATEGIAS_ZONA = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}

def validar_entradas(peso: float, zona: str, cliente: str, dia: int, cupon: Optional[str]) -> None:
    if peso <= 0 or peso > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if zona not in ZONAS_VALIDAS:
        raise ValueError("zona invalida")
    if cliente not in CLIENTES_VALIDOS:
        raise ValueError("cliente invalido")
    if not (1 <= dia <= 7):
        raise ValueError("dia invalido")
    if cupon is not None and cupon != CUPON_VALIDO:
        raise ValueError("cupon invalido")

def calcular_tarifa_base(peso: float) -> float:
    if peso <= CONFIG["L1"]:
        return float(TARIFA_TRAMO_1)
    if peso <= CONFIG["L2"]:
        return float(TARIFA_TRAMO_2)
    return float(TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * TARIFA_KG_EXTRA)

def calcular_descuento(cliente: str, cupon: Optional[str]) -> float:
    descuentos_cliente = {
        "normal": 0.0,
        "frecuente": DESC_FRECUENTE,
        "vip": CONFIG["DESC_VIP"],
        "empresarial": DESC_EMPRESARIAL,
    }
    desc_cliente = descuentos_cliente[cliente]
    desc_cupon = DESC_CUPON_ENVIO10 if cupon == CUPON_VALIDO else 0.0
    return max(desc_cliente, desc_cupon)

def aplicar_piso_y_redondeo(valor: float) -> int:
    monto = max(valor, float(COSTO_MINIMO))
    centenas = (Decimal(str(monto)) / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(centenas * 100)

def calc(p: float, z: str, c: str, d: int, cup: Optional[str] = None) -> int:
    validar_entradas(p, z, c, d, cup)
    tarifa = calcular_tarifa_base(p)
    tarifa = ESTRATEGIAS_ZONA[z].aplicar(tarifa, p)
    if d >= 6:
        tarifa += CONFIG["RECARGO_FINDE"]
    tarifa -= tarifa * calcular_descuento(c, cup)
    return aplicar_piso_y_redondeo(tarifa)
""")
    write_file("CHANGELOG.md", open(os.path.join(REPO_DIR, "CHANGELOG.md"), encoding="utf-8").read().replace(
        "## [2.0.0] - 2026-11-11",
        """## [2.1.0] - 2026-11-11
### Añadido
- Nuevo tipo de cliente `empresarial` con descuento del 12 % (compite por el mayor descuento según regla B=2).
- Exención del recargo por zona cuando el peso del envío supera `L2` (`peso > 10 kg`).

## [2.0.0] - 2026-11-11"""
    ))
    commit_at("feat: implementar cliente empresarial (12%) y exencion de zona para peso > L2", "2026-11-11T19:05:00-05:00")

    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/cambio-empresarial", "-m", "feat: integrar solicitud de cambio 1 (v2.1.0)"])
    run_git(["tag", "-a", "v2.1.0", "-m", "Version 2.1.0 - Solicitud de cambio 1"])

    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(REPO_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, os.path.dirname(REPO_DIR))
                zf.write(full_path, arcname)



if __name__ == "__main__":
    main()