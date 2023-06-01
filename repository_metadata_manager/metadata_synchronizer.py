from sourcegraph.api_client import SourcegraphAPIClient


class MetadataSynchronizer:
    def __init__(self, sourcegraph_api, github_data, sourcegraph_data,sync=False):
        self.sourcegraph_api = sourcegraph_api
        self.github_topics = set(github_data)
        self.sourcegraph_topics = set(sourcegraph_data[0])
        self.sourcegraph_repo_id = sourcegraph_data[1]
        self.sync = sync

    def sync_metadata(self):
        topics_missing_in_sourcegraph = self.github_topics - self.sourcegraph_topics

        if not topics_missing_in_sourcegraph:
            print(f"Metadata synchronization not required. GitHub and Sourcegraph metadata are already in sync.")
            return
    
        # Print the topics that will be added
        print("Topics to be added:")
        for topic in topics_missing_in_sourcegraph:
            print(f"- {topic}")

        if self.sync:
            print('Syncing topics from GitHub to Sourcegraph...')

            for topic in topics_missing_in_sourcegraph:
                self.sourcegraph_api.add_repository_topic(self.sourcegraph_repo_id,topic)
                print(f"Added topic '{topic}' to Sourcegraph")
        else:
            print('Preview mode. No changes will be made. Use --sync as commandline arg to execute metadata synchronization')
