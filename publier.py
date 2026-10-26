#!/usr/bin/env python3
r"""
Publie une version d'un produit OneDrop3D sur GitHub.

    ./publier.py multibook 0.4.0 \
        macos-arm64=../multibook\ tauri/dist-tauri/Multibook-0.4.0-mac-arm64.dmg \
        windows-x64=../multibook\ tauri/dist-tauri/Multibook-0.4.0-windows-x64-installateur.exe \
        --notes notes.md            # facultatif : texte des nouveautés
        --publier                   # sans lui, rien ne part : on montre seulement le manifeste

Produits : multibook, clickdeck-app, clickos.
Plateformes : macos-arm64, macos-x64, windows-x64, linux-x64-appimage,
linux-x64-deb, linux-x64-rpm, android-arm64, esp32-s3 (ClickOS : le .zip
produit par OS-ClickDeck/build.sh).

Avec --publier :
  1. les fichiers partent dans une release GitHub de ce dépôt,
     étiquette « <produit>-v<version> » (gh release create) ;
  2. <produit>.json est réécrit avec leurs adresses, tailles et SHA-256 ;
  3. le manifeste est commité et poussé : les applications le voient au plus
     tard cinq minutes après (cache de raw.githubusercontent.com).

Une plateforme absente de cette version garde le fichier de la précédente
(même règle que le site) : publier d'abord macOS ne retire pas Windows.
Format : voir README.md.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

DEPOT = os.environ.get("ONEDROP3D_DEPOT_MAJ", "OneDrop3D/mises-a-jour")
PRODUITS = ("multibook", "clickdeck-app", "clickos")
PLATEFORMES = ("macos-arm64", "macos-x64", "windows-x64", "linux-x64-appimage",
               "linux-x64-deb", "linux-x64-rpm", "android-arm64", "esp32-s3")
ICI = os.path.dirname(os.path.abspath(__file__))


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def version_tuple(v):
    coeur = v.lstrip("vV").split("-")[0]
    return tuple(int(x or 0) for x in coeur.split("."))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("produit", choices=PRODUITS)
    p.add_argument("version")
    p.add_argument("fichiers", nargs="+", help="plateforme=chemin")
    p.add_argument("--notes", help="fichier texte/Markdown des nouveautés")
    p.add_argument("--min-app", help="ClickOS : version minimale de l'application ClickDeck")
    p.add_argument("--publier", action="store_true", help="crée la release et pousse le manifeste")
    a = p.parse_args()

    version = a.version.lstrip("vV")
    etiquette = f"{a.produit}-v{version}"
    fichiers = {}
    for item in a.fichiers:
        plateforme, _, chemin = item.partition("=")
        if plateforme not in PLATEFORMES or not os.path.isfile(chemin):
            sys.exit(f"argument invalide : {item!r} (plateforme inconnue ou fichier absent)")
        nom = os.path.basename(chemin).replace(" ", "-")
        fichiers[plateforme] = {
            "chemin": chemin,
            "url": f"https://github.com/{DEPOT}/releases/download/{etiquette}/{nom}",
            "name": nom,
            "size": os.path.getsize(chemin),
            "sha256": empreinte(chemin),
        }

    cible = os.path.join(ICI, f"{a.produit}.json")
    ancien = {}
    if os.path.exists(cible):
        with open(cible, encoding="utf-8") as f:
            ancien = json.load(f)
        if ancien.get("version") and version_tuple(ancien["version"]) > version_tuple(version):
            sys.exit(f"{a.produit}.json annonce déjà {ancien['version']}, plus récente que {version}")

    manifeste = {
        "schema": 1,
        "product": a.produit,
        "channel": "stable",
        "version": version,
        "date": datetime.date.today().isoformat(),
        "notes": (open(a.notes, encoding="utf-8").read().strip() if a.notes
                  else ancien.get("notes", "") if ancien.get("version") == version else ""),
        "page": f"https://github.com/{DEPOT}/releases/tag/{etiquette}",
        "files": dict(ancien.get("files", {})),
    }
    if a.min_app:
        manifeste["minAppVersion"] = a.min_app
    for plateforme, f in fichiers.items():
        manifeste["files"][plateforme] = {k: f[k] for k in ("url", "name", "size", "sha256")}

    texte = json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n"
    if not a.publier:
        print(texte)
        print("(aperçu seulement : ajoutez --publier pour envoyer)", file=sys.stderr)
        return

    # les noms sans espace sont ceux des URL : gh garde le nom de base du fichier
    renommes = []
    for f in fichiers.values():
        if os.path.basename(f["chemin"]) != f["name"]:
            lien = os.path.join(os.path.dirname(os.path.abspath(f["chemin"])), f["name"])
            if not os.path.exists(lien):
                os.link(f["chemin"], lien)
                renommes.append(lien)
            f["chemin"] = lien
    try:
        existe = subprocess.run(["gh", "release", "view", etiquette, "--repo", DEPOT],
                                capture_output=True).returncode == 0
        if existe:
            # même version, nouveaux systèmes (ou fichier refait) : on complète la release
            subprocess.run(["gh", "release", "upload", etiquette, "--repo", DEPOT, "--clobber",
                            *[f["chemin"] for f in fichiers.values()]], check=True)
        else:
            subprocess.run(["gh", "release", "create", etiquette, "--repo", DEPOT,
                            "--title", f"{a.produit} {version}", "--notes", manifeste["notes"] or etiquette,
                            *[f["chemin"] for f in fichiers.values()]], check=True)
    finally:
        for lien in renommes:
            os.remove(lien)

    with open(cible, "w", encoding="utf-8") as f:
        f.write(texte)
    subprocess.run(["git", "-C", ICI, "add", f"{a.produit}.json"], check=True)
    systemes = ", ".join(fichiers)
    subprocess.run(["git", "-C", ICI, "commit", "-m", f"{a.produit} {version} ({systemes})"], check=True)
    subprocess.run(["git", "-C", ICI, "push"], check=True)
    print(f"{a.produit} {version} publié.")


if __name__ == "__main__":
    main()
