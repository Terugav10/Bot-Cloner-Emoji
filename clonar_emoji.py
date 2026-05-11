import aiohttp
import asyncio
import os
import base64
import sys

# COLOQUE SEUS DADOS AQUI OU O SCRIPT IRÁ PEDIR AO INICIAR
TOKEN = ""
ID_ORIGEM = ""
ID_DESTINO = ""

async def get_headers(token, is_bot=False):
    clean_token = token.strip()
    auth = f"Bot {clean_token}" if is_bot else clean_token
    return {
        "Authorization": auth,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

async def get_emojis(session, guild_id, token):
    # Tenta primeiro como Usuário
    headers = await get_headers(token, is_bot=False)
    url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
    
    async with session.get(url, headers=headers) as resp:
        if resp.status == 200:
            return await resp.json(), headers
        elif resp.status == 401:
            # Se falhou, tenta como Bot
            print("⚠️ Token de usuário falhou (401). Tentando como Token de Bot...")
            headers_bot = await get_headers(token, is_bot=True)
            async with session.get(url, headers=headers_bot) as resp_bot:
                if resp_bot.status == 200:
                    print("✅ Sucesso! Identificado como Token de Bot.")
                    return await resp_bot.json(), headers_bot
                else:
                    print(f"❌ Erro 401 persistente: O token é inválido.")
        elif resp.status == 403:
            print(f"❌ Erro 403: Sem permissão para acessar o servidor {guild_id}.")
        else:
            print(f"❌ Erro {resp.status} ao buscar emojis.")
        return [], None

async def download_image(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.read()
            encoded = base64.b64encode(data).decode('utf-8')
            mime = resp.headers.get('Content-Type', 'image/png')
            return f"data:{mime};base64,{encoded}"
    return None

async def create_emoji(session, guild_id, name, image_data, headers):
    url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
    payload = {"name": name, "image": image_data}
    async with session.post(url, headers=headers, json=payload) as resp:
        if resp.status == 201:
            return True, "Sucesso"
        elif resp.status == 429:
            data = await resp.json()
            return False, data.get('retry_after', 1)
        else:
            try:
                data = await resp.json()
                return False, data.get('message', 'Erro desconhecido')
            except:
                return False, f"Status {resp.status}"

async def main():
    global TOKEN, ID_ORIGEM, ID_DESTINO
    
    print("="*50)
    print("🚀 DISCORD EMOJI CLONER (SELF-BOT MODE)")
    print("="*50)
    
    if not TOKEN:
        TOKEN = input("🔑 Digite seu Token: ").strip()
    if not ID_ORIGEM:
        ID_ORIGEM = input("📂 ID do Servidor de Origem (onde estão os emojis): ").strip()
    if not ID_DESTINO:
        ID_DESTINO = input("🎯 ID do Servidor de Destino (para onde copiar): ").strip()

    headers = await get_headers(TOKEN)
    
    async with aiohttp.ClientSession() as session:
        print("\n🔍 Verificando emojis de origem...")
        emojis, headers = await get_emojis(session, ID_ORIGEM, TOKEN)
        
        if not emojis or not headers:
            print("🛑 Falha ao carregar emojis. Verifique o Token e os IDs.")
            return

        print(f"📦 Encontrados {len(emojis)} emojis!")
        confirm = input(f"Deseja copiar todos os {len(emojis)} emojis para o servidor {ID_DESTINO}? (s/n): ")
        
        if confirm.lower() != 's':
            print("❌ Operação cancelada.")
            return

        print("\n🚀 Iniciando clonagem... Mantenha esta janela aberta.")
        
        count = 0
        for i, e in enumerate(emojis):
            name = e['name']
            ext = "gif" if e.get('animated') else "png"
            url = f"https://cdn.discordapp.com/emojis/{e['id']}.{ext}"
            
            print(f"[{i+1}/{len(emojis)}] Clonando: {name}...", end="\r")
            
            image_data = await download_image(session, url)
            if image_data:
                success, result = await create_emoji(session, ID_DESTINO, name, image_data, headers)
                
                if success:
                    count += 1
                elif isinstance(result, (int, float)):
                    print(f"\n⏳ Rate limit atingido. Esperando {result} segundos...")
                    await asyncio.sleep(result)
                    # Tenta novamente uma vez
                    success, _ = await create_emoji(session, ID_DESTINO, name, image_data, headers)
                    if success: count += 1
                else:
                    print(f"\n❌ Erro no emoji '{name}': {result}")
            
            # Pausa de segurança recomendada
            await asyncio.sleep(2)
            
        print(f"\n\n✨ CONCLUÍDO! {count} emojis foram clonados com sucesso.")
        print("="*50)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Script encerrado pelo usuário.")
    except Exception as e:
        print(f"\n🚨 Erro inesperado: {e}")
