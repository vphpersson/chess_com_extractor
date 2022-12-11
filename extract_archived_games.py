#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type
from json import dumps as json_dumps
from sys import stderr

from httpx import AsyncClient
from scrape_latest_user_agent import scrape_latest_user_agent, Browser, OperatingSystem

from chess_com_extractor import get_pgn_info, get_archived_game_entries, login
from chess_com_extractor.cli import ExtractArchivedGamesArgumentParser
from chess_com_extractor.structures import PGNInfo
from chess_com_extractor.errors import PlayerNotFoundError


async def extract_archived_games(
    username: str,
    password: str,
    user_agent: str,
    http_client: AsyncClient,
    player_name: str | None = None,
    game_type: str | None = None,
    game_sub_types: list[str] | None = None,
    num_max_pages: int | None = None,
    as_dict: bool = True
) -> list[dict[str, str | int] | PGNInfo]:
    """
    Extract archived games of a player from Chess.com.

    :param username: A username with which to authenticate.
    :param password:  A password with which to authenticate.
    :param user_agent: A `User-Agent` to be used in the login request.
    :param http_client: An HTTP client with which to retrieve data from Chess.com.
    :param player_name: A name of a player whose games info to extract.
    :param game_type:
    :param game_sub_types:
    :param num_max_pages:
    :param as_dict: Whether to return the games info as a list of `dict`s.
    :return: A list of Chess.com games info of a player.
    """

    csrf_token: str = await login(
        username=username,
        password=password,
        user_agent=user_agent,
        http_client=http_client
    )

    return await get_pgn_info(
        archived_game_entries=await get_archived_game_entries(
            http_client=http_client,
            player_name=player_name,
            game_type=game_type,
            game_sub_types=game_sub_types,
            num_max_pages=num_max_pages
        ),
        http_client=http_client,
        csrf_token=csrf_token,
        as_dict=as_dict
    )


async def main():
    args: Type[ExtractArchivedGamesArgumentParser.Namespace] = ExtractArchivedGamesArgumentParser().parse_args()

    user_agent: str
    if not args.user_agent:
        async with AsyncClient() as http_client:
            user_agent = await scrape_latest_user_agent(
                browser=Browser.CHROME,
                operating_system=OperatingSystem.WINDOWS,
                http_client=http_client
            )
    else:
        user_agent = args.user_agent

    async with AsyncClient(base_url='https://www.chess.com') as http_client:
        try:
            print(
                json_dumps(
                    await extract_archived_games(
                        username=args.username,
                        password=args.password,
                        user_agent=user_agent,
                        http_client=http_client,
                        player_name=args.player_name,
                        game_type=args.game_type,
                        game_sub_types=args.game_sub_types,
                        num_max_pages=args.num_max_pages
                    )
                )
            )
        except PlayerNotFoundError as err:
            print(err, file=stderr)

if __name__ == '__main__':
    asyncio_run(main())
