from discord.ext import commands

variable_dict = {}


class Math(commands.Cog):
    @commands.hybrid_group(name='math')
    async def math(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f'No subcommand used')


    @math.command(name='let')
    async def let(self, ctx, variable, value):
        variable_dict[variable] = value
        await ctx.send('Ok, adding value to database')


    @math.command(name='clear')
    async def clear(self, ctx):
        variable_dict.clear()
        await ctx.send('Cleared variable dict')


    @math.command(name='calculate')
    async def _calculate(self, ctx, user_message):
        expression = ''

        for i in user_message:
            if i.isalpha():
                expression += str(variable_dict[i])
                continue
            expression += i

        try:
            result = eval(expression)
            await ctx.send(result)

        except NameError:
            await ctx.send('undefined variable detected, opinion rejected')

        except SyntaxError:
            await ctx.send('Invalid syntax used bozo')

    @math.error
    async def math_error(self, ctx, error):
        if isinstance(error, commands.ExtensionFailed):
            await ctx.send('WARNING: EXTENSION FAILURE DETECTED! CHECK MATH MODULE. '
                           f'RAISED ERROR: {error}')


async def setup(bot):
    await bot.add_cog(Math(bot))
