from typing import Iterable
from itertools import count

from httpx import AsyncClient

from chess_com_extractor.html_parsers import CSRFTokenHTMLParser, ArchivedGameEntriesHTMLParser
from chess_com_extractor.structures import ArchivedGameEntry, PGNInfo
from chess_com_extractor.errors import PlayerNotFoundError


async def login(
    username: str,
    password: str,
    user_agent: str,
    http_client: AsyncClient
) -> str:
    """
    Log in at Chess.com.

    The HTTP client should use "https://www.chess.com" as its base URL.

    Note that a `User-Agent` value must be provided, as Chess.com appears to block non-browser `User-Agent` values.

    :param username: A username with which to authenticate.
    :param password: A password with which to authenticate.
    :param user_agent: A value to put in the `User-Agent` header of the login request.
    :param http_client: An HTTP client with which to perform the authentication.
    :return: A CSRF token that can be used in subsequent calls to Chess.com endpoints.
    """

    login_page_response = await http_client.get(url='/login_and_go')
    login_page_response.raise_for_status()

    csrf_token: str = CSRFTokenHTMLParser.parse(html_content=login_page_response.text)

    login_response = await http_client.post(
        url='/login_check',
        headers={'User-Agent': user_agent},
        data={
            '_username': username,
            '_password': password,
            'login': '',
            '_target_path': 'https://www.chess.com',
            '_token': csrf_token
        },
        follow_redirects=True
    )
    login_response.raise_for_status()

    return csrf_token


async def get_archived_game_entries(
    http_client: AsyncClient,
    player_name: str | None = None,
    game_type: str | None = 'live',
    game_sub_types: list[str] | None = None,
    num_max_pages: int | None = None

) -> list[ArchivedGameEntry]:
    """
    Retrieve archived games.

    :param http_client: An HTTP client with which to perform the request.
    :param player_name: The name of the player whose games to retrieve. Defaults to the logged-in user.
    :param game_type: The game type to retrieve archived game entries for.
    :param game_sub_types: The game subtypes to retrieve archived entries for.
    :param num_max_pages: The maximum number of pages to extract archived game entries from.

    :return: A list of game entries for all archived games.
    """

    all_archived_game_entries: list[ArchivedGameEntry] = []

    for page_number in count(start=1, step=1):
        if page_number > num_max_pages:
            break

        # TODO: I probably should do some kind of sanitation here, but I do not know what characters are allowed.

        params = {
            'page': page_number,
            'gameType': game_type,
            'timeSort': 'desc'
        }

        if game_sub_types:
            match game_type:
                case None:
                    break
                case 'live':
                    params['gameTypeslive[]'] = game_sub_types
                case _:
                    raise NotImplementedError(game_type)

        archived_games_page_response = await http_client.get(
            url='/games/archive' + (f'/{player_name}' if player_name else ''),
            params=params
        )
        archived_games_page_response.raise_for_status()

        html_parser = ArchivedGameEntriesHTMLParser()
        html_parser.feed(data=archived_games_page_response.text)

        if player_name and html_parser.player_name != player_name:
            raise PlayerNotFoundError(player_name=player_name)

        all_archived_game_entries.extend(html_parser.archived_game_entries)

        if page_number == html_parser.num_total_pages:
            break

    return all_archived_game_entries


async def get_pgn_info(
    archived_game_entries: Iterable[ArchivedGameEntry],
    http_client: AsyncClient,
    csrf_token: str,
    as_dict: bool = False
) -> list[dict[str, str | int] | PGNInfo]:
    """
    Return "PGN info" about a provided set of games.

    :param archived_game_entries: An iterable of archived game entries whose info to retrieve.
    :param http_client: An HTTP client with which to perform the request.
    :param csrf_token: A CSRF token to be used in the request.
    :param as_dict: Whether to return the result as a `dict` rather than a `dataclass`.
    :return: A list of "PGN info" elements of the provided set of games.
    """

    game_ids: list[str] = []
    game_types: list[str] = []

    for archived_game_entry in archived_game_entries:
        game_ids.append(archived_game_entry.game_id)
        game_types.append(archived_game_entry.game_type)

    pgn_info_response = await http_client.post(
        url='/callback/game/pgn-info',
        json={
            'ids': ','.join(game_ids),
            'types': ','.join(game_types),
            '_token': csrf_token
        }
    )
    pgn_info_response.raise_for_status()

    json_data_list: list[dict[str, str | int]] = pgn_info_response.json()

    return json_data_list if as_dict else [PGNInfo.from_json(json_object=json_data) for json_data in json_data_list]
