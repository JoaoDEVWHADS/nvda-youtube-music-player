# YouTube Music Player for NVDA
### 1. Arama
1. Eklentiyi açın (`NVDA+Alt+Y`). Otomatik olarak düzenleme alanına düşersiniz.
2. Şarkı veya sanatçı adını yazın.
3. Sağlayıcıyı değiştirmek isterseniz, "YouTube Music" veya "YouTube" seçmek için `Tab` tuşuna basın.
4. Aramak için `Enter` tuşuna basın.

**Gezinme İpucu:**
- **Sağlayıcı seçimine** dönmek için sonuç listesinde `Escape` tuşuna basın. Bir sağlayıcı (aynısı veya farklısı) seçip `Enter`a basarsanız, arama otomatik olarak tekrarlanır.
- **Düzenleme alanına** dönmek için (sağlayıcı seçiminde) **tekrar** `Escape` tuşuna basın.
- **Hızlı Kısayol:** Sonuç listesindeyseniz ve aramanızı düzenlemek için anında geri dönmek istiyorsanız, sadece **iki kez** `Escape` tuşuna basın.
### 2. Sonuçlarda Gezinme
1. Sonuçlar bir listede görünür. `Yukarı` ve `Aşağı` okları kullanın.
2. Çalmak için istediğiniz sonucun üzerinde `Enter` tuşuna basın.
3. Daha fazla sonuç görmek için `Tab` ile "Sonraki Sayfa" düğmesine (veya "Önceki Sayfa" için `Shift+Tab`) gidin ve `Enter` a basın.

**İpucu:** Sonuç listesinde, tercih ettiğiniz sağlayıcıyı tekrar seçmek için `Escape` tuşuna basarak geri dönebilirsiniz. Bir kez daha `Escape` tuşuna basarsanız, yeni bir arama yapmak için düzenleme alanına dönersiniz.

### 3. Oynatıcı Kontrolü
Şarkı başladığında oynatıcı penceresi otomatik olarak açılır.
- Oynatıcıyı kapatıp aramaya dönmek için `Escape` tuşuna basın.
- **Çalan şarkıyı durdurmadan** başka bir şarkı aramak isterseniz:
  1. `Tab` ile "Sonuçlar" düğmesine gidin ve `Enter`a basın.
  2. İki kez `Escape` tuşuna basın.
  3. Arama alanına döneceksiniz. Yeni şarkıyı yazın ve işlemi tekrarlayın.

## Oynatıcı Komutları

### Ses
- Yukarı Ok: Sesi artır
- Aşağı Ok: Sesi azalt

### Parça Gezinme
- Sağ Ok: 1 saniye ileri
- Sol Ok: 1 saniye geri
- Shift+Sağ Ok: 10 saniye ileri
- Shift+Sol Ok: 10 saniye geri
- Ctrl+Sağ Ok: 60 saniye ileri
- Ctrl+Sol Ok: 60 saniye geri

### Hız ve Ton
- Page Up: Hız ve tonu artır
- Page Down: Hız ve tonu azalt
- Ctrl+Page Up: Sadece tonu artır
- Ctrl+Page Down: Sadece tonu azalt
- Ctrl+Yukarı Ok: Sadece hızı artır
- Ctrl+Aşağı Ok: Sadece hızı azalt

### Oynatma
- Boşluk: Oynat/Duraklat
- Escape: Oynatıcıyı kapat (aramaya dön)

> [!IMPORTANT]
> **Kullanım İpucu:** Parça değiştirirken, **"Sonraki" düğmesine çok hızlı bir şekilde art arda basmayın**. Oynatıcının yeni şarkıyı yüklemesi için zamana ihtiyacı vardır.
>
> **Öneri:** Tekrar "Sonraki" düğmesine basmadan önce NVDA'nın **yüklenmeye başlayan** şarkının adını duyurmasını bekleyin. Bu bir MPV sınırlamasıdır ve internetinize bağlı olarak yaklaşık 2 saniyelik bir gecikme olabilir.

## Sürüm 2026.01.17 Yenilikleri

- YouTube ve YouTube Music için yeni arama özelliği
- Tam erişilebilir oynatıcı ve oynatma kontrolleri
- Çalma listesi desteği ve sürekli oynatma (Auto-Play)
- Gelişmiş hız ve ton kontrolleri
- Yeni müzik keşfi için Radio Mix

## Özellikler

- YouTube ve YouTube Music'te arama
- NVDA geri bildirimi ile erişilebilir ses oynatıcı
- Ses, hız ve ton kontrolleri
- Tekrar ve otomatik oynatma modları
- Yeni müzik keşfetmek için Radio Mix
- Otomatik güncelleme kontrolü
- 11 dil desteği

## Yazar

JoaoDEVWHADS

## Lisans

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
