import requests
import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from datetime import datetime

# Cargar configuración
with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)
api_key = config['Api_Steam']

# Diccionario de países
with open('codigos_paises.json', encoding='utf-8') as f:
    codigo_pais_dic = json.load(f)

# Estados de Steam
estado_dic = {
    0: "Desconectado 🔴",
    1: "Conectado 🟢",
    3: "Ausente 🟠",
    4: "Conectado 🟢"
}

# Función para convertir código ISO a bandera Discord
def obtener_bandera(codigo_iso):
    if not codigo_iso:
        return ""
    codigo_iso = codigo_iso.upper()
    return ''.join(chr(127397 + ord(c)) for c in codigo_iso)

# Comando slash
@slash.slash(
    name="steamid",
    description="Obtener información de un usuario de Steam",
    options=[
        create_option(
            name="usuario",
            description="Vanity URL o SteamID64 del usuario",
            option_type=3,
            required=True
        )
    ]
)
async def _steamid(ctx: SlashContext, usuario: str):
    await ctx.defer()
    
    # Resolver vanity URL
    r = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={api_key}&vanityurl={usuario}")
    steamid = r.json().get('response', {}).get('steamid', usuario)  # si ya es SteamID64

    # Información del jugador
    r = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid}")
    players = r.json().get('response', {}).get('players', [])
    if not players:
        await ctx.send("No se encontró el usuario de Steam.")
        return
    player = players[0]

    nombre = player.get('personaname', 'No encontrado')
    estado = estado_dic.get(player.get('personastate', 0), "Desconocido")
    avatar = player.get('avatarfull', '')

    codigo_iso = player.get('loccountrycode', '')
    pais_nombre = codigo_pais_dic.get(codigo_iso, "Desconocido")
    bandera = obtener_bandera(codigo_iso)
    pais_con_bandera = f"{pais_nombre} {bandera}"

    # Fechas
    fecha_creacion = datetime.utcfromtimestamp(player['timecreated']).strftime('%d/%m/%Y %H:%M:%S') if player.get('timecreated') else "No disponible"
    ultimo_cierre = datetime.utcfromtimestamp(player['lastlogoff']).strftime('%d/%m/%Y %H:%M:%S') if player.get('lastlogoff') else "No disponible"

    # Amigos
    r = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steamid}&relationship=friend")
    amigos = r.json().get('friendslist', {}).get('friends', [])
    total_amigos = len(amigos) if amigos else "No tiene amigos ❌"

    # Juegos
    r = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid}&format=json")
    juegos = r.json().get('response', {}).get('games', [])
    total_juegos = len(juegos) if juegos else "No tiene juegos ❌"

    # Actividad reciente
    r = requests.get(f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={steamid}&count=5")
    recent_games_data = r.json().get('response', {}).get('games', [])
    if recent_games_data:
        recent_games = "\n".join([f"{game['name']} ({game['playtime_2weeks']} min en 2 semanas)" for game in recent_games_data])
    else:
        recent_games = "No hay actividad reciente."

    # Baneos y bloqueos
    r = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={api_key}&steamids={steamid}")
    bans = r.json().get('players', [{}])[0]
    vac = "Sí" if bans.get('VACBanned', False) else "No"
    game_bans = bans.get('NumberOfGameBans', 0)
    community = "Sí" if bans.get('CommunityBanned', False) else "No"
    trade = bans.get('EconomyBan', "No")
    trade = "Sí" if trade.lower() == "banned" else "No"

    # Embed
    embed = discord.Embed(
        title=f"Información de Steam 🡺 {nombre}",
        description=(
            f"• SteamID64: {steamid}\n"
            f"• Estado: {estado}\n"
            f"• País: {pais_con_bandera}\n"
            f"• Creado: {fecha_creacion}\n"
            f"• Último cierre: {ultimo_cierre}\n"
            f"• Total amigos: {total_amigos}\n"
            f"• Juegos totales: {total_juegos}\n"
            f"• Actividad reciente:\n{recent_games}\n\n"
            f"• VAC Banned: {vac}\n"
            f"• Game Bans: {game_bans}\n"
            f"• Community Banned: {community}\n"
            f"• Trade/Economy Ban: {trade}"
        ),
        color=discord.Color.random()
    )
    embed.set_thumbnail(url=avatar)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print("BOT listo con Slash Commands!")

bot.run(config['Token_BOT'])
