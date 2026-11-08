# Multibook

**Vos cahiers, vos documents et vos révisions dans une seule application.**
Gratuit, sans compte et sans clé : téléchargez, installez, c'est prêt.

## Télécharger

<!-- telechargements:debut -->
**Version 0.6.22**, publiée le 2026-11-08.

| Système | Téléchargement | Taille |
|---|---|---|
| Mac (Apple Silicon) | [Multibook-0.6.22-mac-arm64.dmg](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.22/Multibook-0.6.22-mac-arm64.dmg) | 79 Mo |
| Windows 64 bits | [Multibook-0.6.22-windows-x64-installateur.exe](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.22/Multibook-0.6.22-windows-x64-installateur.exe) | 74 Mo |
| Android | [Multibook-0.6.20-android.apk](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.20/Multibook-0.6.20-android.apk) | 82 Mo |
| Linux (AppImage) | [Multibook_0.6.22_amd64.AppImage](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.22/Multibook_0.6.22_amd64.AppImage) | 157 Mo |
| Linux (.deb : Ubuntu, Debian) | [Multibook_0.6.22_amd64.deb](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.22/Multibook_0.6.22_amd64.deb) | 80 Mo |
| Linux (.rpm : Fedora) | [Multibook-0.6.22-1.x86_64.rpm](https://github.com/OneDrop3D/mises-a-jour/releases/download/multibook-v0.6.22/Multibook-0.6.22-1.x86_64.rpm) | 80 Mo |
<!-- telechargements:fin -->

Cliquez sur le fichier de votre système. Aucune inscription n'est demandée. Ensuite, Multibook
se met à jour tout seul.

## Ce que fait Multibook

- **Cahiers** : des cahiers, des intercalaires et des feuilles, avec du texte riche, de l'écriture
  au stylet, des formes, des schémas et des cartes mentales.
- **Maths et sciences** : équations, courbes, géométrie, tableaux de signes et de variations,
  opérations posées, calcul automatique.
- **Bureautique** : traitement de texte (`.docx`, `.odt`), tableur (`.xlsx`, `.ods`, CSV),
  présentations (`.pptx`, `.odp`), lecteur de PDF annotable.
- **Révisions** : fiches et jeux de révision, jeux de frappe.
- **Voix et IA** : dictée, lecture à voix haute, assistant IA qui tourne sur votre ordinateur.

Vos notes restent sur votre appareil : voir les [règles de confidentialité](CONFIDENTIALITE.md).

## Installer

### Mac

Pour les Mac à puce Apple (M1 et suivants), macOS 11 ou plus récent.

1. Ouvrez le fichier `.dmg` et glissez **Multibook** dans **Applications**.
2. Au premier lancement, macOS indique qu'il ne peut pas vérifier l'application : Multibook
   n'est pas enregistré auprès d'Apple. Ouvrez **Réglages Système › Confidentialité et sécurité**,
   puis choisissez **Ouvrir quand même**.

Si macOS dit que l'application est endommagée, tapez ceci dans le Terminal, puis relancez-la :

```
xattr -dr com.apple.quarantine /Applications/Multibook.app
```

### Windows

Pour Windows 64 bits.

1. Lancez le fichier `.exe`.
2. Si Windows affiche « Windows a protégé votre ordinateur », cliquez sur
   **Informations complémentaires**, puis sur **Exécuter quand même** : l'installeur n'est pas
   signé par un éditeur reconnu.

### Android

Pour Android 8 ou plus récent, sur un appareil 64 bits.

1. Téléchargez le fichier `.apk` depuis votre appareil et ouvrez-le.
2. Autorisez l'installation depuis votre navigateur quand Android le demande.

### Linux

Pour une distribution de 2024 ou plus récente (Ubuntu 24.04, Debian 13, Fedora 39…).

- **AppImage** : rendez le fichier exécutable, puis lancez-le.
- **Ubuntu, Debian** : `sudo apt install ./Multibook_*_amd64.deb`
- **Fedora** : `sudo dnf install ./Multibook-*.x86_64.rpm`

## Licence

Multibook est distribué sous la licence [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0).
Vous pouvez l'utiliser, le modifier et le partager gratuitement à des fins non commerciales,
y compris à l'école, dans une association ou pour un usage personnel. **L'usage commercial
n'est pas autorisé.** Ce résumé ne remplace pas le texte de la licence, qui fait foi.

## Besoin d'aide ?

Le manuel complet est dans l'application : **Paramètres › Aide**.
Pour une question ou un problème, écrivez à [onedrop3d@gmail.com](mailto:onedrop3d@gmail.com).

---

Ce dépôt sert aussi à distribuer les mises à jour des produits OneDrop3D.
Le fonctionnement interne est décrit dans [PUBLICATION.md](PUBLICATION.md).
