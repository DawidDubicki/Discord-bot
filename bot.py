import lightbulb
import hikari
import json
import requests


def get_kog_data(nickname):
    web = requests.post('https://kog.tw/api.php', json={"type": "players", "player": f"{nickname}"})
    element = json.loads(web.json()['data'])
    return element


def get_skin(nickname):
    element = get_kog_data(nickname)
    last_tee = element['last_tee'][0]
    skin_name = last_tee['SkinName']
    body_color = last_tee['SkinColorBody']
    feet_color = last_tee['SkinColorFeet']
    skin_pic = f'https://kog.tw/render_tee.php?skin={skin_name}&body_color={body_color}&feet_color={feet_color}'
    return skin_pic


def get_fixed_points(nickname):
    element = get_kog_data(nickname)
    points = element['points']['Points']
    rank = element['points']['Rank']
    season_points = element['points']['Seasonpoints']
    all_points = element['points']['TPoints']

    return [rank, points, season_points, all_points]


def get_last_teammates(nickname):
    element = get_kog_data(nickname)
    players = "\n".join([i['Namee'] + " with " + str(i['finishesnumber']) + " finished maps together" for i in element['lastteammates']])
    return players


def get_maps(nickname):
    element = get_kog_data(nickname)
    easy_maps = f"{element['fin_main'][0]['myoutput']} out of {element['easy_maps'][0]['myoutput']}"
    main_maps = f"{element['fin_mn'][0]['myoutput']} out of {element['main_maps'][0]['myoutput']}"
    hard_maps = f"{element['fin_hrd'][0]['myoutput']} out of {element['hard_maps'][0]['myoutput']}"
    insane_maps = f"{element['fin_ins'][0]['myoutput']} out of {element['ins_maps'][0]['myoutput']}"
    extreme_maps = f"{element['fin_ext'][0]['myoutput']} out of {element['ext_maps'][0]['myoutput']}"
    return [easy_maps, main_maps, hard_maps, insane_maps, extreme_maps]


bot = lightbulb.BotApp(token='Change token')


@bot.command
@lightbulb.option('name', 'name of the player')
@lightbulb.command('points', 'points command')
@lightbulb.implements(lightbulb.SlashCommand)
async def fixed_points(context):
    try:
        nick = context.options.name
        if nick.lower() == 'simp':
            nick = 'Gotie'
        points = get_fixed_points(nick)
        embed = hikari.Embed(title=nick)
        embed.set_thumbnail(get_skin(nick))
        embed.add_field('Rank:', points[0])
        embed.add_field('Fixed Points:', points[1])
        embed.add_field('Season Points:', points[2])
        embed.add_field('Points Overall:', points[3])
        await context.respond(embed)
    except:
        await context.respond(f"Player with nickname {nick} does not exist")


@bot.command
@lightbulb.command('help', 'shows all commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def points(context):
    try:
        embed = hikari.Embed(title='Commands')
        embed.add_field('/points [name]:', 'Shows user points')
        embed.add_field('/teammates [name]:', 'Shows most played teammates')
        await context.respond(embed)
    except:
        await context.respond(f"Something went wrong")


@bot.command
@lightbulb.option('name', 'name of the player')
@lightbulb.command('teammates', 'Show players most played with')
@lightbulb.implements(lightbulb.SlashCommand)
async def last_teammates(context):
    try:
        nick = context.options.name
        if nick.lower() == 'simp':
            nick = 'Gotie'
        teammates = get_last_teammates(nick)
        embed = hikari.Embed(title=nick)
        embed.add_field('Teammates most played with:\n', teammates)
        embed.set_thumbnail(get_skin(nick))
        await context.respond(embed)
    except:
        await context.respond(f"Player with nickname {nick} does not exist")


@bot.command
@lightbulb.option('name', 'name of the player')
@lightbulb.command('finishedmaps', 'Shows ammount of finished maps')
@lightbulb.implements(lightbulb.SlashCommand)
async def finished_maps(context):
    try:
        nick = context.options.name
        if nick.lower() == 'simp':
            nick = 'Gotie'
        maps = get_maps(nick)
        embed = hikari.Embed(title=nick)
        embed.set_thumbnail(get_skin(nick))
        embed.add_field('Easy maps:\n', maps[0])
        embed.add_field('Main maps:\n', maps[1])
        embed.add_field('Hard maps:\n', maps[2])
        embed.add_field('Insane maps:\n', maps[3])
        embed.add_field('Extreme maps:\n', maps[4])
        await context.respond(embed)
    except:
        await context.respond(f"Player with nickname {nick} does not exist")

bot.run()
