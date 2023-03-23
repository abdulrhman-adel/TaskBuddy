from Helpers import config
import sqlite3
import requests
from flask import request


config = config.read_config()
conn = sqlite3.connect('database/database.sqlite', check_same_thread=False)


def get_user_token(code):
    url = "https://api.clickup.com/api/v2/oauth/token"
    query = {
        "client_id": config["CLICKUP_CLIENT_ID"],
        "client_secret": config["CLICKUP_CLIENT_SECRET"],
        "code": code
    }

    response = requests.post(url, params=query)
    data: object = response.json()
    token = data['access_token']
    return token


def store_user_token(user_id, token):
    cur = conn.cursor()
    cur.execute("""INSERT INTO users (discord_id, clickup_token) 
               VALUES (?,?);""", (user_id, token))
    conn.commit()
    return


def get_token_by_id(user_id):
    cur = conn.cursor()
    cur.execute("""SELECT clickup_token FROM users WHERE discord_id = ?;""", (user_id,))
    data = cur.fetchone()
    return data[0]


def callback():
    user_id = request.args.get('state')
    code = request.args.get('code')
    token = get_user_token(code)
    store_user_token(user_id, token)

    return "Your code is %s" % code + "& your state is %s" % user_id + "token %s" % token


class Client:
    def __init__(self, access_token):
        self.client_id = config["CLICKUP_CLIENT_ID"]
        self.client_secret = config["CLICKUP_CLIENT_SECRET"]
        self.redirect_url = config["CLICKUP_REDIRECT_URI"]
        self.access_token = access_token
        self.base_url = 'https://api.clickup.com/api'
        # self.oauth2_url = f'https://app.clickup.com/api?client_id={self.client_id}&redirect_uri={self.redirect_url}'
        # self.oauth2_code = None

    def set_oauth2_code(self, code):
        self.oauth2_code = code

    def set_access_token(self, access_token):
        self.access_token = access_token

    def ensure_access_token(self):
        if self.access_token is None:
            self.access_token = self._request(
                'post',
                f'/v2/oauth/token'
                f'?client_id={self.client_id}&client_secret={self.client_secret}&code={self.oauth2_code}',
                authorization=False
            ).get('access_token')
            print(f'Access token retrieved successfully: {self.access_token}')
        return self.access_token

    def _request(self, method, resource, params=None, authorization=True):
        headers = dict()
        if authorization is True:
            headers['Authorization'] = self.ensure_access_token()

        response = requests.request(method, f'{self.base_url}{resource}', headers=headers, json=params)
        if response.status_code == 200:
            result = response.json()
            return result

        else:
            raise Exception(f'Api call failed: {response.status_code}: {response.text}')

    def get_activities(self):
        pass

    def get_teams(self):
        return self._request('get', '/v2/team').get('teams')

    def get_shared_hierarchy(self, team_id):
        return self._request('get', f'/v2/team/{team_id}/shared')

    def get_spaces(self, team_id):
        return self._request('get', f'/v2/team/{team_id}/space?archived=false').get('spaces')

    def get_folders(self, space_id):
        return self._request('get', f'/v2/space/{space_id}/folder?archived=false').get('folders')

    def get_lists(self, space_id=None, folder_id=None):
        if folder_id is not None:
            return self._request('get', f'/v2/folder/{folder_id}/list?archived=false').get('lists')
        else:
            return self._request('get', f'/v2/space/{space_id}/list?archived=false').get('lists')

    def get_views(self, space_id=None, folder_id=None, list_id=None):
        if list_id is not None:
            return self._request('get', f'/v2/list/{list_id}/view').get('views')
        elif folder_id is not None:
            return self._request('get', f'/v2/folder/{folder_id}/view').get('views')
        else:
            return self._request('get', f'/v2/space/{space_id}/view').get('views')

    def get_view_tasks(self, view_id):
        return self._request('get', f'/v2/view/{view_id}/task')
