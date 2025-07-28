from flask import Flask
from src.rss_parser import RSSParser
from src.openai_client import OpenAIClient

app = Flask(__name__)

def get_news():
    try:
        parser = RSSParser("https://news.smol.ai/rss.xml")
        parser.parse_feed()
        title = parser.get_feed_title()
        latest_news = parser.get_latest_entries(1)

        ai = OpenAIClient()
        summary = ai.summarize_text(latest_news, max_length=30)

        print(summary)

        return title, summary
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "AI News", "Unable to fetch news at this time."


@app.route("/", methods=['GET', 'POST'])
def news_update():
    # To be implemented
    return

@app.route("/process_speech", methods=['POST'])
def process_speech():
    # To be implemented
    return

if __name__ == "__main__":
    app.run(debug=True, port=3000)
