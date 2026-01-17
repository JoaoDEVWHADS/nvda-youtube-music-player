#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Setup Completo de Ambiente e Build do YouTube Music Player ===${NC}"

ROOT_DIR=$(pwd)
ADDON_LIB_DIR="$ROOT_DIR/addon/globalPlugins/youtubeMusicPlayer/lib"

echo -e "${BLUE}[1/6] Verificando dependências de sistema...${NC}"

PACKAGES="python3 python3-pip curl unzip p7zip-full gettext"
NEEDS_INSTALL=false

for pkg in $PACKAGES; do
    if ! dpkg -s $pkg >/dev/null 2>&1; then
        NEEDS_INSTALL=true
        break
    fi
done

if [ "$NEEDS_INSTALL" = true ] || ! command -v scons &> /dev/null; then
    echo -e "${YELLOW}Instalando dependências de sistema (pode pedir senha sudo)...${NC}"
    apt-get update && apt-get install -y $PACKAGES
    pip3 install scons markdown --break-system-packages 2>/dev/null || pip3 install scons markdown
    echo -e "${GREEN}Dependências instaladas.${NC}"
else
    echo -e "${GREEN}Dependências de sistema já instaladas.${NC}"
fi

echo -e "${BLUE}[2/6] Instalando bibliotecas Python para Windows na pasta lib...${NC}"
mkdir -p "$ADDON_LIB_DIR"

pip3 install ytmusicapi requests --target "$ADDON_LIB_DIR" --upgrade --break-system-packages 2>/dev/null || pip3 install ytmusicapi requests --target "$ADDON_LIB_DIR" --upgrade

find "$ADDON_LIB_DIR" -name "__pycache__" -type d -exec rm -rf {} +
find "$ADDON_LIB_DIR" -name "*.dist-info" -type d -exec rm -rf {} +
find "$ADDON_LIB_DIR" -name "bin" -type d -exec rm -rf {} +

echo -e "${GREEN}Bibliotecas Python atualizadas em $ADDON_LIB_DIR${NC}"

echo -e "${BLUE}[3/6] Verificando binários Windows...${NC}"

YTDLP_EXE="$ADDON_LIB_DIR/yt-dlp.exe"
echo -e "${YELLOW}Baixando yt-dlp.exe mais recente...${NC}"
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o "$YTDLP_EXE"
chmod +x "$YTDLP_EXE"
echo -e "${GREEN}yt-dlp.exe atualizado.${NC}"

MPV_EXE="$ADDON_LIB_DIR/mpv.exe"
if [ ! -f "$MPV_EXE" ]; then
    echo -e "${YELLOW}mpv.exe não encontrado. Baixando build recente (shinchiro/mpv-winbuild-cmake)...${NC}"
    
    MPV_DL_URL=$(curl -s https://api.github.com/repos/shinchiro/mpv-winbuild-cmake/releases/latest | grep "browser_download_url" | grep ".7z" | grep "v3" | head -n 1 | cut -d '"' -f 4)
    
    if [ -z "$MPV_DL_URL" ]; then
        echo -e "${RED}Erro ao encontrar URL de download do MPV. Tentando fallback...${NC}"
        MPV_DL_URL="https://github.com/shinchiro/mpv-winbuild-cmake/releases/download/20240428/mpv-x86_64-v3-20240428-git-062820a.7z"
    fi
    
    echo -e "Baixando de: $MPV_DL_URL"
    curl -L "$MPV_DL_URL" -o mpv_temp.7z
    
    echo -e "${YELLOW}Extraindo mpv.exe...${NC}"
    7z e mpv_temp.7z mpv.exe -o"$ADDON_LIB_DIR" -y > /dev/null
    
    if [ -f "$MPV_EXE" ]; then
        echo -e "${GREEN}mpv.exe baixado e extraído com sucesso!${NC}"
        rm mpv_temp.7z
    else
        echo -e "${RED}Falha ao extrair mpv.exe. Verifique se p7zip-full está instalado.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}mpv.exe já existe.${NC}"
fi

echo -e "${BLUE}[4/6] Verificando Integridade dos Arquivos...${NC}"

CRITICAL_FILES=(
    "addon/manifest.ini"
    "addon/globalPlugins/youtubeMusicPlayer/__init__.py"
    "addon/globalPlugins/youtubeMusicPlayer/youtubeSearch.py"
    "addon/globalPlugins/youtubeMusicPlayer/playerManager.py"
    "addon/globalPlugins/youtubeMusicPlayer/searchDialog.py"
    "addon/globalPlugins/youtubeMusicPlayer/playerDialog.py"
    "addon/globalPlugins/youtubeMusicPlayer/lib/mpv.exe"
    "addon/globalPlugins/youtubeMusicPlayer/lib/yt-dlp.exe"
    "addon/globalPlugins/youtubeMusicPlayer/lib/ytmusicapi"
    "addon/globalPlugins/youtubeMusicPlayer/lib/requests"
)

printf "+-%-60s-+-%-10s-+\n" "------------------------------------------------------------" "----------"
printf "| %-60s | %-10s |\n" "ARQUIVO / COMPONENTE" "STATUS"
printf "+-%-60s-+-%-10s-+\n" "------------------------------------------------------------" "----------"

INTEGRITY_FAIL=false

for file in "${CRITICAL_FILES[@]}"; do
    if [ -e "$ROOT_DIR/$file" ]; then
        printf "| %-60s | ${GREEN}%-10s${NC} |\n" "$file" "OK"
    else
        printf "| %-60s | ${RED}%-10s${NC} |\n" "$file" "FALTANDO"
        INTEGRITY_FAIL=true
    fi
done

printf "+-%-60s-+-%-10s-+\n" "------------------------------------------------------------" "----------"

if [ "$INTEGRITY_FAIL" = true ]; then
    echo -e "${RED}ERRO CRÍTICO: Arquivos essenciais estão faltando.${NC}"
    echo -e "${RED}O build será abortado para evitar gerar um add-on quebrado.${NC}"
    exit 1
else
    echo -e "${GREEN}Integridade Verificada: Tudo Pronto!${NC}"
fi

TEST_DIR="/tmp/yt_player_build_test"
echo -e "${BLUE}[5/6] Preparando diretório de teste em ${TEST_DIR}...${NC}"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"
cp -r "$ROOT_DIR"/* "$TEST_DIR/"

echo -e "${BLUE}[6/6] Iniciando compilação de teste (SCons)...${NC}"
cd "$TEST_DIR"
scons -Q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}=== Build concluído com SUCESSO! ===${NC}"
    ADDON_FILE=$(ls *.nvda-addon)
    cp "$ADDON_FILE" "$ROOT_DIR/"
    echo -e "Add-on gerado e copiado para: ${GREEN}$ROOT_DIR/$ADDON_FILE${NC}"
else
    echo -e "${RED}=== FALHA no Build ===${NC}"
    exit 1
fi
