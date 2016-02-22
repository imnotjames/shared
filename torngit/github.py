from base64 import b64decode
    urls = dict(repo='%(username)s/%(name)s',
                commit='%(username)s/%(name)s/commit/%(commitid)s',
                commits='%(username)s/%(name)s/commits',
                compare='%(username)s/%(name)s/compare/%(base)s...%(head)s',
                pull='%(username)s/%(name)s/pull/%(pr)s',
                branch='%(username)s/%(name)s/tree/%(branch)s',
                tree='%(username)s/%(name)s/tree/%(commitid)s',
                src='%(username)s/%(name)s/blob/%(commitid)s/%(path)s',
                author='%(username)s/%(name)s/commits?author=%(author)s',)
    def api(self, method, url, body=None, headers=None, reraise=True, **args):
        _log = {}
                        consumer=self.token.get('username'))
                                   follow_redirects=False,
                                   connect_timeout=self.timeouts[0],
                                   request_timeout=self.timeouts[1])
            if e.response.code == 301:
                # repo moved
                repo = yield self.get_repository()
                self.data['owner']['username'] = repo['owner']['username']
                self.data['repo']['name'] = repo['repo']['name']
                self.renamed_repository(repo)


            if '"Bad credentials"' in e.response.body:
                e.message = 'login'

            if reraise:
                raise
    @gen.coroutine
    def get_is_admin(self, user):
        # https://developer.github.com/v3/orgs/members/#get-organization-membership
        res = yield self.api('get', '/orgs/'+self['owner']['username']+'/memberships/'+user['username'])
        raise gen.Return(res['state'] == 'active' and res['role'] == 'admin')

        if self['repo'].get('service_id') is None:
            res = yield self.api('get', '/repositories/' + str(self['repo']['service_id']))

        raise gen.Return(dict(owner=dict(service_id=res['owner']['id'], username=username),
                              repo=dict(service_id=res['id'],
                                        name=repo,
                                        private=res['private'],
                                        branch=res['default_branch'] or 'master')))
    def list_repos(self):
        """
        GitHub includes all visible repos through
        the same endpoint.
        """
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

                data.append(dict(owner=dict(service_id=repo['owner']['id'],
                                            username=_o),
                                 repo=dict(service_id=repo['id'],
                                           name=_r,
                                           language=self._validate_language(repo['language']),
                                           private=_p,
                                           branch=repo['default_branch'],
                                           fork=fork)))
    def get_pull_request_commits(self, pullid):
        # https://developer.github.com/v3/pulls/#list-commits-on-a-pull-request
        # NOTE limited to 250 commits
        res = yield self.api('get', '/repos/' + self.slug + '/pulls/' + str(pullid) + '/commits')
        raise gen.Return([c['sha'] for c in res])
    def post_webhook(self, name, url, events, secret):
    @gen.coroutine
    def edit_webhook(self, hookid, name, url, events, secret):
        # https://developer.github.com/v3/repos/hooks/#edit-a-hook
        yield self.api('patch', '/repos/%s/hooks/%s' % (self.slug, hookid),
                       body=dict(name='web', active=True, events=events,
                                 config=dict(url=url, secret=secret, content_type='json')))
        raise gen.Return(True)

    @gen.coroutine
    def delete_comment(self, issueid, commentid):
        # https://developer.github.com/v3/issues/comments/#delete-a-comment
        yield self.api('delete', '/repos/'+self.slug+'/issues/comments/'+str(commentid))
        raise gen.Return(True)

    def set_commit_status(self, commit, status, context, description, url, _merge=None):
        content = yield self.api('get', '/repos/'+self.slug+'/contents/'+path, ref=ref)
        raise gen.Return(dict(content=b64decode(content['content']), commitid=content['sha']))
    def get_commit_diff(self, commit, context=None):
        # https://developer.github.com/v3/repos/commits/#get-a-single-commit
        res = yield self.api('get', '/repos/'+self.slug+'/commits/'+commit,
                             headers={'Accept': 'application/vnd.github.v3.diff'})
        raise gen.Return(self.diff_to_json(res))

    @gen.coroutine
    def get_compare(self, base, head, context=None, with_commits=True):
        # https://developer.github.com/v3/repos/commits/#compare-two-commits
        res = yield self.api('get', '/repos/'+self.slug+'/compare/'+base+'...'+head)
        files = {}
        for f in res['files']:
            diff = self.diff_to_json('diff --git a/%s b/%s%s\n%s\n%s\n%s' % (
                                     f.get('previous_filename', f.get('filename')),
                                     f.get('filename'),
                                     '\ndeleted file mode 100644' if f['status'] == 'removed' else '\nnew file mode 100644' if f['status'] == 'added' else '',
                                     '--- ' + ('/dev/null' if f['status'] == 'new' else ('a/' + f.get('previous_filename', f.get('filename')))),
                                     '+++ ' + ('/dev/null' if f['status'] == 'removed' else ('b/' + f['filename'])),
                                     f.get('patch')))
            files.update(diff['files'])

        raise gen.Return(dict(diff=dict(files=files),
                              commits=[dict(commitid=c['sha'],
                                            message=c['commit']['message'],
                                            date=c['commit']['author']['date'],
                                            author=c['commit']['author']) for c in ([res['base_commit']] + res['commits'])]))
    def get_commit(self, commitid):
        res = yield self.api('get', '/repos/'+self.slug+'/commits/'+commitid)
        raise gen.Return(dict(author=dict(id=str(res['author']['id']) if res['author'] else None,
                                          username=res['author']['login'] if res['author'] else None,
                                          email=res['commit']['author'].get('email'),
                                          name=res['commit']['author'].get('name')),
                              commitid=commitid,
                              parents=[p['sha'] for p in res['parents']],
                                        commitid=res['base']['sha']),
                                        commitid=res['head']['sha']),
                              title=res['title'],
    def get_pull_requests(self, commitid=None, branch=None, state='open', _was_merge_commit=False):
        if commitid:
            prs = yield self.api('get', '/search/issues', q='%s+repo:%s' % (commitid, self.slug))
                # [TODO] filter out branches
                merge_commit = yield self._get_merge_commit_head(commitid)
                prs.extend([str(b['number'])
                            for b in res
                            if b['state'] == state and
                               (branch is None or b['head']['ref'] == branch)])