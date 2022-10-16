import discord
import sqlite3
import requests
import random
import math
import os
import aiohttp
import json
from discord.ext import commands
from discord.utils import get
from discord import utils
from discord.ext import commands, tasks
import sqlite3
from async_timeout import timeout
import asyncio
import functools
import itertools


client = commands.Bot(command_prefix = '*')

PREFIX = '*'

client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    print (f'{client.user} was connected')

    await client.change_presence(activity=discord.Streaming(name='*хелп', url='https://twitch.tv/404'))

@client.command()
async def хелп(ctx):
    embed = discord.Embed(title = 'ПОМОЩЬ', description = 'Каждый день добавляются команды!\nВот все категории:\n\n1. **Модерирование** - `*модерация`\n\n2. **Утилиты** - `*утилиты`\n\n3. **Развлечение** - `*развлечение`\n\n4. **Рандом** - `*рандом`\n\n5. **NSFW** - `*nsfw`\n\n6. **Ролевые** - `*ролевые`',color = 0x00FF00)
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#Команды модерации
@client.command(name='ban', brief='Банит участника', usage='ban <@user> <reason>', aliases = ['бан'])
@commands.has_permissions(ban_members = True)
async def ban(ctx: commands.context.Context, member: discord.Member, *, reason):
    await ctx.guild.ban(user=member, reason=reason)
    embed = discord.Embed(color =  0x008000 ,title = 'Бан участника', description = f'**Участник был забанен!\nПричина** *{reason}*')
    embed.set_author(name="")
    embed.set_footer(text=f"Модератор: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(name='kick', brief='Кикает участника', usage='kick <@user> <reason>', aliases = ['кик'])
@commands.has_permissions(kick_members = True)
async def kick(ctx: commands.context.Context, member: discord.Member, *, reason):
    await ctx.guild.kick(user=member, reason=reason)
    embed = discord.Embed(color =  0x008000 ,title = 'Кик участника', description = f'**Участник был кикнут!\nПричина** *{reason}*')
    embed.set_author(name="")
    embed.set_footer(text=f"Модератор: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ['очистка'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(color = 0x008000, title="Произошла очистка", description=f"Удалено `{amount}`")    
    embed.set_author(name="")
    embed.set_footer(text=f"Модератор: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    massage = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await massage.delete()

@client.command()
async def модерация(ctx):
    embed = discord.Embed(title = 'Cazino BOT', description = '**МОДЕРИРОВАНИЕ**',color = 0x00FF00)
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`бан, ban` - Забанить пользователя\n`ban <упоминание или id> <причина>`\n\n`кик, kick` - Кикнуть пользователя\n`kick <упоминание или id> <причина>`\n\n`очистить, clear` - Очистить определённое кол-во сообщений в чате\n`clear <кол-во сообщений>`')
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#утилиты
@client.command(aliases = ['аватар'])
async def avatar(ctx, member: discord.Member  = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(color = 0x008000, title = f"Аватар участника - {member.name}", description = f"[Скачать]({member.avatar_url})")
    embed.set_image(url = member.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ['бинфо'])
async def binfo(ctx):
    embed = discord.Embed(color = 0x008000, title = 'Информация о боте', description = f'**Разработчик**\nazino777#0962\n\n**Система**\nPython `3.10.4 (Mar 23 2022, 23:13:41)`\nВерсия discord.py `1.7.3`\n\n**Префикс:**\n!')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command(aliases = ['юзер'])
async def user(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    if member == None:
        emb = discord.Embed(title="Информация о пользователе", color= 0x008000)
        emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о пользователе", color= 0x008000)
        emb.add_field(name="Имя:", value=member.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y"),inline=False)
        embed.set_author(name="")
        embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

@client.command(aliases = ['сервер'])
async def server(ctx):
    guild=ctx.message.guild
    embed=discord.Embed(title=f"Информация о сервере {ctx.guild.name}", color=0x008000)
    embed.add_field(name="Участники", value=f"Всего: {len(ctx.guild.members)}\nИз них боты: {len(([member for member in ctx.guild.members if member.bot]))}\nЛюди: {len(([member for member in ctx.guild.members if not member.bot]))}", inline=True)
    embed.add_field(name="Каналы", value=f"Всего: {len(ctx.guild.channels)}\nИз них голосовые: {len(ctx.guild.voice_channels)}\nТекстовых: {len(ctx.guild.text_channels)}", inline=True)
    embed.add_field(name="Дата создания сервера", value=f"{ctx.guild.created_at.day}.{ctx.guild.created_at.month}.{ctx.guild.created_at.year}, {ctx.guild.created_at.hour}:{ctx.guild.created_at.minute}", inline=True)
    embed.add_field(name="Роли", value=len(ctx.guild.roles), inline=True)
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(aliases = ['связь'])
async def support(ctx):
    embed = discord.Embed(title = 'Связь', description = '', color = 0x008000)
    embed.add_field(name = 'Информация для связи:', value = 'Сервер поддержки: https://discord.gg/urjAEwbUJz')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@client.command()
async def утилиты(ctx):
    embed = discord.Embed(title = 'Cazino BOT', description = '**УТИЛИТЫ**',color = 0x00FF00)
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`avatar, аватар` - Узнать аватар пользователя\n`аватар <упоминание>`\n\n`binfo, бинфо` - Узнать информацию о боте\n`бинфо`\n\n`user, юзер` - Узнать информацию о пользователе\n`юзер`\n\n`support, связь` - Узнать как можно связаться с создателем бота\n`связь`\n\n`server, сервер` - Узнать информацию о сервере\n`сервер`\n\n`ben, бен` - Задать вопрос бену \n`бен <вопрос>`')
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#развлечение
PHL = ["https://img2.joyreactor.cc/pics/post/%D1%87%D1%83%D1%80%D0%BA%D0%B0-%D1%87%D0%B5%D1%87%D0%BD%D1%8F-%D1%83%D0%BD%D0%B8%D0%B2%D0%B5%D1%80-%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D0%B0-269049.jpeg"]

@client.command(aliases = ['чурка'])
async def churka(ctx, member: discord.Member):
    embed = discord.Embed(title="", description="**{0}** теперь чурка!".format(member.name, ctx.message.author.name), color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(PHL))
    await ctx.send(embed=embed)

@client.command(aliases = ['монетка'])
async def money(ctx):
    await ctx.send(random.choice(['Поздравляю, тебе выпал орёл!', 'Поздравляю, тебе выпала решка!']))

@client.command()
async def развлечение(ctx):
    embed = discord.Embed(color = 0x00FF00, title = 'Cazino BOT', description = '**РАЗВЛЕЧЕНИЕ**')
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`money, монетка` - Подкинуть монетку\n`money`\n\n`чурка, churka` - Назвать кого-то чуркой\n`churka <упоминание>`\n\n`shar, шар` - Задать вопрос шару предсказаний\n`shar <вопрос>`')
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#random commands
@client.command(aliases = ['собака'])
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Wurf 🐶", color= 0x008000)
   embed.set_image(url=dogjson['link'])
   await ctx.send(embed=embed)

@client.command()
async def рандом(ctx):
    embed = discord.Embed(color = 0x00FF00, title = 'Cazino BOT', description = '**РАНДОМ**')
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`dog, собака` - Случайная картинка собаки\n`собака`')
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#nsfw
NSFW = ["https://media.tenor.com/Tk2xYonmrsEAAAAM/anime-blushing.gif",
    "https://media.tenor.com/4SzGnEAJ3uQAAAAM/arata-rosetta.gif",
    "https://media.tenor.com/6aZp0W36zAwAAAAM/catgirl-anime.gif",
    "https://media.tenor.com/Pn-mn-nqqrcAAAAM/anime-cute.gif",
    "https://media.tenor.com/TxAEQPfWZ9MAAAAM/chinatsu-yoshikawa-anime.gif",
    "https://media.tenor.com/8B6WJu2xiJAAAAAS/fairy-tail-lucy-heartfilia.gif",
    "https://media.tenor.com/f8cdEpuaxHgAAAAM/hayase-nagatoro-nagatoro.gif",
    "https://media.tenor.com/R4UbdHA3bNgAAAAM/anime-sexy.gif",
    "https://media.tenor.com/TkmMEz3owbgAAAAM/nsfw-anime.gif",
    "https://media.tenor.com/qzEyDsLvn0MAAAAM/punchline-anime.gif",
    "https://media.tenor.com/NB9f0cJ-27kAAAAS/anime-ecchi.gif",]

@client.command(aliases = ['аниме'])
async def anime(ctx):
    embed = discord.Embed(title="", description="", color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(NSFW))
    await ctx.send(embed=embed)

BOOBS = ["https://media.tenor.com/I9yjcAGMizcAAAAM/boobs-anime.gif",
    "https://media.tenor.com/EMnh21qab5cAAAAM/anime-boobs-anime.gif",
    "https://media.tenor.com/rJH1bgY-V14AAAAM/anime-boobs.gif",
    "https://media.tenor.com/YlWinNuaSHUAAAAM/prison-school-mekio.gif",
    "https://media.tenor.com/35na9Tn5CF0AAAAM/heheehehhe.gif",
    "https://media.tenor.com/iol81Ime-7IAAAAM/sexy-anime.gif",
    "https://media.tenor.com/F9-AgR_L8EkAAAAM/boobs-anime.gif",
    "https://media.tenor.com/xLKeH_nMlxcAAAAM/tony-col-anime.gif",
    "https://media.tenor.com/V4egNiSubFkAAAAM/nekopara-cinnamon.gif",]

@client.command(aliases = ['сиськи'])
async def boobs(ctx):
    embed = discord.Embed(title="", description="", color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(BOOBS))
    await ctx.send(embed=embed)

ASS = ["https://media.tenor.com/kEB9QugInOIAAAAM/myero-academia.gif",
    "https://media.tenor.com/k9HIPrrYpC4AAAAM/anime-ass.gif",
    "https://media.tenor.com/sN4wIDoLiIMAAAAM/konosuba-aqua.gif",
    "https://media.tenor.com/JXbgGRTORscAAAAM/anime-ass.gif",
    "https://media.tenor.com/FYba6wxrFYIAAAAM/lav-ass-anime.gif",
    "https://media.tenor.com/o5qga0P3gmgAAAAM/anime-natsuki.gif",
    "https://media.tenor.com/7OZxadKngSoAAAAM/beach-bod-how-heavy-are-the-dumbbells-that-you-lift.gif",
    "https://media.tenor.com/lXXfKoLv2fEAAAAM/iam4ming-butt.gif",
    "https://media.tenor.com/ED8v4vUbKn0AAAAM/anime-bounce.gif",]

@client.command(aliases = ['жопа'])
async def ass(ctx):
    embed = discord.Embed(title="", description="", color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(ASS))
    await ctx.send(embed=embed)

@client.command()
async def nsfw(ctx):
    embed = discord.Embed(title = 'Cazino BOT', description = '**NSFW**',color = 0x00FF00)
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`anime, аниме` - Отправить хентай\n`аниме`\n\n`boobs, сиськи` - Отправить сиськи\n`сиськи`\n\n`ass, жопа` - Отправить жопу\n`жопа`\n\n')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

#roles
HUG = ["https://media.tenor.com/o_LpFqXVbyIAAAAS/polar-bear.gif",
    "https://media.tenor.com/PCIu5V-_c1QAAAAS/iloveyousomuch-iloveyou.gif",
    "https://media.tenor.com/lzKyZchfMzAAAAAS/anime-hug.gif",
    "https://media.tenor.com/0T3_4tv71-kAAAAS/anime-happy.gif",
    "https://media.tenor.com/ucnupKiykIUAAAAS/hugs.gif",
    "https://media.tenor.com/RFY9xILOZHUAAAAS/princess-mononoke-hug.gif",
    "https://media.tenor.com/mB_y2KUsyuoAAAAM/cuddle-anime-hug.gif",
    "https://media.tenor.com/XyMvYx1xcJAAAAAM/super-excited.gif",
    "https://media.tenor.com/Qw4m3inaSZYAAAAM/crying-anime-kyoukai-no-kanata-hug.gif",
    "https://media.tenor.com/AJ_iYJ8nf3sAAAAS/hug.gif",]

KISS = ["https://media.tenor.com/tJiq6XLJccIAAAAS/kiss-couple.gif",
    "https://media.tenor.com/3wE3JNW0fswAAAAS/anime-kiss-love.gif",
    "https://media.tenor.com/nRdyrvS3qa4AAAAS/anime-kiss.gif",
    "https://media.tenor.com/9jB6M6aoW0AAAAAS/val-ally-kiss.gif",
    "https://media.tenor.com/GAr1rMm39pcAAAAS/anime-hug.gif",
    "https://media.tenor.com/Fyq9izHlreQAAAAS/my-little-monster-haru-yoshida.gif",
    "https://media.tenor.com/XkOeAG4Z54gAAAAS/love-you-ily.gif",
    "https://media.tenor.com/lK1PF-Xv1O4AAAAS/yato-anime-noragami.gif",
    "https://media.tenor.com/rQ8qlj_oQ-YAAAAM/anime-kiss.gif",
    "https://media.tenor.com/g9HjxRZM2C8AAAAM/anime-love.gif",]

HIT = ["https://media.tenor.com/vZnHUMCUU6AAAAAM/handa-naru-barakamon.gif",
    "https://media.tenor.com/1T5bgBYtMgUAAAAM/head-hit-anime.gif",
    "https://media.tenor.com/M0Vi6oBi7RcAAAAM/ranma-akane-tendo.gif",]

@client.command(aliases = ['обнять'])
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(title="Объятия!", description="**{1}** обнял(а) **{0}**!".format(member.name, ctx.message.author.name), color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Обнял {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(HUG))
    await ctx.send(embed=embed)

@client.command(aliases = ['поцеловать'])
async def kiss(ctx, member: discord.Member):
    embed = discord.Embed(title="Поцелуи!", description="**{1}** поцеловал(а) **{0}**!".format(member.name, ctx.message.author.name), color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Поцеловал {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(KISS))
    await ctx.send(embed=embed)

@client.command(aliases = ['ударить'])
async def hit(ctx, member: discord.Member):
    embed = discord.Embed(title="Удар!", description="**{1}** ударил(а) **{0}**!".format(member.name, ctx.message.author.name), color = 0x008000)
    embed.set_author(name="")
    embed.set_footer(text=f"Ударил {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    embed.set_image(url = random.choice(HIT))
    await ctx.send(embed=embed)

@client.command()
async def ролевые(ctx):
    embed = discord.Embed(color = 0x00FF00, title = 'Cazino BOT', description = '**РОЛЕВЫЕ**')
    embed.add_field(name = 'Внимание! Перед командой ставьте звездочку!', value = '`kiss, поцелуй` - Поцеловать пользователя\n`поцеловать` <упоминание>\n\n`hug, обнять` - Обнять пользователя\n`обнять` <упоминание>\n\n`hit, ударить` - Ударить пользователя\n`ударить` <упоминание>')
    embed.set_thumbnail(url='https://images.boosty.to/user/2023562/avatar?change_time=1612918860')
    embed.set_author(name="")
    embed.set_footer(text=f"Выполнил: {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

responses = [
    'Это точно.',
    'Очень даже вряд-ли.',
    'Нет.',
    'Да, безусловно.',
    'Вы можете рассчитывать на это.',
    'Вероятно.',
    'Перспектива хорошая.',
    'Да.',
    'Знаки указывают да.',
    'Ответ туманный, попробуйте еще раз.',
    'Спроси позже.',
    'Лучше не говорить тебе сейчас.',
    'Не могу предсказать сейчас.',
    'Сконцентрируйтесь и спросите снова.',
    "Не рассчитывай на это.",
    'мой ответ - нет.',
    'Мои источники говорят нет.',
    'Перспективы не очень.',
    'Очень сомнительно.'
]


@client.command(name='шар', aliases = ['shar'])
async def шар(ctx, *, question):
    embed = discord.Embed(title='Шар', color=0x008000)
    embed.add_field(name='Шар думает...', value=random.choice(responses))
    await ctx.send(embed=embed)

ben = [
    'Yes',
    'No',
    'HoHoHo'
]
@client.command(name='бен', aliases = ['ben'])
async def бен(ctx, *, question):
    embed = discord.Embed(title='', color=0x008000)
    embed.add_field(name='Бен думает...', value=random.choice(ben))
    await ctx.send(embed=embed)

@client.event
async def on_member_join(member: discord.Member):
    channel = client.get_channel(Settings.channel_welcome_id)  # Получение канала для приветствия
    embed = discord.Embed(title=f"Добро пожаловать в {member.guild.name}!",
                          description=f"{member.mention} приглашаю тебя на огонёк в голосовые каналы! Мы всегда рады новым участникам",
                          color=0xff0000)  # Embed
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)  # Отправка сообщения
 
    channel = client.get_channel(Settings.channel_members_id)
    embed = discord.Embed(description=f"✅ {member.mention} присоединился!", color=0x00ff00)  # Embed
    await channel.send(embed=embed)  # Отправка сообщения

#премиум
@client.command(aliases = ['ping'])
async def пинг(ctx):
    ping = client.ws.latency 
    ping_emoji = '🟩🔳🔳🔳🔳' 
    if ping > 0.10000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' 
    if ping > 0.15000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' 
    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' 
    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩'
    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧'
    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' 
    message = await ctx.send('Пожалуйста, подождите. . .')
    await message.edit(content = f'Пинг: {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:') 



token = open ('token.txt', 'r').readline()

client.run(token)