            return url_escape(string, plus=False).replace("%2F", "/")
            return string.encode("utf-8", "replace")
        "javascript",
        "shell",
        "python",
        "ruby",
        "perl",
        "dart",
        "java",
        "c",
        "clojure",
        "d",
        "fortran",
        "go",
        "groovy",
        "kotlin",
        "php",
        "r",
        "scala",
        "swift",
        "objective-c",
        "xtend",
        self,
        oauth_consumer_token=None,
        timeouts=None,
        token=None,
        verify_ssl=None,
        **kwargs,
    ):
        self.data = {"owner": {}, "repo": {}}
        return "<%s slug=%s ownerid=%s repoid=%s>" % (
            self.service,
            self.slug,
            self.data["owner"].get("ownerid"),
            self.data["repo"].get("repoid"),
        )
        if self.data["owner"] and self.data["repo"]:
            if self.data["owner"].get("username") and self.data["repo"].get("name"):
                return "%s/%s" % (
                    self.data["owner"]["username"],
                    self.data["repo"]["name"],
                )
        return {"commitid": start, "parents": parents}
        diff = ("\n%s" % diff).split("\ndiff --git a/")
                before, after = _diff.pop(0).split(" b/", 1)
                    if source.startswith("--- a/"):
                    elif source.startswith("+++ b/"):
                type="new" if before == "/dev/null" else "modified",
                before=None if before == after or before == "/dev/null" else before,
                segments=[],
            )
                if source == "\ No newline at end of file":
                if sol4 == "dele":
                    _file["before"] = after
                    _file["type"] = "deleted"
                    _file.pop("segments")
                elif sol4 == "new " and not source.startswith("new mode "):
                    _file["type"] = "new"
                elif sol4 == "Bina":
                    _file["type"] = "binary"
                    _file.pop("before")
                    _file.pop("segments")
                elif sol4 in ("--- ", "+++ ", "inde", "diff", "old ", "new "):
                elif sol4 == "@@ -":
                    _file["segments"].append(segment)
                elif source == "":
                    segment["lines"].append(source)
            if "segments" in data:
                for segment in data["segments"]:
                    rm += sum([1 for line in segment["lines"] if line[0] == "-"])
                    add += sum([1 for line in segment["lines"] if line[0] == "+"])
            data["stats"] = dict(added=add, removed=rm)
    async def delete_comment(
        self, pullid: str, commentid: str, token: str = None
    ) -> bool:
    async def edit_comment(
        self, pullid: str, commentid: str, body: str, token=None
    ) -> dict:
    async def find_pull_request(
        self, commit=None, branch=None, state="open", token=None
    ):
    async def get_pull_requests(self, state="open", token=None):
    async def set_commit_status(
        self,
        commit: str,
        status,
        context,
        description,
        url,
        coverage=None,
        merge_commit=None,
        token=None,
    ):
    async def edit_webhook(
        self, hookid: str, name, url, events: dict, secret, token=None
    ) -> dict:
    async def get_compare(
        self, base, head, context=None, with_commits=True, token=None
    ):