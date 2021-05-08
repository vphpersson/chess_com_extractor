class PlayerNotFoundError(Exception):
    def __init__(self, player_name: str):
        super().__init__(f'A player named {player_name} was not found.')

        self.player_name = player_name
