from nextcord import *
from nextcord.abc import *
from nextcord.ext.commands import Cog
from config import db
from random import *
from datetime import *
from nextcord.utils import utcnow

no_invites = [925790260263256183, 925790260263256184, 949658438424735774, 949658438785458186, 925790260695281695, 925790260695281696, 930029339137933332, 930029354052894740,
              930029368972042261, 930029393156386836, 930029405529575434, 930029415465877545, 925790261727068247, 925790262104580096, 925790262104580097, 949740376443453460]

class automodcog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
            if 'discord.gg' in message.content:
                if message.channel.id in no_invites:
                    if not message.author.bot:
                        await message.delete()

                        adwarn_channel = message.guild.get_channel(925790260695281703)
                        warn_id = f"{randint(0,100000)}"
                        appeal_id = f"{randint(0,100000)}"
                        

                        reason=f"Incorrectly advertising in {message.channel.mention}"


                        cursor1 = db.execute("INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                                            (message.author.id, self.bot.user.id, reason, warn_id, appeal_id))

                        cursor2 = db.execute(
                            "INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point) VALUES (?,?)", (message.author.id, 1))

                        if cursor1.rowcount == 0:
                            db.execute(
                                f"UPDATE warnData SET moderator_id = {self.bot.user.id}, reason = {reason}, appeal_id = {appeal_id} warn_id = {warn_id} WHERE user_id = {message.author.id}")
                        db.commit()

                        if cursor2.rowcount == 0:
                            db.execute(
                                f"UPDATE warnData_v2 SET warn_point = warn_point + 1 WHERE user_id = {message.author.id}")
                        db.commit()

                        try:
                            warnpointdata = db.execute(
                                f"SELECT warn_point FROM warnData_v2 WHERE user_id = {message.author.id}")
                            warn_point=int(warnpointdata.fetchone()[0])
                        except:
                            warn_point='1'

                        embed = Embed(title="You have been warned", color=0xFF0000)
                        embed.add_field(
                            name="Reason of warn", value=reason, inline = True)
                        embed.add_field(name="Warn ID", value=warn_id, inline=True)
                        embed.add_field(name="Warn Points", value=warn_point, inline=True)

                        if warn_point == 3:
                            await message.author.edit(timeout=utcnow()+timedelta(hours=2), reason="2 hour mute punishment applied")
                            result="Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"
                        
                        elif warn_point == 6:
                            try:
                                kickmsg = Embed(
                                description=f"You are kicked from **{message.guild.name}**\nYou have reached the 6 warn point punishment")
                                await message.author.send(embed=kickmsg)
                            except:
                                pass
                            await message.author.kick(reason="Kick punishment applied")
                            result = "Member has reached the 6 warn point punishment. A kick punishment was applied"
                        
                        elif warn_point == 10:
                            try:
                                banmsg = Embed(
                                    description=f"You are banned from **{message.guild.name}**\nYou have reached the 10 warn point punishment")
                                banmsg.set_footer(
                                    text="To appeal for your ban, click [here](https://discord.gg/qZFhxyhTQh)to the ban appeal server")
                                await message.author.send(embed=kickmsg)
                            except:
                                pass
                            await message.author.kick(reason="Kick punishment applied")
                            result = "Member has reached the 10 warn point punishment. A ban punishment was applied"
                        
                        else:
                            result='No warn point punishment applied'

                        embed.add_field(name="Result", value=result, inline=False)
                        embed.set_footer(text="If you feel this warn was a mistake, please use `/appeal WARN_ID`")
                        embed.set_thumbnail(url=message.author.display_avatar)
                        await adwarn_channel.send(message.author.mention, embed=embed)
                else:
                    pass                       

def setup(bot):
    bot.add_cog(automodcog(bot))
