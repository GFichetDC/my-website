import yaml
from scholarly import scholarly
import time

# Configure scholarly (use Tor if needed)
scholarly.set_timeout(10)
scholarly.set_retries(3)

def get_citations(title):
    try:
        search = scholarly.search_pubs(title)
        pub = next(search).fill()
        return pub.num_citations
    except:
        return None

with open('_data/citations.yml', 'r') as f:
    data = yaml.safe_load(f)

for title in data:
    if 'total_citations' not in data[title]:
        print(f"Fetching citations for: {title}")
        citations = get_citations(title)
        if citations is not None:
            data[title]['total_citations'] = citations
            print(f"Updated {title} with {citations} citations")
        time.sleep(30)  # Avoid rate limiting

with open('_data/citations.yml', 'w') as f:
    yaml.dump(data, f, sort_keys=False)