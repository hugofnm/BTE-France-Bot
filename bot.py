import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    print('Bot is ready!')


@client.command()
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded extension {extension}.')
    except commands.errors.ExtensionNotFound:
        await ctx.send(f'Extension {extension} does not exist!')
    except commands.errors.ExtensionAlreadyLoaded:
        await ctx.send(f'Extension {extension} already loaded!')


@client.command()
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded extension {extension}.')
    except commands.errors.ExtensionNotLoaded:
        await ctx.send(f'Extension {extension} is not loaded!')


@client.command(aliases=['reloadall', 'reload', 'rl'])
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def reload_all(ctx):
    os.system('cls')
    await ctx.send('Reloaded all extensions.')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')


@client.command(aliases=['list', 'extlist'])
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def extension_list(ctx):
    await ctx.send('List of extensions:')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await ctx.send(f'- {filename[:-3]}')


if __name__ == '__main__':
    # Load all extensions when launching the bot.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    client.run(os.environ['DISCORD_TOKEN'])
