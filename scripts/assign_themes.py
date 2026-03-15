# scripts/assign_themes.py

"""
Explanation:
This script reads the config, processes all lines, computes scores, updates the database, and logs statistics.
"""

"""
*Content:
keyword_matches()
assign_theme()
"""









import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from data.database import get_connection
from collections import Counter



#  Load Theme_config
with open('data/theme_config.json', 'r') as f:
    config = json.load(f)

theme           = config['themes']
default_themre  = config ['default_theme']
kw_weight       = config ['scoring']['keyword_weight']
sent_weight     = config ['scoring']['sentiment_weight']

analyzer = SentimentIntensityAnalyzer()

def keyword_matches(text, keywords):
    """Count how many keywords appear in the text (word boundries)."""
    text_lower  = text.lower()
    count       = 0
    for kw in keywords:
        # Use word boundaries to match whole words; handle multi-word keywords
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text_lower):
            count += 1
    return count

def assign_theme(text):
    """Return theme with highest score based on sentiment and keywords"""
    scores    = {}
    sentiment = analyzer.polarity_scores(text)['compound']

    for theme_name, theme_data in theme.items():
        keyword_score = keyword_matches(text,theme_data['keywords']) * kw_weight
        # Sentment score if within range
        low, high = theme_data['sentiment_range']
        if low <= sentiment <= high:
            sentiment_score = sent_weight
        else:
            sentiment_score = 0
        total              = keyword_score + sentiment_score
        scores[theme_name] = total

    # Get theme with max scores; if tie, keep first in config order (stable by list or drer)
    best = max(scores.items(), key=lambda x : x[1])
    if best[1] == 0:
        # no matches, use default ('hard')
        return default_themre
    return best[0]

def main():
    conn    = get_connection()
    cursor  = conn.cursor()

    # Fetch all lines that needs assignment (all lines), this will take some time to processe
    cursor.execute('SELECT id, text FROM lines')
    rows = cursor.fetchall()
    print(f"Processing {len(rows)} lines...")

    theme_counts     = Counter()
    sentiment_sums   = Counter()
    sentiment_counts = Counter()

    for row in rows:
        line_id, text = row['id'], row['text']
        theme         = assign_theme(text)
        # Update line
        cursor.execute('UPDATE lines SET theme = ? WHERE id = ?', (theme, line_id))
        # Statistics
        theme_counts[theme] += 1
        sent = analyzer.polarity_scores(text)['compound']
        sentiment_sums[theme]   += sent
        sentiment_counts[theme] += 1

    conn.commit()

    # Print Statistics
    print("\n--- Themes Assignment Statistics ---")
    for theme, count in theme_counts.most_common():
        avg_sent = sentiment_sums[theme] / sentiment_counts[theme] if sentiment_counts[theme] > 0 else 0
        print(f"{theme} : {count} lines, avg sentiment = {avg_sent:.3f}")

    conn.close()
    print("Theme assignment complete.")

if __name__ == '__main__':
    main()