import discord
import random
import string


class StartMenu(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__()
        self.red_player = player1
        self.yellow_player = player2
        self.match_accepted = False
    
    def create_embed(self):
        embed = discord.Embed(title="Connect Four", description=f"{self.red_player} would like to play Connect Four with {self.yellow_player}")

        return embed
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = True
            await interaction.response.send_message(f"You have joined {self.red_player}'s game of Connect Four!", ephemeral=True)
            game_menu = ConnectFourGame(self.red_player, self.yellow_player)
        else:
            await interaction.response.send_message(f"You are not the requested user!", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button_callback(self, button, interaction: discord.Interaction):
        if self.__is_second_player(interaction.user):
            self.match_accepted = False
            await interaction.response.send_message(f"{self.yellow_player} has declined your Connect Four request!")
        else:
            await interaction.response.send_message(f"You are not the requested user!")
            
    def __is_second_player(self, plr: discord.User):
        return plr == self.yellow_player


class ConnectFourGame(discord.ui.View):
    def __init__(self, red_player, yellow_player):
        super().__init__()
        self.red_player = red_player
        self.yellow_player = yellow_player
        self.rows = []
        self.row_buttons = []

        for _ in range(0, 8):
            row = []
            for col in range(0, 7):
                row.append({"color": "none", "height": col})
            self.rows.append(row)
        
        for row in range(len(self.rows + 1)):
            self.row_buttons.append(discord.ui.Button(
                label=row, style=discord.ButtonStyle.gray, 
                custom_id=''.join(random.choices(string.ascii_letters + string.digits))))
        
        for button in self.row_buttons:
            button.callback = self.button_callback_event
    
    async def button_callback_event(self, interaction: discord.Interaction):
        current = self.__find_index_from_id(interaction.data["custom_id"])

        interaction.response.send_message(current, ephemeral=True)

    def __find_index_from_id(self, id):
        for i, button in enumerate(self.row_buttons):
            if button.custom_id == id:
                return i
        return 0
