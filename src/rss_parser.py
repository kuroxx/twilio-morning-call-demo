import feedparser

class RSSParser:
    """A class for parsing RSS feeds and extracting feed information."""
    
    def __init__(self, rss_url=None):
        self.rss_url = rss_url
        self.feed_info = None
    
    def parse_feed(self, rss_url=None):
        url = rss_url or self.rss_url

        if not url:
            raise ValueError("No RSS URL provided")
        
        try: 
            rss_feed = feedparser.parse(url)

            if rss_feed.bozo: 
                raise ValueError("Failed to parse feed: " + str(rss_feed.bozo_exception))
            
            self.feed_info = {
                'title': rss_feed.feed.get('title', 'No title'),
                'link': rss_feed.feed.get('link', 'No link'),
                'description': rss_feed.feed.get('description', 'No description'),
                'entries': []
            }

            # Extract entries/items from the RSS feed
            for entry in rss_feed.entries:
                entry_data = {
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', 'No link'),
                    'summary': entry.get('summary', 'No summary'),
                    'description': entry.get('description', 'No description'),
                    'published': entry.get('published', 'No date'),
                    'published_parsed': entry.get('published_parsed', None),
                    'id': entry.get('id', 'No id'),
                    'guid': entry.get('guid', 'No guid')
                }
                self.feed_info['entries'].append(entry_data)
            
            return self.feed_info

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def print_summary(self, max_entries=7):
        """Print a summary of the parsed feed."""
        if not self.feed_info:
            print("No feed data available. Please parse a feed first.")
            return
        
        print(f"Found {len(self.feed_info['entries'])} entries")
        print(f"Feed title: {self.feed_info['title']}")

        # Print first few entries for testing
        for i, entry in enumerate(self.feed_info['entries'][:max_entries]):
            print(f"\nEntry {i+1}:")
            print(f"  Title: {entry['title']}")
            print(f"  Link: {entry['link']}")
            print(f"  Published: {entry['published']}")
            print(f"  Summary: {entry['summary'][:300]}...")
    
    def get_latest_entries(self, count=5):
        """Get the latest N entries from the feed."""
        if not self.feed_info:
            return []
        return self.feed_info['entries'][:count]
    
    def get_feed_title(self):
        if not self.feed_info:
            return None
        return self.feed_info['title']
