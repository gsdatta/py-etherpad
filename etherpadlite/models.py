class Pad(object):
    """
    This model encapsulates all Pad functionality. Creation and deletion of Pad objects, however, should be
    done via an ``EtherpadClient``.
    """
    def __init__(self, pad_id, client):
        self.pad_id = pad_id
        self.client = client

    def send_request(self, pad_id=True, **kwargs):
        if pad_id:
            kwargs['padID'] = self.id

        return self.client.send_request(**kwargs)

    def _etherpad_function_call(self, function, return_key=None):
        req = self.send_request(function=function)

        if return_key is None:
            return req['data']
        else:
            return req['data'][return_key]

    @property
    def id(self):
        return self.pad_id

    @property
    def revisions_count(self):
        return self._etherpad_function_call(
            function='getRevisionsCount',
            return_key='revisions'
        )

    @property
    def saved_revisions_count(self):
        return self._etherpad_function_call(
            function='getSavedRevisionsCount',
            return_key='savedRevisions'
        )

    @property
    def saved_revisions(self):
        return self._etherpad_function_call(
            function='listSavedRevisions',
            return_key='savedRevisions'
        )

    def save_revision(self, revision=None):
        params = {
            'function': 'saveRevision',
        }

        if revision is not None:
            params['rev'] = revision

        self.send_request(**params)

    @property
    def users_count(self):
        return self._etherpad_function_call(
            function='padUsersCount',
            return_key='padUsersCount'
        )

    def copy(self, destination, force=False):
        params = {
            'function': 'copyPad',
            'sourceID': self.id,
            'destinationID': destination,
            'force': str(force).lower()
        }

        self.send_request(pad_id=False, **params)
        return Pad(pad_id=destination, client=self.client)

    def move(self, destination, force=False):
        params = {
            'function': 'movePad',
            'sourceID': self.id,
            'destinationID': destination,
            'force': str(force).lower()
        }

        self.send_request(pad_id=False, **params)
        self.pad_id = destination

    @property
    def read_only_id(self):
        return self._etherpad_function_call(
            function='getReadOnlyID',
            return_key='readOnlyID'
        )

    @property
    def public(self):
        return self._etherpad_function_call(
            function='getPublicStatus',
            return_key='publicStatus'
        )

    @public.setter
    def public(self, value):
        params = {
            'function': 'setPublicStatus',
            'publicStatus': str(value).lower()
        }

        self.send_request(**params)

    @property
    def text(self):
        return self._etherpad_function_call(
            function='getText',
            return_key='text'
        )

    @text.setter
    def text(self, value):
        params = {
            'function': 'setText',
            'text': value
        }

        self.send_request(**params)

    @property
    def html(self):
        return self._etherpad_function_call(
            function='getHTML',
            return_key='html'
        )

    @html.setter
    def html(self, value):
        params = {
            'function': 'setHTML',
            'html': value
        }

        self.send_request(**params)