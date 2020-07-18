import discord
from discord.ext import commands



HELP_COLOR = discord.Color.blue()


def format_help(help):

    paragraphs = help.split('\n\n')
    paragraphs = [p.replace('\n', ' ') for p in paragraphs]

    return '\n'.join(paragraphs)


class EmbedHelpCommand(commands.HelpCommand):
    async def send_error_message(self, error):
        # Display error in embed
        embed = discord.Embed(title='Help',
                              description=error,
                              color=HELP_COLOR)
        #set_footer( self.context.bot.user)
        await self.get_destination().send(embed=embed)

    async def send_bot_help(self, mapping):
        # Build embed
        embed = discord.Embed(
            title='Help',
            description=(
                f'See `{self.clean_prefix}help <command>` or '
                f'`{self.clean_prefix}help <category>` for more help.'
            ),
            color=HELP_COLOR)

        # Filter the command lists into a new mapping
        filtered_mapping = dict()
        for cog, commands in zip(mapping.keys(), mapping.values()):
            filtered = await self.filter_commands(commands, sort=True)
            filtered_mapping[cog] = filtered

        # Sort the cogs by number of commands
        # This makes the embed look neater
        zipped = zip(filtered_mapping.keys(), filtered_mapping.values())
        sorted_mapping = sorted(zipped, key=lambda pair: len(pair[1]))

        # Add commands to embed as fields
        for cog, commands in sorted_mapping:
            if len(commands) == 0:
                continue

            # Build list of commands
            command_str = str()
            for command in commands:
                command_str += f'**{command.name}**\n'

            # Add a field for each cog
            if cog is None: title = 'No Category'
            else: title = cog.qualified_name

            embed.add_field(name=title, value=command_str)

        # Send
        set_footer(embed, self.context.bot.user)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        # Get and filter this cog's command list
        commands = cog.get_commands()
        commands = await self.filter_commands(commands, sort=True)

        if len(commands) == 0:
            # No accessible commands for this context
            embed = discord.Embed(
                title=cog.qualified_name,
                description='There are no commands in this catergory '
                'that can be used in this context.',
                color=HELP_COLOR)

            set_footer(embed, self.context.bot.user)
            await self.get_destination().send(embed=embed)
            return

        # Build embed
        embed = discord.Embed(
            title='Help',
            description=(
                f'See `{self.clean_prefix}help <command>` '
                'for more help on a command.'
            ),
            color=HELP_COLOR)

        # Add commands
        for command in commands:
            help = command.short_doc or '*No help available*'
            embed.add_field(name=command.name, value=help, inline=False)

        # Send
        set_footer(embed, self.context.bot.user)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        # Build embed
        title = command.name.replace('_', ' ').title()
        embed = discord.Embed(title=title, color=HELP_COLOR)

        # Add usage
        usage = (
            f'**{self.clean_prefix}{command.qualified_name}'
            f' {command.signature}**'
        )
        embed.add_field(name='Usage', value=usage, inline=False)

        # Add alias list
        if len(command.aliases) > 0:
            alias_string = f'**{command.name}**'
            for alias in command.aliases:
                alias_string += f'\n**{alias}**'

            embed.add_field(name='Aliases', value=alias_string, inline=False)

        # Add description text
        if command.help: help = format_help(command.help)
        else: help = '*Not available.*'

        embed.add_field(name='Description', value=help, inline=False)

        # Send
        set_footer(embed, self.context.bot.user)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        # Build embed
        title = group.name.replace('_', ' ').title()
        embed = discord.Embed(title=title, color=HELP_COLOR)

        # Add usage
        usage = (
            f'**{self.clean_prefix}{group.qualified_name}'
            f' {group.signature}**'
        )
        embed.add_field(name='Usage', value=usage, inline=False)

        # Add alias list
        if len(group.aliases) > 0:
            alias_string = f'**{group.name}**'
            for alias in group.aliases:
                alias_string += f'\n**{alias}**'

            embed.add_field(name='Aliases', value=alias_string, inline=False)

        # Add subcommand list
        subs = await self.filter_commands(group.commands, sort=True)
        if len(subs) > 0:
            sub_strings = list()
            for sub in subs:
                sub_strings.append(f'**{sub.name}**')

            sub_string = '\n'.join(sub_strings)
            embed.add_field(name='Subcommands', value=sub_string, inline=False)
        else:
            embed.add_field(
                name='Subcommands',
                value='*No subcommands available in this context.*',
                inline=False)

        # Add description text
        if group.help: help = format_help(group.help)
        else: help = '*Not available.*'

        embed.add_field(name='Description', value=help, inline=False)

        # Send
        set_footer(embed, self.context.bot.user)
        await self.get_destination().send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Change to our new help command
        bot.help_command = EmbedHelpCommand()


def setup(bot):
    bot.add_cog(Help(bot))
