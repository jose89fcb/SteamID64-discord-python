import requests, bs4
import json
import discord
from discord.ext import commands
import datetime
from datetime import datetime


with open('config.json') as f: 
    config = json.load(f) 



  

bot = commands.Bot(command_prefix=config['prefijo']) #Comando
bot.remove_command("help") # Borra el comando por defecto !help
api = config['Api_Steam'] #consigue la api desde este enlace: https://steamcommunity.com/dev





@bot.command()
    
async def steamid(ctx, *, steamid):
    

    
        response = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" f"{api}" + "&vanityurl=" f"{steamid}")
       
        
        try:
         url = response.json()['response']['players'][0]['avatarfull']
        except KeyError:
                url=" "
        steam = requests.get(f"https://steamcommunity.com/id/" f"{steamid}")
        

        infoplaca = bs4.BeautifulSoup(steam.text, "lxml")

        NombrePlaca = infoplaca.select("img", class_="profile_flag")


        link =   NombrePlaca[5].get("src").replace("_full.jpg", "https://i.imgur.com/zJKj349.png")
        
        



        

        jugando = bs4.BeautifulSoup(steam.content, "html.parser")


        try:
         jugandoSteam = jugando.find("div", class_="profile_in_game_name").text

         


         jugandoSteam1 = jugando.find("div", class_="profile_in_game_header").text
          
        

        except AttributeError:
         jugandoSteam="No está jugando"
         

        try:


         jugandoSteam1 = jugandoSteam1.replace("In non-Steam game","En un juego que no es de Steam")
        except UnboundLocalError:
         jugandoSteam1=""

        

 
      

        try:
                steamid = response.json()['response']['steamid']
       
        except KeyError:
                steamid="No se encuentra❌"
                


       
        


      

        response = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + f"{api}" + "&steamid=" + f"{steamid}" + "&relationship=friend")

        
        
        
      
        

        
         

        
       
        

        

        
       

        try:
        
         totalamigos = response.json()['friendslist']['friends']
        except KeyError:
         totalamigos=""
       


        
        totalamigos=(str(len(totalamigos)))
       

        totalamigos = totalamigos.replace("0","No tiene amigos❌")
        



        


      
      
        

        
        

        response = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" +  f"{api}" + "&steamid=" + f"{steamid}" + "&format=json")


        try:
         juegos = response.json()["response"]["games"]
        except KeyError:
         juegos=""
        juegos=(str(len(juegos)))
        
        
        


        

        
 
        
        
         
         

         
        



                
        
        


        



        
            
        

        response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" f"{api}" + "&steamids=" f"{steamid}")
        
        

        try:
         fecha = response.json()['response']['players'][0]['timecreated']
         ts = int(fecha)
         fecha = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
         
   
        except KeyError:
                fecha="No se encuentra❌" 


        try:
         ultimocierre = response.json()['response']['players'][0]['lastlogoff']
         ts = int(ultimocierre)
         ultimocierre = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
         
   
        except KeyError:
                ultimocierre="No se encuentra❌" 
                

      



        try:  
         avatar = response.json()['response']['players'][0]['avatar']
        except IndexError:
                avatar=""

        
        
        try:
         estado = response.json()['response']['players'][0]['personastate']
        except IndexError:
                estado="No se encuentra❌"


        try:
         usuario = response.json()['response']['players'][0]['personaname']
        except IndexError:
            usuario="No se encuentra❌"
        
        
        
        try:
         bandera = response.json()['response']['players'][0]['loccountrycode']


        except KeyError:
                bandera="no se encuentra❌" 

        except IndexError:
                bandera="no se encuentra❌"     
      
    
 
       

        
       
        


     
        
              
                
        embed = discord.Embed(title="info usuario Steam🡺 " f"{usuario}",  description="•Steam ID 64🡺 "f"{steamid}" "\n\n•Estado🡺 " + (str(estado).replace("0","Desconectado 🔴").replace("1","Conectado 🟢").replace("3","ausente 🟠").replace("4","Conectado 🟢")+ "\n\n•Pais🡺 "  + f"{bandera}".replace("AF","Afganistán") .replace("AL","Albania") .replace("DE","Alemania") .replace("AD", "Andorra") .replace("AO","Angola") .replace("AI","Anguila") .replace("AG","Antigua y Barbuda") .replace("AQ","Antártida") .replace("SA","Arabia Saudí") .replace("DZ","Argelia") .replace("AR","Argentina") .replace("AM","Armenia") .replace("AW","Aruba") .replace("AU","Australia") .replace("AT","Austria") .replace("AZ","Azerbaiyán") .replace("BL","BL") .replace("BQ","BQ") .replace("BS","Bahamas") .replace("BD","Bangladés") .replace("BB","Barbados") .replace("BZ","Belice") .replace("BJ","Benín") .replace("BM","Bermudas") .replace("BY","Bielorrusia") .replace("BO","Bolivia") .replace("BA","Bosnia y Herzegovina") .replace("BW","Botsuana") .replace("BR","Brasil") .replace("BN","Brunéi") .replace("BG","Bulgaria") .replace("BF","Burkina Faso") .replace("BI","Burundi") .replace("BT","Bután") .replace("BE","Bélgica") .replace("CU","CU") .replace("CW","CW") .replace("CV","Cabo Verde") .replace("KH","Camboya") .replace("CM","Camerún") .replace("CA","Canadá") .replace("QA","Catar") .replace("TD","Chad") .replace("CL","Chile") .replace("CN","China") .replace("CY","Chipre") .replace("CO","Colombia") .replace("KM","Comoras") .replace("CG","Congo") .replace("KR","Corea del Sur") .replace("CR","Costa Rica") .replace("CI","Costa de Marfil") .replace("HR","Croacia") .replace("DK","Dinamarca") .replace("DM","Dominica") .replace("EC","Ecuador") .replace("EG","Egipto") .replace("SV","El Salvador") .replace("AE","Emiratos Árabes Unidos") .replace("ER","Eritrea") .replace("SK","Eslovaquia") .replace("SI","Eslovenia") .replace("ES","España") .replace("US","Estados Unidos") .replace("EE","Estonia") .replace("SZ","Esuatini") .replace("ET","Etiopia") .replace("PH","Filipinas") .replace("FI","Finlandia") .replace("FJ","Fiyi") .replace("FR","Francia") .replace("GA","Gabón") .replace("GM","Gambia") .replace("GE","Georgia") .replace("GH","Ghana") .replace("GI","Gibraltar") .replace("GD","Granada") .replace("GR","Grecia") .replace("GL","Groenlandia") .replace("GP","Guadalupe") .replace("GU","Guam") .replace("GT","Guatemala") .replace("GF","Guayana Francesa") .replace("GG","Guernesey") .replace("GN","Guinea") .replace("GW","Guinea-Bisáu") .replace("GQ","Guinea Ecuatorial") .replace("GY","Guyana") .replace("HT","Haití") .replace("HN","Honduras") .replace("HK","Hong Kong") .replace("HU","Hungría") .replace("IN","India") .replace("ID","Indonesia") .replace("IQ","Irak") .replace("IE","Irlanda") .replace("IR","Irán") .replace("BV","Isla Bouvet") .replace("NF","Isla Norfolk") .replace("IM","Isla de Man") .replace("CX","Isla de Navidad") .replace("IS","Islandia") .replace("AX","Islas Aland") .replace("KY","Islas Caimán") .replace("CC","Islas Cocos") .replace("CK","Islas Cook") .replace("FO","Islas Feroe") .replace("GS","Islas Georgias del Sur y Sandwich del Sur") .replace("HM","Islas Heard y Mc Donald") .replace("FK","Islas Malvinas") .replace("MP","Islas Marianas del Norte") .replace("MH","Islas Marshall") .replace("PN","Islas Pitcairn") .replace("SB","Islas Salomón") .replace("TC","Islas Turcas y Caicos") .replace("UM","Islas Ultramarinas Menores de Estados Unidos") .replace("VG","Islas Vírgenes Británicas") .replace("VI","Islas Vírgenes de los Estados Unidos") .replace("IL","Israel") .replace("IT","Italia") .replace("JM","Jamaica") .replace("JP","Japón") .replace("JE","Jersey") .replace("JO","Jordania") .replace("KZ","Kazajistán") .replace("KE","Kenia") .replace("KG","Kirguistán") .replace("KI","Kiribati") .replace("XK","Kosovo") .replace("KW","Kuwait") .replace("LA","Laos") .replace("LS","Lesoto") .replace("LV","Letonia") .replace("LR","Liberia") .replace("LY","Libia") .replace("LI","Liechtenstein") .replace("LT","Lituania") .replace("LU","Luxemburgo") .replace("LB","Líbano") .replace("MF","MF") .replace("MO","Macao") .replace("MK","Macedonia del Norte") .replace("MG","Madagascar") .replace("MY","Malasia") .replace("MW","Malaui") .replace("MV","Maldivas") .replace("ML","Mali") .replace("MT","Malta") .replace("MA","Marruecos") .replace("MQ","Martinica") .replace("MU","Mauricio") .replace("MR","Mauritania") .replace("YT","Mayotte") .replace("FM","Micronesia") .replace("MD","Moldavia") .replace("MN","Mongolia") .replace("ME","Montenegro") .replace("MS","Montserrat") .replace("MZ","Mozambique") .replace("MM","Myanmar") .replace("MX","México") .replace("MC","Mónaco") .replace("NA","Namibia") .replace("NR","Nauru") .replace("NP","Nepal") .replace("NI","Nicaragua") .replace("NG","Nigeria") .replace("NU","Niue") .replace("NO","Noruega") .replace("NC","Nueva Caledonia") .replace("NZ","Nueva Zelanda") .replace("NE","Níger") .replace("OM","Omán") .replace("PK","Pakistán") .replace("PW","Palaos") .replace("PS","Palestina") .replace("PA","Panamá") .replace("PG","Papúa Nueva Guinea") .replace("PY","Paraguay") .replace("NL","Países Bajos") .replace("PE","Perú") .replace("PF","Polinesia Francesa") .replace("PL","Polonia") .replace("PT","Portugal") .replace("PR","Puerto Rico") .replace("GB","Reino Unido") .replace("BH","Reino de Baréin") .replace("CF","República Centroafricana") .replace("CZ","República Checa") .replace("CD","República Democrática del Congo") .replace("DO","República Dominicana") .replace("RE","Reunión") .replace("RW","Ruanda") .replace("RO","Rumanía") .replace("RU","Rusia") .replace("SS","SS") .replace("SX","SX") .replace("WS","Samoa") .replace("AS","Samoa Americana") .replace("KN","San Cristóbal y Nieves") .replace("SM","San Marino") .replace("PM","San Pedro y Miquelón") .replace("VC","San Vicente y las Granadinas") .replace("SH","Santa Elena") .replace("LC","Santa Lucía") .replace("VA","Santa Sede") .replace("ST","Santo Tomé y Príncipe") .replace("SN","Senegal") .replace("RS","Serbia") .replace("SC","Seychelles") .replace("SL","Sierra Leona") .replace("SG","Singapur") .replace("SY","Siria") .replace("SO","Somalia") .replace("LK","Sri Lanka") .replace("ZA","Sudáfrica") .replace("SD","Sudán") .replace("SE","Suecia") .replace("CH","Suiza") .replace("SR","Surinam") .replace("SJ","Svalbard y Jan Mayen") .replace("EH","Sáhara Occidental") .replace("TH","Tailandia") .replace("TW","Taiwán") .replace("TZ","Tanzania") .replace("TJ","Tayikistán") .replace("IO","Territorio Británico del Océano Índico") .replace("TF","Territorios Australes Franceses") .replace("TL","Timor Oriental") .replace("TG","Togo") .replace("TK","Tokelau") .replace("TO","Tonga") .replace("TT","Trinidad y Tobago") .replace("TM","Turkmenistán") .replace("TR","Turquía") .replace("TV","Tuvalu") .replace("TN","Túnez") .replace("UA","Ucrania") .replace("UG","Uganda") .replace("UY","Uruguay") .replace("UZ","Uzbekistán") .replace("VU","Vanuatu") .replace("VE","Venezuela") .replace("VN","Vietnam") .replace("WF","Wallis y Futuna") .replace("YE","Yemen") .replace("DJ","Yibuti") .replace("ZM","Zambia") .replace("ZW","Zimbabue").replace("KP","korea") + "\n\n•Creado🡺 " + f"{fecha}" + "\n\n•último cierre de sesion🡺 " + f"{ultimocierre}" + "\n\n•Jugando🡺 " +jugandoSteam+ jugandoSteam1.replace("Currently In-Game"," ") + "\n\n•Total Amigos🡺 " + totalamigos) + "\n\n•Juegos Totales🡺 " + juegos, color=discord.Color.random())
        

        embed.set_thumbnail(url=f"{avatar}")
        
        embed.set_author(name="steam", icon_url=link)
        
        
        await ctx.send(embed=embed)


        
        
        
        

            
        
 
 
 
@bot.event
async def on_ready():
    print("BOT listo!")
    
 
    
bot.run(config['Token_BOT']) #OBTEN UN TOKEN EN: https://discord.com/developers/applications
