# YouTube Music Player for NVDA
### 1. 検索
1. アドオンを開きます（`NVDA+Alt+Y`）。自動的に入力フィールドにフォーカスが当たります。
2. 曲名やアーティスト名を入力してください。
3. プロバイダーを変更したい場合は `Tab` で "YouTube Music" または "YouTube" を選択します。
4. `Enter` を押して検索します。

**ナビゲーションのヒント:**
- 結果リストで `Escape` を押すと、**プロバイダー選択**に戻ります。プロバイダー（同じもの、または別のもの）を選んで `Enter` を押すと、検索が自動的に繰り返されます。
- **もう一度** `Escape` を押すと（プロバイダー選択時）、**編集フィールド**に戻ります。
- **クイックショートカット:** 結果リストにいて、検索を編集するために即座に戻りたい場合は、`Escape` を **2回** 押すだけです。
### 2. 結果の操作
1. 結果はリストで表示されます。`上矢印` と `下矢印` を使用します。
2. 再生するには、目的の結果の上で `Enter` を押します。
3. 他の結果を見るには、`Tab` で「次のページ」（または `Shift+Tab` で「前のページ」）まで移動し、`Enter` を押します。

**ヒント:** 結果リストで `Escape` を押すと、戻ってプロバイダーを再選択できます。もう一度 `Escape` を押すと、編集フィールドに戻って新しい検索を実行できます。

### 3. プレイヤー操作
曲が始まると、プレイヤー画面が自動的に開きます。
- プレイヤーを閉じて検索に戻るには、`Escape` を押します。
- **再生中の曲を止めずに**別の曲を検索したい場合:
  1. `Tab` で「結果」ボタンまで移動し、`Enter` を押します。
  2. `Escape` を2回押します。
  3. 検索フィールドに戻ります。新しい曲を入力して繰り返してください。

## プレイヤーコマンド

### 音量
- 上矢印: 音量を上げる
- 下矢印: 音量を下げる

### トラック移動
- 右矢印: 1秒進む
- 左矢印: 1秒戻る
- Shift+右矢印: 10秒進む
- Shift+左矢印: 10秒戻る
- Ctrl+右矢印: 60秒進む
- Ctrl+左矢印: 60秒戻る

### 速度と音程
- Page Up: 速度と音程を上げる
- Page Down: 速度と音程を下げる
- Ctrl+Page Up: 音程のみ上げる
- Ctrl+Page Down: 音程のみ下げる
- Ctrl+上矢印: 速度のみ上げる
- Ctrl+下矢印: 速度のみ下げる

### 再生
- スペース: 再生/一時停止
- Escape: プレイヤーを閉じる（検索に戻る）

> [!IMPORTANT]
> **使い方のヒント:** トラックをスキップするときは、**「次へ」を素早く連打しないでください**。プレイヤーが新しい曲を読み込むのに時間がかかります。
>
> **推奨:** NVDAが**読み込みを開始した**曲のタイトルを読み上げるのを待ってから、再度「次へ」をクリックしてください。これはMPVの仕様であり、インターネット環境によっては約2秒の遅延が発生する場合があります。

## バージョン 2026.01.17 の新機能

- YouTubeおよびYouTube Musicの新しい検索機能
- 再生コントロール付きの完全なアクセシブルプレイヤー
- プレイリスト対応と連続再生（自動再生）
- 高度な速度と音程コントロール
- 新しい音楽を発見するRadio Mix

## 機能

- YouTubeとYouTube Musicで検索
- NVDAフィードバック付きのアクセシブルなプレイヤー
- 音量、速度、音程の調整
- リピートと自動再生モード
- 新しい音楽を発見するRadio Mix
- 自動アップデートチェック
- 11言語対応

## 作者

JoaoDEVWHADS

## ライセンス

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
