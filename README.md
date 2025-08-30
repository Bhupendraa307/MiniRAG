# Mini RAG - Retrieval-Augmented Generation App

A full-stack RAG (Retrieval-Augmented Generation) application with Python FastAPI backend and React frontend, featuring vector search, reranking, and LLM-powered question answering with inline citations.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Vector Database│
│   (Tailwind CSS)│◄──►│     (Python)     │◄──►│   (Pinecone)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    MongoDB      │
                       │   (Metadata)    │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  External APIs  │
                       │ OpenAI, Cohere  │
                       │     Groq        │
                       └─────────────────┘
```

## 🚀 Features

### Backend (FastAPI)
- **Document Upload**: Accept files/text, chunk into 800-1200 tokens with 10-15% overlap
- **Vector Storage**: Generate embeddings and store in Pinecone with metadata in MongoDB
- **Smart Retrieval**: MMR (Maximal Marginal Relevance) for diverse results
- **Reranking**: Cohere Rerank for improved relevance
- **LLM Integration**: Generate answers with inline citations using OpenAI/Groq
- **Performance Metrics**: Token usage and latency tracking
- **Error Handling**: Graceful error handling and structured logging

### Frontend (React + Tailwind)
- **File Upload**: Drag-and-drop file upload or text input
- **Query Interface**: Clean search interface with real-time results
- **Citation Display**: Expandable source snippets with inline citations
- **Performance Stats**: Display latency and token usage
- **Dark/Light Mode**: Theme toggle with system preference detection
- **Responsive Design**: Mobile-friendly interface

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- API Keys for:
  - OpenAI (embeddings & LLM)
  - Cohere (reranking)
  - Pinecone (vector database)
  - MongoDB Atlas (metadata storage)
  - Groq (optional LLM alternative)

## 🛠️ Local Setup

### Backend Setup

1. **Clone and navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Environment configuration**:
   ```bash
   cp .env.example .env
   # Set REACT_APP_API_URL=http://localhost:8000/api
   ```

4. **Start development server**:
   ```bash
   npm start
   ```

   Frontend will be available at `http://localhost:3000`

## 🌐 Production Deployment

### Backend (Render/Railway/Fly.io)

1. **Render**: Use `render.yaml` configuration
2. **Railway**: Connect GitHub repo and set environment variables
3. **Fly.io**: Use provided Dockerfile

### Frontend (Vercel/Netlify)

1. **Vercel**: Connect GitHub repo, set build command: `npm run build`
2. **Netlify**: Same as Vercel, ensure `REACT_APP_API_URL` points to production backend

## 📊 Goldset Q/A Examples

### Example 1: Technical Documentation
**Question**: "What are the main components of the RAG pipeline?"
**Expected Answer**: "The RAG pipeline consists of three main components: [1] document processing and chunking, [2] vector storage and retrieval using embeddings, and [3] answer generation with LLM integration [1][2]."

### Example 2: API Usage
**Question**: "How do I upload a document to the system?"
**Expected Answer**: "You can upload documents using the POST /upload endpoint by either sending a file or text content [1]. The system will automatically chunk the content and store it in the vector database [2]."

### Example 3: Performance Metrics
**Question**: "What performance metrics are tracked?"
**Expected Answer**: "The system tracks token usage (prompt, completion, and total tokens) and response latency for each query [1]. These metrics are displayed in the frontend interface [2]."

### Example 4: Error Handling
**Question**: "How does the system handle errors?"
**Expected Answer**: "The system implements graceful error handling with structured logging [1]. API errors are caught and returned with appropriate HTTP status codes and error messages [2]."

### Example 5: Reranking Process
**Question**: "What is the purpose of reranking in the pipeline?"
**Expected Answer**: "Reranking uses Cohere's rerank model to improve the relevance of retrieved documents [1]. It takes the top-k results from vector search and reorders them based on semantic relevance to the query [2]."

## 📈 Performance Notes

### Precision/Recall
- **Precision**: Enhanced by Cohere reranking (typically 15-25% improvement)
- **Recall**: MMR retrieval ensures diverse results while maintaining relevance
- **Latency**: Average response time 2-4 seconds depending on document corpus size

### Optimization Strategies
- Chunk size optimization (800-1200 tokens with 150 token overlap)
- Top-k retrieval tuning (default: 10 candidates, rerank top 5)
- Embedding model selection (text-embedding-ada-002 for balance of speed/quality)

## 🔗 Resume & Contact

**Developer**: [Your Name]
**Resume**: [Your Resume Link]
**GitHub**: [Your GitHub Profile]
**LinkedIn**: [Your LinkedIn Profile]

## ⚠️ Limitations & Next Steps

### Current Limitations
- Text-only document support (TXT, MD files)
- Single-language support (English)
- No user authentication/authorization
- Limited file size handling
- Basic error recovery

### Planned Improvements
1. **Hybrid Search**: Combine vector search with keyword search (BM25)
2. **Caching Layer**: Redis for frequently accessed queries
3. **Reranker Fine-tuning**: Domain-specific reranker training
4. **Multi-modal Support**: PDF, DOCX, image text extraction
5. **User Management**: Authentication and document isolation
6. **Advanced Analytics**: Query analytics and performance monitoring
7. **Streaming Responses**: Real-time answer generation
8. **Multi-language Support**: Internationalization

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Live Demo**: [Frontend URL] | **API Docs**: [Backend URL]/docs"# MiniRAG" 
