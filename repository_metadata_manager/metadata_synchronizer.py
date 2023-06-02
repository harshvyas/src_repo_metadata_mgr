class MetadataSynchronizer:
    def __init__(self, sourcegraph_client):
        self.sourcegraph_client = sourcegraph_client

    def sync_metadata(self, github_data, sourcegraph_data,sync=False):

        # TODO add logic to extract other github repository metadata besides repository topics 
        github_topics = [edge['node']['topic']['name'] for edge in github_data['repository']['repositoryTopics']['edges']]
        sourcegraph_topics = sourcegraph_data[0]
        sourcegraph_repo_id = sourcegraph_data[1]
        sync = sync
        topics_missing_in_sourcegraph = set(github_topics) - set(sourcegraph_topics)

        if not topics_missing_in_sourcegraph:
            print(f"Metadata synchronization not required. GitHub and Sourcegraph metadata are already in sync.")
            return
    
        # Print the topics that will be added
        print("Topics to be added:")
        for topic in topics_missing_in_sourcegraph:
            print(f"- {topic}")

        if sync:
            print('Syncing topics from GitHub to Sourcegraph...')

            for topic in topics_missing_in_sourcegraph:
                self.sourcegraph_client.add_repository_topic(sourcegraph_repo_id,topic, None)
                print(f"Added topic '{topic}' to Sourcegraph")
        else:
            print('Preview mode. No changes will be made. Use --sync as commandline arg to execute metadata synchronization')
