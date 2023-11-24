import random
import discord
from PIL import Image, ImageDraw
import string

class InteractionCheck(discord.ui.View):
    def __init__(self, message:discord.Interaction):
        self.msg = message
        super().__init__(timeout=120)
    async def interaction_check(self, inter: discord.MessageInteraction) -> bool:
        if inter.user.id != self.msg.user.id:
            await inter.response.send_message(content="You don't have permission to press this button.", ephemeral=True)
            return False
        return True
    async def on_timeout(self) -> None:
        await self.msg.delete_original_response()

async def generate_verification_code(interaction:discord.Interaction):
    randoms = (''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4)))
    with Image.new('RGBA', (50,50), (255, 0, 0, 0)) as im:
        newim = ImageDraw.Draw(im)
        c = 0
        for i, e in enumerate(tuple(randoms)):
            c += random.randrange(7, 10)
            newim.text((i+c,0+random.randrange(20, 40)), e, fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        im = im.resize((100,100))
        im.save('captcha.png', 'PNG')



    modal = discord.ui.Modal(title="Enter Letters").add_item(discord.ui.TextInput(
        label="Captcha",
        placeholder="Enter the letters here",
        required=True
    ))
    async def on_submit(interaction=interaction, modal=modal, randoms = randoms):
        if modal.children[0].value == randoms:
            # Do success conditionals here
            await interaction.response.send_message("You have now been verified!", ephemeral=True)
            await interaction.delete_original_response()
        else:
            await interaction.response.send_message("Incorrect code, please try again", ephemeral=True)
    modal.on_submit = on_submit
    async def sendModal(interaction:discord.Interaction):
        await interaction.response.send_modal(modal)

    button = InteractionCheck(interaction)
    button.add_item(discord.ui.Button(
        label="Verify",
    ))
    button.children[0].callback = sendModal

    embed = discord.Embed(
        title="Verification",
        description="Please enter the verification code below",
        color=discord.Color.blue()
    )
    img = discord.File('captcha.png')
    embed.set_image(url="attachment://captcha.png")
    ctx = await interaction.response.send_message(embed=embed, file=img,view=button,ephemeral=True) # Add button to detect when user is ready to enter Captcha

    #await interaction.response.send_modal(modal)
    return randoms
