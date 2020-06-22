import hashlib
import base64
from typing import Optional
from shared.metrics import metrics
from shared.torngit.base import TorngitBaseAdapter, TokenType
METRICS_PREFIX = "services.torngit.github"

class Github(TorngitBaseAdapter, OAuth2Mixin):
        token_to_use = token or self.token
                bot=token_to_use.get("username"),
                repo_slug=self.slug,
                loggable_token=self.loggable_token(token_to_use),
            with metrics.timer(f"{METRICS_PREFIX}.api.run"):
                res = await self.fetch(url, **kwargs)
                metrics.incr(f"{METRICS_PREFIX}.api.unreachable")
                metrics.incr(f"{METRICS_PREFIX}.api.5xx")
                    body=e.response.body.decode()
                    if e.response.body is not None
                    else "NORESPONSE",
            metrics.incr(f"{METRICS_PREFIX}.api.clienterror")
            metrics.incr(f"{METRICS_PREFIX}.api.unreachable")
        token = self.get_token_by_type_if_none(token, TokenType.read)
    async def get_repository(self, token=None):
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.admin)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.admin)
        token = self.get_token_by_type_if_none(token, TokenType.admin)
        token = self.get_token_by_type_if_none(token, TokenType.admin)
        token = self.get_token_by_type_if_none(token, TokenType.comment)
        token = self.get_token_by_type_if_none(token, TokenType.comment)
        token = self.get_token_by_type_if_none(token, TokenType.comment)
        token = self.get_token_by_type_if_none(token, TokenType.status)
        token = self.get_token_by_type_if_none(token, TokenType.status)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
                "get", "/repos/%s/pulls/%s" % (self.slug, pullid), token=token,
            "get",
            "/repos/%s/pulls/%s/commits" % (self.slug, pullid),
            token=token,
            per_page=250,
        if current_level == [res["head"]["sha"]]:
            log.warning(
                "Head not found in PR. PR has probably too many commits to list all of them",
                extra=dict(number_commits=len(commits), pullid=pullid),
        else:
            possible_bases = [x for x in current_level if x not in all_commits_in_pr]
            if possible_bases and result["base"]["commitid"] not in possible_bases:
                log.info(
                    "Github base differs from original base",
                    extra=dict(
                        current_level=current_level,
                        github_base=result["base"]["commitid"],
                        possible_bases=possible_bases,
                        pullid=pullid,
                    ),
                )
                result["base"]["commitid"] = possible_bases[0]
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
        token = self.get_token_by_type_if_none(token, TokenType.read)
    # Checks
    # ------
    # Checks Docs: https://developer.github.com/v3/checks/
    #
    # The Checks API is currently marked as being in a 'Preview Period' by github
    # In order to access the API during this preview period we must provide the following header:
    # {"Accept": "application/vnd.github.antiope-preview+json"} see https://developer.github.com/changes/2018-05-07-new-checks-api-public-beta/ for more info

    async def create_check_run(
        self, check_name, head_sha, status="in_progress", token=None
    ):
        res = await self.api(
            "post",
            "/repos/{}/check-runs".format(self.slug),
            body=dict(name=check_name, head_sha=head_sha, status=status),
            headers={"Accept": "application/vnd.github.antiope-preview+json"},
            token=token,
        )
        return res["id"]

    async def get_check_runs(
        self, check_suite_id=None, head_sha=None, name=None, token=None
    ):
        if check_suite_id is None and head_sha is None:
            raise Exception(
                "check_suite_id and head_sha parameter should not both be None"
            )
        url = ""
        if check_suite_id is not None:
            url = (
                "/repos/{}/check-suites/{}/check-runs".format(
                    self.slug, check_suite_id,
                ),
            )
        elif head_sha is not None:
            url = "/repos/{}/commits/{}/check-runs".format(self.slug, head_sha)
        if name is not None:
            url += "?check_name={}".format(name)
        res = await self.api(
            "get",
            url,
            headers={"Accept": "application/vnd.github.antiope-preview+json"},
            token=token,
        )
        return res

    async def get_check_suites(self, git_sha, token=None):
        res = await self.api(
            "get",
            "/repos/{}/commits/{}/check-suites".format(self.slug, git_sha),
            headers={"Accept": "application/vnd.github.antiope-preview+json"},
            token=token,
        )
        return res

    async def update_check_run(
        self, check_run_id, conclusion, status="completed", output=None, token=None
    ):
        res = await self.api(
            "patch",
            "/repos/{}/check-runs/{}".format(self.slug, check_run_id),
            body=dict(conclusion=conclusion, status=status, output=output),
            headers={"Accept": "application/vnd.github.antiope-preview+json"},
            token=token,
        )
        return res


    def loggable_token(self, token) -> str:
        """Gets a "loggable" version of the current repo token.

        The idea here is to get something in the logs that is enough for us to make comparisons like
            "this log line is probably using the same token as this log line"

        But nothing else

        When there is a username, we will just log who owns that token

        For this, on the cases that there are no username, which is the case for integration tokens,
            we are taking the token, mixing it with a secret that is present only in the code,
            doing a sha256, base64-encoding and only logging the first 5 chars from it
            (from the original 44 chars)

        This, added with the fact that each token is valid only for 1 hour, should be enough
            for people not to be able to extract any useful information from it

        Returns:
            str: A good enough string to tell tokens apart
        """
        if token.get("username"):
            username = token.get("username")
            return f"{username}'s token"
        if token is None or token.get("key") is None:
            return "notoken"
        some_secret = "v1CAF4bFYi2+7sN7hgS/flGtooomdTZF0+uGiigV3AY8f4HHNg".encode()
        hasher = hashlib.sha256()
        hasher.update(some_secret)
        hasher.update(self.service.encode())
        if self.slug:
            hasher.update(self.slug.encode())
        hasher.update(token.get("key").encode())
        return base64.b64encode(hasher.digest()).decode()[:5]

    def get_token_by_type_if_none(self, token: Optional[str], token_type: TokenType):
        if token is not None:
            return token
        return self.get_token_by_type(token_type)