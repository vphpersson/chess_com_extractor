from typed_argument_parser import TypedArgumentParser


class ExtractArchivedGamesArgumentParser(TypedArgumentParser):

    class Namespace:
        username: str
        password: str
        user_agent: str | None
        player_name: str | None
        game_type: str
        game_sub_types: list[str] | None
        num_max_pages: int | None

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
            '--user-agent',
            help='A value to be used as `User-Agent` in the login request.'
        )

        self.add_argument(
            '--player-name',
            help='The name of the player whose games to extract. Defaults to the logged-in user.'
        )

        self.add_argument(
            '--game-type',
            default='live',
            help='The game type to extract archived games for.'
        )

        self.add_argument(
            '--game-sub-types',
            nargs='*',
            help='The game sub-types to extract archived games for.'
        )

        self.add_argument(
            '--num-max-pages',
            type=int,
            help='The maximum number of pages from which to extract games from on Chess.com.'
        )
