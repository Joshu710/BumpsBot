import discord
from discord.ext import commands
import yt_dlp
import asyncio


URLs = []

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl':'test.%(ext)s',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    'overwrites': True,
}

DISCORD_TOKEN = ""

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='skip', help='Stops the song')
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        if voice_client != None:
            voice_client.stop()
            await playSongs(ctx,voice_client)

    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='clear', help='Stops the song')
async def clear(ctx):
    global URLs
    URLs = []
    voice_client = ctx.message.guild.voice_client
    if voice_client != None:
        if voice_client.is_playing():
            voice_client.stop()



@bot.command()
async def play(ctx, url):

    voice_client = ctx.message.guild.voice_client
    if not voice_client:
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()


    URLs.append(url)
    print(URLs)


    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing() or voice_client.is_paused():
        return

    
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        await playSongs(ctx,voice_channel)

    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


async def playSongs(ctx,voice_channel):
    if len(URLs) > 0:
        title = tester(URLs.pop(0))
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="test.m4a"), after=lambda e: asyncio.run_coroutine_threadsafe(playSongs(ctx,voice_channel),bot.loop))
        await ctx.send('**Now playing:** {}'.format(title))


def tester(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url,download=True)
        video_title = info_dict.get('title', None)
        return video_title

if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)