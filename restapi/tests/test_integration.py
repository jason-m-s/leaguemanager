from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase, APIClient


class PlayerTestCases(APITestCase):
    fixtures = ['test-data.yaml']

    def test_unauthenticated_user_attempts(self):
        """Checks if unauthenticated request to /players fails with 401 Unauthorized"""
        self.assertEqual(HTTP_401_UNAUTHORIZED, APIClient().get('/players/').status_code)

    # Player User Tests
    def test_player_user_attempts(self):
        """Checks if player request to /players fails with 401 Unauthorized"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'player1A@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        self.assertEqual(HTTP_403_FORBIDDEN, client.get('/players/').status_code)

    # Coach User Tests
    def test_coach_user_list_players(self):
        """Checks if a coach user queries only relevant players in assigned team"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/', format='json')
        self.assertEqual(2, response.data['count'])
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual('1A', response.data['results'][0]['name'])
        self.assertEqual('2A', response.data['results'][1]['name'])

    def test_coach_user_list_players_with_percentile_filter(self):
        """Checks if coach attempt to filter players by percentile only applied filetering to related players"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/?percentile=90', format='json')
        self.assertEqual(1, response.data['count'])
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual('2A', response.data['results'][0]['name'])

    def test_coach_user_get_unrelated_player(self):
        """Checks if an attempt by coach to access an unrelated player returns 403 Forbidden"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        self.assertEqual(HTTP_403_FORBIDDEN, client.get('/players/6/').status_code)

    def test_coach_user_get_related_player(self):
        """Checks if an attempt by coach to access a related player succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/4/')
        self.assertEqual('1A', response.data['name'])

    def test_coach_user_expand_summary(self):
        """Checks if coach attempt to expand player summary yields expected results"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/4/?expand=summary')
        self.assertEqual('1A', response.data['name'])
        self.assertEqual(15, response.data['avg_score'])
        self.assertEqual(2, response.data['game_count'])

    # Admin Test Cases
    def test_admin_user_list_players(self):
        """Checks if admin user queries all players in assigned team"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/', format='json')
        self.assertEqual(4, response.data['count'])
        self.assertEqual(4, len(response.data['results']))
        self.assertEqual('1A', response.data['results'][0]['name'])
        self.assertEqual('2A', response.data['results'][1]['name'])
        self.assertEqual('1B', response.data['results'][2]['name'])
        self.assertEqual('2B', response.data['results'][3]['name'])

    def test_admin_user_list_players_with_percentile_filter(self):
        """Checks if admin attempt to filter players by percentile applies this to all players"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/?percentile=90', format='json')
        self.assertEqual(1, response.data['count'])
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual('2B', response.data['results'][0]['name'])

    def test_admin_user_get_any_player(self):
        """Checks if an attempt by admin to access a related player succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/6/')
        self.assertEqual('1B', response.data['name'])

    def test_admin_user_expand_summary(self):
        """Checks if coach attempt to expand player summary yields expected results"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/players/6/?expand=summary')
        self.assertEqual('1B', response.data['name'])
        self.assertEqual(10, response.data['avg_score'])
        self.assertEqual(2, response.data['game_count'])


