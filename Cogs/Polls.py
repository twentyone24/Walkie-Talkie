import discord
from discord.ext import commands
import asyncio

class Polls(commands.Cog, name='Polls'):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:', ':regional_indicator_g:', ':regional_indicator_h:', ':regional_indicator_i:', ':regional_indicator_j:', ':regional_indicator_k:', ':regional_indicator_l:', ':regional_indicator_m:', ':regional_indicator_n:', ':regional_indicator_o:', ':regional_indicator_p:', ':regional_indicator_q:', ':regional_indicator_r:', ':regional_indicator_s:', ':regional_indicator_t:']
        self.emojisRxn = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹']

    @commands.command(pass_context=True)
    async def poll(self, ctx, *, question):
        toDel = [ctx.message]
        answers = []
        i = 0
        def check(message):
            return message.author == ctx.message.author and message.channel == ctx.message.channel and len(message.content) <= 100

        tellMeE = discord.Embed(title='Poll creator', description=f'Enter the choice {i+1} of the poll or \nmake `-p` to publish the poll or\n`-c` to cancel the poll', color=0x00ff00)
        tellMeE.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        tellMeE.set_footer(text=f'-poll command requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        timeoutE = discord.Embed(title='Poll creator', description='Your poll creation has timeouted :/\n You can create another one by using `-poll <question>` command')
        timeoutE.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        timeoutE.set_footer(text=f'-poll command requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        for i in range(0, 20):
            toDel.append(await ctx.send(embed=tellMeE))
            try:
                possibleChoice = await self.bot.wait_for('message', check=check, timeout=60.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=timeoutE)
                break

            toDel.append(possibleChoice)

            if possibleChoice.clean_content.startswith('-p'):
                publish = True
                break

            elif possibleChoice.clean_content.startswith('-c'):
                publish = False
                break

            answers.append(possibleChoice.clean_content)
            tellMeE = discord.Embed(
                        title='Poll creator',
                        description=f'`Your choice {len(answers)}`: *({answers[i]})* has been saved !\nType in the choice {i+2}\nmake `-p` to publish the poll or\n`-c` to cancel the poll',
                        color=0x00dcff
                    )
            tellMeE.set_author(
                        name=self.bot.user.name,
                        icon_url=self.bot.user.avatar_url
                    )
            tellMeE.set_footer(
                        text=f'-poll command requested by {ctx.message.author}',
                        icon_url=ctx.message.author.avatar_url
                    )

        try:
            await ctx.message.channel.delete_messages(toDel)
        except:
            pass

        if publish == True:
            pollEmbed = discord.Embed(title=f'{ctx.message.author} asks', description=f'*{question}*', color=0x00dcff)
            pollEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            pollEmbed.set_footer(text=f'-poll command requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

            for i in range(0, len(answers)):
                pollEmbed.add_field(name=f'React with {self.emojis[i]} to vote for', value=answers[i], inline=True)

            pollMsg = await ctx.send(embed=pollEmbed)

            for i in range(0, len(answers)):
                await pollMsg.add_reaction(self.emojisRxn[i])

        else:
            cancelE = discord.Embed(
                            title='Poll creator',
                            description=f'{ctx.message.author} your poll has been cancelled',
                            color=0x00dcff
                        )
            cancelE.set_author(
                            name=self.bot.user.name,
                            icon_url=self.bot.user.avatar_url
                        )
            cancelE.set_footer(
                            text=f'poll cancel requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=cancelE, delete_after=5)


def setup(bot):
    bot.add_cog(Polls(bot))
