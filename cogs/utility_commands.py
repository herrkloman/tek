import discord
import json
import asyncio
import os
import random
from datetime import datetime
from discord.ext import tasks, commands

verification_users = {}


def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)


class utility_commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(253619793691803658, 345951762173394954)
    @commands.command(
        name = 'verify',
        description = "ID Verification"
    )
    async def verify(self, ctx, user: discord.Member):
        print(verification_users)
        user_roles = user.roles[1:]
        if not str(user.id) in verification_users:
            verification_users[str(user.id)] = user_roles
        for i in user.roles[1:]:
            await user.remove_roles(i)
        if ctx.guild.id == 253612214148136981:
            verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        else:
            verification = discord.utils.get(ctx.guild.roles, id = 730509216883802244)
        await user.add_roles(verification)
        embed = discord.Embed(
            title = "Success!",
            description = f"User **{user.name} [{user.id}]** has been put in verification.",
            colour = 0x7289da
        )
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.has_any_role(253619793691803658, 345951762173394954)
    @commands.command(
        name = 'verified'
    )
    async def verified(self, ctx, user: discord.Member, *reason: str):
        if ctx.guild.id == 253612214148136981:
            verification = discord.utils.get(ctx.guild.roles, id = 476377701154947082)
        else:
            verification = discord.utils.get(ctx.guild.roles, id = 730509216883802244)
        if reason:
            reason_str = ": " + " ".join(reason)
        else:
            reason_str = ""
        if str(user.id) in verification_users:
            for i in verification_users[str(user.id)]:
                await user.add_roles(i)
        await user.remove_roles(verification)
        embed = discord.Embed(
            title = "Verified User",
            description = f"User **{user.name} [{user.id}]** has been verified by **{ctx.author.name}**{reason_str}",
            colour = 0x7289da,
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f"User ID: {user.id}")
        if ctx.guild.id == 253612214148136981:
            verified_channel = discord.utils.get(ctx.guild.text_channels, id = int(655009478936363008))
        else:
            verified_channel = discord.utils.get(ctx.guild.text_channels, id = int(730512825449185472))
        await verified_channel.send(embed = embed)
        success_embed = discord.Embed(
            title = "Success!",
            description = f"User **{user.name} [{user.id}]** has been successfully verified.",
            colour = 0x7289da
        )
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = success_embed)


    
    @commands.has_any_role(585558166834774047, 585550892091310080, 345951762173394954, 289876378868908042)
    @commands.command(
        name = 'colour',
        aliases = ['color']
    )
    async def colour(self, ctx, r: int, g: int, b: int):
        rgb = [r, g, b]
        if ctx.guild.id == 253612214148136981:
            comedown = discord.utils.get(ctx.guild.roles, name = 'Comedown')
            kingpin = discord.utils.get(ctx.guild.roles, name = 'Kingpin 👾')
            range_list = list(range(kingpin.position, comedown.position))
        else:
            baked = discord.utils.get(ctx.guild.roles, name = 'Baked')
            nitro = discord.utils.get(ctx.guild.roles, name = 'Nitro Boosters')
            range_list = list(range(nitro.position, baked.position))
        if all(0 <= i <= 255 for i in rgb):
            role_colour = discord.Colour.from_rgb(r, g, b)
            if not discord.utils.get(ctx.guild.roles, name = ctx.author.name):
                new_role = await ctx.guild.create_role(name = ctx.author.name, colour = role_colour)
                await new_role.edit(position = range_list[1])
                await ctx.author.add_roles(new_role)
            else:
                new_role = await discord.utils.get(ctx.guild.roles, name = ctx.author.name).edit(colour = role_colour, position = range_list[1])
            embed = discord.Embed(
                title = "Custom colour applied!",
                description = f"Applied colour **[{r}, {g}, {b}]** to **{ctx.author.display_name}**!",
                colour = role_colour
            )
            await ctx.channel.send(embed = embed)
        else:
            await ctx.channel.send('**Error:** That is not a valid RGB colour code!')

    @commands.command(
        name = 'clearcolour',
        aliases = ['clearcolor']
    )
    async def clearcolour(self, ctx):
        colour_role = discord.utils.get(ctx.guild.roles, name = ctx.author.name)
        if colour_role:
            await colour_role.delete()
            await ctx.channel.send(f"Custom role for {ctx.author.display_name} deleted.")



    @commands.has_any_role(401512090449215489, 723896600086315079, 339896504447795210, 335169145039486976)
    @commands.command(
        name = 'triptoggle',
        aliases = ['toggletrip']
    )
    async def triptoggle(self, ctx, member: discord.Member):
        if ctx.guild.id == 335167514961248256:
            trip_role = discord.utils.get(ctx.guild.roles, id = 455415325018685451)
        else:
            trip_role = discord.utils.get(ctx.guild.roles, id = 273134198498394112)
        if trip_role in member.roles:
            await member.remove_roles(trip_role)
            await ctx.channel.send(f"The tripping role has been taken off {member.display_name}.")
        else:
            await member.add_roles(trip_role)
            await ctx.channel.send(f"{member.display_name} has been given the tripping role.")

    @commands.command(
        name = 'gtoke',
        description = "Starts a group toke",
        aliases = ['tokeup', 'sesh']
    )
    async def gtoke(self, ctx):
        emotes = ['<:Weeed:581023462534021120>', '<:weed:255964645561466880>', '<:smoke:478661373417619476>', '<:pepetoke:502604660927102977>', '<:musky:487937634157461505>', '<:joint:585773581980663811>', '<:blunt:585774074094026763>', '<:bongface:456821076387823626>']
        bot_message = await ctx.channel.send(f"{ctx.author.display_name} has started a group toke - use the reaction to join in! Toke up in: two minutes")
        emote = random.choice(emotes)
        reaction_add = await bot_message.add_reaction(emote)
        cached_message = await ctx.channel.fetch_message(bot_message.id)
        users = list()
        users.append(str(ctx.author.display_name))
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60)
                if str(reaction) == str(emote):
                    if not str(user.display_name) in users:
                        users.append(str(user.display_name))
            except asyncio.TimeoutError:
                break
        bot_message = await ctx.channel.send("Group toke commencing in one minute! Use the reaction to join in")
        emote = random.choice(emotes)
        reaction_add = await bot_message.add_reaction(emote)
        cached_message = await ctx.channel.fetch_message(bot_message.id)
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30)
                if str(reaction) == str(emote):
                    if not str(user.display_name) in users:
                        users.append(str(user.display_name))
            except asyncio.TimeoutError:
                break
        bot_message = await ctx.channel.send("Group toke commencing in 30 seconds! Use the reaction to join in")
        emote = random.choice(emotes)
        reaction_add = await bot_message.add_reaction(emote)
        cached_message = await ctx.channel.fetch_message(bot_message.id)
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=25)
                if str(reaction) == str(emote):
                    if not str(user.display_name) in users:
                        users.append(str(user.display_name))
            except asyncio.TimeoutError:
                break
        timer = 5
        msg = await ctx.channel.send("5...")
        for i in range(timer):
            timer = timer - 1
            await asyncio.sleep(1)
            if not timer == 0:
                await msg.edit(content=f'{timer}...')
            else:
                await msg.edit(content='Toke up!')
        await asyncio.sleep(3)
        finished_users = ', '.join(users)
        await ctx.channel.send(f"{finished_users} toked up! {emote}")



def setup(bot):
    bot.add_cog(utility_commands(bot))
