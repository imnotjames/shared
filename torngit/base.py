from tornwrap import logger
    _log_handler = None
    _aws_key = None
    _token = None
    timeouts = tuple(map(int, os.getenv('ASYNC_TIMEOUTS', '5,15').split(',')))
    # Important. Leave this commented out to properly override
    # def get_oauth_token(self, service):
    #     return dict(key=os.getenv(service.upper() + '_ACCESS_TOKEN'),
    #                 secret=os.getenv(service.upper() + '_ACCESS_TOKEN_SECRET'),
    #                 username='_guest_')

    @classmethod
    def new(cls, ioloop=None, log_handler=None, **kwargs):
        self = cls()
        self._ioloop = ioloop
        self._token = kwargs.pop('token', None)
        self.data = {
            "owner": {},
            "repo": {}
        }
        self._log_handler = log_handler
        self.data.update(kwargs)
        return self

    def log(self, **kwargs):
        if self._log_handler:
            self._log_handler(kwargs)

        default = getattr(self, 'get_log_payload', dict)()
        if hasattr(self, 'request_id'):
            default['id'] = self.request_id
        default.update(kwargs)
        logger.log(**default)
    def _validate_language(self, language):
        if language:
            language = language.lower()
            if language in ('javascript', 'shell', 'python', 'ruby', 'perl', 'dart', 'java', 'c', 'clojure', 'd', 'fortran', 'go', 'groovy', 'kotlin', 'php', 'r', 'scala', 'swift', 'objective-c', 'xtend'):
                return language

    def renamed_repository(self, repo):
        pass

    def get_href(self, endpoint='repo', **data):
        d = self.data['owner'].copy()
        d.update(self.data['repo'])
        d.update(self.data.get('commit', {}))
    def set_token(self, token):
        self._token = token
        if not self._token:
    def _oauth_consumer_token(self):
        service = self.service.upper()
        return dict(key=os.getenv('%s_CLIENT_ID' % service, ''),
                    secret=os.getenv('%s_CLIENT_SECRET' % service, ''))
        return (self['owner']['username'] + "/" + self['repo']['name']) if self['repo'].get('name') else None
                for source in ('diff --git a/' + _diff).splitlines():
        return dict(files=results)