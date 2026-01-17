# YouTube Music Player for NVDA
### 1. 搜索
1. 打开插件 (`NVDA+Alt+Y`)。您将自动进入编辑区域。
2. 输入歌曲或艺术家名称。
3. 如果想更改提供商，按 `Tab` 选择 "YouTube Music" 或 "YouTube"。
4. 按 `Enter` 进行搜索。

**导航提示:**
- 在结果列表中按 `Escape` 返回**提供商选择**。如果您选择提供商（相同的或不同的）并按 `Enter`，搜索将自动重复。
- **再次**按 `Escape`（在提供商选择时）返回**编辑字段**。
- **快速捷径:** 如果您在结果列表中想要立即返回编辑您的搜索，只需按 `Escape` **两次**。
### 2. 浏览结果
1. 结果显示在列表中。使用 `上` 和 `下` 箭头。
2. 要播放，在想要的结果上按 `Enter`。
3. 查看更多结果，按 `Tab` 到 "下一页" 按钮（或 `Shift+Tab` 到 "上一页"）并按 `Enter`。

**提示:** 在结果列表中，您可以按 `Escape` 返回并再次选择您的首选提供商。如果再按一次 `Escape`，您将返回编辑字段以执行新的搜索。

### 3. 控制播放器
歌曲开始时，播放器窗口会自动打开。
- 关闭播放器并返回搜索，按 `Escape`。
- 如果想要搜索另一首歌曲**而不停止当前正在播放的**:
  1. `Tab` 到 "结果" 按钮并按 `Enter`。
  2. 按两次 `Escape`。
  3. 您将返回搜索栏。输入新歌曲并重复该过程。

## 播放器命令

### 音量
- 上箭头: 增加音量
- 下箭头: 减少音量

### 曲目导航
- 右箭头: 前进1秒
- 左箭头: 后退1秒
- Shift+右箭头: 前进10秒
- Shift+左箭头: 后退10秒
- Ctrl+右箭头: 前进60秒
- Ctrl+左箭头: 后退60秒

### 速度和音调
- Page Up: 增加速度和音调
- Page Down: 减少速度和音调
- Ctrl+Page Up: 仅增加音调
- Ctrl+Page Down: 仅减少音调
- Ctrl+上箭头: 仅增加速度
- Ctrl+下箭头: 仅减少速度

### 播放
- 空格: 播放/暂停
- Escape: 关闭播放器（返回搜索）

> [!IMPORTANT]
> **使用提示:** 切换曲目时，**不要过快重复点击"下一首"**。播放器需要时间加载新歌曲。
>
> **建议:** 在再次点击"下一首"之前，等待NVDA朗读**开始加载**的歌曲标题。这是MPV的限制，根据您的网络情况，可能会有约2秒的延迟。

## 2026.01.17 版本新功能

- YouTube和YouTube Music的新搜索功能
- 带播放控制的完整无障碍播放器
- 播放列表支持和连续播放（自动播放）
- 高级速度和音调控制
- Radio Mix发现新音乐

## 功能

- 在YouTube和YouTube Music搜索
- 带NVDA反馈的无障碍音频播放器
- 音量、速度和音调控制
- 重复和自动播放模式
- Radio Mix发现新音乐
- 自动更新检查
- 支持11种语言

## 作者

JoaoDEVWHADS

## 许可证

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
