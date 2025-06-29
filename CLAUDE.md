# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Yale Network Search is an AI-powered people search platform for the Yale community, inspired by happenstance.ai. It enables natural language searches like "VC investors from NYC who went to Yale" through intelligent query parsing and SQL generation.

## Architecture

### Core Components
- **Backend API**: FastAPI server with two main entry points:
  - `backend/api_server.py` - Production API with enhanced search
  - `backend/app/main.py` - Base FastAPI application structure
- **Search Engine**: Located in `backend/app/search/`
  - `search_engine.py` - Main search logic and result processing
  - `query_parser.py` - Natural language query parsing
  - `sql_generator.py` - SQL query generation from parsed queries
- **Data Layer**: PostgreSQL with pgvector extension for semantic search
- **Enhanced Search**: `backend/enhanced_search.py` - Advanced search with scoring and ranking

### Database Schema
- **people** - Core person profiles
- **experience** - Work history and current positions
- **education** - Educational background
- **yale_affiliations** - Yale-specific data (schools, class years, affiliations)
- **profile_embeddings** - Vector embeddings for semantic search
- Full schema in `database/schema.sql`

## Development Commands

### Setup and Environment
```bash
# Install dependencies
cd backend && pip install -r requirements.txt

# Set up database (requires PostgreSQL with pgvector)
createdb yale_network
psql yale_network -c "CREATE EXTENSION IF NOT EXISTS vector"
psql yale_network < database/schema.sql
```

### Running the Application
```bash
# Primary API server (production-ready with enhanced search)
cd backend && python api_server.py

# Alternative FastAPI app structure
cd backend && uvicorn app.main:app --reload
```

### Testing
```bash
# Test API endpoints
python backend/test_api.py

# Test search functionality
python backend/test_search.py

# Test AWS/S3 connection
python backend/test_s3_connection.py

# Test data import
python backend/test_real_data.py
```

### Data Import
```bash
# Quick sample import
python backend/quick_import.py

# Full S3 data import (3.2GB dataset)
python backend/full_import.py

# Import real data
python backend/import_real_data.py
```

## API Endpoints

### Primary API Server (`api_server.py`)
- `GET /` - API information and available endpoints
- `POST /search` - Enhanced search with detailed results
- `GET /search?q=query` - URL-friendly search endpoint
- `GET /stats` - Database statistics and metrics
- `GET /health` - Health check with database connection test
- `GET /examples` - Example queries and search tips

### Base API (`app/main.py`)
- `POST /api/search` - Basic search functionality
- `POST /api/import-data` - Import data from S3
- `POST /api/update-embeddings` - Update profile embeddings
- `GET /api/health` - Health check

## Environment Variables

Required in `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost/yale_network
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-2
```

## Key Features

### Natural Language Query Processing
The system parses queries to extract:
- **Locations**: NYC, San Francisco, Connecticut, etc.
- **Roles**: VC, founder, professor, doctor, etc.
- **Industries**: tech, finance, healthcare, education, etc.
- **Yale specifics**: Schools (SOM, Law School), class years, affiliations

### Search Capabilities
- **Enhanced search** with relevance scoring and match reasons
- **Semantic search** using OpenAI embeddings
- **SQL generation** from natural language queries
- **Yale-specific filtering** for schools and affiliations

### Data Import Pipeline
- Streams large S3 datasets efficiently
- Parses LinkedIn/BrightData format
- Filters for Yale affiliations only
- Batch processing for performance

## Development Notes

- Use `enhanced_search.py` for the most advanced search capabilities
- The system supports both structured SQL search and semantic vector search
- Profile embeddings are generated using OpenAI's text-embedding-ada-002 model
- All Yale-specific data is stored in the `yale_affiliations` table
- The database uses full-text search indexes for performance