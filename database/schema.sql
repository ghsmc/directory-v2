-- Yale Network Search Database Schema

-- People table
CREATE TABLE IF NOT EXISTS people (
    uuid_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    location VARCHAR(255),
    headline VARCHAR(500),
    summary TEXT,
    profile_url VARCHAR(500),
    linkedin_url VARCHAR(500),
    twitter_handle VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employment/Experience table
CREATE TABLE IF NOT EXISTS experience (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    company VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    date_from DATE,
    date_to DATE,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Education table
CREATE TABLE IF NOT EXISTS education (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    institution VARCHAR(255),
    degree VARCHAR(255),
    field_of_study VARCHAR(255),
    title TEXT, -- Full education title for searching
    date_from DATE,
    date_to DATE,
    gpa DECIMAL(3,2),
    activities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    skill_name VARCHAR(100),
    endorsement_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Connections table (for network relationships)
CREATE TABLE IF NOT EXISTS connections (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    connected_person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    connection_type VARCHAR(50), -- 'direct', 'second_degree', 'group_member'
    connection_source VARCHAR(50), -- 'linkedin', 'twitter', 'email', 'yale_directory'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(person_uuid, connected_person_uuid)
);

-- Yale-specific affiliations
CREATE TABLE IF NOT EXISTS yale_affiliations (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    affiliation_type VARCHAR(100), -- 'undergraduate', 'graduate', 'faculty', 'staff', 'alumni'
    school VARCHAR(255), -- 'Yale College', 'Yale Law School', 'Yale SOM', etc.
    class_year INT,
    residential_college VARCHAR(100),
    major VARCHAR(255),
    sports_teams TEXT,
    clubs_organizations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search history for learning
CREATE TABLE IF NOT EXISTS search_queries (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    query_text TEXT,
    parsed_filters JSONB,
    sql_query TEXT,
    result_count INT,
    clicked_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profile embeddings for semantic search
CREATE TABLE IF NOT EXISTS profile_embeddings (
    id SERIAL PRIMARY KEY,
    person_uuid UUID REFERENCES people(uuid_id) ON DELETE CASCADE,
    embedding_text TEXT, -- Concatenated profile text
    embedding vector(1536), -- OpenAI embeddings dimension
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(person_uuid)
);

-- Indexes for performance
CREATE INDEX idx_people_name ON people(full_name);
CREATE INDEX idx_people_location ON people(location);
CREATE INDEX idx_experience_title ON experience(title);
CREATE INDEX idx_experience_company ON experience(company);
CREATE INDEX idx_experience_current ON experience(is_current);
CREATE INDEX idx_education_institution ON education(institution);
CREATE INDEX idx_education_yale ON education(institution) WHERE institution LIKE '%Yale%';
CREATE INDEX idx_connections_person ON connections(person_uuid);
CREATE INDEX idx_connections_connected ON connections(connected_person_uuid);
CREATE INDEX idx_yale_affiliations_person ON yale_affiliations(person_uuid);
CREATE INDEX idx_profile_embeddings_vector ON profile_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Full text search indexes
CREATE INDEX idx_people_fulltext ON people USING gin(to_tsvector('english', 
    coalesce(full_name, '') || ' ' || 
    coalesce(headline, '') || ' ' || 
    coalesce(summary, '')
));

CREATE INDEX idx_experience_fulltext ON experience USING gin(to_tsvector('english',
    coalesce(title, '') || ' ' || 
    coalesce(company, '') || ' ' || 
    coalesce(description, '')
));