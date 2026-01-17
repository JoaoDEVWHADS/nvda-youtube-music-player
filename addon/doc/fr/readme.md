# YouTube Music Player for NVDA
### 1. Recherche
1. Ouvrez le module (`NVDA+Alt+Y`). Vous arriverez automatiquement dans le champ d'édition.
2. Tapez le nom de la chanson ou de l'artiste.
3. Si vous voulez changer de fournisseur, appuyez sur `Tab` pour sélectionner "YouTube Music" ou "YouTube".
4. Appuyez sur `Entrée` pour rechercher.

**Conseil de Navigation:**
- Appuyez sur `Échap` dans la liste des résultats pour revenir à la **sélection du fournisseur**. Si vous sélectionnez un fournisseur (le même ou un autre) et appuyez sur `Entrée`, la recherche sera répétée automatiquement.
- Appuyez à nouveau sur `Échap` (dans la sélection du fournisseur) pour revenir au **champ d'édition**.
- **Raccourci Rapide:** Si vous êtes dans la liste des résultats et souhaitez revenir instantanément pour modifier votre recherche, appuyez simplement sur `Échap` **deux fois**.
### 2. Navigation des Résultats
1. Les résultats apparaissent dans une liste. Utilisez les flèches `Haut` et `Bas`.
2. Pour lire, appuyez sur `Entrée` sur le résultat souhaité.
3. Pour voir plus de résultats, appuyez sur `Tab` jusqu'au bouton "Page Suivante" (ou `Shift+Tab` pour "Page Précédente") et faites `Entrée`.

**Astuce:** Dans la liste des résultats, vous pouvez appuyer sur `Échap` pour revenir en arrière et choisir à nouveau votre fournisseur préféré. Si vous appuyez une fois de plus sur `Échap`, vous reviendrez au champ d'édition pour effectuer une nouvelle recherche.

### 3. Contrôle du Lecteur
Quand la chanson commence, la fenêtre du lecteur s'ouvre automatiquement.
- Pour fermer le lecteur et revenir à la recherche, appuyez sur `Échap`.
- Si vous voulez rechercher une autre chanson **sans arrêter celle qui joue**:
  1. Naviguez avec `Tab` jusqu'au bouton "Résultats" et faites `Entrée`.
  2. Appuyez deux fois sur `Échap`.
  3. Vous reviendrez au champ de recherche. Tapez la nouvelle chanson et répétez.

## Commandes du Lecteur

### Volume
- Flèche Haut: Augmenter le volume
- Flèche Bas: Diminuer le volume

### Navigation dans la Piste
- Flèche Droite: Avancer de 1 seconde
- Flèche Gauche: Reculer de 1 seconde
- Shift+Flèche Droite: Avancer de 10 secondes
- Shift+Flèche Gauche: Reculer de 10 secondes
- Ctrl+Flèche Droite: Avancer de 60 secondes
- Ctrl+Flèche Gauche: Reculer de 60 secondes

### Vitesse et Tonalité
- Page Haut: Augmenter vitesse et tonalité
- Page Bas: Diminuer vitesse et tonalité
- Ctrl+Page Haut: Augmenter tonalité uniquement
- Ctrl+Page Bas: Diminuer tonalité uniquement
- Ctrl+Flèche Haut: Augmenter vitesse uniquement
- Ctrl+Flèche Bas: Diminuer vitesse uniquement

### Lecture
- Espace: Lecture/Pause
- Échap: Fermer lecteur (retour à la recherche)

> [!IMPORTANT]
> **Conseil d'Utilisation:** En changeant de piste, **n'appuyez pas sur "Suivant" trop rapidement**. Le lecteur a besoin de temps pour charger la nouvelle chanson.
>
> **Recommandation:** Attendez que NVDA annonce le titre de la chanson qui **commence à charger** avant de cliquer à nouveau sur "Suivant". Il s'agit d'une limitation de MPV et il peut y avoir un délai d'environ 2 secondes selon votre internet.

## Nouveautés Version 2026.01.17

