from typing import Optional

from pyutils.argparse.typed_argument_parser import TypedArgumentParser


class ExtractArchivedGamesArgumentParser(TypedArgumentParser):

    class Namespace:
        username: str
        password: str
        player_name: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(
                    description='Extract archived games of a player from Chess.com.',
                ) | kwargs
            )
        )

        self.add_argument(
            'username',
            help='The username with which to authenticate.'
        )

        self.add_argument(
            'password',
            help='The password with which to authenticate.'
        )

        self.add_argument(
            '--player-name',
            help='The name of the player whose games to extract. Defaults to the logged-in user.'
        )
