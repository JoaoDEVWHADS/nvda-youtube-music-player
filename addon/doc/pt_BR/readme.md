# YouTube Music Player

## 1. Pesquisando
1. Abra o add-on (NVDA+Alt+Y). Você cairá automaticamente no campo de edição.
2. Digite o nome da música ou artista.
3. Se quiser mudar o provedor, use Tab até selecionar "YouTube Music" ou "YouTube".
4. Dê Enter para pesquisar.

**Dica de Navegação:**
- Pressione `Escape` na lista de resultados para voltar à seleção de provedor. Se você selecionar um provedor (o mesmo ou outro) e der Enter, a pesquisa será repetida automaticamente.
- Pressione `Escape` novamente (na seleção de provedor) para voltar ao campo de edição.
- **Atalho Rápido:** Se estiver na lista de resultados e quiser voltar instantaneamente para editar sua pesquisa, basta pressionar `Escape` duas vezes.

## 2. Navegando nos Resultados
1. Os resultados aparecem em uma lista. Use as setas `Cima` e `Baixo`.
2. Para tocar, pressione `Enter` sobre o resultado desejado.
3. Para ver mais resultados, pressione `Tab` até o botão "Próxima Página" (ou `Shift+Tab` para "Página Anterior") e dê `Enter`.

**Dica:** Na lista de resultados, você pode pressionar `Escape` para voltar e escolher seu provedor de preferência novamente. Se pressionar `Escape` mais uma vez, voltará para o campo de edição para realizar uma nova pesquisa.

## 3. Controlando o Player
Quando a música começa, a janela do player abre automaticamente.
- Para fechar o player e voltar para a busca, pressione `Escape`.
- Se quiser pesquisar outra música sem parar a que está tocando:
  1. Navegue com `Tab` até o botão "Resultados" e dê `Enter`.
  2. Pressione `Escape` duas vezes.
  3. Você voltará para o campo de busca. Digite a nova música e repita o processo.

### Comandos do Player

**Volume**
- `Seta Cima`: Aumenta volume
- `Seta Baixo`: Diminui volume

**Navegação na Música**
- `Seta Direita`: Avança 1 segundo
- `Seta Esquerda`: Volta 1 segundo
- `Shift+Seta Direita`: Avança 10 segundos
- `Shift+Seta Esquerda`: Volta 10 segundos
- `Ctrl+Seta Direita`: Avança 60 segundos
- `Ctrl+Seta Esquerda`: Volta 60 segundos

**Velocidade e Tonalidade**
- `Page Up`: Aumenta velocidade e tonalidade
- `Page Down`: Diminui velocidade e tonalidade
- `Ctrl+Page Up`: Aumenta somente tonalidade
- `Ctrl+Page Down`: Diminui somente tonalidade
- `Ctrl+Seta Cima`: Aumenta somente velocidade
- `Ctrl+Seta Baixo`: Diminui somente velocidade

**Reprodução**
- `Espaço`: Play/Pause
- `Escape`: Fechar player (volta para busca)

> [!IMPORTANT]
> **Dica de Uso:** Ao passar de faixa, não pressione "Próxima" repetidamente muito rápido. O player precisa de um tempo para carregar a nova música.
> **Recomendação:** Aguarde o NVDA falar o nome da música que começou a carregar antes de clicar em "Próxima" novamente. Isso é uma limitação do MPV e pode haver um atraso de cerca de 2 segundos dependendo da sua internet.

## ⚙️ Configuração
Você pode configurar o add-on indo em **Menu NVDA > Preferências > Configurações > YouTube Music Player**.

### Autenticação (Cookies)
Para acessar conteúdo com restrição de idade ou playlists pessoais, você pode fornecer um arquivo `cookies.txt` no formato Netscape.
1. Faça login no YouTube Music no navegador.
2. Use uma extensão como "Get cookies.txt LOCALLY" para exportar seus cookies.
3. Salve o arquivo e selecione-o no campo "Arquivo de Cookies" no painel de configurações do add-on.

**Solução de Problemas:** Se os cookies pararem de funcionar (ex: após logout) ou você encontrar erros, basta **limpar o caminho** do campo de configurações para desativar a autenticação.

## 📚 Uso Avançado

### Navegação nos Resultados
- Os resultados são exibidos em páginas (geralmente 20 itens por página).
- Use os botões **Página Anterior** e **Próxima Página** na parte inferior do diálogo para navegar.
- **Atalhos:**
  - `Escape` na lista: Volta para a seleção de provedor.
  - `Escape` novamente: Volta para a caixa de busca.
  - `Enter` na lista: Toca a faixa selecionada.

### Controles Rápidos do Player
Quando o foco está no botão **Player** dentro da janela de Resultados, você pode usar estes atalhos rápidos sem abrir a janela completa:
- `Espaço`: Play/Pause
- `Seta Esquerda` / `Seta Direita`: Retroceder/Avançar 10s
- `Seta Cima` / `Seta Baixo`: Volume +/- 5%

## Novidades da Versão 2026.01.17
- Nova funcionalidade de busca no YouTube e YouTube Music
- Player acessível completo com controles de reprodução
- Suporte a playlists e reprodução contínua (Auto-Play)
- Controles avançados de velocidade e tonalidade
- Radio Mix para descoberta de novas músicas

## Funcionalidades
- Pesquisar no YouTube e YouTube Music
- Player de áudio acessível com feedback do NVDA
- Controles de volume, velocidade e tonalidade
- Modos de repetição e reprodução automática
- Radio Mix para descobrir novas músicas
- Verificador de atualizações automático
- Suporte a 11 idiomas

## Autor
JoaoDEVWHADS

## Licença
GPL v2

## 📞 Contact / Contato
Feedback: https://t.me/tierryt2021
