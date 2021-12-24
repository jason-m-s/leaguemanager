from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase, APIClient


class PlayerTestCases(APITestCase):
    fixtures = ['test-data.yaml']

    def test_unauthenticated_user_attempts(self):
        """Checks if unauthenticated request to /players fails with 401 Unauthorized"""
        client = APIClient()

        self.assertEqual(HTTP_401_UNAUTHORIZED, client.get('/players/').status_code)

    def test_player_user_attempts(self):
        """Checks if unauthenticated request to /players fails with 401 Unauthorized"""
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
        """Checks if an attempt by coach to access a related player succeeds"""
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