- Nouvelle fonctionnalité de recherche sur YouTube et YouTube Music
- Lecteur accessible complet avec contrôles de lecture
- Support des playlists et lecture continue (Auto-Play)
- Contrôles avancés de vitesse et tonalité
- Radio Mix pour découvrir de nouvelles musiques

## Fonctionnalités

- Recherche sur YouTube et YouTube Music
- Lecteur audio accessible avec retour NVDA
- Contrôles de volume, vitesse et tonalité
- Modes répétition et lecture automatique
- Radio Mix pour découvrir de nouvelles musiques
- Vérificateur de mises à jour automatique
- Support de 11 langues

## Auteur

JoaoDEVWHADS

## Licence

GPL v2


## ✨ Features

- 🔍 Search YouTube and YouTube Music
- 🎧 Accessible audio player with NVDA feedback
- 🎚️ Volume, speed, and pitch controls
- 🔁 Repeat and auto-play modes
- 📻 Radio Mix for discovering new music
- 🔄 Automatic update checker
- 🌐 11 languages supported



## ⌨️ Keyboard Shortcuts

| Command | Action |
|---------|--------|
| `NVDA+Alt+Y` | Open YouTube Music Player |
| `↑` / `↓` | Volume |
| `←` / `→` | Seek ±1s |
| `Space` | Play/Pause |



---

## ✨ Features

- 🔍 Search YouTube and YouTube Music
- 🎧 Accessible audio player with NVDA feedback
- 🎚️ Volume, speed, and pitch controls
- 🔁 Repeat and auto-play modes
- 📻 Radio Mix for discovering new music
- 🔄 Automatic update checker
- 🌐 11 languages supported


---

## ⌨️ Keyboard Shortcuts

| Command | Action |
|---------|--------|
| `NVDA+Alt+Y` | Open YouTube Music Player |
| `↑` / `↓` | Volume |
| `←` / `→` | Seek ±1s |
| `Space` | Play/Pause |


---


---

## ⚙️ Configuration

You can configure the add-on by going to **NVDA Menu > Preferences > Settings > YouTube Music Player**.

### Authentication (Cookies)
To access age-restricted content or your personal premium features, you can provide a `cookies.txt` file in Netscape format.
1. Log in to YouTube Music in your browser.
2. Use an extension like "Get cookies.txt LOCALLY" to export your cookies.
3. Save the file and select it in the add-on settings panel "Cookies File" field.

**Troubleshooting:** If the cookies stop working (e.g., after logging out) or you encounter errors, simply **clear the path** from the generic settings field to disable authentication.

## 📚 Advanced Usage

### Search Results Navigation
- Results are displayed in pages (usually 20 items per page).
- Use the **Previous Page** and **Next Page** buttons at the bottom of the dialog to browse more results.
- **Shortcuts:**
  - `Escape` on list: Returns to provider selection.
  - `Escape` again: Returns to search edit box.
  - `Enter` on list: Plays the selected track.

### Quick Player Controls
When the focus is on the **Player** button within the Results dialog, you can control playback without opening the full window:
- `Space`: Play/Pause
- `Left` / `Right`: Seek -10s / +10s
- `Up` / `Down`: Volume +/- 5%

## 📄 License

GPL v2 - See [LICENSE](../../../LICENSE)

## 👤 Author

**JoaoDEVWHADS**


---

## ✨ Features

- 🔍 Search YouTube and YouTube Music
- 🎧 Accessible audio player with NVDA feedback
- 🎚️ Volume, speed, and pitch controls
- 🔁 Repeat and auto-play modes
- 📻 Radio Mix for discovering new music
- 🔄 Automatic update checker
- 🌐 11 languages supported


---

## ⌨️ Keyboard Shortcuts

| Command | Action |
|---------|--------|
| `NVDA+Alt+Y` | Open YouTube Music Player |
| `↑` / `↓` | Volume |
| `←` / `→` | Seek ±1s |
| `Space` | Play/Pause |


---


## 📞 Contact / Contato
Feedback: https://t.me/tierryt2021
