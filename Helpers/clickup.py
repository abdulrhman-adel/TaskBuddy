from Helpers import config
import sqlite3
import requests
from flask import request
import json

config = config.read_config()
conn = sqlite3.connect('database/database.sqlite', check_same_thread=False)


class Client:
    def __init__(self, access_token, user_id):
        self.client_id = config["CLICKUP_CLIENT_ID"]
        self.client_secret = config["CLICKUP_CLIENT_SECRET"]
        self.redirect_url = config["CLICKUP_REDIRECT_URI"]
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = 'https://api.clickup.com/api'
        self.oauth2_url = f'https://app.clickup.com/api?client_id={self.client_id}&redirect_uri={self.redirect_url}&state={self.user_id}'
        self.oauth2_code = None

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

    def get_tasks(self, list_id):
        return self._request('get', f'/v2/list/{list_id}/task')


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


def get_members(team):
    teams = json.dumps(team, indent=4, sort_keys=True)
    teams = json.loads(teams)
    for team in teams:
        members = team['members']
        return members


def get_team_id(team):
    teams = json.dumps(team, indent=4, sort_keys=True)
    teams = json.loads(teams)
    for team in teams:
        team_id = team['id']
        return team_id


def get_space_id(space):
    spaces = json.dumps(space, indent=4, sort_keys=True)
    spaces = json.loads(spaces)
    for space in spaces:
        space_id = space['id']
        return space_id


############################################################################################################


def add_channel(user_id, channel_id, folder_id):
    cur = conn.cursor()
    cur.execute("""INSERT INTO channels (discord_id, channel_id, folder_id) 
               VALUES (?,?,?);""", (user_id, channel_id, folder_id))
    conn.commit()
    return


def get_folder_by_user_id(user_id):
    cur = conn.cursor()
    cur.execute("""SELECT folder_id FROM channels WHERE discord_id = ?;""", (user_id,))
    data = cur.fetchone()
    return data[0]


def get_channel_by_user_id(user_id):
    cur = conn.cursor()
    cur.execute("""SELECT channel_id FROM channels WHERE discord_id = ?;""", (user_id,))
    data = cur.fetchone()
    return data[0]


def get_user_by_channel_id(channel_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE channel_id = ?;""", (channel_id,))
    data = cur.fetchone()
    return data[0]


def get_user_by_folder_id(folder_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE folder_id = ?;""", (folder_id,))
    data = cur.fetchone()
    return data[0]


def get_folder_id_by_channel_id(user_id, channel_id):
    cur = conn.cursor()
    cur.execute("""SELECT folder_id FROM channels WHERE discord_id = ? AND channel_id = ?;""", (user_id, channel_id))
    data = cur.fetchone()
    return data[0]

def get_user_by_space_id(space_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE space_id = ?;""", (space_id,))
    data = cur.fetchone()
    return data[0]


def get_user_by_list_id(list_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE list_id = ?;""", (list_id,))
    data = cur.fetchone()
    return data[0]


def get_user_by_task_id(task_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE task_id = ?;""", (task_id,))
    data = cur.fetchone()
    return data[0]


def get_user_by_team_id(team_id):
    cur = conn.cursor()
    cur.execute("""SELECT discord_id FROM channels WHERE team_id = ?;""", (team_id,))
    data = cur.fetchone()


###

def store_channel_id(discord_id, channel_id, space_id, folder_id, team_id):
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) FROM channels WHERE discord_id = ? AND channel_id = ?;""", (discord_id, channel_id))
    data = cur.fetchone()
    if data[0] == 0:
        cur.execute("""INSERT INTO channels (discord_id, channel_id, space_id, folder_id, team_id) 
                       VALUES (?,?,?,?,?);""", (discord_id, channel_id, space_id, folder_id, team_id))
        conn.commit()
        return
    else:
        cur.execute("""UPDATE channels SET space_id = ?, folder_id = ?, team_id = ? WHERE discord_id = ? AND channel_id = ?;""",
                    (space_id, folder_id, team_id, discord_id, channel_id))
        conn.commit()
        return


def get_folder_by_id(folders, folder_id):
    folders = json.dumps(folders, indent=4, sort_keys=True)
    folders = json.loads(folders)
    for folder in folders:
        if folder['id'] == folder_id:
            return folder
