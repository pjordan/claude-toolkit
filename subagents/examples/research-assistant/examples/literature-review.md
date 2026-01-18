# Example: Literature Review Session

This example demonstrates how the Research Assistant subagent handles a literature review request.

## User Request

```
I'm researching the impact of transformer architectures on natural language processing.
Can you help me understand the key papers and developments in this area?
```

## Expected Response Pattern

The Research Assistant will:

1. **Identify key foundational papers**
   - "Attention Is All You Need" (Vaswani et al., 2017)
   - BERT, GPT series, and their variants

2. **Organize by themes**
   - Architecture innovations
   - Pre-training objectives
   - Scaling laws
   - Efficiency improvements

3. **Highlight methodology**
   - Self-attention mechanisms
   - Transfer learning approaches
   - Benchmark evaluations

4. **Suggest research directions**
   - Current open problems
   - Emerging trends
   - Gaps in literature

## Configuration Used

```json
{
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.5,
  "max_tokens": 4096
}
```

The moderate temperature (0.5) balances factual accuracy with helpful synthesis.
