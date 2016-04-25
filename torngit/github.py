import socket
from time import time
from sys import stdout
from tornado.escape import json_decode, json_encode, url_escape
                issues='%(username)s/%(name)s/issues/%(issueid)s',
                comment='%(username)s/%(name)s/issues/%(pullid)s#issuecomment-%(commentid)s',
                create_file='%(username)s/%(name)s/new/%(branch)s?filename=%(path)s&value=%(content)s',
                pull='%(username)s/%(name)s/pull/%(pullid)s',
    def api(self, method, url, body=None, headers=None, reraise=True, token=None, **args):
                    'User-Agent': os.getenv('USER_AGENT', 'Default')}

        if token or self.token:
            _headers['Authorization'] = 'token %s' % (token or self.token)['key']

                        bot=(token or self.token).get('username'))
        kwargs = dict(method=method,
                      body=json_encode(body) if body else None,
                      headers=_headers,
                      ca_certs=self.verify_ssl if type(self.verify_ssl) is not bool else None,
                      validate_cert=self.verify_ssl if type(self.verify_ssl) is bool else None,
                      follow_redirects=False,
                      connect_timeout=self._timeouts[0],
                      request_timeout=self._timeouts[1])

        if method != 'GET' and self.torngit_disable_write:
            _headers['Authorization'] = (token or self.token or {}).get('username')
            getattr(self, 'torngit_disable_write_callback', lambda u, k: None)(url, kwargs)
            raise gen.Return(None)

        start = time()
            res = yield self.fetch(url, **kwargs)
            if e.response is None:
                stdout.write('count#%s.timeout=1\n' % self.service)
                raise ClientError(502, 'GitHub was not able to be reached, server timed out.')
            else:
                if e.response.code == 301:
                    # repo moved
                    repo = yield self.get_repository()
                    self.data['owner']['username'] = repo['owner']['username']
                    self.data['repo']['name'] = repo['repo']['name']
                    self.renamed_repository(repo)

                self.log(status=e.response.code,
                         body=e.response.body,
                         rlx=e.response.headers.get('X-RateLimit-Remaining'),
                         rly=e.response.headers.get('X-RateLimit-Limit'),
                         rlr=e.response.headers.get('X-RateLimit-Reset'),
                         **_log)

                if '"Bad credentials"' in e.response.body:
                    e.login = True
                    e.message = 'Bad credentials'

                if reraise:
                    raise ClientError(e.response.code, 'GitHub API: %s' % e.message)

        except socket.gaierror:
            raise ClientError(502, 'GitHub was not able to be reached.')
        finally:
            stdout.write("source=%s measure#service=%dms\n" % (self.service, int((time() - start) * 1000)))

    def get_branches(self, token=None):
            res = yield self.api('get', '/repos/%s/branches' % self.slug,
                                 per_page=100, page=page, token=token)
            self.set_token(dict(key=session['access_token']))
    def get_is_admin(self, user, token=None):
        res = yield self.api('get', '/orgs/%s/memberships/%s' % (self.data['owner']['username'], user['username']), token=token)
    def get_authenticated(self, token=None):
        r = yield self.api('get', '/repos/%s' % self.slug, token=token)
    def get_repository(self, token=None):
        if self.data['repo'].get('service_id') is None:
            res = yield self.api('get', '/repos/%s' % self.slug, token=token)
            res = yield self.api('get', '/repositories/%s' % self.data['repo']['service_id'], token=token)
        parent = res.get('parent')

        if parent:
            fork = dict(owner=dict(service_id=parent['owner']['id'],
                                   username=parent['owner']['login']),
                        repo=dict(service_id=parent['id'],
                                  name=parent['name'],
                                  language=self._validate_language(parent['language']),
                                  private=parent['private'],
                                  branch=parent['default_branch']))
        else:
            fork = None

                                        language=self._validate_language(res['language']),
                                        fork=fork,
    def list_repos(self, token=None):
                                   headers=headers, token=token)
                _o, _r, parent = repo['owner']['login'], repo['name'], None
                        parent = yield self.api('get', '/repos/%s/%s' % (_o, _r),
                                                headers=headers, token=token)
                                           private=repo['private'],
    def list_teams(self, token=None):
        orgs = yield self.api('get', '/user/orgs', token=token)
            org = yield self.api('get', '/users/%s' % org['login'], token=token)
    def get_pull_request_commits(self, pullid, token=None):
        res = yield self.api('get', '/repos/%s/pulls/%s/commits' % (self.slug, pullid), token=token)
    def post_webhook(self, name, url, events, secret, token=None):
        res = yield self.api('post', '/repos/%s/hooks' % self.slug,
                                       config=dict(url=url, secret=secret, content_type='json')),
                             token=token)
    def edit_webhook(self, hookid, name, url, events, secret, token=None):
                                 config=dict(url=url, secret=secret, content_type='json')),
                       token=token)
    def post_comment(self, issueid, body, token=None):
        res = yield self.api('post', '/repos/%s/issues/%s/comments' % (self.slug, issueid),
                             body=dict(body=body), token=token)
    def edit_comment(self, issueid, commentid, body, token=None):
        yield self.api('patch', '/repos/%s/issues/comments/%s' % (self.slug, commentid),
                       body=dict(body=body), token=token)
    def delete_comment(self, issueid, commentid, token=None):
        yield self.api('delete', '/repos/%s/issues/comments/%s' % (self.slug, commentid), token=token)
    def set_commit_status(self, commit, status, context, description, url, token=None):
        yield self.api('post', '/repos/%s/statuses/%s' % (self.slug, commit),
                                 description=description),
                       token=token)
    def get_commit_statuses(self, commit, token=None):
        res = yield self.api('get', '/repos/%s/commits/%s/statuses' % (self.slug, commit), token=token)
    def get_commit_status(self, commit, token=None):
        res = yield self.api('get', '/repos/%s/commits/%s/status' % (self.slug, commit), token=token)
    def get_source(self, path, ref, token=None):
        content = yield self.api('get', '/repos/%s/contents/%s' % (self.slug, path), ref=ref, token=token)
    def get_commit_diff(self, commit, context=None, token=None):
        res = yield self.api('get', '/repos/%s/commits/%s' % (self.slug, commit),
                             headers={'Accept': 'application/vnd.github.v3.diff'},
                             token=token)
    def get_compare(self, base, head, context=None, with_commits=True, token=None):
        res = yield self.api('get', '/repos/%s/compare/%s...%s' % (self.slug, base, head), token=token)
                                     f.get('patch', '')))
                                            timestamp=c['commit']['author']['date'],
                                            author=dict(id=(c['author'] or {}).get('id'),
                                                        username=(c['author'] or {}).get('login'),
                                                        name=c['commit']['author']['name'],
                                                        email=c['commit']['author']['email'])) for c in ([res['base_commit']] + res['commits'])][::-1]))
    def get_commit(self, commitid, token=None):
        res = yield self.api('get', '/repos/%s/commits/%s' % (self.slug, commitid), token=token)
                              timestamp=res['commit']['author'].get('date')))
    def get_pull_request(self, pullid, token=None):
        res = yield self.api('get', '/repos/%s/pulls/%s' % (self.slug, pullid), token=token)
                              id=str(pullid), number=str(pullid)))
    def get_pull_requests(self, commitid=None, branch=None, state='open', token=None):
        query = '%srepo:%s+type:pr%s%s' % (
                (('%s+' % commitid) if commitid else ''),
                url_escape(self.slug),
                (('+state:%s' % state) if state else ''),
                (('+head:%s' % branch) if branch else ''))

        # https://developer.github.com/v3/search/#search-issues
        prs = yield self.api('get', '/search/issues?q=%s' % query, token=token)
        if prs['items']:
            raise gen.Return([str(pr['number']) for pr in prs['items']])
            raise gen.Return([])