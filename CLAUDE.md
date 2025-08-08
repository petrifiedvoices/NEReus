# Latin Inscription NER & POS Tagging Project

## Core Research Objective
Evaluate and improve part-of-speech (POS) tagging and named entity recognition (NER) performance on Latin epigraphic texts, creating gold standards and assessing multiple computational approaches.

## Key Data Structure
All inscriptions contain these critical fields:
- `inscription`: Raw epigraphic text with notation (brackets, parentheses, etc.)
- `text_interpretive_word`: Cleaned, expanded text for computational analysis
- `text_conservative`: Diplomatic transcription preserving abbreviations
- `LIST-ID`: Unique identifier
- `type_of_inscription_auto`: Classification (epitaph, defixio, etc.)

## Epigraphic Notation Conventions
- `[...]`: Reconstructed/missing text
- `(...)`: Expanded abbreviations
- `[3]`: Gap of approximately 3 characters
- `/`: Line break on stone
- `<...>`: Editorial corrections
- `{...}`: Superfluous text
- `?`: Uncertain reading

## Project Stages
1. **Stage 1: POS Gold Standard Creation**
   - 1.1: Generate annotation spreadsheets
   - 1.2: Manual annotation
   - 1.3: Inter-annotator agreement

2. **Stage 2: POS Tagger Evaluation**
   - Test multiple taggers on gold standard
   - Compare performance metrics

3. **Stage 3: NER Development**
   - Entity type definition
   - Gold standard creation
   - Model training/evaluation

## Technical Specifications
- Output format: XLSX (LibreOffice compatible)
- POS tagset: Universal Dependencies v2 (17 tags)
- Programming: Python with openpyxl
- Character encoding: UTF-8 (handle Latin and Greek)

## Critical Design Principles
1. **Preserve alignment** between inscription and interpretive text
2. **Computer-parsable** outputs (clean data columns, metadata separate)
3. **Visual clarity** for human annotators (highlighting, context windows)
4. **Handle edge cases**: fragmentary text, nonsense words in curse tablets, Greek passages

## Special Considerations
- Curse tablets (defixiones) contain magical/nonsensical text
- Inscriptions are often heavily fragmentary
- One epigraphic token may expand to multiple interpretive words
- Maintain scholarly rigor while enabling computational analysis

## Success Metrics
- Clean, consistent gold standard annotations
- Reproducible evaluation pipeline
- Clear documentation of edge cases and decisions
- Measurable improvements in tagger performance for epigraphic Latin

## Working Principles & Collaboration Style

### Academic Standards
- This is rigorous academic research in Latin epigraphy
- Accuracy and precision supersede politeness or encouragement
- Question assumptions, including your own
- Document uncertainty explicitly

### Problem-Solving Approach
1. **Ask one specific question at a time** - no question dumps
2. **Prefer smaller, verifiable steps** over ambitious leaps
3. **Critique before implementing** - "Is this actually better than the simple approach?"
4. **Test edge cases immediately** - especially fragmentary inscriptions and defixiones

### Debugging Methodology
When issues arise:
1. State the exact error/problem
2. Consider similar cases and patterns
3. Propose solution WITH criticism of that solution
4. Ask: "What could go wrong with this approach?"
5. Only then implement

### Decision Framework
Before any "clever" solution:
- Will this actually help the annotation process?
- Does this handle the messiest inscriptions?
- Is the complexity justified by the benefit?
- What's the simplest approach that could work?

### Communication Style
- Be direct and specific about problems
- Skip reassurances and flattery
- Flag uncertainties immediately
- Challenge proposed solutions, especially your own
- If something seems elegant, ask why it might be wrong

### Example Interaction Pattern
BAD: "Great idea! Let me implement this sophisticated alignment algorithm..."
GOOD: "That could work, but won't it fail on inscription #2 where... Should we test the simpler line-based approach first?"

Whenever there is a bug or decision we make, we should add it to an appropriate section of a FAQ.md
