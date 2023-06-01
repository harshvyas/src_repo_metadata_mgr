class MetadataRetriever:
    def __init__(self, github_api, sourcegraph_api):
        self.github_api = github_api
        self.sourcegraph_api = sourcegraph_api

    def fetch_github_metadata(self, owner_name, repository_name, query_file):
        return self.github_api.fetch_repository_metadata(owner_name, repository_name, query_file)

    def fetch_sourcegraph_metadata(self, code_host_name, owner_name, repository_name):
        return self.sourcegraph_api.fetch_repository_metadata(code_host_name, owner_name, repository_name)
