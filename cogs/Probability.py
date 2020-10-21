import discord
import random
from discord.ext import commands


class Probability(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Roll some dice!",
                      description="You can specify the type and number of dice that you want to roll. The result will "
                                  "be the sum of your various dice rolls. Your command must look like this: !!roll "
                                  "<x>d<y>, where x and y are numbers above 0 (x is optional). Numbers after decimal "
                                  "places are removed.")
    async def roll(self, ctx, dice):
        try:
            if "d" not in dice:
                await ctx.send("You used incorrect formatting for this command. Check !!help for more info.")
                return
            x = dice.split("d")
            final_exp = ""
            dice_sum = 0
            if x[0] == "":
                dice_num = 1
            else:
                dice_num = int(float(x[0]))
            dice_type = int(float(x[1]))

            # Invalid Dice Types and Numbers
            if dice_num == 0:
                await ctx.send("...nothing happened.")
                return
            if dice_num < 0:
                await ctx.send("After attempting to roll a negative amount of dice, you created a rift in the "
                               "space-time continuum and compromised the integrity of the universe itself... You "
                               "rolled a 0.")
                return
            if dice_type <= 1:
                await ctx.send(f"Sorry, a d{dice_type} is literally impossible.")
                return
            if dice_type > 100:
                await ctx.send(f"Sorry, the highest dice type I can roll is a d100")
                return
            if dice_num > 100:
                await ctx.send(f"Sorry, I can only roll a maximum of 100 dice.")
                return

            for i in range(dice_num):
                roll_result = random.randrange(1, dice_type + 1)
                dice_sum += roll_result
                final_exp += f"D{dice_type} #{i + 1} was a {roll_result}"
                if i < dice_num - 1:
                    final_exp += "; "

            final_exp += f"\nAfter rolling {dice_num} d{dice_type}, you rolled a total of {dice_sum}!"

            await ctx.send(f"{final_exp}")
        except Exception as ex:
            await ctx.send("You used incorrect formatting for this command. Check !!help for more info.")
            raise ex

    @commands.command(aliases=["coinflip", "flipcoin", "coin"], brief="Flip a coin!",
                      description="This is a standalone command, meaning you don't need to include anything with the "
                                  "actual command call. Simply type !!flip_coin or the other aliases to use this "
                                  "command.")
    async def flip_coin(self, ctx):
        await ctx.send(f"The result is a {random.choice(['Heads', 'Tails'])}!")


def setup(client):
    client.add_cog(Probability(client))
