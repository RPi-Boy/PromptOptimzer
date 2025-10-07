# Sample Questions for Testing

## Text Format (questions.txt)

```
What is artificial intelligence?
Explain quantum computing in simple terms.
How does blockchain technology work?
What are the benefits of machine learning?
Describe the concept of neural networks.
What is the difference between AI and ML?
How does natural language processing work?
Explain reinforcement learning with an example.
What are large language models?
How does GPT technology work?
```

## JSON Format - Simple Array (questions.json)

```json
[
  "What is artificial intelligence?",
  "Explain quantum computing in simple terms.",
  "How does blockchain technology work?",
  "What are the benefits of machine learning?",
  "Describe the concept of neural networks.",
  "What is the difference between AI and ML?",
  "How does natural language processing work?",
  "Explain reinforcement learning with an example.",
  "What are large language models?",
  "How does GPT technology work?"
]
```

## JSON Format - Array of Objects (questions_detailed.json)

```json
[
  {
    "question": "What is artificial intelligence?",
    "category": "basics",
    "difficulty": "easy"
  },
  {
    "question": "Explain quantum computing in simple terms.",
    "category": "technology",
    "difficulty": "medium"
  },
  {
    "question": "How does blockchain technology work?",
    "category": "technology",
    "difficulty": "medium"
  },
  {
    "question": "What are the benefits of machine learning?",
    "category": "ai",
    "difficulty": "easy"
  },
  {
    "question": "Describe the concept of neural networks.",
    "category": "ai",
    "difficulty": "medium"
  }
]
```

## JSON Format - Nested Structure (questions_nested.json)

```json
{
  "questions": [
    "What is artificial intelligence?",
    "Explain quantum computing in simple terms.",
    "How does blockchain technology work?"
  ],
  "metadata": {
    "source": "sample",
    "date": "2024-01-01"
  }
}
```

## Code-Related Questions

```json
[
  "Write a Python function to calculate factorial.",
  "Explain the difference between let, const, and var in JavaScript.",
  "How do you implement a binary search algorithm?",
  "What are the SOLID principles in software engineering?",
  "Explain the concept of REST APIs.",
  "How does asynchronous programming work in Python?",
  "What is the difference between SQL and NoSQL databases?",
  "Describe the MVC architecture pattern.",
  "How do you handle errors in JavaScript?",
  "What are design patterns in software development?"
]
```

## Creative Writing Prompts

```json
[
  "Write a haiku about programming.",
  "Describe a futuristic city in 100 words.",
  "Create a short story about a time traveler.",
  "Write a product description for a smart home device.",
  "Compose a motivational speech about learning.",
  "Draft a cover letter for a software engineering position.",
  "Write a blog post introduction about climate change.",
  "Create dialogue between a human and an AI.",
  "Write a poem about the internet.",
  "Describe your perfect day in vivid detail."
]
```

## Business & Professional Questions

```json
[
  "How do you create an effective marketing strategy?",
  "Explain the concept of ROI in business.",
  "What are the key components of a business plan?",
  "How do you conduct a SWOT analysis?",
  "Describe effective team management strategies.",
  "What is the importance of customer service?",
  "How do you handle difficult conversations at work?",
  "Explain the agile methodology in project management.",
  "What are KPIs and why are they important?",
  "How do you build a strong company culture?"
]
```

## Science & Education Questions

```json
[
  "Explain photosynthesis in simple terms.",
  "How does the human immune system work?",
  "What causes climate change?",
  "Describe the theory of evolution.",
  "How do vaccines work?",
  "What is the periodic table?",
  "Explain Einstein's theory of relativity simply.",
  "How does DNA replication occur?",
  "What are renewable energy sources?",
  "Describe the water cycle."
]
```

## Tips for Creating Effective Test Questions

1. **Be Specific**: Clear, unambiguous questions get better responses
2. **Vary Complexity**: Mix easy, medium, and hard questions
3. **Different Types**: Include factual, creative, and analytical questions
4. **Relevant Context**: Provide necessary background information
5. **Consistent Format**: Keep question structure similar for fair comparison
6. **Avoid Ambiguity**: Questions should have a clear intent
7. **Test Edge Cases**: Include unusual or challenging scenarios
8. **Domain Variety**: Cover different topics to test versatility
9. **Length Variation**: Mix short and long questions
10. **Actionable**: Questions should prompt useful, measurable responses

## System Prompt Suggestions

### For Technical Questions
```
You are a knowledgeable technical expert with years of experience in software development, computer science, and technology. Provide clear, accurate, and well-structured explanations with examples when appropriate.
```

### For Creative Writing
```
You are a creative writing assistant with excellent storytelling abilities. Generate engaging, imaginative, and well-crafted content that captures the reader's attention.
```

### For Educational Content
```
You are an experienced educator who excels at explaining complex topics in simple, understandable terms. Use analogies and examples to make concepts clear.
```

### For Business Advice
```
You are a seasoned business consultant with expertise in strategy, management, and operations. Provide practical, actionable advice based on best practices.
```

### For Coding Help
```
You are an expert programmer proficient in multiple programming languages. Provide clean, efficient, and well-commented code with explanations.
```

## Usage Example

1. Create a file with your questions (any format above)
2. Upload it using the "Upload File" button
3. Select a question from the dropdown
4. Enter an appropriate system prompt
5. Select 1-3 models to test
6. Run the test and compare responses
7. Download results for further analysis

---

Use these samples as templates to create your own question sets for testing different prompts and models!
