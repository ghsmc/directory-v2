# Yale Network Search - Backend

AI-powered search engine for Yale people with natural language processing and AI-enhanced profiles.

## 🚀 Current Status

- ✅ **14,412 Yale profiles** imported and searchable
- ✅ **AI enhancement system** for generating summaries and tags
- ✅ **Natural language search** with relevance scoring
- ✅ **Optimized SQL** with full-text search indexes
- ✅ **FastAPI server** with comprehensive endpoints

## 📁 Key Files

### Core Components
- `ai_enhanced_api_server.py` - Main API server with AI features
- `search_api.py` - Advanced search engine with natural language processing
- `batch_ai_enhancement.py` - AI enhancement for all profiles
- `clean_full_import.py` - Data import from S3 (3GB dataset)

### Database Setup
- `add_ai_columns.sql` - Database schema for AI features
- `setup_search_indexes.py` - Performance optimization indexes
- `create_missing_indexes.py` - Additional search indexes

### Legacy/Alternative
- `api_server.py` - Original API server (uses different search engine)
- `ai_profile_enhancer.py` - Individual profile AI enhancement
- `app/` - Alternative FastAPI structure

## 🔧 Usage

### Start the AI-Enhanced API Server
```bash
python ai_enhanced_api_server.py
```
Server runs at: http://localhost:8000

### API Endpoints

**Search:**
- `GET /search?q=data science students` - URL search
- `POST /search` - JSON search with advanced options

**Management:**
- `GET /health` - Health check with AI enhancement progress
- `GET /stats` - Database statistics and AI tag analysis
- `GET /examples` - Example queries and usage tips
- `POST /enhance-batch` - Trigger AI enhancement for profiles

### Example Searches

**Natural Language:**
- "students studying artificial intelligence at Yale"
- "people with data science experience"
- "Yale School of Medicine researchers"

**Simple Terms:**
- "computer science"
- "medicine"
- "research fellows"

## 🤖 AI Features

### AI-Generated Summaries
- Engaging one-sentence descriptions
- Professional focus and achievements
- Generated using GPT-4o-mini (~$1.50 for 50K profiles)

### AI-Generated Tags
- Categorizes profiles (Student, Faculty, Research, etc.)
- Field-specific tags (Data Science, Medicine, Law, etc.)
- Yale school affiliations
- Searchable and filterable

### Enhanced Search
- AI content included in relevance scoring
- Natural language query parsing
- Smart filtering by location, role, school, etc.

## 🗄️ Database Schema

The `people` table includes AI enhancement columns:
- `ai_summary` (TEXT) - AI-generated description
- `ai_tags` (JSONB) - Array of AI-generated tags
- `ai_processed` (BOOLEAN) - Enhancement status
- `ai_processed_at` (TIMESTAMP) - Enhancement date

## 📊 Current Data

- **Total profiles:** 14,412
- **AI enhanced:** 5 (test batch)
- **Remaining:** 14,407
- **Enhancement rate:** ~0.8 profiles/second
- **Estimated cost:** $2.88 for full dataset

## 🧹 Archived Files

Old/experimental files are in `archive/` directory:
- Various search implementations
- Test scripts and samples
- Alternative API servers
- Development prototypes

## 🚀 Next Steps

1. **Run full AI enhancement:**
   ```bash
   python batch_ai_enhancement.py --limit 1000
   ```

2. **Frontend integration:**
   - Connect React frontend to `/search` endpoint
   - Display AI summaries and tags
   - Implement search filters

3. **Performance optimization:**
   - Monitor search performance
   - Add caching if needed
   - Optimize AI enhancement batch size

## 💡 Cost & Performance

- **Search:** Sub-second response times with 14K+ profiles
- **AI Enhancement:** ~$0.0002 per profile (GPT-4o-mini)
- **Full dataset cost:** ~$2.88 for 14,412 profiles
- **Database:** PostgreSQL with GIN indexes for fast full-text search