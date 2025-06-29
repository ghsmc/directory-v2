# Yale Network Search

A powerful AI-powered people search platform for the Yale community, inspired by happenstance.ai.

## Features

- **Natural Language Search**: Search for people using queries like "VC investors from NYC who went to Yale"
- **Smart Query Parsing**: Automatically extracts filters for location, education, companies, titles, and more
- **SQL Generation**: Converts natural language to optimized SQL queries
- **Semantic Search**: Uses embeddings for finding similar profiles
- **Yale-Specific Features**: Special handling for Yale affiliations, schools, and class years

## Architecture

```
yale-network-search/
├── backend/
│   ├── app/
│   │   ├── models.py           # Database models
│   │   ├── main.py            # FastAPI application
│   │   ├── search/
│   │   │   ├── query_parser.py    # Natural language parsing
│   │   │   ├── sql_generator.py   # SQL query generation
│   │   │   └── search_engine.py   # Main search logic
│   │   └── data_loader/
│   │       └── s3_loader.py       # S3 data import
│   └── requirements.txt
├── database/
│   └── schema.sql             # PostgreSQL schema
└── frontend/                  # (Future React app)
```

## Setup

1. **Install PostgreSQL with pgvector extension**:
   ```bash
   # macOS
   brew install postgresql
   brew install pgvector
   
   # Ubuntu
   sudo apt install postgresql postgresql-contrib
   # Install pgvector from source
   ```

2. **Create database**:
   ```bash
   createdb yale_network
   psql yale_network -c "CREATE EXTENSION IF NOT EXISTS vector"
   ```

3. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run database migrations**:
   ```bash
   psql yale_network < database/schema.sql
   ```

## Usage

1. **Test S3 connection**:
   ```bash
   python backend/test_s3_connection.py
   ```

2. **Start the API server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. **Import data from S3**:
   ```bash
   curl -X POST http://localhost:8000/api/import-data
   ```

4. **Search for people**:
   ```bash
   curl -X POST http://localhost:8000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "VC investors from NYC who went to Yale"}'
   ```

## API Endpoints

- `POST /api/search` - Search for people
- `POST /api/import-data` - Import data from S3
- `POST /api/update-embeddings` - Update profile embeddings
- `GET /api/health` - Health check

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost/yale_network
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-2
```

## Example Searches

- "NYC VC Yale investors looking for education startups"
- "Yale SOM alumni working at Goldman Sachs"
- "Computer science graduates from Yale College class of 2015-2020"
- "Yale entrepreneurs in the sustainability space"

## Security Notes

- Never commit `.env` files with real credentials
- Use IAM roles in production instead of access keys
- Implement proper authentication before deploying
- Consider data privacy regulations for personal information