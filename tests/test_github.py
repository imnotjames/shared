import pytest

from torngit.exceptions import ObjectNotFoundException

from torngit.github import Github


@pytest.fixture
def valid_handler():
    return Github(
        repo=dict(name='example-python'),
        owner=dict(username='ThiagoCodecov'),
        token=dict(key='test16riktah0708pwaldsik7mi2nlgh522bfo4w')
        # oauth_consumer_token=dict(),
        # http://localhost:8080/callback?code=9dd09c3d672558d3de72
        # b'access_token=testyhmil9snn07dczp6i0ivu2ofivio2hn0mwxw&scope=admin%3Arepo_hook%2Cread%3Auser%2Crepo%2Cwrite%3Adiscussion&token_type=bearer'
    )


class TestGithubTestCase(object):

    @pytest.mark.asyncio
    async def test_post_comment(self, valid_handler, codecov_vcr):
        expected_result = {
            'url': 'https://api.github.com/repos/ThiagoCodecov/example-python/issues/comments/436811257',
            'html_url': 'https://github.com/ThiagoCodecov/example-python/pull/1#issuecomment-436811257',
            'issue_url': 'https://api.github.com/repos/ThiagoCodecov/example-python/issues/1',
            'id': 436811257,
            'node_id': 'MDEyOklzc3VlQ29tbWVudDQzNjgxMTI1Nw==',
            'user': {
                'login': 'ThiagoCodecov', 'id': 44376991, 'node_id': 'MDQ6VXNlcjQ0Mzc2OTkx',
                'avatar_url': 'https://avatars3.githubusercontent.com/u/44376991?v=4',
                'gravatar_id': '', 'url': 'https://api.github.com/users/ThiagoCodecov',
                'html_url': 'https://github.com/ThiagoCodecov',
                'followers_url': 'https://api.github.com/users/ThiagoCodecov/followers',
                'following_url': 'https://api.github.com/users/ThiagoCodecov/following{/other_user}',
                'gists_url': 'https://api.github.com/users/ThiagoCodecov/gists{/gist_id}',
                'starred_url': 'https://api.github.com/users/ThiagoCodecov/starred{/owner}{/repo}',
                'subscriptions_url': 'https://api.github.com/users/ThiagoCodecov/subscriptions',
                'organizations_url': 'https://api.github.com/users/ThiagoCodecov/orgs',
                'repos_url': 'https://api.github.com/users/ThiagoCodecov/repos',
                'events_url': 'https://api.github.com/users/ThiagoCodecov/events{/privacy}',
                'received_events_url': 'https://api.github.com/users/ThiagoCodecov/received_events',
                'type': 'User',
                'site_admin': False
            },
            'created_at': '2018-11-07T23:08:03Z',
            'updated_at': '2018-11-07T23:08:03Z',
            'author_association': 'OWNER',
            'body': 'Hello world'
        }

        res = await valid_handler.post_comment("1", "Hello world")
        print(res)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_edit_comment(self, valid_handler, codecov_vcr):
        res = await valid_handler.edit_comment("1", "436811257", "Hello world numbah 2 my friendo")
        assert res is not None
        assert res['id'] == 436811257
        assert res['body'] == 'Hello world numbah 2 my friendo'

    @pytest.mark.asyncio
    async def test_edit_comment_not_found(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.edit_comment("1", "113979999", "Hello world number 2")

    @pytest.mark.asyncio
    async def test_delete_comment(self, valid_handler, codecov_vcr):
        assert await valid_handler.delete_comment("1", "436805577") is True

    @pytest.mark.asyncio
    async def test_delete_comment_not_found(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.delete_comment("1", 113977999)

    @pytest.mark.asyncio
    async def test_find_pull_request_nothing_found(self, valid_handler, codecov_vcr):
        assert await valid_handler.find_pull_request('a' * 40, 'no-branch') is None

    @pytest.mark.asyncio
    async def test_get_pull_request_fail(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.get_pull_request("100")

    get_pull_request_test_data = [
        (
            '1',
            {
                'base': {
                    'branch': 'master',
                    'commitid': 'b92edba44fdd29fcc506317cc3ddeae1a723dd08'
                },
                'head': {
                    'branch': 'reason/some-testing',
                    'commitid': 'a06aef4356ca35b34c5486269585288489e578db'
                },
                'number': '1',
                'id': '1',
                'state': 'open',
                'title': 'Creating new code for reasons no one knows',
            }
        ),
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("a,b", get_pull_request_test_data)
    async def test_get_pull_request(self, valid_handler, a, b, codecov_vcr):
        res = await valid_handler.get_pull_request(a)
        print(res)
        assert res == b

    @pytest.mark.asyncio
    async def test_get_pull_request_commits(self, valid_handler, codecov_vcr):
        expected_result = ["a06aef4356ca35b34c5486269585288489e578db"]
        res = await valid_handler.get_pull_request_commits("1")
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_pull_requests(self, valid_handler, codecov_vcr):
        expected_result = [1]
        res = await valid_handler.get_pull_requests()
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_commit(self, valid_handler, codecov_vcr):
        expected_result = {
            'author': {
                'id': '8398772',
                'username': 'jerrode',
                'email': 'jerrod@fundersclub.com',
                'name': 'Jerrod'
            },
            'message': "Adding 'include' term if multiple sources\n\nbased on a support ticket around multiple sources\r\n\r\nhttps://codecov.freshdesk.com/a/tickets/87",
            'parents': ['adb252173d2107fad86bcdcbc149884c2dd4c609'],
            'commitid': '6895b64',
            'timestamp': '2018-07-09T23:39:20Z'
        }

        commit = await valid_handler.get_commit('6895b64')
        assert commit['author'] == expected_result['author']
        assert commit == expected_result

    @pytest.mark.asyncio
    async def test_get_commit_not_found(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.get_commit('6b7cf45238ec409064893b51f8dfa2f3ce51c888')

    @pytest.mark.asyncio
    async def test_get_commit_diff(self, valid_handler, codecov_vcr):
        expected_result = {
            'files': {
                '.travis.yml': {
                    'type': 'modified', 'before': None,
                    'segments': [
                        {
                            'header': ['1', '3', '1', '5'],
                                'lines': ['+sudo: false', '+', ' language: python', ' ', ' python:']
                        }
                    ],
                    'stats': {'added': 2, 'removed': 0}
                }
            }
        }

        res = await valid_handler.get_commit_diff('2be550c135cc13425cb2c239b9321e78dcfb787b')
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_commit_diff_not_found(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.get_commit_diff('3be850c135ccaa425cb2c239b9321e78dcfb78ff')

    @pytest.mark.asyncio
    async def test_get_commit_statuses(self, valid_handler, codecov_vcr):
        res = await valid_handler.get_commit_statuses('2be550c135cc13425cb2c239b9321e78dcfb787b')
        assert res == 'success'

    @pytest.mark.asyncio
    async def test_set_commit_status(self, valid_handler, codecov_vcr):
        target_url = 'https://localhost:50036/gitlab/codecov/ci-repo?ref=ad798926730aad14aadf72281204bdb85734fe67'
        expected_result = {
            'url': 'https://api.github.com/repos/ThiagoCodecov/example-python/statuses/a06aef4356ca35b34c5486269585288489e578db',
            'avatar_url': 'https://avatars0.githubusercontent.com/oa/930123?v=4',
            'id': 5770593059,
            'node_id': 'MDEzOlN0YXR1c0NvbnRleHQ1NzcwNTkzMDU5',
            'state': 'success',
            'description': 'aaaaaaaaaa',
            'target_url': 'https://localhost:50036/gitlab/codecov/ci-repo?ref=ad798926730aad14aadf72281204bdb85734fe67',
            'context': 'context',
            'created_at': '2018-11-07T22:57:42Z',
            'updated_at': '2018-11-07T22:57:42Z',
            'creator': {
                'login': 'ThiagoCodecov',
                'id': 44376991,
                'node_id': 'MDQ6VXNlcjQ0Mzc2OTkx',
                'avatar_url': 'https://avatars3.githubusercontent.com/u/44376991?v=4',
                'gravatar_id': '',
                'url': 'https://api.github.com/users/ThiagoCodecov',
                'html_url': 'https://github.com/ThiagoCodecov',
                'followers_url': 'https://api.github.com/users/ThiagoCodecov/followers',
                'following_url': 'https://api.github.com/users/ThiagoCodecov/following{/other_user}',
                'gists_url': 'https://api.github.com/users/ThiagoCodecov/gists{/gist_id}',
                'starred_url': 'https://api.github.com/users/ThiagoCodecov/starred{/owner}{/repo}',
                'subscriptions_url': 'https://api.github.com/users/ThiagoCodecov/subscriptions',
                'organizations_url': 'https://api.github.com/users/ThiagoCodecov/orgs',
                'repos_url': 'https://api.github.com/users/ThiagoCodecov/repos',
                'events_url': 'https://api.github.com/users/ThiagoCodecov/events{/privacy}',
                'received_events_url': 'https://api.github.com/users/ThiagoCodecov/received_events',
                'type': 'User',
                'site_admin': False
            }
        }
        res = await valid_handler.set_commit_status(
            'a06aef4356ca35b34c5486269585288489e578db',
            'success',
            'context',
            'aaaaaaaaaa',
            target_url
        )
        print(res)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_branches(self, valid_handler, codecov_vcr):
        expected_result = ['example', 'future', 'master', 'reason/some-testing']
        branches = sorted(await valid_handler.get_branches())
        assert list(map(lambda a: a[0], branches)) == expected_result

    @pytest.mark.asyncio
    async def test_post_webhook(self, valid_handler, codecov_vcr):
        url = 'http://requestbin.net/r/1ecyaj51'
        events = [
            "push",
            "pull_request",
        ]
        name, secret = 'a', 'd'
        expected_result = {
            'type': 'Repository',
            'id': 61813206,
            'name': 'web',
            'active': True,
            'events': [
                'pull_request',
                'push'
            ],
            'config': {
                'content_type': 'json',
                'secret': '********',
                'url': 'http://requestbin.net/r/1ecyaj51',
                'insecure_ssl': '0'
            },
            'updated_at': '2018-11-07T23:03:28Z',
            'created_at': '2018-11-07T23:03:28Z',
            'url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206',
            'test_url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206/test',
            'ping_url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206/pings',
            'last_response': {
                'code': None,
                'status': 'unused',
                'message': None
            }
        }
        res = await valid_handler.post_webhook(name, url, events, secret)
        print(res)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_edit_webhook(self, valid_handler, codecov_vcr):
        url = 'http://requestbin.net/r/1ecyaj51'
        events = [
            "project",
            "pull_request",
            "release"
        ]
        new_name, secret = 'new_name', 'new_secret'
        expected_result = {
            'type': 'Repository',
            'id': 61813206,
            'name': 'web',
            'active': True,
            'events': [
                'pull_request',
                'project',
                'release'
            ],
            'config': {
                'content_type': 'json',
                'secret': '********',
                'url': 'http://requestbin.net/r/1ecyaj51',
                'insecure_ssl': '0'
            },
            'updated_at': '2018-11-07T23:10:09Z',
            'created_at': '2018-11-07T23:03:28Z',
            'url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206',
            'test_url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206/test',
            'ping_url': 'https://api.github.com/repos/ThiagoCodecov/example-python/hooks/61813206/pings',
            'last_response': {'code': 200, 'message': 'OK', 'status': 'active'}
        }
        res = await valid_handler.edit_webhook(
            '61813206', new_name, url, events, secret)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_delete_webhook(self, valid_handler, codecov_vcr):
        res = await valid_handler.delete_webhook('61813206')
        assert res is True

    @pytest.mark.asyncio
    async def test_delete_webhook_not_found(self, valid_handler, codecov_vcr):
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.delete_webhook('4742f011-8397-aa77-8876-5e9a06f10f98')

    @pytest.mark.asyncio
    async def test_get_authenticated(self, valid_handler, codecov_vcr):
        res = await valid_handler.get_authenticated()
        assert res == (True, True)

    @pytest.mark.asyncio
    async def test_get_compare(self, valid_handler, codecov_vcr):
        base, head = '6ae5f17', 'b92edba'
        expected_result = {
            'diff': {
                'files': {
                    'README.rst': {
                        'type': 'modified',
                        'before': None,
                        'segments': [
                            {
                                'header': ['9', '7', '9', '8'],
                                'lines': [
                                    ' Overview',
                                    ' --------',
                                    ' ',
                                    '-Main website: `Codecov <https://codecov.io/>`_.',
                                    '+',
                                    '+website: `Codecov <https://codecov.io/>`_.',
                                    ' ',
                                    ' .. code-block:: shell-session',
                                    ' '
                                ]
                            },
                            {
                                'header': ['46', '12', '47', '19'],
                                'lines': [
                                    ' ',
                                    ' You may need to configure a ``.coveragerc`` file. Learn more `here <http://coverage.readthedocs.org/en/latest/config.html>`_. Start with this `generic .coveragerc <https://gist.github.com/codecov-io/bf15bde2c7db1a011b6e>`_ for example.',
                                    ' ',
                                    '-We highly suggest adding `source` to your ``.coveragerc`` which solves a number of issues collecting coverage.',
                                    '+We highly suggest adding ``source`` to your ``.coveragerc``, which solves a number of issues collecting coverage.',
                                    ' ',
                                    ' .. code-block:: ini',
                                    ' ',
                                    '    [run]',
                                    '    source=your_package_name',
                                    '+   ',
                                    '+If there are multiple sources, you instead should add ``include`` to your ``.coveragerc``',
                                    '+',
                                    '+.. code-block:: ini',
                                    '+',
                                    '+   [run]',
                                    '+   include=your_package_name/*',
                                    ' ',
                                    ' unittests',
                                    ' ---------'
                                ]
                            },
                            {
                                'header': ['150', '5', '158', '4'],
                                'lines': [
                                    ' * Twitter: `@codecov <https://twitter.com/codecov>`_.',
                                    ' * Email: `hello@codecov.io <hello@codecov.io>`_.',
                                    ' ',
                                    '-We are happy to help if you have any questions. Please contact email our Support at [support@codecov.io](mailto:support@codecov.io)',
                                    '-',
                                    '+We are happy to help if you have any questions. Please contact email our Support at `support@codecov.io <mailto:support@codecov.io>`_.'
                                ]
                            }
                        ],
                        'stats': {'added': 11, 'removed': 4}
                    }
                }
            },
            'commits': [
                {
                    'commitid': 'b92edba44fdd29fcc506317cc3ddeae1a723dd08',
                    'message': 'Update README.rst',
                    'timestamp': '2018-07-09T23:51:16Z',
                    'author': {
                        'id': 8398772,
                        'username': 'jerrode',
                        'name': 'Jerrod',
                        'email': 'jerrod@fundersclub.com'}
                },
                {
                    'commitid': 'c7f608036a3d2e89f8c59989ee213900c1ef39d1',
                    'message': 'Update README.rst',
                    'timestamp': '2018-07-09T23:48:34Z',
                    'author': {
                        'id': 8398772,
                        'username': 'jerrode',
                        'name': 'Jerrod',
                        'email': 'jerrod@fundersclub.com'}
                },
                {
                    'commitid': '6895b6479dbe12b5cb3baa02416c6343ddb888b4',
                    'message': "Adding 'include' term if multiple sources\n\nbased on a support ticket around multiple sources\r\n\r\nhttps://codecov.freshdesk.com/a/tickets/87",
                    'timestamp': '2018-07-09T23:39:20Z',
                    'author': {
                        'id': 8398772,
                        'username': 'jerrode',
                        'name': 'Jerrod',
                        'email': 'jerrod@fundersclub.com'}},
                {
                    'commitid': 'adb252173d2107fad86bcdcbc149884c2dd4c609',
                    'message': 'Update README.rst',
                    'timestamp': '2018-04-26T08:39:32Z',
                    'author': {
                        'id': 11602092,
                        'username': 'TomPed',
                        'name': 'Thomas Pedbereznak',
                        'email': 'tom@tomped.com'}},
                {
                    'commitid': '6ae5f1795a441884ed2847bb31154814ac01ef38',
                    'message': 'Update README.rst',
                    'timestamp': '2018-04-26T08:35:58Z',
                    'author': {
                        'id': 11602092,
                        'username': 'TomPed',
                        'name': 'Thomas Pedbereznak',
                        'email': 'tom@tomped.com'
                    }
                }
            ]
        }

        res = await valid_handler.get_compare(base, head)
        print(res)
        assert sorted(list(res.keys())) == sorted(list(expected_result.keys()))
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_compare_same_commit(self, valid_handler, codecov_vcr):
        base, head = '6ae5f17', '6ae5f17'
        expected_result = {
            'diff': {'files': {}},
            'commits': [
                {
                    'commitid': '6ae5f1795a441884ed2847bb31154814ac01ef38',
                    'author':  {
                        'email': 'tom@tomped.com', 'id': 11602092,
                        'name': 'Thomas Pedbereznak', 'username': 'TomPed'
                    },
                    'message': 'Update README.rst',
                    'timestamp': '2018-04-26T08:35:58Z'
                }
            ]
        }
        res = await valid_handler.get_compare(base, head)
        assert sorted(list(res.keys())) == sorted(list(expected_result.keys()))
        assert len(res['commits']) == len(expected_result['commits'])
        assert res['commits'][0] == expected_result['commits'][0]
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_repository(self, valid_handler, codecov_vcr):
        expected_result = {
            'owner': {
                'service_id': 44376991,
                'username': 'ThiagoCodecov'
            },
            'repo': {
                'branch': 'master',
                'language': 'python',
                'name': 'example-python',
                'private': False,
                'service_id': 156617777,
                'fork': {
                    'owner': {'service_id': 8226205, 'username': 'codecov'},
                    'repo': {
                        'branch': 'master',
                        'language': 'python',
                        'name': 'example-python',
                        'private': False,
                        'service_id': 24344106
                    }
                }
            }
        }
        res = await valid_handler.get_repository()
        assert res['owner'] == expected_result['owner']
        assert res['repo'] == expected_result['repo']
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_source_master(self, valid_handler, codecov_vcr):
        expected_result = {
            'commitid': '92aa2034f5283ff318a294116fe585e521d9f6d0',
            'content':  b'import unittest\n\nimport awesome\n\n\nclass TestMethods(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(awesome.smile(), ":)")\n\n\nif __name__ == \'__main__\':\n    unittest.main()\n'
        }
        path, ref = 'tests.py', 'master'
        res = await valid_handler.get_source(path, ref)
        print(res)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_source_random_commit(self, valid_handler, codecov_vcr):
        expected_result = {
            'commitid': '4d34acc61e7abe5536c84fec4fe9fd9b26311cc7',
            'content': b'def smile():\n    return ":)"\n\ndef frown():\n    return ":("\n'
        }
        path, ref = 'awesome/__init__.py', '96492d409fc86aa7ae31b214dfe6b08ae860458a'
        res = await valid_handler.get_source(path, ref)
        assert res == expected_result

    @pytest.mark.asyncio
    async def test_get_source_random_commit_not_found(self, valid_handler, codecov_vcr):
        path, ref = 'awesome/non_exising_file.py', '96492d409fc86aa7ae31b214dfe6b08ae860458a'
        with pytest.raises(ObjectNotFoundException):
            await valid_handler.get_source(path, ref)

    @pytest.mark.asyncio
    async def test_list_repos(self, valid_handler, codecov_vcr):
        res = await valid_handler.list_repos()
        assert len(res) == 49
        print(res[-1])
        one_expected_result = {
            'owner': {
                'service_id': 44376991, 'username': 'ThiagoCodecov'
            },
            'repo': {
                'service_id': 156617777, 'name': 'example-python', 'language': 'python',
                'private': False, 'branch': 'master',
                'fork': {
                    'owner': {
                        'service_id': 8226205, 'username': 'codecov'
                    },
                    'repo': {
                        'service_id': 24344106, 'name': 'example-python', 'language': 'python',
                        'private': False, 'branch': 'master'
                    }
                }
            }
        }

        assert one_expected_result in res

    @pytest.mark.asyncio
    async def test_list_teams(self, valid_handler, codecov_vcr):
        expected_result = [{
            'email': 'hello@codecov.io',
            'id': '8226205',
            'name': 'Codecov',
            'username': 'codecov'
        }]
        res = await valid_handler.list_teams()
        assert res == expected_result
