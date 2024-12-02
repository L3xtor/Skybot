import discord
from discord.ext import commands

class pfView(discord.ui.View):
    chosenclass = None

    @discord.ui.select(
        placeholder="Which class are you going to play?",
        options=[
            discord.SelectOption(label="🏹 Archer", value="archer"),
            discord.SelectOption(label="⚔️ Berserk", value="berserk"),
            discord.SelectOption(label="🧙‍♂️ Mage", value="mage"),
            discord.SelectOption(label="🛡️ Tank", value="tank"),
            discord.SelectOption(label="⛑️ Healer", value="healer"),
        ]
    )
    async def select_class(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.chosenclass = select.values[0]  # Get the selected class

        role_names = ["Archer", "Berserk", "Mage", "Tank", "Healer"]
        class_roles = {}

        for role_name in role_names:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role:
                class_roles[role_name.lower()] = f"<@&{role.id}>"
            else:
                class_roles[role_name.lower()] = None  # Handle roles that don't exist

        # Ensure roles exist
        for role_name in role_names:
            if not discord.utils.get(interaction.guild.roles, name=role_name):
                await interaction.guild.create_role(name=role_name)

        # List of all classes
        all_classes = list(class_roles.keys())
    
        # Remove the chosen class from the list
        remaining_classes = [cls for cls in all_classes if cls != self.chosenclass]

        # Create the searching message
        searching_message = f"{interaction.user.mention} (selected {self.chosenclass}) is looking for: "
        searching_message += ', '.join(class_roles[cls] for cls in remaining_classes if class_roles[cls] is not None)

        # Get the next available channel number
        existing_channels = interaction.guild.channels
        lfp_number = 1  # Start with 1
    
        while any(channel.name == f"lfp-{lfp_number}" for channel in existing_channels):
            lfp_number += 1  # Increment the number until an available name is found

        # Create the new channel
        new_channel = await interaction.guild.create_text_channel(f"lfp-{lfp_number}")

        # Create the button for selecting missing classes
        button = discord.ui.Button(label="Select Missing Class", style=discord.ButtonStyle.primary)

        async def button_callback(button_interaction: discord.Interaction):
            if button_interaction.user == interaction.user:
                await button_interaction.response.send_message("This is your own party!", ephemeral=True)
                return
            
            # Send a new dropdown for selecting the missing class
            missing_class_view = MissingClassView(remaining_classes)
            await button_interaction.response.send_message("Please select your class:", view=missing_class_view, ephemeral=True)

        button.callback = button_callback

        # Send the message in the new channel with the button
        await new_channel.send(searching_message, view=discord.ui.View().add_item(button))
        await interaction.response.send_message(f"A new channel has been created: <#{new_channel.id}>", ephemeral=True)


class MissingClassView(discord.ui.View):
    def __init__(self, remaining_classes):
        super().__init__()
        self.add_item(MissingClassDropdown(remaining_classes))


class MissingClassDropdown(discord.ui.Select):
    def __init__(self, remaining_classes):
        options = [
            discord.SelectOption(label=cls.capitalize(), value=cls)
            for cls in remaining_classes
        ]
        
        super().__init__(placeholder="Select your class", options=options)

    async def callback(self, interaction: discord.Interaction):
        chosen_class = self.values[0]
        await interaction.response.send_message(f"You selected {chosen_class}!", ephemeral=True)


class Party(commands.Cog):

    @commands.hybrid_command()
    async def pcreate(self, ctx):
        """Creates a party in the custom discord PF"""
        view = pfView()  
        await ctx.send("Please select your class:", view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Party(bot))
