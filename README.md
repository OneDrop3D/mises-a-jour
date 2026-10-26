# OneDrop3D — construire, publier et mettre à jour

Ce dépôt est le **point de distribution** des trois produits OneDrop3D. Ce guide explique,
étape par étape, où se trouve chaque chose, comment construire une nouvelle version pour
chaque système, et comment la livrer aux utilisateurs.

| Produit | Ce que c'est | Systèmes |
|---|---|---|
| **Multibook** | l'application de notes (cahiers, intercalaires, feuilles) | macOS, Windows, Linux, Android |
| **Application ClickDeck** | le logiciel qui configure et pilote le boîtier | macOS, Windows, Linux |
| **ClickOS** | le firmware du boîtier ClickDeck (ESP32-S3) | flashé par l'application ClickDeck |

---

## 1. Où sont les choses

### Sur GitHub (compte `OneDrop3D`)

| Dépôt | Visibilité | Contenu |
|---|---|---|
| [`OneDrop3D/multibook`](https://github.com/OneDrop3D/multibook) | privé | code de Multibook ; GitHub Actions y construit la version Linux |
| [`OneDrop3D/clickdeck`](https://github.com/OneDrop3D/clickdeck) | privé | code de l'application ClickDeck et du firmware ClickOS ; GitHub Actions y construit Windows et Linux |
| [`OneDrop3D/mises-a-jour`](https://github.com/OneDrop3D/mises-a-jour) | **public** | ce guide, les manifestes (`multibook.json`, `clickdeck-app.json`, `clickos.json`) et, dans les *Releases*, les installeurs |
| [`OneDrop3D/site-web`](https://github.com/OneDrop3D/site-web) | — | le site OneDrop3D (boutique, téléchargements, API de mises à jour) |

Le dépôt `mises-a-jour` doit rester **public** : les applications le lisent sans compte.
Les dépôts de code peuvent rester privés.

### Sur le Mac

| Dossier | Contenu |
|---|---|
| `~/Desktop/Application/multibook tauri/` | Multibook (dépôt `OneDrop3D/multibook`) |
| `~/Desktop/Application/Clickdeck travail/VA/app/` | ClickDeck : `desktop-app/` (application), `OS-ClickDeck/` (firmware) — dépôt `OneDrop3D/clickdeck` |
| `~/Desktop/Application/mises-a-jour/` | ce dépôt-ci, avec le script `publier.py` |
| `~/Desktop/Site web V2/` | le site (dépôt `OneDrop3D/site-web`) |
| `~/Desktop/Application/.backups/` | archives faites avant les grosses modifications |

### Où sortent les fichiers construits

| Produit | Système | Fichier produit |
|---|---|---|
| Multibook | macOS | `multibook tauri/dist-tauri/Multibook-<version>-mac-arm64.dmg` |
| Multibook | Windows | `multibook tauri/dist-tauri/Multibook-<version>-windows-x64-installateur.exe` |
| Multibook | Android | `multibook tauri/dist-tauri/Multibook-<version>-android.apk` |
| Multibook | Linux | artefact `multibook-linux` de GitHub Actions (`.AppImage`, `.deb`, `.rpm`) |
| ClickDeck | macOS | `desktop-app/dist/Clickdeck-<version>-arm64.dmg` |
| ClickDeck | Windows | artefact `clickdeck-windows` de GitHub Actions (`.exe`) |
| ClickDeck | Linux | artefact `clickdeck-linux` de GitHub Actions (`.AppImage`, `.deb`, `.rpm`) |
| ClickOS | boîtier | `desktop-app/react-app/public/firmware/clickos-v<version>.zip` |

---

## 2. Préparer le Mac (une seule fois)

1. **GitHub en ligne de commande** : `brew install gh`, puis `gh auth login` (compte
   `OneDrop3D`, protocole HTTPS). Vérifier avec `gh auth status`.
2. **Rust** (Multibook) : les outils sont dans `/opt/homebrew/opt/rustup/bin` et `~/.cargo/bin`.
   Dans chaque terminal où l'on construit Multibook :
   ```sh
   export PATH=/opt/homebrew/opt/rustup/bin:$HOME/.cargo/bin:$PATH
   ```
3. **Windows depuis le Mac** (Multibook) : LLVM et LLD de Homebrew (`brew install llvm lld`) et
   `cargo install cargo-xwin` ; `build.sh` règle le reste.
4. **Android** (Multibook) : Android Studio (SDK dans `~/Library/Android/sdk`, NDK 28) et un
   JDK 21 dans `~/.jdks/` — le JDK 25 du système est trop récent pour Gradle. `build.sh` les trouve.
5. **Node.js 20** (ClickDeck) : `brew install node@20`.
6. **PlatformIO** (firmware) : il est déjà installé dans `OS-ClickDeck/.venv-pio/`.

---

## 3. Sortir une nouvelle version, étape par étape

Exemple : Multibook passe en **0.5.0**, l'application ClickDeck en **1.15.0** et ClickOS en **4.7.0**.
Ne faire que les parties du produit concerné.

### Étape 1 — Changer les numéros de version

| Produit | Fichiers à modifier |
|---|---|
| Multibook | `package.json`, `src-tauri/tauri.conf.json` et `src-tauri/Cargo.toml` (ligne `version = …`) — les trois identiques. Pour Android, augmenter aussi `bundle.android.versionCode` dans `tauri.conf.json`. |
| Application ClickDeck | `desktop-app/package.json`, `desktop-app/react-app/package.json` et le `package.json` racine |
| ClickOS | `OS-ClickDeck/src/Config.h` → `#define OS_VERSION "4.7.0"` |

Écrire les nouveautés :

- Multibook : une section « Nouveautés de la version … » en haut de `README.md`, et le manuel
  intégré `app/js/manual.js` pour toute nouvelle fonction ;
- ClickDeck : une entrée en tête de `CHANGELOG.md`, et le manuel `react-app/src/components/HelpManual.tsx` ;
- ClickOS : un fichier `docs/releases/v4.7.0.md`.

### Étape 2 — Construire Multibook

```sh
cd ~/Desktop/Application/"multibook tauri"
export PATH=/opt/homebrew/opt/rustup/bin:$HOME/.cargo/bin:$PATH
./build.sh                 # Mac + Windows + Android (environ 15 min)
./build.sh mac             # ou un seul système : mac, win, android
```

Les fichiers arrivent dans `dist-tauri/`. **Linux** se construit sur GitHub (étape 5).

> Ne pas modifier `app/` pendant un build : l'interface est intégrée au moment de la compilation.

### Étape 3 — Construire l'application ClickDeck (Mac)

```sh
cd ~/Desktop/Application/"Clickdeck travail/VA/app/desktop-app"
npm run dist:mac           # → dist/Clickdeck-<version>-arm64.dmg
```

Depuis le terminal de VS Code, lancer `env -u ELECTRON_RUN_AS_NODE npm run dist:mac`.
**Windows et Linux** se construisent sur GitHub (étape 5).

### Étape 4 — Construire ClickOS (si le firmware change)

```sh
cd ~/Desktop/Application/"Clickdeck travail/VA/app/OS-ClickDeck"
./build.sh
```

Le script compile, copie les binaires et `version.json` dans `desktop-app/react-app/public/firmware/`,
crée `clickos-v<version>.zip`, puis flashe le boîtier s'il est branché. Construire le firmware
**avant** l'application ClickDeck, car celle-ci embarque la dernière version.

Si la commande `pio` est introuvable, lancer `./.venv-pio/bin/python -m platformio run`.

### Étape 5 — Pousser le code et construire Windows / Linux sur GitHub

```sh
# Multibook
cd ~/Desktop/Application/"multibook tauri"
git add -A && git commit -m "0.5.0 — ce qui change" && git push
gh workflow run linux.yml --repo OneDrop3D/multibook

# ClickDeck
cd ~/Desktop/Application/"Clickdeck travail/VA/app"
git add -A && git commit -m "1.15.0 — ce qui change" && git push
gh workflow run build.yml --repo OneDrop3D/clickdeck
```

Suivre l'avancement (15 à 25 minutes) :

```sh
gh run watch --repo OneDrop3D/clickdeck      # ou OneDrop3D/multibook
```

Puis récupérer les installeurs dans un dossier de travail :

```sh
mkdir -p ~/Desktop/Application/livraison && cd ~/Desktop/Application/livraison
gh run download --repo OneDrop3D/multibook  -n multibook-linux   -D multibook-linux
gh run download --repo OneDrop3D/clickdeck  -n clickdeck-windows -D clickdeck-windows
gh run download --repo OneDrop3D/clickdeck  -n clickdeck-linux   -D clickdeck-linux
```

Pousser une étiquette (`git tag v1.15.0 && git push --tags`) lance aussi ces builds automatiquement.

### Étape 6 — Publier pour les utilisateurs

Toujours depuis ce dépôt. Une commande **sans** `--publier` montre seulement le manifeste qui
serait écrit : la relire, puis relancer avec `--publier`.

```sh
cd ~/Desktop/Application/mises-a-jour
git pull

# Multibook : tous les systèmes d'un coup
./publier.py multibook 0.5.0 \
  macos-arm64="../multibook tauri/dist-tauri/Multibook-0.5.0-mac-arm64.dmg" \
  windows-x64="../multibook tauri/dist-tauri/Multibook-0.5.0-windows-x64-installateur.exe" \
  android-arm64="../multibook tauri/dist-tauri/Multibook-0.5.0-android.apk" \
  linux-x64-appimage=../livraison/multibook-linux/appimage/Multibook_0.5.0_amd64.AppImage \
  linux-x64-deb=../livraison/multibook-linux/deb/Multibook_0.5.0_amd64.deb \
  linux-x64-rpm=../livraison/multibook-linux/rpm/Multibook-0.5.0-1.x86_64.rpm \
  --notes notes.md --publier

# Application ClickDeck
./publier.py clickdeck-app 1.15.0 \
  macos-arm64="../Clickdeck travail/VA/app/desktop-app/dist/Clickdeck-1.15.0-arm64.dmg" \
  windows-x64="../livraison/clickdeck-windows/Clickdeck Setup 1.15.0.exe" \
  linux-x64-appimage=../livraison/clickdeck-linux/Clickdeck-1.15.0.AppImage \
  linux-x64-deb=../livraison/clickdeck-linux/clickdeck-desktop_1.15.0_amd64.deb \
  linux-x64-rpm=../livraison/clickdeck-linux/clickdeck-desktop-1.15.0.x86_64.rpm \
  --notes notes.md --publier

# ClickOS (--min-app : version de l'application nécessaire pour ce firmware)
./publier.py clickos 4.7.0 \
  esp32-s3="../Clickdeck travail/VA/app/desktop-app/react-app/public/firmware/clickos-v4.7.0.zip" \
  --notes "../Clickdeck travail/VA/app/docs/releases/v4.7.0.md" --min-app 1.15.0 --publier
```

Les noms exacts des fichiers Linux et Windows dépendent de l'outil de build : faire `ls` dans
`../livraison/…` et recopier. Le fichier `notes.md` contient le texte des nouveautés ; c'est lui
que voit l'utilisateur.

`publier.py` :

1. calcule la taille et l'empreinte SHA-256 de chaque fichier ;
2. crée la release `<produit>-v<version>` sur GitHub et y dépose les fichiers ;
3. réécrit `<produit>.json`, puis le commite et le pousse.

On peut publier un système plus tard : les fichiers déjà publiés pour les autres systèmes sont
gardés. Pour ajouter Windows à une version déjà sortie, relancer la même commande avec seulement
`windows-x64=…` : le script détecte que la release existe et y ajoute le fichier.

### Étape 7 — Vérifier

```sh
curl -s https://raw.githubusercontent.com/OneDrop3D/mises-a-jour/main/multibook.json | head -20
gh release list --repo OneDrop3D/mises-a-jour
```

Le manifeste peut mettre jusqu'à 5 minutes à se rafraîchir (cache de GitHub). Ensuite, sur une
machine qui a une version plus ancienne :

- **Multibook** : Paramètres › Données › Mises à jour › « Vérifier maintenant » ;
- **ClickDeck** : la fenêtre de mise à jour s'ouvre au démarrage ;
- **ClickOS** : ClickDeck le propose quand le boîtier branché a une version plus ancienne.

---

## 4. Ce que vit l'utilisateur

1. Au démarrage, l'application lit le manifeste sur le site OneDrop3D (s'il est configuré) **et**
   sur GitHub, et garde la version la plus récente.
2. Si elle est plus récente que la version installée, les nouveautés s'affichent.
3. « Télécharger » rapatrie le fichier **de son système**. Sa taille et son empreinte SHA-256
   sont comparées au manifeste ; un fichier différent est supprimé, jamais ouvert.
4. L'installeur s'ouvre (sous Windows, l'application se ferme pour le laisser travailler). Les
   données de l'utilisateur ne sont pas touchées.
5. Pour le firmware, l'application ClickDeck compare avec la version que le boîtier **exécute
   vraiment**, télécharge le paquet vérifié et le flashe depuis Paramètres → ClickOS.

> Une machine qui a encore Multibook 0.3.0 ou ClickDeck 1.13.0 n'a pas ce système : il faut y
> installer une fois les nouvelles versions à la main, depuis les Releases de ce dépôt.

---

## 5. Passer de GitHub au site OneDrop3D

Le site sait déjà servir le même manifeste (`GET /api/mises-a-jour/<produit>`) à partir des
fichiers déposés dans Administration › Téléchargements. Le jour où il est en ligne :

1. Y déposer les installeurs et cocher « publié ».
2. Indiquer son adresse aux applications :
   - Multibook : construire avec `MULTIBOOK_SITE_MAJ=https://<domaine> ./build.sh` ;
   - ClickDeck : la variable `CLICKDECK_UPDATE_SITE_URL=https://<domaine>`, ou l'écrire comme
     valeur par défaut dans `desktop-app/src/update/UpdateManager.ts`.
3. Garder GitHub en secours : les deux sources cohabitent, la plus récente l'emporte.

Les détails techniques sont dans `Site web V2/docs/MISES-A-JOUR.md`.

---

## 6. Dépannage

| Symptôme | Cause probable | Que faire |
|---|---|---|
| `publier.py` : « annonce déjà x.y.z, plus récente » | on publie un numéro plus petit | augmenter la version |
| `gh: authentication required` | session `gh` expirée | `gh auth login` |
| L'application ne voit pas la nouvelle version | cache GitHub de 5 min, ou version identique | attendre ; vérifier le numéro avec `curl` |
| « Empreinte SHA-256 invalide » chez l'utilisateur | fichier remplacé après publication | republier la version avec `publier.py` |
| Le build GitHub échoue | voir le journal | `gh run view --repo OneDrop3D/<dépôt> --log-failed` |
| `pio: command not found` | raccourci PlatformIO cassé | `./.venv-pio/bin/python -m platformio run` |
| Build Windows de Multibook : `lld` introuvable | PATH incomplet | `export PATH=/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/lld/bin:$PATH` |

---

## 7. Référence : le manifeste (schema 1)

```json
{
  "schema": 1,
  "product": "multibook",
  "channel": "stable",
  "version": "0.4.0",
  "date": "2026-10-26",
  "notes": "Texte des nouveautés (Markdown)",
  "page": "https://github.com/OneDrop3D/mises-a-jour/releases/tag/multibook-v0.4.0",
  "minAppVersion": "1.14.0",
  "files": {
    "macos-arm64": {
      "url": "https://github.com/…/Multibook-0.4.0-mac-arm64.dmg",
      "name": "Multibook-0.4.0-mac-arm64.dmg",
      "size": 78082796,
      "sha256": "64 caractères hexadécimaux"
    }
  }
}
```

Clés de `files` : `macos-arm64`, `macos-x64`, `windows-x64`, `linux-x64-appimage`,
`linux-x64-deb`, `linux-x64-rpm`, `android-arm64`, `esp32-s3`. `minAppVersion` ne sert qu'à
ClickOS. Les applications refusent un fichier sans `sha256`.
