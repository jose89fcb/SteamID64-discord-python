import requests
import json
import discord
from discord.ext import commands
import datetime

with open('config.json') as f: 
    config = json.load(f) 

bot = commands.Bot(command_prefix=config['prefijo']) #Comando
bot.remove_command("help") # Borra el comando por defecto !help
api = config['Api_Steam'] #consigue la api desde este enlace: https://steamcommunity.com/dev




@bot.command()
    
async def steamid(ctx, *, steamid):
    

    
        response = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" f"{api}" + "&vanityurl=" f"{steamid}")
       
        steamid = response.json()['response']['steamid'] 
        
            
        

        response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" f"{api}" + "&steamids=" f"{steamid}")
       
        avatar = response.json()['response']['players'][0]['avatar']
        
    
        estado = response.json()['response']['players'][0]['personastate']
        usuario = response.json()['response']['players'][0]['personaname']
        
        try:
              bandera = response.json()['response']['players'][0]['loccountrycode']
    
 

        except KeyError:
                bandera=("No tiene bandera de pais❌")
                
               
      
        embed = discord.Embed(title="info usuario Steam🡺 " f"{usuario}",  description="•Steam ID 64🡺 "f"{steamid}" "\n\n•Estado🡺 " + (str(estado).replace("0","Desconectado 🔴").replace("1","Conectado 🟢").replace("3","ausente 🟠") +"\n\n•Bandera🡺 " f"{bandera}"))
    

        embed.set_thumbnail(url=f"{avatar}")
        await ctx.send(embed=embed)
        
        

            
        
 
 
 
@bot.event
async def on_ready():
    print("BOT listo!")
    
 
    
bot.run(config['Token_BOT']) #OBTEN UN TOKEN EN: https://discord.com/developers/applications