# OneDrop3D — mises à jour

Ce dépôt (`OneDrop3D/mises-a-jour`, **public**) sert les mises à jour des trois
produits tant que le site OneDrop3D n'est pas en ligne :

| fichier | produit | lu par |
|---|---|---|
| `multibook.json` | Multibook | Multibook (`src-tauri/src/maj.rs`) |
| `clickdeck-app.json` | application ClickDeck | ClickDeck (`desktop-app/src/update/UpdateManager.ts`) |
| `clickos.json` | firmware ClickOS | ClickDeck, qui le flashe sur le boîtier |

Les binaires sont attachés aux **releases** de ce dépôt (étiquettes
`multibook-v0.4.0`, `clickdeck-app-v1.14.0`, `clickos-v4.6.0`…). Les
applications lisent `https://raw.githubusercontent.com/OneDrop3D/mises-a-jour/main/<produit>.json`.

## Publier une version

```sh
gh auth login                      # une fois
./publier.py multibook 0.4.0 \
  macos-arm64="../multibook tauri/dist-tauri/Multibook-0.4.0-mac-arm64.dmg" \
  windows-x64="../multibook tauri/dist-tauri/Multibook-0.4.0-windows-x64-installateur.exe" \
  --notes notes-0.4.0.md           # aperçu du manifeste
./publier.py … --publier           # release + manifeste commité et poussé
```

ClickOS : publier le `.zip` produit par `OS-ClickDeck/build.sh` sur la
plateforme `esp32-s3`, avec `--min-app` si le firmware exige une version de
l'application.

## Format (schema 1)

Identique à celui du site (`GET /api/mises-a-jour/<produit>`) — détail dans
`Site web V2/docs/MISES-A-JOUR.md`.

```json
{
  "schema": 1,
  "product": "multibook",
  "channel": "stable",
  "version": "0.4.0",
  "date": "2026-10-26",
  "notes": "Markdown des nouveautés",
  "page": "https://…",
  "minAppVersion": "1.14.0",
  "files": {
    "macos-arm64": { "url": "https://…", "name": "….dmg", "size": 123, "sha256": "64 hex" }
  }
}
```

Les applications interrogent le site **et** GitHub, gardent la version la plus
haute, ne proposent un fichier que s'il porte un SHA-256, et le suppriment si
l'empreinte ne correspond pas après téléchargement.
