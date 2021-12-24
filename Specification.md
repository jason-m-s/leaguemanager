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
While supported in both `/players/` and `/teams/` APIs along with their `/{id}` counterparts, it is advised to not use it 
in the list views due possible performance reasons of averaging all entries individually (safe to use in `/{id}`)

## Authentication

* Simple token based authentication is implemented (no expiry since this is a demo application)
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

## Use Case Reconciliation

> All 3 types of users can login to the site and logout. Upon login they will view the scoreboard, 
> which will display all games and final scores, and will reflect how the competition progressed and who won.

* /token/ endpoint will be used to exchange credentials to a valid token
* /games/ endpoint will be used to view game details and scores
* /games/{id}/events endpoint will be used to view individual events of the game

> A coach may select his team in order to view a list of the players on it, and the average score of the team. 
> When one of the players in the list is selected, his personal details will be presented, 
> including - player’s name, height, average score, and the number of games he participated in.

* /teams/?expand=summary with a COACH token will only allow user to see team assigned to that user along 
with summary for that team 
* /players/?expand=summary will allow COACH user to query players related to a particular team,
along with avg_score and game_count

> A coach can filter players to see only the ones whose average score is in the 90 percentile across the team.

* /players/?percentile=90 will allow COACH to filter players of his team according to the scoring distribution 
within the team 

> The league admin may view all teams details - their average scores, their list of players, and players details. 

* A user with an ADMIN token will be able to fire all the above-mentioned requests, providing access to 
all persisted entities without being constrained to a user (unlike COACH)

> The admin can also view the statistics of the site’s usage - number of times each user logged into the system, 
> the total amount of time each user spent on the site, and who is currently online. (i.e. logged into the site)

* Since this is a REST server (which is not supposed to track state between requests), it is beyond its scope. 
* This should only be done in the frontend webserver