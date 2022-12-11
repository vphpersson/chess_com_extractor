# chess_com_extractor

Extract information from Chess.com.

## extract_archived_games.py

### Usage

```
usage: extract_archived_games.py [-h] [--user-agent USER_AGENT] [--player-name PLAYER_NAME] [--game-type GAME_TYPE] [--game-sub-types [GAME_SUB_TYPES ...]] [--num-max-pages NUM_MAX_PAGES] username password

Extract archived games of a player from Chess.com.

positional arguments:
  username              The username with which to authenticate.
  password              The password with which to authenticate.

options:
  -h, --help            show this help message and exit
  --user-agent USER_AGENT
                        A value to be used as `User-Agent` in the login request.
  --player-name PLAYER_NAME
                        The name of the player whose games to extract. Defaults to the logged-in user.
  --game-type GAME_TYPE
                        The game type to extract archived games for.
  --game-sub-types [GAME_SUB_TYPES ...]
                        The game sub-types to extract archived games for.
  --num-max-pages NUM_MAX_PAGES
                        The maximum number of pages from which to extract games from on Chess.com.
```

#### Example

```shell
$ ./extract_archived_games.py 'USERNAME' 'PASSWORD' --player-name 'virrevvv' | jq '.'
```

**Output:**

```javascript
[
  {
    "name": "Live Chess",
    "gameId": 13026220933,
    "startDate": 1619287458,
    "player1Name": "virrevvv",
    "player2Name": "kattsaros",
    "timeControl": "600",
    "tcnMoves": "mC0Kbs5QfH9ziq",
    "moveTimestamps": "5998,5970,5975,5864,5908,5789,5806,5369",
    "initialSetup": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "variant": "Standard Chess",
    "player1ResultID": 1,
    "player2ResultID": 6,
    "round": "-",
    "firstMovePly": 1,
    "variantId": 1,
    "whiteRating": 982,
    "blackRating": 779,
    "endTime": "11:04:18 PDT"
  },
  ...
]
```

You can also parse the `tcnMoves` field into `python-chess` `Move`s using the `decode_tcn` function included in this library.

:thumbsup:

## Implementation references

- [jschessengine.min.5ea1f76f.js](https://www.chess.com/bundles/app/js/vendor/jschessengine/jschessengine.min.5ea1f76f.js) - The JavaScript file that includes the original TCN decoder function, `decodeTCN`, that I ported.
