# YouTube Music Player for NVDA
### 1. Suchen
1. Öffnen Sie das Add-on (`NVDA+Alt+Y`). Sie landen automatisch im Eingabefeld.
2. Geben Sie den Namen des Liedes oder Künstlers ein.
3. Wenn Sie den Anbieter wechseln möchten, drücken Sie `Tab`, bis "YouTube Music" oder "YouTube" ausgewählt ist.
4. Drücken Sie `Enter`, um zu suchen.

**Navigations-Tipp:**
- Drücken Sie `Escape` in der Ergebnisliste, um zur **Anbieterauswahl** zurückzukehren. Wenn Sie einen Anbieter (denselben oder einen anderen) wählen und `Enter` drücken, wird die Suche automatisch wiederholt.
- Drücken Sie **erneut** `Escape` (bei der Anbieterauswahl), um zum **Bearbeitungsfeld** zurückzukehren.
- **Schnellzugriff:** Wenn Sie sich in der Ergebnisliste befinden und sofort zur Bearbeitung Ihrer Suche zurückkehren möchten, drücken Sie einfach **zweimal** `Escape`.
### 2. Ergebnisse navigieren
1. Ergebnisse erscheinen in einer Liste. Nutzen Sie `Pfeil Hoch` und `Runter`.
2. Zum Abspielen drücken Sie `Enter` auf dem gewünschten Ergebnis.
3. Für mehr Ergebnisse drücken Sie `Tab` bis zur Schaltfläche "Nächste Seite" (oder `Shift+Tab` für "Vorherige Seite") und drücken Sie `Enter`.

**Tipp:** In der Ergebnisliste können Sie `Escape` drücken, um zurückzugehen und Ihren bevorzugten Anbieter erneut auszuwählen. Wenn Sie noch einmal `Escape` drücken, kehren Sie zum Bearbeitungsfeld zurück, um eine neue Suche durchzuführen.

### 3. Player steuern
Wenn ein Lied startet, öffnet sich das Player-Fenster automatisch.
- Um den Player zu schließen und zur Suche zurückzukehren, drücken Sie `Escape`.
- Wenn Sie ein anderes Lied suchen möchten, **ohne das laufende zu stoppen**:
  1. Navigieren Sie mit `Tab` zur Schaltfläche "Ergebnisse" und drücken Sie `Enter`.
  2. Drücken Sie zweimal `Escape`.
  3. Sie kehren zum Suchfeld zurück. Geben Sie das neue Lied ein und wiederholen Sie den Vorgang.

## Player-Befehle

### Lautstärke
- Pfeil Hoch: Lautstärke erhöhen
- Pfeil Runter: Lautstärke verringern

### Track-Navigation
- Pfeil Rechts: 1 Sekunde vorwärts
- Pfeil Links: 1 Sekunde zurück
- Shift+Pfeil Rechts: 10 Sekunden vorwärts
- Shift+Pfeil Links: 10 Sekunden zurück
- Strg+Pfeil Rechts: 60 Sekunden vorwärts
- Strg+Pfeil Links: 60 Sekunden zurück

### Geschwindigkeit und Tonhöhe
- Bild Auf: Geschwindigkeit und Tonhöhe erhöhen
- Bild Ab: Geschwindigkeit und Tonhöhe verringern
- Strg+Bild Auf: Nur Tonhöhe erhöhen
- Strg+Bild Ab: Nur Tonhöhe verringern
- Strg+Pfeil Hoch: Nur Geschwindigkeit erhöhen
- Strg+Pfeil Runter: Nur Geschwindigkeit verringern

### Wiedergabe
- Leertaste: Play/Pause
- Escape: Player schließen (zurück zur Suche)

> [!IMPORTANT]
> **Nutzungstipp:** Beim Wechseln der Titel **drücken Sie nicht zu schnell wiederholt auf "Weiter"**. Der Player benötigt Zeit zum Laden des neuen Songs.
>
> **Empfehlung:** Warten Sie, bis NVDA den Titel des Songs ansagt, **der zu laden beginnt**, bevor Sie erneut auf "Weiter" klicken. Dies ist eine MPV-Einschränkung und es kann je nach Internetverbindung eine Verzögerung von etwa 2 Sekunden geben.

## Neu in Version 2026.01.17

- Neue Suchfunktion für YouTube und YouTube Music
- Vollständiger barrierefreier Player mit Wiedergabesteuerung
- Playlist-Unterstützung und kontinuierliche Wiedergabe (Auto-Play)
- Erweiterte Geschwindigkeits- und Tonhöhensteuerung
- Radio Mix zum Entdecken neuer Musik

## Funktionen

- Suche auf YouTube und YouTube Music
- Barrierefreier Audioplayer mit NVDA-Feedback
- Lautstärke-, Geschwindigkeits- und Tonhöhenregler
- Wiederholungs- und Auto-Play-Modi
- Radio Mix zum Entdecken neuer Musik
- Automatische Update-Prüfung
- Unterstützung für 11 Sprachen

## Autor

JoaoDEVWHADS

## Lizenz

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
