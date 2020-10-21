import discord
import random
import aiohttp
import json
import praw
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord.ext import commands


class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession(loop=client.loop)
        self.credentials = {}
        self.emoji_list = []
        self.subreddit_list = []
        self.caption_list = {}
        self.get_credentials()
        self.create_emoji_list()
        self.create_caption_list()
        self.create_subreddit_list()

    def get_credentials(self):
        # Initial Text File Reading
        with open("./lists/credentials.json", "r") as f:
            self.credentials = json.load(f)

    def create_emoji_list(self):
        # Initial Text File Reading
        with open("./lists/emojis.txt", "r", encoding="utf8") as f:
            self.emoji_list = f.read().splitlines()

    def create_caption_list(self):
        # Initial Text File Reading
        with open("./lists/captions.json", "r") as f:
            self.caption_list = json.load(f)

    def create_subreddit_list(self):
        # Initial Text File Reading
        with open("./lists/subreddits.txt", "r") as f:
            self.subreddit_list = f.read().splitlines()

    @commands.command(aliases=["caption", "addc", "captionadd", "addcaption"],
                      brief="Add a meme caption to Ribbot's list!", description="You must include a phrase after the "
                                                                                "command. For example: !!add_caption "
                                                                                "<Your caption goes here>. Your "
                                                                                "caption must be fewer than 40 "
                                                                                "characters (for now). Keep in mind, "
                                                                                "your captions will be tied to your "
                                                                                "Discord username!")
    async def add_caption(self, ctx, *, caption):
        if len(caption) > 40:
            await ctx.send("Sorry, I only accept captions under 40 characters long for now!")
            return

        discord_user = str(ctx.message.author)
        if discord_user in list(self.caption_list.keys()):
            # Update existing user's dictionary values
            if len(self.caption_list[discord_user]["captions"]) >= 30:
                await ctx.send("Sorry, each user can only have 30 max captions for now!")
                return
            self.caption_list[discord_user].setdefault("captions", []).append(caption)
            self.caption_list[discord_user]["nickname"] = ctx.message.author.display_name
        else:
            # Create new user's dictionary values
            self.caption_list.update(
                {
                    discord_user:
                        {
                            "nickname": ctx.message.author.display_name,
                            "captions": [caption]
                        },
                })

        # Update json file
        with open("./lists/captions.json", "w") as f:
            json.dump(self.caption_list, f, indent=2)

        await ctx.send(f"{ctx.message.author.display_name}, your caption has been added to my list!")

    @commands.command(aliases=["randomizer"],
                      brief="Randomly generate a meme!", description="Ribbot will randomly generate a meme using 1) a "
                                                                     "caption previously entered using the "
                                                                     "!!add_caption command, 2) a random submission "
                                                                     "from a random pre-determined subreddit, "
                                                                     "3) a random emoji from a a pre-determined list")
    async def meme(self, ctx):
        # Get Reddit credentials
        reddit = praw.Reddit(client_id=self.credentials["client_id"], client_secret=self.credentials["client_secret"],
                             user_agent=self.credentials["user_agent"], username=self.credentials["username"],
                             password=self.credentials["password"])
        sub_choice = random.choice(self.subreddit_list)
        # print(f"Subreddit choice: {sub_choice}")
        submission = reddit.subreddit(sub_choice).random()
        # Cycle though random reddit submission until post is a picture and non-NSFW
        while submission.over_18 or not str(submission.url).endswith((".jpg", ".png", ".gif", ".jpeg")):
            # print(f"Rerolling URL: {str(submission.url)}")
            submission = reddit.subreddit(sub_choice).random()
        url = submission.url
        # print(f"Final URL: {str(url)}")
        # print(f"Final Title: {str(submission.title)}")

        # Store image byte data into variable
        async with self.session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = BytesIO(await resp.read())

        # Convert byte data into Image object for PILLOW
        converted_image = Image.open(data).convert("RGBA")

        # Resizing the original image
        ci_width, ci_height = converted_image.size
        calculated_height = (abs(2100 - ci_width) / ci_width) * ci_height
        if ci_width > 2100:
            calculated_height = int(ci_height - calculated_height)
        else:
            calculated_height = int(ci_height + calculated_height)
        converted_image = converted_image.resize((2100, calculated_height))

        ci_width = 2100
        ci_height = calculated_height

        # Create black caption box around initial image
        # caption_box = Image.new("RGBA", (int(ci_width+10), int(ci_height + (ci_height/5))), "black")
        caption_box = Image.new("RGBA", (int(ci_width + 10), int(ci_height + 400)), "black")
        caption_box.paste(converted_image, (5, 5, (ci_width + 5), (ci_height + 5)))

        # Get caption details from dict
        caption_user = random.choice(list(self.caption_list.keys()))
        caption_nick = self.caption_list[caption_user]["nickname"]
        caption_original = random.choice(self.caption_list[caption_user]["captions"])

        # Randomly choose caption emoji
        caption_emoji = random.choice(self.emoji_list)
        caption_text = f"{caption_emoji} {caption_original} {caption_emoji}"
        caption_font = ImageFont.truetype("seguiemj.ttf", 100)
        caption_width, caption_height = caption_font.getsize(caption_text)

        draw = ImageDraw.Draw(caption_box)
        # draw.text((int((ci_width-caption_width)/2), int((ci_height+((ci_height/5)-caption_height)/2))), caption_text,
        #           font=caption_font, fill="white", embedded_color=

        # if len(caption_original) <= 30:
        draw.text((int((ci_width - caption_width) / 2), int((ci_height + (400 - caption_height) / 2))),
                  caption_text, font=caption_font, fill="white", embedded_color=True)
        # elif len(caption_original) > 30:
        #     draw.text((10, int((ci_height + (400 - caption_height) / 2))), caption_emoji,
        #               font=caption_font, fill="white", embedded_color=True)
        #     draw.text((ci_width - 130, int((ci_height + (400 - caption_height) / 2))), caption_emoji,
        #               font=caption_font, fill="white", embedded_color=True)
        #     # draw.text((int((ci_width - caption_width) / 6), int((ci_height + (400 - caption_height) / 2))),
        #     #           caption_original[0:30] + "\n" + caption_original[30:], font=caption_font, fill="white",
        #     #           align="center")
        #     draw.text((185, int((ci_height + (400 - caption_height) / 2))),
        #               caption_original[0:30] + "\n" + caption_original[30:], font=caption_font, fill="white",
        #               align="center")

        with BytesIO() as output:
            caption_box.save(output, format="PNG")
            output.seek(0)
            try:
                await ctx.send(f"Here is your randomly generated meme! (Caption provided by {caption_nick})",
                               file=discord.File(output, "cool_image.png"))
            except discord.HTTPException:
                await ctx.send("The picture that was randomly generated from the Internet was too large to send "
                               "through Discord. Try again!")


def setup(client):
    client.add_cog(Reddit(client))
