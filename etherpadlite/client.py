import requests
import urllib.parse


class EtherpadException(Exception): pass


class EtherpadParamsException(EtherpadException): pass


class EtherpadInternalException(EtherpadException): pass


class EtherpadAPIKeyException(EtherpadException): pass


def clean_url(url):
    return url[:-1] if url.endswith('/') else url


def generate_url(url, function, params, api_key):
    return '%s/%s?%s' % (clean_url(url), function, urllib.parse.urlencode(dict(apikey=api_key, **params)))


class EtherpadClient(object):
    def __init__(self, base_url, api_key):
        self.api_key = api_key
        self.base_url = base_url

    def _send_request(self, function, **kwargs):
        """
        Sends a request to the Etherpad API

        :param function: The API function to call
        :param kwargs: API Function parameters
        :return: JSON data from request
        """
        req = requests.get(generate_url(url=self.base_url, function=function, params=kwargs, api_key=self.api_key))
        data = req.json()

        # TODO: Add exceptions based on message
        code = data['code']
        if code == 0:
            return req.json()
        elif code == 1:
            raise EtherpadParamsException('Incorrect parameters to API call: [%s].' % data['message'])
        elif code == 2:
            raise EtherpadInternalException('Internal error with etherpad: [%s].' % data['message'])
        elif code == 3:
            raise EtherpadException('Function does not exist: [%s].' % data['message'])
        elif code == 4:
            raise EtherpadAPIKeyException('Incorrect Etherpad API Key: [%s].' % data['message'])

    def list_pads(self, author_id=None, group_id=None):
        """
        Returns a list of pads, optionally filtered by group_id, author_id, or both.

        If no params are provided, it will attempt to get a list of all pads on the EPL instance.

        If only author_id is provided, it will find pads by that author.

        If only group_id is provided, it will find all pads in that group.

        If both author_id and group_id are provided, it will find pads in that group by that author.

        :param author_id: Author ID to filter by (optional)
        :param group_id: Group ID to filter by (optional)
        :return: List of Pad ID's
        """
        if author_id is not None and group_id is not None:
            params = {'authorID': author_id}
            req = self._send_request(function='listPadsOfAuthor', **params)

            pads_for_author = req['data']['padIDs']
            return [pad for pad in pads_for_author if group_id in pad]

        params = {}
        if author_id is None and group_id is None:
            params['function'] = 'listAllPads'
        if author_id is not None:
            params['function'] = 'listPadsOfAuthor'
            params['authorID'] = author_id
        elif group_id is not None:
            params['function'] = 'listPads'
            params['groupID'] = group_id

        req = self._send_request(**params)
        return req['data']

    # ============================================= GROUP FUNCTIONS =============================================
    def create_group(self, group_id=None):
        """
        Creates a group. If a group ID is specified, it will create a new group whose ID maps to group_id

        :param group_id: The group ID to map to (optional)
        :return: Group ID of the group created.
        """
        params = {'function': 'createGroup'}

        if group_id is not None:
            params['function'] = 'createGroupIfNotExistsFor'
            params['groupMapper'] = group_id

        req = self._send_request(**params)
        return req['data']['groupID']

    def delete_group(self, group_id):
        req = self._send_request(function='deleteGroup', groupID=group_id)

    def list_groups(self):
        req = self._send_request(function='listAllGroups')
        return req['data']['groupIDs']

    # ============================================= AUTHOR FUNCTIONS =============================================
    def create_author(self, name=None, author_id=None):
        """
        Creates a author. If a author ID is specified, it will create a new author whose ID maps to ``author_id``

        :param author_id: The author ID to map to (optional)
        :return: Author ID of the author created.
        """
        params = {'function': 'createAuthor'}

        if name is not None:
            params['name'] = name

        if author_id is not None:
            params['function'] = 'createAuthorIfNotExistsFor'
            params['authorID'] = author_id

        req = self._send_request(**params)
        return req['data']['authorID']

    def get_author_name(self, author_id):
        params = {
            'function': 'getAuthorName',
            'authorID': author_id
        }
        req = self._send_request(**params)
        return req['data']

    # ============================================= SESSION FUNCTIONS =============================================
    def create_session(self, group_id, author_id, valid_until):
        """
        Creates a session, which should be set as a cookie with key ``sessionID``. It allows the author specified to
        access the group specified up to a certain time.

        :param group_id: The group ID to give access to
        :param author_id: The author to create a session for
        :param valid_until: a UNIX timestamp up to which the session is valid
        :return: The new Session ID
        """
        params = {
            'function': 'createSession',
            'groupID': group_id,
            'authorID': author_id,
            'validUntil': valid_until
        }
        req = self._send_request(**params)
        return req['data']['sessionID']

    def delete_session(self, session_id):
        params = {
            'function': 'deleteSession',
            'sessionID': session_id
        }
        req = self._send_request(**params)

    def list_sessions(self, group_id=None, author_id=None):
        """
        Returns a list of sessions, optionally filtered by ``group_id``, ``author_id``, or both.

        * If no params are provided, it will throw a ``ValueError``.
        * If only ``author_id is provided``, it will find sessions for that author.
        * If only ``group_id`` is provided, it will find all sessions in that group.
        * If both ``author_id`` and ``group_id`` are provided, it will find sessions in that group by that author.

        :param author_id: Author ID to filter by
        :param group_id: Group ID to filter by
        :return: Dictionary of sessions, with key=sessionID and value={authorID, groupID, validUntil}
        """
        if group_id is None and author_id is None:
            raise ValueError('author_id and group_id both cannot be None')

        if group_id is not None and author_id is not None:
            author_session_params = {
                'function': 'listSessionsOfAuthor',
                'authorID': author_id
            }
            req = self._send_request(**author_session_params)
            author_sessions = req['data']
            return {key:author_sessions[key] for key in author_sessions if group_id in author_sessions[key]['groupID']}

        params = {}
        if group_id is not None:
            params['function'] = 'listSessionsOfGroup'
            params['groupID'] = group_id
        elif author_id is not None:
            params['function'] = 'listSessionsOfAuthor'
            params['authorID'] = author_id

        req = self._send_request(**params)
        return req['data']

    def get_session_details(self, session_id):
        params = {
            'function': 'getSessionInfo',
            'sessionID': session_id
        }
        req = self._send_request(**params)
        return req['data']