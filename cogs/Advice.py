import discord
import json
import random
from discord.ext import commands


class Advice(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.advice_list = {}
        self.create_advice_list()

    def create_advice_list(self):
        # Initial Text File Reading
        with open("./lists/advice.json", "r") as f:
            self.advice_list = json.load(f)

    @commands.command(aliases=["addadvice", "adviceadd", "giveadvice", "advicegive", "give", "give_advice"],
                      brief="Add to the advice Ribbot can give!",
                      description="You must include a phrase after the command. For example: !!add_advice <Your "
                                  "advice goes here>. You do not need to include your Discord name. Ribbot will "
                                  "automatically store that for you.")
    async def add_advice(self, ctx, *, phrase):
        if len(phrase) > 200:
            await ctx.send("Sorry, I only accept advice under 200 characters long!")
            return

        # Add to dictionary
        discord_user = str(ctx.message.author)
        if discord_user in list(self.advice_list.keys()):
            # Update existing user's dictionary values
            if len(self.advice_list[discord_user]["quotes"]) >= 30:
                await ctx.send("Sorry, each user can only have 30 quotes of advice for now!")
                return
            self.advice_list[discord_user].setdefault("quotes", []).append(phrase)
            self.advice_list[discord_user]["nickname"] = ctx.message.author.display_name
        else:
            # Create new user's dictionary values
            self.advice_list.update(
                {
                    discord_user:
                        {
                            "nickname": ctx.message.author.display_name,
                            "quotes": [phrase]
                        },
                })

        # Update json file
        with open("./lists/advice.json", "w") as f:
            json.dump(self.advice_list, f, indent=2)

        await ctx.send(f"Thanks for the advice, {ctx.message.author.display_name}! It has been added to my list!")

    @commands.command(aliases=["advice", "askvice", "askadvice", "adviceask"],
                      brief="Ask Ribbot for advice!",
                      description="Ribbot will randomly generate a quote that a user had previously given to it. Each "
                                  "user who has submitted advice has an equal chance of being selected.")
    async def ask_advice(self, ctx):
        user_key = random.choice(list(self.advice_list.keys()))
        await ctx.send(f"\"{random.choice(self.advice_list[user_key]['quotes'])}\" - {self.advice_list[user_key]['nickname']}")


def setup(client):
    client.add_cog(Advice(client))
