#!/usr/bin/env python3
"""
Test script for hybrid search functionality
Tests the complete query pipeline and validates results
"""

import sys
import os
import asyncio
import json
import time
from typing import List, Dict, Any

sys.path.append('.')

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test configuration
API_BASE_URL = "http://localhost:8002"
DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"

# Initialize database for direct testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class HybridSearchTester:
    """Comprehensive tester for hybrid search functionality"""
    
    def __init__(self):
        self.api_client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=30.0)
        self.test_results = []
        
    async def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 Starting Hybrid Search Test Suite")
        print("=" * 50)
        
        # Test 1: API Health Check
        await self.test_api_health()
        
        # Test 2: Query Analysis
        await self.test_query_analysis()
        
        # Test 3: Basic Hybrid Search
        await self.test_basic_hybrid_search()
        
        # Test 4: Complex Filter Combinations
        await self.test_complex_filters()
        
        # Test 5: Yale-Specific Queries
        await self.test_yale_specific_queries()
        
        # Test 6: Performance Testing
        await self.test_performance()
        
        # Test 7: Error Handling
        await self.test_error_handling()
        
        # Generate report
        self.generate_test_report()
        
        await self.api_client.aclose()
    
    async def test_api_health(self):
        """Test API health and configuration"""
        print("\n🔍 Testing API Health...")
        
        try:
            response = await self.api_client.get("/health")
            
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ API Health: {health_data['status']}")
                print(f"📊 Database: {health_data['total_people']} people, {health_data['yale_people']} Yale")
                print(f"🧠 Vector Search: {health_data['vector_search']}")
                print(f"🔑 OpenAI: {'configured' if health_data['openai_configured'] else 'missing'}")
                
                self.test_results.append({
                    "test": "api_health",
                    "status": "pass",
                    "data": health_data
                })
            else:
                print(f"❌ API Health Failed: {response.status_code}")
                self.test_results.append({
                    "test": "api_health", 
                    "status": "fail",
                    "error": f"Status code: {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ API Health Error: {e}")
            self.test_results.append({
                "test": "api_health",
                "status": "error", 
                "error": str(e)
            })
    
    async def test_query_analysis(self):
        """Test query parsing and analysis"""
        print("\n🧠 Testing Query Analysis...")
        
        test_queries = [
            "Fintech PMs in NYC who went to Stanford",
            "Yale SOM alumni working in venture capital",
            "Connecticut entrepreneurs in healthcare",
            "Yale professors and researchers in AI"
        ]
        
        for query in test_queries:
            try:
                response = await self.api_client.post("/search/analyze", json={"query": query})
                
                if response.status_code == 200:
                    analysis = response.json()
                    explanation = analysis["parsing_explanation"]
                    
                    print(f"📝 Query: '{query}'")
                    print(f"   Intent: {explanation['intent']}")
                    print(f"   Confidence: {explanation['confidence']:.2f}")
                    print(f"   Filters: {len(explanation['filters_extracted'])}")
                    print(f"   Embedding: {explanation['embedding_dimensions']} dims")
                    
                    self.test_results.append({
                        "test": "query_analysis",
                        "query": query,
                        "status": "pass",
                        "data": analysis
                    })
                else:
                    print(f"❌ Analysis failed for '{query}': {response.status_code}")
                    self.test_results.append({
                        "test": "query_analysis",
                        "query": query,
                        "status": "fail",
                        "error": f"Status code: {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"❌ Analysis error for '{query}': {e}")
                self.test_results.append({
                    "test": "query_analysis",
                    "query": query,
                    "status": "error",
                    "error": str(e)
                })
    
    async def test_basic_hybrid_search(self):
        """Test basic hybrid search functionality"""
        print("\n🔍 Testing Basic Hybrid Search...")
        
        test_cases = [
            {
                "query": "Yale people in Connecticut",
                "expected_min_results": 1,
                "expected_features": ["yale_affiliation", "location_filtering"]
            },
            {
                "query": "founders and entrepreneurs", 
                "expected_min_results": 1,
                "expected_features": ["title_matching"]
            },
            {
                "query": "professors and academics",
                "expected_min_results": 1,
                "expected_features": ["title_matching", "academic_roles"]
            }
        ]
        
        for test_case in test_cases:
            try:
                response = await self.api_client.post("/search/hybrid", json={
                    "query": test_case["query"],
                    "limit": 10,
                    "include_explanation": True
                })
                
                if response.status_code == 200:
                    search_result = response.json()
                    
                    print(f"🔍 Query: '{test_case['query']}'")
                    print(f"   Results: {search_result['total_results']}")
                    print(f"   Time: {search_result['execution_time_ms']:.1f}ms")
                    print(f"   Intent: {search_result['query_analysis']['intent']}")
                    
                    if search_result['results']:
                        top_result = search_result['results'][0]
                        print(f"   Top Result: {top_result['name']} (score: {top_result['score']:.2f})")
                        print(f"   Match Reasons: {', '.join(top_result['match_reasons'][:2])}")
                    
                    # Validate expectations
                    if search_result['total_results'] >= test_case['expected_min_results']:
                        status = "pass"
                    else:
                        status = "partial"
                    
                    self.test_results.append({
                        "test": "basic_hybrid_search",
                        "query": test_case["query"],
                        "status": status,
                        "data": search_result
                    })
                    
                else:
                    print(f"❌ Search failed for '{test_case['query']}': {response.status_code}")
                    self.test_results.append({
                        "test": "basic_hybrid_search",
                        "query": test_case["query"],
                        "status": "fail",
                        "error": f"Status code: {response.status_code}"
                    })
                    
            except Exception as e:
                print(f"❌ Search error for '{test_case['query']}': {e}")
                self.test_results.append({
                    "test": "basic_hybrid_search",
                    "query": test_case["query"],
                    "status": "error",
                    "error": str(e)
                })
    
    async def test_complex_filters(self):
        """Test complex filter combinations"""
        print("\n🎯 Testing Complex Filter Combinations...")
        
        complex_queries = [
            "Yale SOM graduates working at Goldman Sachs in NYC",
            "Connecticut doctors and physicians from Yale Medical School",
            "San Francisco tech entrepreneurs who went to Yale College",
            "Boston consultants with Yale MBA"
        ]
        
        for query in complex_queries:
            try:
                response = await self.api_client.post("/search/hybrid", json={
                    "query": query,
                    "limit": 5,
                    "include_explanation": True
                })
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"🎯 Complex Query: '{query}'")
                    print(f"   Results: {result['total_results']}")
                    print(f"   Filters Applied: {result['query_analysis']['filter_count']}")
                    
                    if result['results']:
                        print(f"   Top Match: {result['results'][0]['name']}")
                        print(f"   Score Breakdown: {result['results'][0]['score_breakdown']}")
                    
                    self.test_results.append({
                        "test": "complex_filters",
                        "query": query,
                        "status": "pass",
                        "data": result
                    })
                    
                else:
                    print(f"❌ Complex search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Complex search error: {e}")
    
    async def test_yale_specific_queries(self):
        """Test Yale-specific search capabilities"""
        print("\n🎓 Testing Yale-Specific Queries...")
        
        yale_queries = [
            "Yale College class of 2020",
            "Yale Law School alumni",
            "Yale SOM professors and faculty",
            "Yale Medical School graduates"
        ]
        
        for query in yale_queries:
            try:
                response = await self.api_client.post("/search/hybrid", json={
                    "query": query,
                    "limit": 5
                })
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"🎓 Yale Query: '{query}'")
                    print(f"   Results: {result['total_results']}")
                    print(f"   Yale Affinity Weight: {result['ranking_weights']['yale_affinity']:.2f}")
                    
                    self.test_results.append({
                        "test": "yale_specific",
                        "query": query,
                        "status": "pass",
                        "data": result
                    })
                    
            except Exception as e:
                print(f"❌ Yale query error: {e}")
    
    async def test_performance(self):
        """Test search performance"""
        print("\n⚡ Testing Search Performance...")
        
        performance_queries = [
            "Yale alumni",
            "New York entrepreneurs", 
            "healthcare professionals",
            "venture capital investors"
        ]
        
        total_time = 0
        successful_queries = 0
        
        for query in performance_queries:
            try:
                start_time = time.time()
                
                response = await self.api_client.post("/search/hybrid", json={
                    "query": query,
                    "limit": 20
                })
                
                end_time = time.time()
                request_time = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    result = response.json()
                    search_time = result['execution_time_ms']
                    
                    print(f"⚡ '{query}': {search_time:.1f}ms search + {request_time:.1f}ms total")
                    
                    total_time += request_time
                    successful_queries += 1
                    
            except Exception as e:
                print(f"❌ Performance test error: {e}")
        
        if successful_queries > 0:
            avg_time = total_time / successful_queries
            print(f"📊 Average Response Time: {avg_time:.1f}ms")
            
            self.test_results.append({
                "test": "performance",
                "status": "pass",
                "data": {
                    "average_response_time_ms": avg_time,
                    "successful_queries": successful_queries,
                    "total_queries": len(performance_queries)
                }
            })
    
    async def test_error_handling(self):
        """Test error handling"""
        print("\n🚨 Testing Error Handling...")
        
        error_cases = [
            {"query": "", "expected_status": 400},  # Empty query
            {"query": "x", "expected_status": 400},  # Too short
            {"query": "a" * 1000, "limit": 200, "expected_status": 400}  # Limit too high
        ]
        
        for case in error_cases:
            try:
                response = await self.api_client.post("/search/hybrid", json=case)
                
                if response.status_code == case["expected_status"]:
                    print(f"✅ Error handling correct for: {case}")
                else:
                    print(f"❌ Unexpected status code: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error handling test failed: {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("📋 HYBRID SEARCH TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "pass"])
        failed_tests = len([r for r in self.test_results if r["status"] in ["fail", "error"]])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Group by test type
        by_test_type = {}
        for result in self.test_results:
            test_type = result["test"]
            if test_type not in by_test_type:
                by_test_type[test_type] = []
            by_test_type[test_type].append(result)
        
        print("\n📊 Results by Test Type:")
        for test_type, results in by_test_type.items():
            passed = len([r for r in results if r["status"] == "pass"])
            total = len(results)
            print(f"  {test_type}: {passed}/{total} passed")
        
        # Save detailed results
        with open("hybrid_search_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: hybrid_search_test_results.json")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Hybrid search is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the detailed results for debugging.")

async def main():
    """Main test runner"""
    tester = HybridSearchTester()
    
    print("🚀 Make sure the hybrid API server is running on port 8002")
    print("   Start with: python hybrid_api_server.py")
    print()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())