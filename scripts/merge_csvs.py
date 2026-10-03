import pandas as pd
import csv

# Initialize the unified dataset
unified_data = []

def safe_read_csv(filename, text_col, platform_col=None, default_platform=None, coded_term=None, keyword_col=None):
    """Safely read CSV with error handling"""
    try:
        print(f'Processing {filename}...')
        # Try with different encodings and error handling
        try:
            df = pd.read_csv(filename, encoding='utf-8', on_bad_lines='skip')
        except:
            df = pd.read_csv(filename, encoding='latin-1', on_bad_lines='skip')
        
        count = 0
        for _, row in df.iterrows():
            try:
                platform = row[platform_col] if platform_col else default_platform
                comment = row[text_col]
                
                # Get coded term - either from column or default
                term = row[keyword_col] if keyword_col and keyword_col in df.columns else coded_term
                
                # Skip empty comments
                if pd.isna(comment) or str(comment).strip() == '':
                    continue
                    
                unified_data.append({
                    'platform': platform,
                    'comment': str(comment).strip(),
                    'coded_term': term
                })
                count += 1
            except Exception as e:
                continue
        
        print(f'  Added {count} comments from {filename}')
        return count
    except Exception as e:
        print(f'  Error processing {filename}: {e}')
        return 0

# Process each CSV file
total_count = 0

# abdul.csv
total_count += safe_read_csv('abdul.csv', 'text', 'platform', coded_term='abdul')

# hate_speech_tweets (check if it has keyword_matched column)
total_count += safe_read_csv('hate_speech_tweets_20251011_221838.csv', 'text', default_platform='Twitter', keyword_col='keyword_matched')

# kebab.csv
total_count += safe_read_csv('kebab - kebab.csv', 'text', 'platform', coded_term='kebab')

# Mohammedan.csv
total_count += safe_read_csv('Mohammedan - Mohammedan.csv', 'text', 'platform', coded_term='mohammedan')

# muzrat.csv
total_count += safe_read_csv('muzrat - muzrat.csv', 'text', 'platform', coded_term='muzrat')

# pislam.csv
total_count += safe_read_csv('pislam - pislam.csv', 'text', 'platform', coded_term='pislam')

# raghead.csv
total_count += safe_read_csv('raghead - raghead.csv', 'text', 'platform', coded_term='raghead')

# toxic-file-merge.csv (mixed terms)
total_count += safe_read_csv('toxic-file-merge.csv', 'Text', default_platform='Unknown', coded_term='mixed')

# YouTube file (check if it has query column)
total_count += safe_read_csv('youtube_hate_comments_with_audio_20251002_210907 - hate_comments_with_audio_20251002_210907.csv', 'comment_text', default_platform='YouTube', keyword_col='query')

# Save unified dataset
print(f'\nTotal comments collected: {len(unified_data)}')
if unified_data:
    unified_df = pd.DataFrame(unified_data)
    unified_df.to_csv('unified_hate_speech_dataset.csv', index=False)
    print('Unified dataset saved to unified_hate_speech_dataset.csv!')
    
    # Show platform distribution
    platform_counts = unified_df['platform'].value_counts()
    print('\nPlatform distribution:')
    for platform, count in platform_counts.items():
        print(f'  {platform}: {count} comments')
    
    # Show coded term distribution
    term_counts = unified_df['coded_term'].value_counts()
    print('\nCoded term distribution:')
    for term, count in term_counts.items():
        print(f'  {term}: {count} comments')
else:
    print('No data collected!')