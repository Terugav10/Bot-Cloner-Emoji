# 🚀 Discord Emoji Cloner Bot

Um bot premium para clonar emojis de outros servidores diretamente para o seu, com suporte a comandos de barra (Slash Commands).

## ✨ Funcionalidades
- `/clonar`: Clona um único emoji personalizado.
- `/clonar_varios`: Clona múltiplos emojis de uma vez (até 10).
- `/ping`: Verifica a latência do bot.
- Suporte a emojis estáticos (.png) e animados (.gif).
- Interface moderna com embeds elegantes.

## 🛠️ Instalação

1. **Requisitos**: Python 3.8+ instalado.
2. **Dependências**: Instale as bibliotecas necessárias:
   ```bash
   pip install disnake aiohttp python-dotenv
   ```
3. **Configuração**:
   - Renomeie o arquivo `.env` e coloque seu Token do Discord.
   - Certifique-se de que o bot tenha as permissões `Gerenciar Emojis e Figurinhas` e `Intents de Conteúdo de Mensagem` no [Developer Portal](https://discord.com/developers/applications).

## 🚀 Como Rodar
Execute o arquivo principal:
```bash
python main.py
```

## 📝 Notas
- O bot precisa estar nos servidores de onde você deseja clonar os emojis, ou você deve fornecer a string completa do emoji (ex: `<:nome:id>`).
- Respeite os Termos de Serviço do Discord e os direitos autorais dos emojis.
