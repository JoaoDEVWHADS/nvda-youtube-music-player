# Translations

Adding and updating translations.

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| pt_BR | Portuguese (Brazil) |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| ru | Russian |
| ja | Japanese |
| zh_CN | Chinese (Simplified) |
| tr | Turkish |
| ar | Arabic |

## File Structure

```
addon/
├── locale/
│   ├── en/LC_MESSAGES/nvda.po
│   ├── pt_BR/LC_MESSAGES/nvda.po
│   └── .../
└── doc/
    ├── en/readme.md
    ├── pt_BR/readme.md
    └── .../
```

## Adding a New Language

### Step 1: Create locale directory
```bash
mkdir -p addon/locale/XX/LC_MESSAGES
```

### Step 2: Copy template
```bash
cp addon/locale/en/LC_MESSAGES/nvda.po addon/locale/XX/LC_MESSAGES/
```

### Step 3: Translate strings
Edit `nvda.po` and translate all `msgstr` entries.

### Step 4: Create documentation
```bash
mkdir -p addon/doc/XX
```
Create `addon/doc/XX/readme.md` with translated user documentation.

### Step 5: Rebuild
```bash
scons
```

## PO File Format

```po
msgid "Search"
msgstr "Buscar"

msgid "Play"
msgstr "Reproduzir"
```

## Tools

### Poedit
GUI editor for PO files:
```bash
sudo apt install poedit
poedit addon/locale/XX/LC_MESSAGES/nvda.po
```

### Command Line
Compile PO to MO:
```bash
msgfmt -o nvda.mo nvda.po
```

## Translation Tips

1. Keep keyboard shortcuts consistent
2. Test all translated dialogs
3. Check string length (UI may overflow)
4. Use formal language for accessibility