class TeamTestCases(APITestCase):
    fixtures = ['test-data.yaml']

    def test_unauthenticated_user_attempts(self):
        """Checks if unauthenticated request to /teams fails with 401 Unauthorized"""
        self.assertEqual(HTTP_401_UNAUTHORIZED, APIClient().get('/teams/').status_code)

    # Player User Tests
    def test_player_user_attempts(self):
        """Checks if player request to /teams fails with 401 Unauthorized"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'player1A@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        self.assertEqual(HTTP_403_FORBIDDEN, client.get('/players/').status_code)

    # Coach User Tests
    def test_coach_user_list_teams(self):
        """Checks if a coach user queries only relevant team"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/', format='json')
        self.assertEqual(1, response.data['count'])
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual('Team A', response.data['results'][0]['name'])

    def test_coach_user_get_unrelated_team(self):
        """Checks if an attempt by coach to access an unrelated team returns 403 Forbidden"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        self.assertEqual(HTTP_403_FORBIDDEN, client.get('/teams/2/').status_code)

    def test_coach_user_get_related_team(self):
        """Checks if an attempt by coach to access a related player succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/1/')
        self.assertEqual('Team A', response.data['name'])

    def test_coach_user_get_related_team_with_summary(self):
        """Checks if an attempt by coach to access a related player with summary succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/1/?expand=summary')
        self.assertEqual('Team A', response.data['name'])
        self.assertEqual(35, response.data["avg_score"])

    # Admin Test Cases
    def test_admin_user_list_teams(self):
        """Checks if admin user queries all teams in assigned team"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/', format='json')
        self.assertEqual(2, response.data['count'])
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual('Team A', response.data['results'][0]['name'])
        self.assertEqual('Team B', response.data['results'][1]['name'])

    def test_admin_user_get_any_team(self):
        """Checks if an attempt by admin to access a related player succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/2/')
        self.assertEqual('Team B', response.data['name'])

    def test_admin_user_get_related_team_with_summary(self):
        """Checks if an attempt by admin to access a related player with summary succeeds"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/teams/2/?expand=summary')
        self.assertEqual('Team B', response.data['name'])
        self.assertEqual(35, response.data["avg_score"])


class GameTestCases(APITestCase):
    fixtures = ['test-data.yaml']

    def test_unauthenticated_user_attempts(self):
        """Checks if unauthenticated request to /games fails with 401 Unauthorized"""
        self.assertEqual(HTTP_401_UNAUTHORIZED, APIClient().get('/games/').status_code)

    # Player User Tests
    def test_player_user_attempts(self):
        """Checks if player has access to all games"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'player1A@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/')
        self.common_user_games_validation(response)

    # Coach User Tests
    def test_coach_user_list_games(self):
        """Checks if a coach has access to all games"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/', format='json')
        self.common_user_games_validation(response)

    # Admin Test Cases
    def test_admin_user_list_games(self):
        """Checks if admin has access to all games"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/', format='json')
        self.common_user_games_validation(response)

    def common_user_games_validation(self, response):
        self.assertEqual(2, response.data['count'])
        self.assertEqual(2, len(response.data['results']))
        self.assertEqual('Game 2', response.data['results'][0]['name'])
        self.assertEqual('Game 1', response.data['results'][1]['name'])
        self.assertEqual(2, len(response.data['results'][1]['teams']))
        self.assertEqual('Team A', response.data['results'][1]['teams'][0]['team_name'])
        self.assertEqual('Team B', response.data['results'][1]['teams'][1]['team_name'])


class GameEventTest(APITestCase):
    fixtures = ['test-data.yaml']

    def test_unauthenticated_user_attempts(self):
        """Checks if unauthenticated request to /games fails with 401 Unauthorized"""
        self.assertEqual(HTTP_401_UNAUTHORIZED, APIClient().get('/games/1/events/').status_code)

    # Player User Tests
    def test_player_user_list_game_events(self):
        """Checks if player has access to all game events1"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'player1A@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/1/events/')
        self.common_user_game_event_validation(response)

    # Coach User Tests
    def test_coach_user_list_game_events(self):
        """Checks if a coach has access to all games events"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'coach1@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/1/events/', format='json')
        self.common_user_game_event_validation(response)

    # Admin Test Cases
    def test_admin_user_list_games(self):
        """Checks if admin has access to all game events"""
        client = APIClient()
        auth_res = client.post('/token/', {'username': 'admin@domain.com', 'password': 'test123#'}, format='json')
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_res.data["token"]}')

        response = client.get('/games/1/events/', format='json')
        self.common_user_game_event_validation(response)

    def common_user_game_event_validation(self, response):
        self.assertEqual(5, response.data['count'])
        self.assertEqual(5, len(response.data['results']))
        self.assertEqual('foul', response.data['results'][0]['type'])
        self.assertEqual('score', response.data['results'][1]['type'])
        self.assertEqual('score', response.data['results'][2]['type'])
        self.assertEqual('score', response.data['results'][3]['type'])
        self.assertEqual('score', response.data['results'][4]['type'])
