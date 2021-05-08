#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type, Optional, Union
from json import dumps as json_dumps
from sys import stderr

from httpx import AsyncClient

from chess_com_extractor import get_pgn_info, get_archived_game_entries, login
from chess_com_extractor.cli import ExtractArchivedGamesArgumentParser
from chess_com_extractor.structures import PGNInfo
from chess_com_extractor.errors import PlayerNotFoundError


async def extract_archived_games(
    username: str,
    password: str,
    http_client: AsyncClient,
    player_name: Optional[str] = None,
    as_dict: bool = True
) -> list[Union[dict[str, Union[str, int]], PGNInfo]]:
    """
    Extract archived games of a player from Chess.com.

    :param username: A username with which to authenticate.
    :param password:  A password with which to authenticate.
    :param http_client: An HTTP client with which to retrieve data from Chess.com.
    :param player_name: A name of a player whose games info to extract.
    :param as_dict: Whether to return the games info as a list of `dict`s.
    :return: A list of Chess.com games info of a player.
    """

    csrf_token: str = await login(
        username=username,
        password=password,
        http_client=http_client
    )

    return await get_pgn_info(
        archived_game_entries=await get_archived_game_entries(
            http_client=http_client,
            player_name=player_name
        ),
        http_client=http_client,
        csrf_token=csrf_token,
        as_dict=as_dict
    )


async def main():
    args: Type[ExtractArchivedGamesArgumentParser.Namespace] = ExtractArchivedGamesArgumentParser().parse_args()

    async with AsyncClient(base_url='https://www.chess.com') as http_client:
        try:
            print(
                json_dumps(
                    await extract_archived_games(
                        username=args.username,
                        password=args.password,
                        http_client=http_client,
                        player_name=args.player_name
                    )
                )
            )
        except PlayerNotFoundError as err:
            print(err, file=stderr)

if __name__ == '__main__':
    asyncio_run(main())
