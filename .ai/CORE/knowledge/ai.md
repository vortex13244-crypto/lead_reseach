# AI Engineering — Knowledge Base

> **Purpose:** Practical guide to building production AI features with LLMs.
> **Related:** [prompt-engineering.md](prompt-engineering.md) · [llm.md](llm.md) · [../roles/ai-engineer.md](../roles/ai-engineer.md)

---

## Overview

AI features in this workspace are built using OpenAI and Anthropic APIs, with local models via Ollama for development. Always consider cost, latency, and reliability when designing AI features.

---

## Core Principles

1. **Start with retrieval, not generation** — RAG almost always beats pure generation for factual tasks
2. **Measure before optimizing** — Benchmark before switching to expensive models
3. **Fail gracefully** — LLMs fail; always have a fallback
4. **Cache aggressively** — Semantic cache can cut costs 50-80% in many use cases
5. **Stream for UX** — Users tolerate long waits better when they see progress

---

## LLM API Integration

### OpenAI

```typescript
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  maxRetries: 3,
  timeout: 30 * 1000,  // 30s timeout
})

// Model selection guide:
// gpt-4o-mini  → Fast, cheap ($0.15/1M in). Use for classification, extraction, simple QA
// gpt-4o       → Balanced. Use for complex reasoning, code, structured output
// o1-mini      → Chain-of-thought reasoning. Use for complex problem solving
// o1           → Best reasoning. Use only when quality is critical

// Always use response_format for structured output
const response = await openai.beta.chat.completions.parse({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: prompt }],
  response_format: zodResponseFormat(schema, 'result'),
})
```

### Anthropic (Claude)

```typescript
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

const response = await anthropic.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [{ role: 'user', content: prompt }],
  system: SYSTEM_PROMPT,  // Claude's system prompt is separate
})
const text = response.content[0].type === 'text' ? response.content[0].text : ''
```

---

## RAG Architecture

### Indexing Pipeline

```
Documents → Chunking → Embedding → Vector DB Storage
```

```typescript
// Chunking strategy (RecursiveCharacterTextSplitter equivalent)
function chunkDocument(content: string, chunkSize = 512, overlap = 50): string[] {
  const chunks: string[] = []
  let start = 0

  while (start < content.length) {
    const end = Math.min(start + chunkSize, content.length)
    const chunk = content.slice(start, end)

    // Try to break at paragraph or sentence boundary
    const lastNewline = chunk.lastIndexOf('\n')
    const lastPeriod = chunk.lastIndexOf('. ')
    const breakPoint = lastNewline > chunkSize * 0.5 ? lastNewline : lastPeriod

    chunks.push(breakPoint > 0 && end < content.length
      ? content.slice(start, start + breakPoint)
      : chunk
    )

    start = start + (breakPoint > 0 && end < content.length ? breakPoint : chunkSize) - overlap
  }

  return chunks.filter(c => c.trim().length > 50)
}

// Embed and store
async function indexDocument(doc: Document): Promise<void> {
  const chunks = chunkDocument(doc.content)

  const embeddings = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: chunks,
  })

  await prisma.$transaction(
    chunks.map((chunk, i) =>
      prisma.$executeRaw`
        INSERT INTO document_chunks (document_id, content, embedding)
        VALUES (${doc.id}, ${chunk}, ${embeddings.data[i].embedding}::vector)
      `
    )
  )
}
```

### Query Pipeline

```typescript
async function queryRAG(question: string): Promise<string> {
  // 1. Embed the question
  const { data: [{ embedding }] } = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: question,
  })

  // 2. Search for relevant chunks
  const chunks = await prisma.$queryRaw<{ content: string; similarity: number }[]>`
    SELECT content, 1 - (embedding <=> ${embedding}::vector) AS similarity
    FROM document_chunks
    WHERE 1 - (embedding <=> ${embedding}::vector) > 0.7
    ORDER BY embedding <=> ${embedding}::vector
    LIMIT 5
  `

  if (chunks.length === 0) {
    return "I don't have relevant information to answer that question."
  }

  // 3. Generate answer with context
  const context = chunks.map((c, i) => `[${i + 1}] ${c.content}`).join('\n\n')

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    temperature: 0.1,
    messages: [
      {
        role: 'system',
        content: `Answer questions using ONLY the provided context. Cite sources as [1], [2], etc.
If the context doesn't contain the answer, say "I don't have information about that."`,
      },
      { role: 'user', content: `Context:\n${context}\n\nQuestion: ${question}` },
    ],
  })

  return response.choices[0].message.content ?? ''
}
```

---

## AI Evaluation

### LLM-as-Judge Pattern

```typescript
async function evaluateResponse(
  question: string,
  answer: string,
  criteria: string[]
): Promise<{ score: number; reasoning: string }> {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',  // Use a smarter model as judge
    messages: [{
      role: 'user',
      content: `Evaluate this answer against the criteria. Return JSON.
Question: ${question}
Answer: ${answer}
Criteria: ${criteria.join(', ')}

JSON format: {"score": 0-10, "reasoning": "explanation"}`
    }],
    response_format: { type: 'json_object' },
  })

  return JSON.parse(response.choices[0].message.content!)
}
```

---

## Cost Optimization

```typescript
// Semantic caching — cache by semantic similarity, not exact match
class SemanticCache {
  async get(query: string): Promise<string | null> {
    const embedding = await embed(query)
    const cached = await db.query(`
      SELECT response FROM ai_cache
      WHERE 1 - (embedding <=> $1::vector) > 0.95  -- Very similar queries
      ORDER BY embedding <=> $1::vector
      LIMIT 1
    `, [embedding])
    return cached[0]?.response ?? null
  }

  async set(query: string, response: string): Promise<void> {
    const embedding = await embed(query)
    await db.query('INSERT INTO ai_cache (query, embedding, response) VALUES ($1, $2, $3)',
      [query, embedding, response])
  }
}

// Token counting before calling API
const estimatedCost = countTokens(prompt) * 0.00000015  // gpt-4o-mini input price
if (estimatedCost > 0.01) logger.warn('Expensive AI call', { estimated_cost: estimatedCost })
```

---

## Resources

- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Anthropic Docs](https://docs.anthropic.com/)
- [LangChain JS](https://js.langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Ollama](https://ollama.ai/) — Local models
- [LangSmith](https://www.langchain.com/langsmith) — LLM observability
