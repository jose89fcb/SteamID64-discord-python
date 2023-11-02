import requests, bs4
import json
import discord
from discord.ext import commands
import datetime
from datetime import datetime

with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config['prefijo'])
bot.remove_command("help")
api = config['Api_Steam']

@bot.command()
async def steamid(ctx, *, steamid):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" f"{api}" + "&vanityurl=" f"{steamid}")

    try:
        url = response.json()['response']['players'][0]['avatarfull']
    except KeyError:
        url = " "
    steam = requests.get(f"https://steamcommunity.com/id/" f"{steamid}")
    
    infoplaca = bs4.BeautifulSoup(steam.text, "lxml")
    NombrePlaca = infoplaca.select("img", class_="profile_flag")
    link = NombrePlaca[5].get("src").replace("_full.jpg", "https://i.imgur.com/zJKj349.png")

    jugando = bs4.BeautifulSoup(steam.content, "html.parser")

    try:
        jugandoSteam = jugando.find("div", class_="profile_in_game_name").text
        jugandoSteam1 = jugando.find("div", class_="profile_in_game_header").text
    except AttributeError:
        jugandoSteam = "No está jugando"

    try:
        jugandoSteam1 = jugandoSteam1.replace("In non-Steam game", "En un juego que no es de Steam")
    except UnboundLocalError:
        jugandoSteam1 = ""

    try:
        steamid = response.json()['response']['steamid']
    except KeyError:
        steamid = "No se encuentra❌"

    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + f"{api}" + "&steamid=" + f"{steamid}" + "&relationship=friend")

    try:
        totalamigos = response.json()['friendslist']['friends']
    except KeyError:
        totalamigos = ""
    totalamigos = (str(len(totalamigos)))
    totalamigos = totalamigos.replace("0", "No tiene amigos❌")

    response = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + f"{api}" + "&steamid=" + f"{steamid}" + "&format=json")
    
    try:
        juegos = response.json()["response"]["games"]
    except KeyError:
        juegos = ""
    juegos = (str(len(juegos)))

    response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" f"{api}" + "&steamids=" f"{steamid}")
    
    try:
        fecha = response.json()['response']['players'][0]['timecreated']
        ts = int(fecha)
        fecha = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
    except KeyError:
        fecha = "No se encuentra❌"

    try:
        ultimocierre = response.json()['response']['players'][0]['lastlogoff']
        ts = int(ultimocierre)
        ultimocierre = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:M:%S')
    except KeyError:
        ultimocierre = "No se encuentra❌"

    try:
        avatar = response.json()['response']['players'][0]['avatar']
    except IndexError:
        avatar = ""

    try:
        estado = response.json()['response']['players'][0]['personastate']
    except IndexError:
        estado = "No se encuentra❌"

    try:
        usuario = response.json()['response']['players'][0]['personaname']
    except IndexError:
        usuario = "No se encuentra❌"
    
    try:
        bandera = response.json()['response']['players'][0]['loccountrycode']
    except KeyError:
        bandera = "no se encuentra❌"
    except IndexError:
        bandera = "no se encuentra❌"



     

    codigo_pais_dic = {
          "AF": "Afganistán",
        "AL": "Albania",
        "DE": "Alemania",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguila",
        "AG": "Antigua y Barbuda",
        "AQ": "Antártida",
        "SA": "Arabia Saudí",
        "DZ": "Argelia",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaiyán",
        "BL": "BL",
        "BQ": "BQ",
        "BS": "Bahamas",
        "BD": "Bangladés",
        "BB": "Barbados",
        "BZ": "Belice",
        "BJ": "Benín",
        "BM": "Bermudas",
        "BY": "Bielorrusia",
        "BO": "Bolivia",
        "BA": "Bosnia y Herzegovina",
        "BW": "Botsuana",
        "BR": "Brasil",
        "BN": "Brunéi",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "BT": "Bután",
        "BE": "Bélgica",
        "CU": "CU",
        "CW": "CW",
        "CV": "Cabo Verde",
        "KH": "Camboya",
        "CM": "Camerún",
        "CA": "Canadá",
        "QA": "Catar",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CY": "Chipre",
        "CO": "Colombia",
        "KM": "Comoras",
        "CG": "Congo",
        "KR": "Corea del Sur",
        "CR": "Costa Rica",
        "CI": "Costa de Marfil",
        "HR": "Croacia",
        "DK": "Dinamarca",
        "DM": "Dominica",
        "EC": "Ecuador",
        "EG": "Egipto",
        "SV": "El Salvador",
        "AE": "Emiratos Árabes Unidos",
        "ER": "Eritrea",
        "SK": "Eslovaquia",
        "SI": "Eslovenia",
        "ES": "España",
        "US": "Estados Unidos",
        "EE": "Estonia",
        "SZ": "Esuatini",
        "ET": "Etiopía",
        "PH": "Filipinas",
        "FI": "Finlandia",
        "FJ": "Fiyi",
        "FR": "Francia",
        "GA": "Gabón",
        "GM": "Gambia",
        "GE": "Georgia",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GD": "Granada",
        "GR": "Grecia",
        "GL": "Groenlandia",
        "GP": "Guadalupe",
        "GU": "Guam",
        "GT": "Guatemala",
        "GF": "Guayana Francesa",
        "GG": "Guernesey",
        "GN": "Guinea",
        "GW": "Guinea-Bisáu",
        "GQ": "Guinea Ecuatorial",
        "GY": "Guyana",
        "HT": "Haití",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungría",
        "IN": "India",
        "ID": "Indonesia",
        "IQ": "Irak",
        "IE": "Irlanda",
        "IR": "Irán",
        "BV": "Isla Bouvet",
        "NF": "Isla Norfolk",
        "IM": "Isla de Man",
        "CX": "Isla de Navidad",
        "IS": "Islandia",
        "AX": "Islas Aland",
        "KY": "Islas Caimán",
        "CC": "Islas Cocos",
        "CK": "Islas Cook",
        "FO": "Islas Feroe",
        "GS": "Islas Georgias del Sur y Sandwich del Sur",
        "HM": "Islas Heard y Mc Donald",
        "FK": "Islas Malvinas",
        "MP": "Islas Marianas del Norte",
        "MH": "Islas Marshall",
        "PN": "Islas Pitcairn",
        "SB": "Islas Salomón",
        "TC": "Islas Turcas y Caicos",
        "UM": "Islas Ultramarinas Menores de Estados Unidos",
        "VG": "Islas Vírgenes Británicas",
        "VI": "Islas Vírgenes de los Estados Unidos",
        "IL": "Israel",
        "IT": "Italia",
        "JM": "Jamaica",
        "JP": "Japón",
        "JE": "Jersey",
        "JO": "Jordania",
        "KZ": "Kazajistán",
        "KE": "Kenia",
        "KG": "Kirguistán",
        "KI": "Kiribati",
        "XK": "Kosovo",
        "KW": "Kuwait",
        "LA": "Laos",
        "LS": "Lesoto",
        "LV": "Letonia",
        "LR": "Liberia",
        "LY": "Libia",
        "LI": "Liechtenstein",
        "LT": "Lituania",
        "LU": "Luxemburgo",
        "LB": "Líbano",
        "MF": "MF",
        "MO": "Macao",
        "MK": "Macedonia del Norte",
        "MG": "Madagascar",
        "MY": "Malasia",
        "MW": "Malaui",
        "MV": "Maldivas",
        "ML": "Mali",
        "MT": "Malta",
        "MA": "Marruecos",
        "MQ": "Martinica",
        "MU": "Mauricio",
        "MR": "Mauritania",
        "YT": "Mayotte",
        "FM": "Micronesia",
        "MD": "Moldavia",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MS": "Montserrat",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "MX": "México",
        "MC": "Mónaco",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NI": "Nicaragua",
        "NG": "Nigeria",
        "NU": "Niue",
        "NO": "Noruega",
        "NC": "Nueva Caledonia",
        "NZ": "Nueva Zelanda",
        "NE": "Níger",
        "OM": "Omán",
        "PK": "Pakistán",
        "PW": "Palaos",
        "PS": "Palestina",
        "PA": "Panamá",
        "PG": "Papúa Nueva Guinea",
        "PY": "Paraguay",
        "NL": "Países Bajos",
        "PE": "Perú",
        "PF": "Polinesia Francesa",
        "PL": "Polonia",
        "PT": "Portugal",
        "PR": "Puerto Rico",
        "GB": "Reino Unido",
        "BH": "Reino de Baréin",
        "CF": "República Centroafricana",
        "CZ": "República Checa",
        "CD": "República Democrática del Congo",
        "DO": "República Dominicana",
        "RE": "Reunión",
        "RW": "Ruanda",
        "RO": "Rumanía",
        "RU": "Rusia",
        "SS": "SS",
        "SX": "SX",
        "WS": "Samoa",
        "AS": "Samoa Americana",
        "KN": "San Cristóbal y Nieves",
        "SM": "San Marino",
        "PM": "San Pedro y Miquelón",
        "VC": "San Vicente y las Granadinas",
        "SH": "Santa Elena",
        "LC": "Santa Lucía",
        "VA": "Santa Sede",
        "ST": "Santo Tomé y Príncipe",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leona",
        "SG": "Singapur",
        "SY": "Siria",
        "SO": "Somalia",
        "LK": "Sri Lanka",
        "ZA": "Sudáfrica",
        "SD": "Sudán",
        "SE": "Suecia",
        "CH": "Suiza",
        "SR": "Surinam",
        "SJ": "Svalbard y Jan Mayen",
        "EH": "Sáhara Occidental",
        "TH": "Tailandia",
        "TW": "Taiwán",
        "TZ": "Tanzania",
        "TJ": "Tayikistán",
        "IO": "Territorio Británico del Océano Índico",
        "TF": "Territorios Australes Franceses",
        "TL": "Timor Oriental",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad y Tobago",
        "TM": "Turkmenistán",
        "TR": "Turquía",
        "TV": "Tuvalu",
        "TN": "Túnez",
        "UA": "Ucrania",
        "UG": "Uganda",
        "UY": "Uruguay",
        "UZ": "Uzbekistán",
        "VU": "Vanuatu",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "WF": "Wallis y Futuna",
        "YE": "Yemen",
        "DJ": "Yibuti",
        "ZM": "Zambia",
        "ZW": "Zimbabue",
        "KP": "Korea"
    }
    
    try:
        nombre_pais = codigo_pais_dic[bandera]
    except KeyError:
        nombre_pais = "País Desconocido"


    


    estado_dic = {
    0: "Desconectado 🔴",
    1: "Conectado 🟢",
    3: "Ausente 🟠",
    4: "Conectado 🟢"
    }
    estado_steam = estado_dic[estado]
    
   

    embed = discord.Embed(
        title=f"info usuario Steam🡺 {usuario}",
        description=f"•Steam ID 64🡺 {steamid}\n\n"
        f"•Estado🡺 {estado_steam}\n\n"
        f"•Pais🡺 {str(nombre_pais)}\n\n"
        f"•Creado🡺 {fecha}\n\n"
        f"•último cierre de sesion🡺 {ultimocierre}\n\n"
        f"•Jugando🡺 {jugandoSteam}{jugandoSteam1.replace('Currently In-Game', ' ')}\n\n"
        f"•Total Amigos🡺 {totalamigos}\n\n"
        f"•Juegos Totales🡺 {juegos}",
        color=discord.Color.random())

    embed.set_thumbnail(url=f"{avatar}")
    embed.set_author(name="steam", icon_url=link)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print("BOT listo!")

bot.run(config['Token_BOT'])
