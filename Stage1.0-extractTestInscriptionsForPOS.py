#!/usr/bin/env python3
"""
Script to extract 20 random Latin inscriptions from the top decile by length
for POS tagging evaluation.
"""

import pandas as pd
import numpy as np
import json
import random
from pathlib import Path
from rich import print

def clean_text_for_length(text):
    """Clean text field for length calculation, handling nulls."""
    if pd.isna(text) or text is None:
        return ""
    return str(text).strip()

def extract_inscriptions_for_pos_testing(
    input_parquet="LIST_v1-2.parquet",
    output_json="POS-LIST-test1.json",
    n_samples=20,
    random_seed=42
):
    """
    Extract random sample of inscriptions from top decile by length.
    
    Parameters:
    -----------
    input_parquet : str
        Path to input parquet file
    output_json : str
        Path to output JSON file
    n_samples : int
        Number of random samples to extract (default: 20)
    random_seed : int
        Random seed for reproducibility (default: 42)
    """
    
    print(f"Reading parquet file: {input_parquet}")
    try:
        df = pd.read_parquet(input_parquet)
        print(f"Successfully loaded {len(df):,} inscriptions")
    except FileNotFoundError:
        print(f"Error: Could not find file {input_parquet}")
        return
    except Exception as e:
        print(f"Error reading parquet file: {e}")
        return
    
    # Verify required columns exist
    required_cols = [
        'LIST-ID', 
        'inscription',
        'clean_text_conservative',
        'clean_text_interpretive_word',
        'clean_text_interpretive_sentence',
        'not_before',
        'not_after',
        'Latitude',
        'Longitude',
        'type_of_inscription_auto',
        'urban_context_city'
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns in parquet file: {missing_cols}")
        print("Available columns:", df.columns.tolist()[:10], "...")
    
    # Calculate text lengths for filtering
    print("\nCalculating text lengths...")
    df['text_length'] = df['clean_text_interpretive_word'].apply(
        lambda x: len(clean_text_for_length(x))
    )
    
    # Remove entries with zero length
    df_with_text = df[df['text_length'] > 0].copy()
    print(f"Inscriptions with text: {len(df_with_text):,}")
    
    # Calculate the 90th percentile threshold
    length_threshold = df_with_text['text_length'].quantile(0.9)
    print(f"\n90th percentile length threshold: {length_threshold:.0f} characters")
    
    # Filter for top decile
    df_top_decile = df_with_text[df_with_text['text_length'] >= length_threshold].copy()
    print(f"Inscriptions in top decile: {len(df_top_decile):,}")
    
    # Set random seed for reproducibility
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Sample 20 random inscriptions
    n_to_sample = min(n_samples, len(df_top_decile))
    if n_to_sample < n_samples:
        print(f"\nWarning: Only {n_to_sample} inscriptions available in top decile")
    
    sampled_df = df_top_decile.sample(n=n_to_sample, random_state=random_seed)
    print(f"\nSampled {len(sampled_df)} inscriptions")
    
    # Prepare output data
    output_data = []
    
    for idx, row in sampled_df.iterrows():
        inscription_data = {
            'LIST-ID': row.get('LIST-ID'),
            'inscription': row.get('inscription'),
            'text_conservative': row.get('clean_text_conservative'),
            'text_interpretive_word': row.get('clean_text_interpretive_word'),
            'text_interpretive_sentence': row.get('clean_text_interpretive_sentence'),
            'type_of_inscription_auto': row.get('type_of_inscription_auto'),
            'dating': {
                'not_before': int(row['not_before']) if pd.notna(row.get('not_before')) else None,
                'not_after': int(row['not_after']) if pd.notna(row.get('not_after')) else None
            },
            'geography': {
                'latitude': row.get('Latitude') if pd.notna(row.get('Latitude')) else None,
                'longitude': row.get('Longitude') if pd.notna(row.get('Longitude')) else None,
                'urban_context_city': row.get('urban_context_city') if pd.notna(row.get('urban_context_city')) else None
            },
            'text_length': int(row['text_length'])
        }
        output_data.append(inscription_data)
    
    # Sort by LIST-ID for consistent output
    output_data.sort(key=lambda x: x['LIST-ID'] if x['LIST-ID'] else '')
    
    # print output with rich
    print("\nSampled inscriptions:")
    for item in output_data:
        print(f"  - LIST-ID: {item['LIST-ID']}, Length: {item['text_length']} characters")
        # and print out type of each field
        for key, value in item.items():
            if isinstance(value, dict):
                print(f"    {key}: {{")
                for subkey, subvalue in value.items():
                    print(f"      {subkey}: {type(subvalue).__name__}")
                print("    }")
            else:
                print(f"    {key}: {type(value).__name__}")
    # Write to JSON file
    print(f"\nWriting output to: {output_json}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Print summary statistics
    print("\n" + "="*50)
    print("EXTRACTION COMPLETE")
    print("="*50)
    print(f"Output file: {output_json}")
    print(f"Number of inscriptions: {len(output_data)}")
    
    lengths = [item['text_length'] for item in output_data]
    print(f"\nText length statistics:")
    print(f"  Min length: {min(lengths):,} characters")
    print(f"  Max length: {max(lengths):,} characters")
    print(f"  Mean length: {np.mean(lengths):,.0f} characters")
    print(f"  Median length: {np.median(lengths):,.0f} characters")
    
    # Check for missing data
    missing_stats = {
        'conservative_text': sum(1 for item in output_data if not item['text_conservative']),
        'interpretive_word': sum(1 for item in output_data if not item['text_interpretive_word']),
        'interpretive_sentence': sum(1 for item in output_data if not item['text_interpretive_sentence']),
        'not_before': sum(1 for item in output_data if item['dating']['not_before'] is None),
        'not_after': sum(1 for item in output_data if item['dating']['not_after'] is None),
        'urban_context_city': sum(1 for item in output_data if not item['geography']['urban_context_city'])
    }
    
    if any(missing_stats.values()):
        print("\nMissing data counts:")
        for field, count in missing_stats.items():
            if count > 0:
                print(f"  {field}: {count}/{len(output_data)}")
    
    return output_data

if __name__ == "__main__":
    # Run the extraction
    extract_inscriptions_for_pos_testing()