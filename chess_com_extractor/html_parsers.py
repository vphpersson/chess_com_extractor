from logging import getLogger
from html.parser import HTMLParser
from re import sub as re_sub

from chess_com_extractor.structures import ArchivedGameEntry

LOG = getLogger(__name__)


class CSRFTokenHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.csrf_token: str | None = None

    @staticmethod
    def _attr_to_dict(attrs_list: list[tuple[str, str]]) -> dict[str, str]:
        return {key: value for key, value in attrs_list}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        attrs_dict: dict[str, str] = self._attr_to_dict(attrs_list=attrs)

        if attrs_dict.get('id') == '_token':
            self.csrf_token = attrs_dict['value']

    def error(self, message: str):
        LOG.error(message)

    @classmethod
    def parse(cls, html_content: str) -> str:
        parser = cls()
        parser.feed(data=html_content)

        return parser.csrf_token


class ArchivedGameEntriesHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.archived_game_entries: list[ArchivedGameEntry] = []
        self.num_total_pages: int | None = None
        self.player_name: str | None = None
        self._handle_title_data = False

    @staticmethod
    def _attr_to_dict(attrs_list: list[tuple[str, str]]) -> dict[str, str]:
        return {key: value for key, value in attrs_list}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        attrs_dict: dict[str, str] = self._attr_to_dict(attrs_list=attrs)

        if tag == 'title':
            self._handle_title_data = True
        elif (game_id := attrs_dict.get('data-game-id')) is not None:
            self.archived_game_entries.append(
                ArchivedGameEntry(
                    game_id=game_id,
                    game_type=attrs_dict['data-game-type']
                )
            )
        elif (num_total_pages := attrs_dict.get('data-total-pages')) is not None:
            self.num_total_pages = int(num_total_pages)

    def handle_data(self, data: str):
        if self._handle_title_data:
            self.player_name = re_sub(pattern=r'^.+ (.+) - Chess\.com$', repl=r'\1', string=data)
            self._handle_title_data = False

    def error(self, message: str):
        LOG.error(message)
