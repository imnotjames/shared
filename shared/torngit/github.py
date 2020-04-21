    TorngitObjectNotFoundError,
    TorngitServerUnreachableError,
    TorngitServer5xxCodeError,
    TorngitClientError,
    TorngitRepoNotFoundError,
    service = "github"
    service_url = "https://github.com"
    api_url = "https://api.github.com"
        repo="{username}/{name}",
        owner="{username}",
        user="{username}",
        issues="{username}/{name}/issues/%(issueid)s",
        commit="{username}/{name}/commit/{commitid}",
        commits="{username}/{name}/commits",
        compare="{username}/{name}/compare/%(base)s...%(head)s",
        comment="{username}/{name}/issues/%(pullid)s#issuecomment-%(commentid)s",
        create_file="{username}/{name}/new/%(branch)s?filename=%(path)s&value=%(content)s",
        pull="{username}/{name}/pull/%(pullid)s",
        branch="{username}/{name}/tree/%(branch)s",
        tree="{username}/{name}/tree/%(commitid)s",
        src="{username}/{name}/blob/%(commitid)s/%(path)s",
        author="{username}/{name}/commits?author=%(author)s",
    async def api(self, method, url, body=None, headers=None, token=None, **args):
            "Accept": "application/json",
            "User-Agent": os.getenv("USER_AGENT", "Default"),
            _headers["Authorization"] = "token %s" % (token or self.token)["key"]
        method = (method or "GET").upper()
        if url[0] == "/":
                event="api",
                bot=(token or self.token).get("username"),
            )
        url = url_concat(url, args).replace(" ", "%20")
            ca_certs=self.verify_ssl if type(self.verify_ssl) is not bool else None,
            validate_cert=self.verify_ssl if type(self.verify_ssl) is bool else None,
            request_timeout=self._timeouts[1],
        )
                log.info("count#%s.timeout=1\n" % self.service)
                raise TorngitServerUnreachableError(
                    "Github was not able to be reached, server timed out."
                )
                "Github HTTP %s" % e.response.code,
                    rlx=e.response.headers.get("X-RateLimit-Remaining"),
                    rly=e.response.headers.get("X-RateLimit-Limit"),
                    rlr=e.response.headers.get("X-RateLimit-Reset"),
                    **log_dict,
                ),
            message = f"Github API: {e.message}"
            raise TorngitServerUnreachableError("GitHub was not able to be reached.")
                "GitHub HTTP %s" % res.code,
                    rlx=res.headers.get("X-RateLimit-Remaining"),
                    rly=res.headers.get("X-RateLimit-Limit"),
                    rlr=res.headers.get("X-RateLimit-Reset"),
                    **log_dict,
                ),
            elif res.headers.get("Content-Type")[:16] == "application/json":
            log.debug(
                "source=%s measure#service=%dms\n"
                % (self.service, int((time() - start) * 1000))
            )
                "get",
                "/repos/%s/branches" % self.slug,
                token=token,
            )
            branches.extend([(b["name"], b["commit"]["sha"]) for b in res])
            "get",
            self.service_url + "/login/oauth/access_token",
            code=self.get_argument("code"),
            client_id=creds["key"],
            client_secret=creds["secret"],
        )
        if session.get("access_token"):
            self.set_token(dict(key=session["access_token"]))
            user = await self.api("get", "/user")
            "get",
            "/orgs/%s/memberships/%s"
            % (self.data["owner"]["username"], user["username"]),
            token=token,
        )
        return res["state"] == "active" and res["role"] == "admin"
        r = await self.api("get", "/repos/%s" % self.slug, token=token)
        ok = r["permissions"]["admin"] or r["permissions"]["push"]
        if self.data["repo"].get("service_id") is None:
            res = await self.api("get", "/repos/%s" % self.slug, token=token)
                "get", "/repositories/%s" % self.data["repo"]["service_id"], token=token
            )
        username, repo = tuple(res["full_name"].split("/", 1))
        parent = res.get("parent")
                    service_id=parent["owner"]["id"], username=parent["owner"]["login"]
                ),
                    service_id=parent["id"],
                    name=parent["name"],
                    language=self._validate_language(parent["language"]),
                    private=parent["private"],
                    branch=parent["default_branch"],
                ),
            owner=dict(service_id=res["owner"]["id"], username=username),
                service_id=res["id"],
                language=self._validate_language(res["language"]),
                private=res["private"],
                branch=res["default_branch"] or "master",
            ),
                "get",
                "/installation/repositories?per_page=100&page=%d" % page,
                headers={"Accept": "application/vnd.github.machine-man-preview+json"},
            )
            if len(res["repositories"]) == 0:
            repos.extend([repo["id"] for repo in res["repositories"]])
            if len(res["repositories"]) <= 100:
                    "get", "/user/repos?per_page=100&page=%d" % page, token=token
                )
                    "get",
                    "/users/%s/repos?per_page=100&page=%d" % (username, page),
                    token=token,
                )
                _o, _r, parent = repo["owner"]["login"], repo["name"], None
                if repo["fork"]:
                            "get", "/repos/%s/%s" % (_o, _r), token=token
                        )
                        parent = parent["source"]
                            service_id=parent["owner"]["id"],
                            username=parent["owner"]["login"],
                        ),
                            service_id=parent["id"],
                            name=parent["name"],
                            language=self._validate_language(parent["language"]),
                            private=parent["private"],
                            branch=parent["default_branch"],
                        ),
                    )
                        owner=dict(service_id=repo["owner"]["id"], username=_o),
                            service_id=repo["id"],
                            language=self._validate_language(repo["language"]),
                            private=repo["private"],
                            branch=repo["default_branch"],
                            fork=fork,
                        ),
                    )
                )
            orgs = await self.api("get", "/user/orgs", page=page, token=token)
                org = await self.api("get", "/users/%s" % org["login"], token=token)
                        name=org["name"] or org["login"],
                        id=str(org["id"]),
                        email=org["email"],
                        username=org["login"],
                    )
                )
            "get", "/repos/%s/pulls/%s/commits" % (self.slug, pullid), token=token
        )
        return [c["sha"] for c in res]
            "post",
            "/repos/%s/hooks" % self.slug,
                name="web",
                config=dict(url=url, secret=secret, content_type="json"),
            ),
            token=token,
        )
    async def edit_webhook(self, hookid, name, url, events, secret, token=None):
                "patch",
                "/repos/%s/hooks/%s" % (self.slug, hookid),
                    name="web",
                    config=dict(url=url, secret=secret, content_type="json"),
                ),
                token=token,
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Cannot find webhook {hookid}"
                )
        try:
                "delete", "/repos/%s/hooks/%s" % (self.slug, hookid), token=token
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Cannot find webhook {hookid}"
                )
            "post",
            "/repos/%s/issues/%s/comments" % (self.slug, issueid),
            token=token,
        )
                "patch",
                "/repos/%s/issues/comments/%s" % (self.slug, commentid),
                token=token,
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(),
                    f"Cannot find comment {commentid} from PR {issueid}",
                )
                "delete",
                "/repos/%s/issues/comments/%s" % (self.slug, commentid),
                token=token,
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(),
                    f"Cannot find comment {commentid} from PR {issueid}",
                )
    async def set_commit_status(
        self,
        commit,
        status,
        context,
        description,
        url,
        merge_commit=None,
        token=None,
        coverage=None,
    ):
        assert status in ("pending", "success", "error", "failure"), "status not valid"
                "post",
                "/repos/%s/statuses/%s" % (self.slug, commit),
                    description=description,
                ),
                token=token,
            )
                "post",
                "/repos/%s/statuses/%s" % (self.slug, merge_commit[0]),
                    description=description,
                ),
                token=token,
            )
                "get",
                "/repos/%s/commits/%s/status" % (self.slug, commit),
                token=token,
            )
            statuses.extend(
                [
                    {
                        "time": s["updated_at"],
                        "state": s["state"],
                        "description": s["description"],
                        "url": s["target_url"],
                        "context": s["context"],
                    }
                    for s in provided_statuses
                ]
            )
            "get", "/repos/%s/commits/%s/status" % (self.slug, commit), token=token
        )
        return res["state"]
                "get",
                "/repos/{0}/contents/{1}".format(self.slug, path.replace(" ", "%20")),
                token=token,
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Path {path} not found at {ref}"
                )
        return dict(content=b64decode(content["content"]), commitid=content["sha"])
                "get",
                "/repos/%s/commits/%s" % (self.slug, commit),
                headers={"Accept": "application/vnd.github.v3.diff"},
                token=token,
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Commit with id {commit} does not exist"
                )
        return self.diff_to_json(res.decode("utf-8"))

    async def get_compare(
        self, base, head, context=None, with_commits=True, token=None
    ):
            "get", "/repos/%s/compare/%s...%s" % (self.slug, base, head), token=token
        )
        for f in res["files"]:
                "diff --git a/%s b/%s%s\n%s\n%s\n%s"
                % (
                    f.get("previous_filename") or f.get("filename"),
                    f.get("filename"),
                    "\ndeleted file mode 100644"
                    if f["status"] == "removed"
                    else "\nnew file mode 100644"
                    if f["status"] == "added"
                    else "",
                    "--- "
                    + (
                        "/dev/null"
                        if f["status"] == "new"
                        else ("a/" + f.get("previous_filename", f.get("filename")))
                    ),
                    "+++ "
                    + (
                        "/dev/null"
                        if f["status"] == "removed"
                        else ("b/" + f["filename"])
                    ),
                    f.get("patch", ""),
                )
            )
            files.update(diff["files"])
            diff=dict(files=files),
                    commitid=c["sha"],
                    message=c["commit"]["message"],
                    timestamp=c["commit"]["author"]["date"],
                        id=(c["author"] or {}).get("id"),
                        username=(c["author"] or {}).get("login"),
                        name=c["commit"]["author"]["name"],
                        email=c["commit"]["author"]["email"],
                    ),
                )
                for c in ([res["base_commit"]] + res["commits"])
            ][::-1],
                "get", "/repos/%s/commits/%s" % (self.slug, commit), token=token
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Commit with id {commit} does not exist"
                )
                raise TorngitRepoNotFoundError(
                    ce.response.body.decode(),
                    f"Repo {self.slug} cannot be found by this user",
                )
                id=str(res["author"]["id"]) if res["author"] else None,
                username=res["author"]["login"] if res["author"] else None,
                email=res["commit"]["author"].get("email"),
                name=res["commit"]["author"].get("name"),
            parents=[p["sha"] for p in res["parents"]],
            message=res["commit"]["message"],
            timestamp=res["commit"]["author"].get("date"),
        )
                id=str(pull["user"]["id"]) if pull["user"] else None,
                username=pull["user"]["login"] if pull["user"] else None,
            base=dict(branch=pull["base"]["ref"], commitid=pull["base"]["sha"]),
            head=dict(branch=pull["head"]["ref"], commitid=pull["head"]["sha"]),
            state="merged" if pull["merged"] else pull["state"],
            title=pull["title"],
            id=str(pull["number"]),
            number=str(pull["number"]),
                "get", "/repos/%s/pulls/%s" % (self.slug, pullid), token=token
            )
                raise TorngitObjectNotFoundError(
                    ce.response.body.decode(), f"Pull Request {pullid} not found"
                )
        commits = await self.api(
            "get", "/repos/%s/pulls/%s/commits" % (self.slug, pullid), token=token
        )
        commit_mapping = {
            val["sha"]: [k["sha"] for k in val["parents"]] for val in commits
        }
        all_commits_in_pr = set([val["sha"] for val in commits])
        current_level = [res["head"]["sha"]]
        if possible_bases and result["base"]["commitid"] not in possible_bases:
                "Github base differs from original base",
                    github_base=result["base"]["commitid"],
                    pullid=pullid,
                ),
            result["base"]["commitid"] = possible_bases[0]
    async def get_pull_requests(self, state="open", token=None):
                "get",
                "/repos/%s/pulls" % self.slug,
                token=token,
            )
            pulls.extend([pull["number"] for pull in res])
    async def find_pull_request(
        self, commit=None, branch=None, state="open", token=None
    ):
        query = "%srepo:%s+type:pr%s" % (
            (("%s+" % commit) if commit else ""),
            url_escape(self.slug),
            (("+state:%s" % state) if state else ""),
        )
        res = await self.api("get", "/search/issues?q=%s" % query, token=token)
        if res["items"]:
            return res["items"][0]["number"]
        return await self.list_files(ref, dir_path="", token=None)
            url = f"/repos/{self.slug}/contents/{dir_path}"
            url = f"/repos/{self.slug}/contents"
        content = await self.api("get", url, ref=ref, token=token)
                "name": f["name"],
                "path": f["path"],
                "type": self._github_type_to_torngit_type(f["type"]),
            }
            for f in content
        if val == "file":
            return "file"
        elif val == "dir":
            return "folder"
        return "other"
            "get", "/repos/%s/commits" % self.slug, token=token, sha=commitid
        start = res[0]["sha"]
        commit_mapping = {val["sha"]: [k["sha"] for k in val["parents"]] for val in res}
            return self.urls["commit"].format(
                username=self.data["owner"]["username"],
                name=self.data["repo"]["name"],
                commitid=kwargs["commitid"],

        if run["repository"]["private"]:
            start_time=run["created_at"],
            finish_time=run["updated_at"],
            status=run["status"],
            slug=run["repository"]["full_name"],
            commit_sha=run["head_sha"],

        res = await self.api(
            "get", "/repos/%s/actions/runs/%s" % (self.slug, run_id), token=token
        )