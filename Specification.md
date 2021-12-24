# League Manager Specification

## Architecture

* REST was chosen as the architectural model at Maturity level 3 (no hyperlinking)
* This also means this application will not be storing any session information (which will be more applicable on the frontend webserver)

## Supported Endpoints:

| Endpoint                                                   | Description                                                       |
|------------------------------------------------------------|-------------------------------------------------------------------|
| POST /token/                                               | Allows users to generate tokens using their username and password |
| GET /players/(?percentile=X)(&)(expand=summary)(team_id=Y) | Allows users to query players (protected)                         |
| GET /players/{id}/(?expand=summary)                        | Allows users to query a single player (protected)                 |
| GET /teams/                                                | Allows users to query teams (protected)                           |
| GET /teams/{id}                                            | Allows users to query a single team (protected)                   |
| GET /games/                                                | Allows users to query games (protected)                           |
| GET /games/{id}/events/                                    | Allows users to query events for a particular game (protected)    |

* protected: These endpoints require you to first authenticate with the /token/ endpoint 
and provide this token as a header `Authorization: Token asda8uqweqwnaokasd0`


* percentile: This url parameter allows you to filter players based on a percentile. 
If the token associates with an Admin, then `?percentile=90` will return all players with total score over the 90th percentile, 
If the token associates with a Coach, then this will do the filtering only within their associated team


* expand=summary: This url parameter allows you to query further player info such as `avg_score` and `game_count`.
While supported in both /players/ and /players/{id} APIs, it is advised to not use it in the former due possible performance reasons

## Authentication

* Simple token based authentication is implemented
* Clients need to simply call the `/token/` endpoint to generate a token by exchanging their credentials
* Note that the above endpoints provide **opinionated results** based on the type of user querying them
* The following permissions rules will be in effect:

|                                                            | ADMIN                                                 | COACH                                                                      | PLAYER      |
|------------------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------------------------|-------------|
| GET /players/(?percentile=X)(&)(expand=summary)(team_id=Y) | FULL_ACCESS (percentile filtering across all players) | LIMITED_ACCESS (players from assigned team only, same goes for percentile) | DENY        |
| GET /players/{id}/(?expand=summary)                        | FULL_ACCESS                                           | LIMITED_ACCESS (attempt to access players in other teams result in 403)    | DENY        |
| GET /teams/                                                | FULL_ACCESS                                           | LIMITED_ACCESS (only returns assigned team)                                | DENY        |
| GET /teams/{id}                                            | FULL_ACCESS                                           | LIMITED_ACCESS (attempt to access unrelated teams result in 403)           | DENY        |
| GET /games/                                                | FULL_ACCESS                                           | FULL_ACCESS                                                                | FULL_ACCESS |
| GET /games/{id}/events/                                    | FULL_ACCESS                                           | FULL_ACCESS                                                                | FULL_ACCESS |

