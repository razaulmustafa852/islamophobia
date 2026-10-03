import pandas as pd
import re
from collections import Counter

def classify_hate_speech(comment, coded_term):
    """
    Classify hate speech as direct/explicit or implicit/coded
    """
    comment_lower = comment.lower()
    
    # Explicit hate indicators
    explicit_slurs = [
        'nigger', 'nigga', 'kike', 'spic', 'chink', 'gook', 'wetback', 'towelhead',
        'raghead', 'muzrat', 'muzzie', 'koranimal', 'pislam', 'mohammedan'
    ]
    
    explicit_hate_terms = [
        'terrorist', 'scum', 'vermin', 'rats', 'animals', 'filth', 'cancer',
        'disease', 'plague', 'infestation', 'invasion', 'destroy', 'kill',
        'death to', 'exterminate', 'genocide', 'final solution'
    ]
    
    dehumanizing_terms = [
        'subhuman', 'savage', 'barbarian', 'primitive', 'uncivilized',
        'cockroach', 'parasite', 'virus', 'tumor'
    ]
    
    violence_indicators = [
        'kill', 'murder', 'shoot', 'bomb', 'execute', 'hang', 'lynch',
        'gas', 'burn', 'torture', 'rape', 'assault', 'attack'
    ]
    
    # Check for explicit indicators
    explicit_score = 0
    
    # Direct slurs
    for slur in explicit_slurs:
        if slur in comment_lower:
            explicit_score += 3
    
    # Hate terms
    for term in explicit_hate_terms:
        if term in comment_lower:
            explicit_score += 2
    
    # Dehumanizing language
    for term in dehumanizing_terms:
        if term in comment_lower:
            explicit_score += 2
    
    # Violence indicators
    for term in violence_indicators:
        if term in comment_lower:
            explicit_score += 2
    
    # Profanity (general cursing)
    profanity = [
        'fuck', 'shit', 'damn', 'hell', 'bitch', 'bastard', 'cunt',
        'asshole', 'prick', 'whore', 'slut'
    ]
    
    for curse in profanity:
        if curse in comment_lower:
            explicit_score += 1
    
    # Special case: coded terms used in obviously hateful context
    coded_hate_patterns = [
        r'\babdul\b.*\b(go back|deport|terrorist|bomber)',
        r'\bkebab\b.*(remove|out|back)',
        r'fucking.*\babdul\b',
        r'\babdul\b.*shit',
    ]
    
    for pattern in coded_hate_patterns:
        if re.search(pattern, comment_lower):
            explicit_score += 2
    
    # Classification logic
    if explicit_score >= 3:
        return 'explicit'
    elif explicit_score >= 1:
        return 'mixed'  # Some explicit elements but not overwhelming
    else:
        # Check if it's likely implicit hate
        implicit_indicators = [
            coded_term in ['abdul', 'kebab'] and len(comment) < 100,  # Short dismissive comments
            'abdul' in comment_lower and any(word in comment_lower for word in ['why', 'crying', 'when', 'what']),
            coded_term in comment_lower and any(word in comment_lower for word in ['typical', 'always', 'these people'])
        ]
        
        if any(implicit_indicators):
            return 'implicit'
        else:
            return 'unclear'  # Might be legitimate mention

def analyze_dataset():
    """Analyze and classify the unified dataset"""
    
    # Load the dataset
    print("Loading unified dataset...")
    df = pd.read_csv('unified_hate_speech_dataset.csv')
    
    print(f"Total comments: {len(df)}")
    
    # Classify each comment
    print("Classifying hate speech types...")
    df['hate_type'] = df.apply(lambda row: classify_hate_speech(row['comment'], row['coded_term']), axis=1)
    
    # Save the classified dataset
    df.to_csv('classified_hate_speech_dataset.csv', index=False)
    print("Classified dataset saved to 'classified_hate_speech_dataset.csv'")
    
    # Analysis
    print("\n=== HATE SPEECH CLASSIFICATION RESULTS ===")
    
    # Overall distribution
    hate_type_counts = df['hate_type'].value_counts()
    print(f"\nOverall Classification:")
    for hate_type, count in hate_type_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {hate_type}: {count} ({percentage:.1f}%)")
    
    # By coded term
    print(f"\nClassification by Coded Term:")
    term_analysis = df.groupby(['coded_term', 'hate_type']).size().unstack(fill_value=0)
    
    # Show top terms
    top_terms = df['coded_term'].value_counts().head(10).index
    for term in top_terms:
        term_data = df[df['coded_term'] == term]
        term_dist = term_data['hate_type'].value_counts()
        print(f"\n  {term} ({len(term_data)} comments):")
        for hate_type, count in term_dist.items():
            percentage = (count / len(term_data)) * 100
            print(f"    {hate_type}: {count} ({percentage:.1f}%)")
    
    # By platform
    print(f"\nClassification by Platform (top 10):")
    top_platforms = df['platform'].value_counts().head(10).index
    for platform in top_platforms:
        platform_data = df[df['platform'] == platform]
        platform_dist = platform_data['hate_type'].value_counts()
        print(f"\n  {platform} ({len(platform_data)} comments):")
        for hate_type, count in platform_dist.items():
            percentage = (count / len(platform_data)) * 100
            print(f"    {hate_type}: {count} ({percentage:.1f}%)")
    
    # Sample comments for each type
    print(f"\n=== SAMPLE COMMENTS BY TYPE ===")
    for hate_type in ['explicit', 'mixed', 'implicit', 'unclear']:
        if hate_type in df['hate_type'].values:
            samples = df[df['hate_type'] == hate_type].sample(min(3, len(df[df['hate_type'] == hate_type])))
            print(f"\n{hate_type.upper()} Examples:")
            for idx, row in samples.iterrows():
                comment_preview = row['comment'][:100] + "..." if len(row['comment']) > 100 else row['comment']
                print(f"  [{row['coded_term']}] {comment_preview}")

if __name__ == "__main__":
    analyze_dataset()