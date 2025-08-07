#!/usr/bin/env python3
"""
Proof of concept: Test Latin POS taggers one by one
"""
from rich import print

# Test inscription
TEST_TEXT = "Dis Manibus sacrum Marisa Frontonis filia pia vixit annos LX hic sita est Dis Manibus sacrum Marhulus Luci filius pius vixit annis LXV hic est"

print("="*60)
print("Testing Latin POS Taggers")
print("="*60)
print(f"\nTest text: {TEST_TEXT[:50]}...")
print("="*60)

# Test 1: LatinCy (spaCy-based)
print("\n1. Testing LatinCy...")
try:
    import spacy
    nlp = spacy.load('la_core_web_lg')
    doc = nlp(TEST_TEXT)
    
    print("✓ LatinCy loaded successfully")
    print("\nFirst 5 tokens:")
    for i, token in enumerate(doc[:5]):
        print(f"  {token.text:10} -> POS: {token.pos_:6} Lemma: {token.lemma_}")
    print(f"  ... ({len(doc)} tokens total)")
    
except Exception as e:
    print(f"✗ LatinCy failed: {e}")

print("\n" + "="*60)


# Test 2: Stanza
print("\n[bold]2. Testing Stanza...[/bold]")
try:
    import stanza
    # Initialize with silent mode to reduce verbosity
    nlp_stanza = stanza.Pipeline('la', processors='tokenize,mwt,pos,lemma', verbose=False)
    doc_stanza = nlp_stanza(TEST_TEXT)
    
    print("[green]✓ Stanza loaded successfully[/green]")
    print("\nFirst 5 tokens:")
    token_count = 0
    for sent in doc_stanza.sentences:
        for token in sent.words[:5]:
            print(f"  {token.text:10} -> UPOS: {token.upos:6} XPOS: {token.xpos:6} Feats: {token.feats if token.feats else '_':15} Lemma: {token.lemma}")

            token_count += 1
            if token_count >= 5:
                break
        if token_count >= 5:
            break
    
    total_tokens = sum(len(sent.words) for sent in doc_stanza.sentences)
    print(f"  [dim]... ({total_tokens} tokens total)[/dim]")
    
except Exception as e:
    print(f"[red]✗ Stanza failed: {e}[/red]")

print("\n" + "="*60)