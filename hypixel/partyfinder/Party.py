import discord
from discord.ext import commands


class pfView(discord.ui.View):
    def __init__(self, party_creator_id):
        super().__init__()
        self.party_creator_id = party_creator_id  # Store the creator's ID
        self.chosenclass = None
        self.selected_classes = {}  # Keep track of which users have selected which class

    @discord.ui.select(
        placeholder="Which class are you going to play?",
        options=[
            discord.SelectOption(label="🏹 Archer", value="🏹 Archer"),
            discord.SelectOption(label="⚔️ Berserk", value="⚔️ Berserk"),
            discord.SelectOption(label="🧙‍♂️ Mage", value="🧙‍♂️ Mage"),
            discord.SelectOption(label="🛡️ Tank", value="🛡️ Tank"),
            discord.SelectOption(label="⛑️ Healer", value="⛑️ Healer"),
        ],
    )
    async def select_class(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        # Check if the user is the party creator
        if interaction.user.id == self.party_creator_id:
            # If it's the party creator, they can select their class without restrictions
            self.chosenclass = select.values[0]
            self.selected_classes[interaction.user.id] = (
                self.chosenclass.lower()
            )  # Store the creator's class
            await interaction.response.send_message(
                f"You've selected {self.chosenclass} as your class!", ephemeral=True
            )
            return

        # If the user is not the party creator and has already selected a class
        if interaction.user.id in self.selected_classes:
            await interaction.response.send_message(
                "Already applied to this party.", ephemeral=True
            )
            return

        # For non-creator players, allow them to select a class
        self.chosenclass = select.values[0]
        self.selected_classes[interaction.user.id] = (
            self.chosenclass.lower()
        )  # Store their selected class

        role_names = ["🏹 Archer", "⚔️ Berserk", "🧙‍♂️ Mage", "🛡️ Tank", "⛑️ Healer"]
        class_roles = {
            role.lower(): f"<@&{discord.utils.get(interaction.guild.roles, name=role).id}>"
            for role in role_names
            if discord.utils.get(interaction.guild.roles, name=role)
        }

        # Update remaining classes to exclude already selected ones
        remaining_classes = [
            cls for cls in class_roles if cls not in self.selected_classes.values()
        ]

        # Construct the searching message
        searching_message = (
            f"{interaction.user.mention} (playing {self.chosenclass}) is looking for: "
        )
        searching_message += ", ".join(
            class_roles[cls]
            for cls in remaining_classes
            if class_roles[cls] is not None
        )

        # Get the next available channel number
        existing_channels = interaction.guild.channels
        lfp_number = 1  # Start with 1

        while any(channel.name == f"lfp-{lfp_number}" for channel in existing_channels):
            lfp_number += 1  # Increment the number until an available name is found

        # Create the new channel
        new_channel = await interaction.guild.create_text_channel(f"lfp-{lfp_number}")

        # Create the button for selecting missing classes
        button = discord.ui.Button(
            label="Select Missing Class", style=discord.ButtonStyle.primary
        )

        async def button_callback(button_interaction: discord.Interaction):
            if button_interaction.user == interaction.user:
                await button_interaction.response.send_message(
                    "This is your own party!", ephemeral=True
                )
                return

            # Send a new dropdown for selecting the missing class
            missing_class_view = MissingClassView(
                remaining_classes, self.selected_classes, self.party_creator_id
            )
            await button_interaction.response.send_message(
                "Please select your class:", view=missing_class_view, ephemeral=True
            )

        button.callback = button_callback

        # Send the message in the new channel with the button
        await new_channel.send(
            searching_message, view=discord.ui.View().add_item(button)
        )
        await interaction.response.send_message(
            f"A new channel has been created: <#{new_channel.id}>", ephemeral=True
        )


class MissingClassView(discord.ui.View):
    def __init__(self, remaining_classes, selected_classes, party_creator_id):
        super().__init__()
        self.add_item(
            MissingClassDropdown(remaining_classes, selected_classes, party_creator_id)
        )


class MissingClassDropdown(discord.ui.Select):
    def __init__(self, remaining_classes, selected_classes, party_creator_id):
        options = [
            discord.SelectOption(label=cls.capitalize(), value=cls)
            for cls in remaining_classes
        ]

        super().__init__(placeholder="Select your class", options=options)
        self.selected_classes = selected_classes  # Store selected_classes
        self.party_creator_id = party_creator_id  # Store the party creator's ID

    async def callback(self, interaction: discord.Interaction):
        # If the user has already selected a class, prevent them from changing it
        if interaction.user.id in self.selected_classes:
            await interaction.response.send_message(
                "Already applied to this party.", ephemeral=True
            )
            return

        chosen_class = self.values[0]

        # Create the embed message
        embed = discord.Embed(
            title="New Join Request",
            description=f"{interaction.user.mention} wants to join the party as {chosen_class.capitalize()}!",
            color=discord.Color.blue(),
        )

        # Send the embed to the party chat (the newly created channel)
        # Get the party chat (lfp-<number>) channel
        party_channel = discord.utils.get(
            interaction.guild.text_channels,
            name=f"lfp-{interaction.channel.name.split('-')[1]}",
        )

        if party_channel:
            await party_channel.send(embed=embed)

        # Notify the user who selected the class
        await interaction.response.send_message(
            f"You selected {chosen_class}! Sent a party join request to the party chat.",
            ephemeral=True,
        )


class Party(commands.Cog):
    @commands.hybrid_command()
    async def pcreate(self, ctx):
        """Creates a party in the custom discord PF"""
        view = pfView(ctx.author.id)  # Pass the party creator's ID
        await ctx.send("Please select your class:", view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Party(bot))
