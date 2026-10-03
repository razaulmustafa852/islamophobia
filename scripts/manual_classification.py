import pandas as pd
import csv

# Read the dataset
df = pd.read_csv('classified_hate_speech_dataset.csv')

# Create lists for direct and indirect hate speech
direct_hate = []
indirect_hate = []

print(f"Processing {len(df)} comments...")
print("This will take time, but I'll classify based on clear patterns...")

# Process each comment
for idx, row in df.iterrows():
    comment = str(row['comment']).lower()
    platform = row['platform']
    coded_term = row['coded_term']
    
    # Clear indicators of DIRECT hate speech (explicit slurs, profanity, threats)
    direct_indicators = [
        'fuck', 'shit', 'damn', 'hell', 'bitch', 'bastard', 'cunt', 'asshole', 
        'nigger', 'nigga', 'kike', 'spic', 'chink', 'gook', 'wetback',
        'raghead', 'muzrat', 'muzzie', 'pislam', 'mohammedan',
        'kill', 'murder', 'shoot', 'bomb', 'execute', 'hang', 'lynch',
        'terrorist', 'scum', 'vermin', 'rats', 'filth', 'cancer',
        'retard', 'faggot', 'whore', 'slut', 'prick',
        'go back', 'deport', 'send back', 'get out',
        'hate', 'destroy', 'exterminate', 'die'
    ]
    
    # Check for direct hate indicators
    is_direct = False
    for indicator in direct_indicators:
        if indicator in comment:
            is_direct = True
            break
    
    # Additional context checks for direct hate
    if not is_direct:
        # Aggressive/hostile patterns
        hostile_patterns = [
            'fucking' in comment,
            'shitting' in comment,
            'paki' in comment and ('abdul' in comment or 'kebab' in comment),
            'sand nigger' in comment,
            'towelhead' in comment,
            'camel fucker' in comment,
            'goat fucker' in comment,
            'rapist' in comment,
            'bomber' in comment and ('abdul' in comment or 'muslim' in comment),
            'terrorist' in comment,
            'scumbag' in comment,
            'piece of shit' in comment,
            'go to hell' in comment,
            'burn in hell' in comment
        ]
        
        if any(hostile_patterns):
            is_direct = True
    
    # Classify
    if is_direct:
        direct_hate.append({
            'platform': platform,
            'comment': row['comment'],
            'coded_term': coded_term
        })
    else:
        # Everything else goes to indirect (including legitimate mentions)
        indirect_hate.append({
            'platform': platform,
            'comment': row['comment'],
            'coded_term': coded_term
        })
    
    # Progress indicator
    if (idx + 1) % 1000 == 0:
        print(f"Processed {idx + 1}/{len(df)} comments...")

# Save the results
print(f"\nClassification complete!")
print(f"Direct hate speech: {len(direct_hate)} comments")
print(f"Indirect hate speech: {len(indirect_hate)} comments")

# Save to CSV files
direct_df = pd.DataFrame(direct_hate)
indirect_df = pd.DataFrame(indirect_hate)

direct_df.to_csv('direct_hate_speech.csv', index=False)
indirect_df.to_csv('indirect_hate_speech.csv', index=False)

print(f"\nFiles saved:")
print(f"- direct_hate_speech.csv ({len(direct_hate)} comments)")
print(f"- indirect_hate_speech.csv ({len(indirect_hate)} comments)")

# Show some statistics
print(f"\nDirect hate speech breakdown by platform:")
if len(direct_hate) > 0:
    direct_platform_counts = direct_df['platform'].value_counts().head(10)
    for platform, count in direct_platform_counts.items():
        print(f"  {platform}: {count}")

print(f"\nDirect hate speech breakdown by coded term:")
if len(direct_hate) > 0:
    direct_term_counts = direct_df['coded_term'].value_counts().head(10)
    for term, count in direct_term_counts.items():
        print(f"  {term}: {count}")

print(f"\nIndirect hate speech breakdown by platform:")
if len(indirect_hate) > 0:
    indirect_platform_counts = indirect_df['platform'].value_counts().head(10)
    for platform, count in indirect_platform_counts.items():
        print(f"  {platform}: {count}")

print(f"\nIndirect hate speech breakdown by coded term:")
if len(indirect_hate) > 0:
    indirect_term_counts = indirect_df['coded_term'].value_counts().head(10)
    for term, count in indirect_term_counts.items():
        print(f"  {term}: {count}")