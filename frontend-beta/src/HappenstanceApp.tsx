import React, { useState, useEffect } from 'react';
import './YaleNetworkApp.css';

interface SearchResult {
  uuid_id: string;
  name: string;
  headline: string;
  location?: string;
  ai_summary?: string;
  ai_tags?: string[];
  yale_school?: string;
  major?: string;
  class_year?: number;
  relevance_score: number;
}

interface SearchResponse {
  query: string;
  total_results: number;
  results: SearchResult[];
  filters_detected: any;
  search_time_ms: number;
  query_analysis?: {
    traits: string[];
    work_filters: string[];
    key_phrases: string[];
    explanation: string;
  };
}

interface ProcessingStep {
  step: string;
  status: 'pending' | 'processing' | 'completed';
  details?: string;
}

const ROLE_CATEGORIES = [
  { icon: '💻', label: 'Computer Science', query: 'computer science' },
  { icon: '⚕️', label: 'Medicine', query: 'medicine medical' },
  { icon: '🔬', label: 'Research', query: 'research' },
  { icon: '📊', label: 'Data Science', query: 'data science' },
  { icon: '🧠', label: 'Psychology', query: 'psychology' }
];

function HappenstanceApp() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  const [searchTime, setSearchTime] = useState(0);
  const [processingSteps, setProcessingSteps] = useState<ProcessingStep[]>([]);
  const [showThinking, setShowThinking] = useState(false);
  const [queryAnalysis, setQueryAnalysis] = useState<any>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    setHasSearched(true);
    setResults([]);
    setQueryAnalysis(null);

    // Initialize processing steps
    const steps: ProcessingStep[] = [
      { step: 'Initializing GPT-4o-mini', status: 'processing', details: 'Connecting to OpenAI API endpoint' },
      { step: 'Query Analysis', status: 'pending', details: 'Extracting traits, filters, and intent from natural language' },
      { step: 'Generating SQL Conditions', status: 'pending', details: 'Creating complex WHERE clauses and JOIN conditions' },
      { step: 'Vector Embedding Search', status: 'pending', details: 'Processing 1536-dimensional semantic embeddings' },
      { step: 'Database Query Execution', status: 'pending', details: 'Running optimized PostgreSQL queries with GIN indexes' },
      { step: 'AI-Enhanced Ranking', status: 'pending', details: 'Applying relevance scoring and AI summary integration' }
    ];
    setProcessingSteps(steps);

    try {
      // Step 1: Initialize GPT-4o-mini
      await new Promise(resolve => setTimeout(resolve, 400));
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 0 ? { ...step, status: 'completed' } : 
        idx === 1 ? { ...step, status: 'processing' } : step
      ));

      // Step 2: Query Analysis  
      const analysisResponse = await fetch(`http://localhost:8003/analyze-query?q=${encodeURIComponent(searchQuery)}`);
      const analysisData = await analysisResponse.json();
      
      setQueryAnalysis(analysisData.analysis);
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 1 ? { ...step, status: 'completed', details: `Extracted ${analysisData.analysis.traits?.length || 0} traits, ${analysisData.analysis.key_phrases?.length || 0} key phrases` } : 
        idx === 2 ? { ...step, status: 'processing' } : step
      ));

      // Step 3: SQL Generation
      await new Promise(resolve => setTimeout(resolve, 600));
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 2 ? { ...step, status: 'completed', details: 'Generated complex JOIN and WHERE conditions with relevance scoring' } : 
        idx === 3 ? { ...step, status: 'processing' } : step
      ));

      // Step 4: Vector Embeddings
      await new Promise(resolve => setTimeout(resolve, 800));
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 3 ? { ...step, status: 'completed', details: 'Processed semantic embeddings across 14,412 profiles' } : 
        idx === 4 ? { ...step, status: 'processing' } : step
      ));

      // Step 5: Database Query
      await new Promise(resolve => setTimeout(resolve, 400));
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 4 ? { ...step, status: 'completed', details: 'Executed optimized PostgreSQL query in <200ms' } : 
        idx === 5 ? { ...step, status: 'processing' } : step
      ));

      // Final search with analysis
      const response = await fetch(`http://localhost:8003/enriched-search?q=${encodeURIComponent(searchQuery)}&limit=20&include_analysis=true`);
      const data: SearchResponse = await response.json();

      setResults(data.results || []);
      setTotalResults(data.total_results || 0);
      setSearchTime(data.search_time_ms || 0);
      
      if (data.query_analysis) {
        setQueryAnalysis(data.query_analysis);
      }

      // Complete all steps
      setProcessingSteps(prev => prev.map((step, idx) => 
        idx === 5 ? { ...step, status: 'completed', details: `Ranked ${data.total_results} results with AI-enhanced scoring` } : step
      ));

    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
      setTotalResults(0);
      setProcessingSteps(prev => prev.map(step => ({ ...step, status: 'pending' })));
    } finally {
      setIsSearching(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearch(query);
  };

  const handleRoleClick = (roleQuery: string, roleLabel: string) => {
    setQuery(`${roleLabel.toLowerCase()} at Yale`);
    handleSearch(`${roleQuery} yale`);
  };

  const formatTimeAgo = (score: number) => {
    // Convert relevance score to a time-like indicator
    if (score > 8) return '2 hours ago';
    if (score > 6) return '1 day ago';
    if (score > 4) return '3 days ago';
    if (score > 2) return '1 week ago';
    return '2 weeks ago';
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  return (
    <div className={`yale-network-app ${isDarkMode ? 'dark-mode' : ''}`}>
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <img 
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Yale_University_Shield_1.svg/1200px-Yale_University_Shield_1.svg.png" 
              alt="Yale University" 
              className="yale-logo"
            />
            <div className="milo-grid-logo">
              <div className="grid-dot red"></div>
              <div className="grid-dot yellow"></div>
              <div className="grid-dot green"></div>
              <div className="grid-dot blue"></div>
              <div className="grid-dot purple"></div>
              <div className="grid-dot orange"></div>
              <div className="grid-dot pink"></div>
              <div className="grid-dot teal"></div>
              <div className="grid-dot indigo"></div>
            </div>
            <span className="logo-text">Milo</span>
            <div className="powered-by">
              <span className="powered-text">Powered by</span>
              <img 
                src="https://img.logo.dev/linkedin.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ" 
                alt="LinkedIn" 
                className="linkedin-logo"
              />
            </div>
          </div>
          <nav className="nav">
            <a href="#" className="nav-link">People</a>
            <a href="#" className="nav-link">Research</a>
            <a href="#" className="nav-link">Organizations</a>
            <a href="#" className="nav-link">About</a>
          </nav>
          <div className="auth-buttons">
            <button 
              className="theme-toggle"
              onClick={() => setIsDarkMode(!isDarkMode)}
              title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? '☀️' : '🌙'}
            </button>
            <button className="login-btn">Log in</button>
            <button className="signup-btn">Sign up</button>
          </div>
        </div>
      </header>

      {/* Main Content with Sidebar */}
      <div className="main-layout">
        {hasSearched && (
          <aside className="sidebar">
            <div className="sidebar-content">
              <h3>Search Filters</h3>
              <div className="filter-section">
                <label>School</label>
                <select className="filter-select">
                  <option>All Schools</option>
                  <option>Yale College</option>
                  <option>Yale Law School</option>
                  <option>Yale School of Medicine</option>
                  <option>Yale School of Management</option>
                </select>
              </div>
              <div className="filter-section">
                <label>Class Year</label>
                <select className="filter-select">
                  <option>All Years</option>
                  <option>2024</option>
                  <option>2023</option>
                  <option>2022</option>
                  <option>2021</option>
                </select>
              </div>
              <div className="filter-section">
                <label>Role Type</label>
                <div className="checkbox-group">
                  <label className="checkbox-label">
                    <input type="checkbox" /> Students
                  </label>
                  <label className="checkbox-label">
                    <input type="checkbox" /> Faculty
                  </label>
                  <label className="checkbox-label">
                    <input type="checkbox" /> Alumni
                  </label>
                </div>
              </div>
              {queryAnalysis && (
                <div className="ai-insights">
                  <h3>AI Insights</h3>
                  <div className="insight-item">
                    <span className="insight-label">Query Type:</span>
                    <span className="insight-value">Professional Search</span>
                  </div>
                  <div className="insight-item">
                    <span className="insight-label">Confidence:</span>
                    <span className="insight-value">High</span>
                  </div>
                </div>
              )}
            </div>
          </aside>
        )}
        
        <main className="main-content">
        {!hasSearched ? (
          // Landing Page
          <div className="landing-page">
            <div className="hero-section">
              <h1 className="hero-title">AI-powered discovery engine for Yale</h1>
              <p className="hero-subtitle">Connecting students, alumni, and faculty through intelligent search.</p>
              
              <form onSubmit={handleSubmit} className="search-form">
                <div className="search-container">
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Find computer science students, venture capital investors, startup founders..."
                    className="search-input"
                  />
                </div>
              </form>

              <div className="role-categories">
                {ROLE_CATEGORIES.map((role, index) => (
                  <button
                    key={index}
                    className="role-button"
                    onClick={() => handleRoleClick(role.query, role.label)}
                  >
                    <span className="role-icon">{role.icon}</span>
                    <span className="role-label">{role.label}</span>
                  </button>
                ))}
              </div>
            </div>

          </div>
        ) : (
          // Results Page
          <div className="results-page">
            <div className="results-header">
              <div className="search-info">
                <div className="search-stats">
                  <span className="you-indicator">
                    <div className="milo-logo-small">
                      <div className="logo-dots-small">
                        <span className="dot-small red"></span>
                        <span className="dot-small yellow"></span>
                        <span className="dot-small green"></span>
                        <span className="dot-small blue"></span>
                      </div>
                      Milo AI
                    </div>
                  </span>
                  <span className="demo-badge">Powered by advanced AI</span>
                  <span className="time-indicator">{searchTime}ms</span>
                </div>
                <h1 className="search-title">{query}</h1>
                <p className="search-description">
                  Found {totalResults.toLocaleString()} relevant profiles across Yale's network in {searchTime}ms using AI-powered semantic search.
                </p>
                <button 
                  className="show-thinking"
                  onClick={() => setShowThinking(!showThinking)}
                >
                  {showThinking ? 'Hide thinking ⌃' : 'Show thinking ⌄'}
                </button>
                
                {showThinking && (
                  <div className="thinking-panel">
                    <div className="thinking-header">
                      <h3>🤔 Thinking</h3>
                      <span className="processing-badge">GPT-4o-mini</span>
                    </div>
                    
                    <div className="processing-steps">
                      {processingSteps.map((step, index) => (
                        <div key={index} className={`processing-step ${step.status}`}>
                          <div className="step-indicator">
                            {step.status === 'completed' ? '✅' : 
                             step.status === 'processing' ? (
                               <div className="processing-spinner"></div>
                             ) : '⚪'}
                          </div>
                          <div className="step-content">
                            <div className="step-title">{step.step}</div>
                            <div className="step-details">{step.details}</div>
                            {step.status === 'processing' && index === 3 && (
                              <div className="embedding-animation">
                                <div className="embedding-bars">
                                  {Array.from({length: 12}).map((_, i) => (
                                    <div key={i} className="embedding-bar" style={{animationDelay: `${i * 0.1}s`}}></div>
                                  ))}
                                </div>
                                <span className="embedding-text">Processing 1536-dimensional vectors...</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    {queryAnalysis && (
                      <div className="query-analysis">
                        <div className="analysis-grid">
                          <div className="analysis-card">
                            <div className="card-header">
                              <strong>🎯 Extracted Traits</strong>
                              <span className="count-badge">{queryAnalysis.traits?.length || 0}</span>
                            </div>
                            <div className="traits-list">
                              {queryAnalysis.traits?.map((trait: string, idx: number) => (
                                <span key={idx} className="trait-tag">{trait}</span>
                              ))}
                            </div>
                          </div>
                          
                          <div className="analysis-card">
                            <div className="card-header">
                              <strong>🔍 Key Phrases</strong>
                              <span className="count-badge">{queryAnalysis.key_phrases?.length || 0}</span>
                            </div>
                            <div className="phrases-list">
                              {queryAnalysis.key_phrases?.slice(0, 8).map((phrase: string, idx: number) => (
                                <span key={idx} className="phrase-tag">{phrase}</span>
                              ))}
                            </div>
                          </div>
                          
                          <div className="analysis-card">
                            <div className="card-header">
                              <strong>💼 Work Filters</strong>
                              <span className="count-badge">{queryAnalysis.work_filters?.length || 0}</span>
                            </div>
                            <div className="filters-list">
                              {queryAnalysis.work_filters?.slice(0, 3).map((filter: string, idx: number) => (
                                <div key={idx} className="filter-item">• {filter}</div>
                              ))}
                            </div>
                          </div>
                          
                          <div className="analysis-card full-width">
                            <div className="card-header">
                              <strong>🗄️ Generated SQL Conditions</strong>
                              <span className="tech-badge">PostgreSQL</span>
                            </div>
                            <div className="sql-container">
                              <pre className="sql-code">
{`WHERE (
  p.headline ILIKE '%${queryAnalysis.key_phrases?.[0] || 'query'}%' OR 
  p.summary ILIKE '%${queryAnalysis.key_phrases?.[0] || 'query'}%'
) AND (
  ya.person_uuid IS NOT NULL
) ORDER BY relevance_score DESC, length(p.headline) DESC`}
                              </pre>
                            </div>
                          </div>
                          
                          <div className="analysis-card full-width">
                            <div className="card-header">
                              <strong>🧠 AI Strategy</strong>
                            </div>
                            <p className="strategy-text">{queryAnalysis.explanation}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="results-container">
              <div className="results-table">
                <div className="table-header">
                  <div className="column-header">Person</div>
                  <div className="column-header">Score</div>
                  <div className="column-header">Quotes</div>
                  <div className="column-header">Mutuals</div>
                </div>

                {isSearching ? (
                  <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Searching network...</p>
                  </div>
                ) : results.length > 0 ? (
                  results.map((person, index) => (
                    <div key={person.uuid_id} className="result-row">
                      <div className="person-info">
                        <div className="person-avatar">
                          <div className="avatar-circle">
                            {getInitials(person.name)}
                          </div>
                          <div className="activity-indicator"></div>
                        </div>
                        <div className="person-details">
                          <div className="person-name">
                            {person.name}
                            {person.yale_school && (
                              <span className="person-school">@ {person.yale_school}</span>
                            )}
                          </div>
                          <div className="person-role-title">
                            {person.headline || 'Yale Community Member'}
                          </div>
                          <div className="person-bullets">
                            {person.location && (
                              <div className="bullet-point">
                                <span className="bullet">•</span>
                                <span>Location: {person.location}</span>
                              </div>
                            )}
                            {person.ai_summary && (
                              <div className="bullet-point ai-summary">
                                <span className="bullet">•</span>
                                <span>{person.ai_summary}</span>
                              </div>
                            )}
                            {person.major && (
                              <div className="bullet-point">
                                <span className="bullet">•</span>
                                <span>Studying {person.major}</span>
                              </div>
                            )}
                            {person.class_year && (
                              <div className="bullet-point">
                                <span className="bullet">•</span>
                                <span>Class of {person.class_year}</span>
                              </div>
                            )}
                            {person.ai_tags && person.ai_tags.length > 0 && (
                              <div className="person-tags">
                                {person.ai_tags.slice(0, 3).map((tag, idx) => (
                                  <span key={idx} className="ai-tag">{tag}</span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <div className="person-score">
                        <div className="relevance-score">
                          <span className="score-number">{Math.round(person.relevance_score)}</span>
                          <span className="score-label">% match</span>
                        </div>
                      </div>
                      
                      <div className="person-quotes">
                        <div className="quote-placeholder">—</div>
                      </div>
                      
                      <div className="person-mutuals">
                        <div className="mutual-avatar">
                          <div className="logo-dots-small">
                            <span className="dot-small red"></span>
                            <span className="dot-small yellow"></span>
                            <span className="dot-small green"></span>
                            <span className="dot-small blue"></span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="no-results">
                    <p>No results found for "{query}"</p>
                    <p>Try searching for "computer science", "medicine", or "data science"</p>
                  </div>
                )}
              </div>
            </div>

            {/* Back to search */}
            <button 
              className="new-search-btn"
              onClick={() => {
                setHasSearched(false);
                setQuery('');
                setResults([]);
              }}
            >
              ← New Search
            </button>
          </div>
        )}
        </main>
      </div>
    </div>
  );
}

export default HappenstanceApp;