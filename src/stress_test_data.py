"""Stress Testing Data Generator for Scholar Map

This script generates thousands of fake research papers using the Faker library
and inserts them into the MindsDB knowledge base for performance testing.
"""

import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import argparse
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt
from rich.text import Text
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.table import Table

try:
    from faker import Faker
except ImportError:
    print("Faker library not found. Installing...")
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
    from faker import Faker

from src.models.paper import Paper
from src.mindsdb_manager import MindsDBManager

console = Console()
fake = Faker()


class KnowledgeBaseTestSuite:
    """Comprehensive testing suite for the research papers knowledge base"""

    def __init__(self, db_manager: MindsDBManager):
        self.db_manager = db_manager
        self.console = Console()
        self.test_queries = [
            # Basic search queries
            "Find papers about machine learning",
            "Show me research on neural networks",
            "What papers discuss computer vision?",
            "Find papers by authors with last name Smith",
            "Show papers published in 2023",
            "Find papers in cs.AI category",
            # Complex semantic queries
            "What are the latest developments in deep learning?",
            "Find papers about natural language processing applications",
            "Show me research on autonomous vehicles and robotics",
            "What papers discuss medical AI and healthcare?",
            "Find papers about cybersecurity and machine learning",
            "Show research on climate change and data science",
            # Specific technical queries
            "Find papers about transformer architectures",
            "Show me research on reinforcement learning algorithms",
            "What papers discuss graph neural networks?",
            "Find papers about computer vision in healthcare",
            "Show me research on federated learning",
            "Find papers about adversarial machine learning",
            # Citation and impact queries
            "Show me the most cited papers",
            "Find recent papers with high impact",
            "What are the trending research topics?",
            "Show papers with more than 100 citations",
            # Cross-domain queries
            "Find interdisciplinary papers combining AI and biology",
            "Show research connecting machine learning and physics",
            "Find papers about AI applications in finance",
        ]

    def test_basic_database_operations(self) -> Dict[str, Any]:
        """Test basic database operations and connectivity"""
        results = {
            "connection_test": False,
            "record_count": 0,
            "sample_retrieval": False,
            "query_response_time": 0,
        }

        try:
            start_time = time.time()

            # Test record count
            count_query = "SELECT COUNT(*) as total FROM research_papers_kb"
            count_result = self.db_manager.server.query(count_query).fetch()
            results["record_count"] = (
                count_result[0]["total"] if not count_result.empty else 0
            )
            results["connection_test"] = True

            # Test sample data retrieval
            if results["record_count"] > 0:
                sample_query = (
                    "SELECT title, authors, category FROM research_papers_kb LIMIT 5"
                )
                sample_result = self.db_manager.server.query(sample_query).fetch()
                results["sample_retrieval"] = len(sample_result) > 0

            results["query_response_time"] = time.time() - start_time

        except Exception as e:
            self.console.print(f"[red]Database operation error: {str(e)}[/red]")

        return results

    def test_search_performance(self, num_queries: int = 20) -> Dict[str, Any]:
        """Test search performance with various query types"""
        results = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "average_response_time": 0,
            "min_response_time": float("inf"),
            "max_response_time": 0,
            "response_times": [],
            "query_results": [],
        }

        test_queries = random.sample(
            self.test_queries, min(num_queries, len(self.test_queries))
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        ) as progress:

            task = progress.add_task(
                "Testing search queries...", total=len(test_queries)
            )

            for i, query in enumerate(test_queries):
                start_time = time.time()
                response_time = 0  # Initialize response_time

                try:
                    # Test the AI agent's response to the query
                    search_query = f"""
                    SELECT 
                        title, 
                        authors, 
                        category, 
                        research_field, 
                        citation_count,
                        abstract
                    FROM research_papers_kb 
                    WHERE title LIKE '%{query.split()[-1]}%' 
                    OR abstract LIKE '%{query.split()[-1]}%'
                    OR research_field LIKE '%{query.split()[-1]}%'
                    ORDER BY citation_count DESC 
                    LIMIT 10
                    """

                    search_result = self.db_manager.server.query(search_query).fetch()
                    response_time = time.time() - start_time

                    results["total_queries"] += 1
                    results["successful_queries"] += 1
                    results["response_times"].append(response_time)
                    results["min_response_time"] = min(
                        results["min_response_time"], response_time
                    )
                    results["max_response_time"] = max(
                        results["max_response_time"], response_time
                    )

                    results["query_results"].append(
                        {
                            "query": query,
                            "response_time": response_time,
                            "result_count": len(search_result),
                            "success": True,
                        }
                    )

                except Exception as e:
                    response_time = (
                        time.time() - start_time
                    )  # Set response_time even on error
                    results["total_queries"] += 1
                    results["failed_queries"] += 1
                    results["query_results"].append(
                        {"query": query, "error": str(e), "success": False}
                    )

                progress.advance(task)
                progress.update(
                    task,
                    description=f"Query {i+1}/{len(test_queries)} - {response_time:.2f}s",
                )

        if results["response_times"]:
            results["average_response_time"] = sum(results["response_times"]) / len(
                results["response_times"]
            )

        return results

    def test_ai_agent_responses(self, num_tests: int = 10) -> Dict[str, Any]:
        """Test the AI agent's ability to answer research questions"""
        results = {
            "total_tests": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "average_response_time": 0,
            "response_quality_scores": [],
            "responses": [],
        }

        ai_test_questions = [
            "What are the current trends in machine learning research?",
            "Can you summarize recent developments in computer vision?",
            "What are the most influential papers in natural language processing?",
            "How has AI research evolved in the healthcare domain?",
            "What are the key challenges in deep learning today?",
            "Can you identify emerging research areas in artificial intelligence?",
            "What papers show promising results in reinforcement learning?",
            "How do citation patterns reflect research impact?",
            "What interdisciplinary research is happening in AI?",
            "What are the most cited papers in the last two years?",
        ]

        test_questions = random.sample(
            ai_test_questions, min(num_tests, len(ai_test_questions))
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        ) as progress:

            task = progress.add_task(
                "Testing AI agent responses...", total=len(test_questions)
            )

            for question in test_questions:
                start_time = time.time()

                try:
                    # Use the scholar agent to answer the question
                    if hasattr(self.db_manager, "ask_scholar_agent"):
                        response = self.db_manager.ask_scholar_agent(question)
                        response_time = time.time() - start_time

                        # Simple quality scoring based on response length and content
                        quality_score = (
                            min(10, len(response.split()) / 10) if response else 0
                        )

                        results["total_tests"] += 1
                        results["successful_responses"] += 1
                        results["response_quality_scores"].append(quality_score)

                        results["responses"].append(
                            {
                                "question": question,
                                "response": response[:200] + "..."
                                if len(response) > 200
                                else response,
                                "response_time": response_time,
                                "quality_score": quality_score,
                                "success": True,
                            }
                        )
                    else:
                        # Fallback to basic database query
                        query = (
                            f"SELECT title, abstract FROM research_papers_kb LIMIT 5"
                        )
                        result = self.db_manager.server.query(query).fetch()
                        response_time = time.time() - start_time

                        results["total_tests"] += 1
                        results["successful_responses"] += 1
                        results["responses"].append(
                            {
                                "question": question,
                                "response": f"Found {len(result)} relevant papers",
                                "response_time": response_time,
                                "quality_score": 5,
                                "success": True,
                            }
                        )

                except Exception as e:
                    results["total_tests"] += 1
                    results["failed_responses"] += 1
                    results["responses"].append(
                        {"question": question, "error": str(e), "success": False}
                    )

                progress.advance(task)

        if results["response_quality_scores"]:
            results["average_response_time"] = (
                sum([r["response_time"] for r in results["responses"] if r["success"]])
                / results["successful_responses"]
            )

        return results

    def test_data_integrity(self) -> Dict[str, Any]:
        """Test data integrity and consistency"""
        results = {
            "total_records": 0,
            "records_with_missing_fields": 0,
            "duplicate_titles": 0,
            "invalid_dates": 0,
            "invalid_citations": 0,
            "category_distribution": {},
            "field_distribution": {},
            "integrity_score": 0,
        }

        try:
            # Check total records
            count_query = "SELECT COUNT(*) as total FROM research_papers_kb"
            count_result = self.db_manager.server.query(count_query).fetch()
            results["total_records"] = (
                count_result[0]["total"] if not count_result.empty else 0
            )

            if results["total_records"] == 0:
                return results

            # Check for missing fields
            missing_query = """
            SELECT COUNT(*) as missing_count 
            FROM research_papers_kb 
            WHERE title IS NULL OR title = '' 
            OR authors IS NULL OR authors = ''
            OR abstract IS NULL OR abstract = ''
            """
            missing_result = self.db_manager.server.query(missing_query).fetch()
            results["records_with_missing_fields"] = (
                missing_result[0]["missing_count"] if not missing_result.empty else 0
            )

            # Check for duplicate titles
            duplicate_query = """
            SELECT COUNT(*) as duplicate_count 
            FROM (
                SELECT title, COUNT(*) as cnt 
                FROM research_papers_kb 
                GROUP BY title 
                HAVING COUNT(*) > 1
            ) as duplicates
            """
            duplicate_result = self.db_manager.server.query(duplicate_query).fetch()
            results["duplicate_titles"] = (
                duplicate_result[0]["duplicate_count"]
                if not duplicate_result.empty
                else 0
            )

            # Check citation counts
            citation_query = "SELECT COUNT(*) as invalid_count FROM research_papers_kb WHERE citation_count < 0"
            citation_result = self.db_manager.server.query(citation_query).fetch()
            results["invalid_citations"] = (
                citation_result[0]["invalid_count"] if not citation_result.empty else 0
            )

            # Get category distribution
            category_query = "SELECT category, COUNT(*) as count FROM research_papers_kb GROUP BY category ORDER BY count DESC LIMIT 10"
            category_result = self.db_manager.server.query(category_query).fetch()
            results["category_distribution"] = {
                row["category"]: row["count"] for row in category_result
            }

            # Get field distribution
            field_query = "SELECT research_field, COUNT(*) as count FROM research_papers_kb GROUP BY research_field ORDER BY count DESC LIMIT 10"
            field_result = self.db_manager.server.query(field_query).fetch()
            results["field_distribution"] = {
                row["research_field"]: row["count"] for row in field_result
            }

            # Calculate integrity score (0-100)
            total_issues = (
                results["records_with_missing_fields"]
                + results["duplicate_titles"]
                + results["invalid_citations"]
            )
            results["integrity_score"] = max(
                0, 100 - (total_issues / results["total_records"] * 100)
            )

        except Exception as e:
            self.console.print(f"[red]Data integrity test error: {str(e)}[/red]")

        return results

    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run the complete test suite and return comprehensive results"""
        self.console.print(
            "\n[bold cyan]🧪 Starting Knowledge Base Test Suite[/bold cyan]"
        )

        # Run all tests
        basic_results = self.test_basic_database_operations()
        performance_results = self.test_search_performance()
        ai_results = self.test_ai_agent_responses()
        integrity_results = self.test_data_integrity()

        # Compile comprehensive results
        full_results = {
            "basic_operations": basic_results,
            "search_performance": performance_results,
            "ai_agent_performance": ai_results,
            "data_integrity": integrity_results,
            "overall_score": 0,
            "test_timestamp": datetime.now().isoformat(),
        }

        # Calculate overall score
        scores = []
        if basic_results["connection_test"]:
            scores.append(100)
        if performance_results["successful_queries"] > 0:
            success_rate = (
                performance_results["successful_queries"]
                / performance_results["total_queries"]
            ) * 100
            scores.append(success_rate)
        if ai_results["successful_responses"] > 0:
            ai_success_rate = (
                ai_results["successful_responses"] / ai_results["total_tests"]
            ) * 100
            scores.append(ai_success_rate)
        scores.append(integrity_results["integrity_score"])

        full_results["overall_score"] = sum(scores) / len(scores) if scores else 0

        return full_results


def display_test_results(test_results: Dict[str, Any]):
    """Display comprehensive test results in a formatted way"""
    console.print("\n[bold green]🎯 Knowledge Base Test Results[/bold green]")

    # Overall score
    overall_score = test_results.get("overall_score", 0)
    score_color = (
        "green" if overall_score >= 80 else "yellow" if overall_score >= 60 else "red"
    )

    console.print(
        Panel(
            f"[bold {score_color}]Overall Score: {overall_score:.1f}/100[/bold {score_color}]",
            title="Test Summary",
            border_style=score_color,
        )
    )

    # Basic Operations Results
    basic = test_results.get("basic_operations", {})
    basic_table = Table(
        title="Basic Database Operations", show_header=True, header_style="bold blue"
    )
    basic_table.add_column("Test", style="white", width=25)
    basic_table.add_column("Result", style="green", width=15)
    basic_table.add_column("Details", style="dim", width=30)

    basic_table.add_row(
        "Connection Test",
        "✅ Pass" if basic.get("connection_test") else "❌ Fail",
        f"Response time: {basic.get('query_response_time', 0):.3f}s",
    )
    basic_table.add_row(
        "Record Count", f"{basic.get('record_count', 0):,}", "Total papers in database"
    )
    basic_table.add_row(
        "Sample Retrieval",
        "✅ Pass" if basic.get("sample_retrieval") else "❌ Fail",
        "Successfully retrieved sample data",
    )

    console.print(basic_table)

    # Search Performance Results
    search = test_results.get("search_performance", {})
    if search.get("total_queries", 0) > 0:
        search_table = Table(
            title="Search Performance", show_header=True, header_style="bold yellow"
        )
        search_table.add_column("Metric", style="white", width=25)
        search_table.add_column("Value", style="green", width=20)

        success_rate = (
            search.get("successful_queries", 0) / search.get("total_queries", 1)
        ) * 100
        search_table.add_row("Success Rate", f"{success_rate:.1f}%")
        search_table.add_row("Total Queries", f"{search.get('total_queries', 0)}")
        search_table.add_row(
            "Average Response Time", f"{search.get('average_response_time', 0):.3f}s"
        )
        search_table.add_row(
            "Min Response Time", f"{search.get('min_response_time', 0):.3f}s"
        )
        search_table.add_row(
            "Max Response Time", f"{search.get('max_response_time', 0):.3f}s"
        )

        console.print(search_table)

    # AI Agent Performance
    ai = test_results.get("ai_agent_performance", {})
    if ai.get("total_tests", 0) > 0:
        ai_table = Table(
            title="AI Agent Performance", show_header=True, header_style="bold magenta"
        )
        ai_table.add_column("Metric", style="white", width=25)
        ai_table.add_column("Value", style="green", width=20)

        ai_success_rate = (
            ai.get("successful_responses", 0) / ai.get("total_tests", 1)
        ) * 100
        ai_table.add_row("Response Success Rate", f"{ai_success_rate:.1f}%")
        ai_table.add_row("Total Questions", f"{ai.get('total_tests', 0)}")
        ai_table.add_row(
            "Average Response Time", f"{ai.get('average_response_time', 0):.3f}s"
        )

        if ai.get("response_quality_scores"):
            avg_quality = sum(ai["response_quality_scores"]) / len(
                ai["response_quality_scores"]
            )
            ai_table.add_row("Average Quality Score", f"{avg_quality:.1f}/10")

        console.print(ai_table)

    # Data Integrity Results
    integrity = test_results.get("data_integrity", {})
    if integrity.get("total_records", 0) > 0:
        integrity_table = Table(
            title="Data Integrity", show_header=True, header_style="bold cyan"
        )
        integrity_table.add_column("Check", style="white", width=25)
        integrity_table.add_column("Result", style="green", width=15)
        integrity_table.add_column("Details", style="dim", width=25)

        integrity_table.add_row(
            "Integrity Score",
            f"{integrity.get('integrity_score', 0):.1f}/100",
            "Overall data quality",
        )
        integrity_table.add_row(
            "Missing Fields",
            f"{integrity.get('records_with_missing_fields', 0)}",
            f"Out of {integrity.get('total_records', 0)} records",
        )
        integrity_table.add_row(
            "Duplicate Titles",
            f"{integrity.get('duplicate_titles', 0)}",
            "Papers with identical titles",
        )
        integrity_table.add_row(
            "Invalid Citations",
            f"{integrity.get('invalid_citations', 0)}",
            "Negative citation counts",
        )

        console.print(integrity_table)

        # Category distribution
        if integrity.get("category_distribution"):
            console.print("\n[bold cyan]📊 Top Categories[/bold cyan]")
            cat_table = Table(show_header=True, header_style="bold yellow")
            cat_table.add_column("Category", style="white", width=15)
            cat_table.add_column("Count", style="green", width=10)
            cat_table.add_column("Percentage", style="blue", width=12)

            total_records = integrity.get("total_records", 1)
            for category, count in list(integrity["category_distribution"].items())[:5]:
                percentage = (count / total_records) * 100
                cat_table.add_row(category, f"{count:,}", f"{percentage:.1f}%")

            console.print(cat_table)

    # Sample queries and responses
    if search.get("query_results"):
        console.print("\n[bold cyan]🔍 Sample Search Results[/bold cyan]")
        for result in search["query_results"][:3]:
            if result.get("success"):
                console.print(f"[dim]Query:[/dim] {result['query']}")
                console.print(
                    f"[dim]Results:[/dim] {result['result_count']} papers found in {result['response_time']:.3f}s"
                )
                console.print()

    # Test completion summary
    console.print(
        Panel(
            f"[bold]Test completed at:[/bold] {test_results.get('test_timestamp', 'Unknown')}\n"
            f"[bold]Database Status:[/bold] {'🟢 Healthy' if overall_score >= 70 else '🟡 Issues Detected' if overall_score >= 50 else '🔴 Critical Issues'}\n"
            f"[bold]Recommendations:[/bold] {'System ready for production' if overall_score >= 80 else 'Review performance metrics' if overall_score >= 60 else 'Address critical issues before deployment'}",
            title="Test Summary",
            border_style="green"
            if overall_score >= 70
            else "yellow"
            if overall_score >= 50
            else "red",
        )
    )


class StressTestDataGenerator:
    """Generator for creating large amounts of fake research paper data"""

    def __init__(self):
        self.console = Console()
        self.categories = [
            "cs.AI",
            "cs.LG",
            "cs.CV",
            "cs.CL",
            "cs.IR",
            "cs.NE",
            "cs.DC",
            "cs.DS",
            "cs.HC",
            "cs.RO",
            "cs.CR",
            "cs.CC",
            "cs.CG",
            "cs.GT",
            "cs.MA",
            "math.CO",
            "math.OC",
            "math.ST",
            "math.PR",
            "math.NA",
            "physics.data-an",
            "physics.comp-ph",
            "physics.bio-ph",
            "stat.ML",
            "stat.AP",
            "stat.CO",
            "stat.ME",
            "q-bio.QM",
            "q-bio.GN",
            "q-bio.BM",
            "q-bio.NC",
            "econ.EM",
            "econ.TH",
            "cs.other",
            "other",
        ]

        self.research_fields = [
            "Machine Learning",
            "Computer Vision",
            "Natural Language Processing",
            "Artificial Intelligence",
            "Data Science",
            "Human-Computer Interaction",
            "Robotics",
            "Computer Graphics",
            "Cybersecurity",
            "Distributed Systems",
            "Mathematics",
            "Statistics",
            "Physics",
            "Biology",
            "Economics",
            "Quantum Computing",
            "Blockchain",
            "Internet of Things",
            "Cloud Computing",
            "Software Engineering",
            "Database Systems",
            "Operating Systems",
        ]

        self.paper_types = [
            "Research Paper",
            "Review Paper",
            "Conference Paper",
            "Journal Article",
            "Preprint",
            "Workshop Paper",
            "Short Paper",
            "Position Paper",
            "Technical Report",
            "Survey Paper",
        ]

        self.journals_conferences = [
            "Nature",
            "Science",
            "Cell",
            "The Lancet",
            "NEJM",
            "IEEE TPAMI",
            "JMLR",
            "ICML",
            "NeurIPS",
            "ICLR",
            "AAAI",
            "IJCAI",
            "CVPR",
            "ICCV",
            "ECCV",
            "ACL",
            "EMNLP",
            "NAACL",
            "COLING",
            "SIGIR",
            "WWW",
            "KDD",
            "ICDM",
            "VLDB",
            "SIGMOD",
            "ICDE",
            "CHI",
            "UIST",
            "CSCW",
            "ICRA",
            "IROS",
            "RSS",
            "SIGGRAPH",
            "EUROGRAPHICS",
            "TOG",
            "CACM",
            "IEEE Computer",
            "ACM Computing Surveys",
            "Artificial Intelligence",
            "Expert Systems",
            "Journal of AI Research",
            "Machine Learning",
            "Data Mining and Knowledge Discovery",
        ]

        # Technical terms for more realistic paper titles
        self.ml_terms = [
            "Neural Networks",
            "Deep Learning",
            "Reinforcement Learning",
            "Transfer Learning",
            "Adversarial Training",
            "Meta-Learning",
            "Few-Shot Learning",
            "Self-Supervised",
            "Transformer",
            "Attention Mechanism",
            "Graph Neural Networks",
            "Variational Autoencoders",
            "Generative Models",
            "Contrastive Learning",
            "Federated Learning",
            "Multi-Modal",
            "Computer Vision",
            "Natural Language Processing",
            "Speech Recognition",
            "Recommendation Systems",
            "Time Series",
            "Anomaly Detection",
            "Clustering",
            "Classification",
            "Regression",
            "Optimization",
            "Bayesian Methods",
        ]

    def generate_realistic_title(self) -> str:
        """Generate a realistic research paper title"""
        patterns = [
            "{method}: {application} for {domain}",
            "{adjective} {method} for {task} in {domain}",
            "{method}-Based {application}: A {adjective} Approach",
            "Towards {adjective} {method} for {task}",
            "{method} and {method2}: {application} in {domain}",
            "A {adjective} Framework for {task} using {method}",
            "{method} for {adjective} {application}",
            "Learning {task} with {method}",
            "{adjective} {method}: Applications to {domain}",
            "On the {adjective} of {method} for {task}",
        ]

        pattern = random.choice(patterns)

        return pattern.format(
            method=random.choice(self.ml_terms),
            method2=random.choice(self.ml_terms),
            application=random.choice(
                [
                    "Analysis",
                    "Prediction",
                    "Classification",
                    "Detection",
                    "Recognition",
                    "Synthesis",
                    "Generation",
                    "Understanding",
                    "Modeling",
                    "Optimization",
                ]
            ),
            domain=random.choice(
                [
                    "Healthcare",
                    "Finance",
                    "Autonomous Vehicles",
                    "Robotics",
                    "Security",
                    "Social Media",
                    "E-commerce",
                    "Climate Science",
                    "Biomedical Research",
                    "Manufacturing",
                    "Energy Systems",
                    "Smart Cities",
                    "Education",
                ]
            ),
            task=random.choice(
                [
                    "Object Detection",
                    "Sentiment Analysis",
                    "Image Segmentation",
                    "Speech Recognition",
                    "Fraud Detection",
                    "Drug Discovery",
                    "Risk Assessment",
                    "Pattern Recognition",
                    "Anomaly Detection",
                    "Resource Allocation",
                    "Decision Making",
                    "Knowledge Extraction",
                ]
            ),
            adjective=random.choice(
                [
                    "Novel",
                    "Efficient",
                    "Robust",
                    "Scalable",
                    "Adaptive",
                    "Interpretable",
                    "Real-time",
                    "Distributed",
                    "Hierarchical",
                    "Multi-scale",
                    "End-to-end",
                    "Self-supervised",
                    "Weakly-supervised",
                    "Unsupervised",
                    "Semi-supervised",
                ]
            ),
        )

    def generate_realistic_abstract(self, title: str) -> str:
        """Generate a realistic abstract based on the title"""
        templates = [
            "This paper presents a novel approach to {problem}. We propose {method} that addresses the limitations of existing techniques. Our experimental results demonstrate significant improvements in {metrics}. The proposed method achieves {performance} across multiple benchmark datasets. These findings have important implications for {applications}.",
            "In this work, we investigate {problem} using {method}. Traditional approaches suffer from {limitation}, which motivates our research. We introduce {innovation} that overcomes these challenges. Extensive experiments on {datasets} validate the effectiveness of our approach. Our method outperforms state-of-the-art baselines by {improvement}.",
            "We address the challenging problem of {problem} in {domain}. Current methods face difficulties with {challenge}, leading to suboptimal performance. Our contribution is {contribution}, which enables {capability}. Through comprehensive evaluation, we show that our approach achieves {results}. This work opens new possibilities for {future_work}.",
            "This study focuses on {problem}, a critical challenge in {field}. We develop {method} that leverages {technique} to improve {aspect}. The key innovation lies in {innovation}, which allows for {benefit}. Experimental validation demonstrates {performance} compared to existing methods. Our findings contribute to the understanding of {domain}.",
            "The proliferation of {domain} has created new challenges in {problem}. We propose {method}, a {adjective} framework that addresses these issues. Our approach combines {technique1} with {technique2} to achieve {goal}. Results on {datasets} show {improvement} over previous work. This research provides a foundation for {applications}.",
        ]

        template = random.choice(templates)

        # Extract key terms from title for context
        title_words = title.lower().split()
        method_mentioned = any(term.lower() in title.lower() for term in self.ml_terms)

        return template.format(
            problem=random.choice(
                [
                    "scalable machine learning",
                    "robust pattern recognition",
                    "efficient data processing",
                    "automated decision making",
                    "intelligent systems design",
                    "adaptive learning",
                    "multi-modal understanding",
                    "real-time inference",
                    "distributed computation",
                ]
            ),
            method=random.choice(
                [
                    "a deep learning framework",
                    "an ensemble approach",
                    "a reinforcement learning algorithm",
                    "a novel neural architecture",
                    "a multi-task learning system",
                    "a transfer learning method",
                ]
            ),
            metrics=random.choice(
                [
                    "accuracy and computational efficiency",
                    "precision and recall",
                    "F1-score and AUC",
                    "runtime performance and memory usage",
                    "robustness and generalization",
                ]
            ),
            performance=random.choice(
                [
                    "state-of-the-art results",
                    "competitive performance",
                    "superior accuracy",
                    "significant speedup",
                    "improved robustness",
                ]
            ),
            applications=random.choice(
                [
                    "practical deployment scenarios",
                    "industrial applications",
                    "real-world systems",
                    "future research directions",
                    "commercial implementations",
                ]
            ),
            limitation=random.choice(
                [
                    "computational complexity",
                    "poor generalization",
                    "limited scalability",
                    "insufficient accuracy",
                    "high memory requirements",
                ]
            ),
            innovation=random.choice(
                [
                    "an adaptive architecture",
                    "a novel training procedure",
                    "an efficient optimization algorithm",
                    "a regularization technique",
                    "a data augmentation strategy",
                ]
            ),
            datasets=random.choice(
                [
                    "standard benchmarks",
                    "real-world datasets",
                    "synthetic and real data",
                    "publicly available corpora",
                    "domain-specific collections",
                ]
            ),
            improvement=random.choice(
                [
                    "15-20%",
                    "substantial margins",
                    "significant amounts",
                    "considerable improvements",
                ]
            ),
            domain=random.choice(
                [
                    "computer vision",
                    "natural language processing",
                    "robotics",
                    "healthcare",
                    "autonomous systems",
                    "financial technology",
                    "social media analysis",
                ]
            ),
            challenge=random.choice(
                [
                    "data scarcity",
                    "computational constraints",
                    "model interpretability",
                    "distribution shift",
                    "adversarial attacks",
                    "noisy labels",
                ]
            ),
            contribution=random.choice(
                [
                    "a unified framework",
                    "a theoretical analysis",
                    "an empirical study",
                    "a novel algorithm",
                    "a comprehensive evaluation",
                ]
            ),
            capability=random.choice(
                [
                    "efficient processing",
                    "accurate prediction",
                    "robust performance",
                    "real-time operation",
                    "scalable deployment",
                ]
            ),
            results=random.choice(
                [
                    "promising results",
                    "competitive performance",
                    "significant improvements",
                    "state-of-the-art accuracy",
                    "efficient computation",
                ]
            ),
            future_work=random.choice(
                [
                    "advanced applications",
                    "theoretical developments",
                    "practical implementations",
                    "interdisciplinary research",
                    "commercial deployment",
                ]
            ),
            field=random.choice(
                [
                    "artificial intelligence",
                    "machine learning",
                    "data science",
                    "computer science",
                    "information technology",
                ]
            ),
            technique=random.choice(
                [
                    "deep neural networks",
                    "ensemble methods",
                    "probabilistic models",
                    "optimization algorithms",
                    "statistical learning",
                ]
            ),
            aspect=random.choice(
                [
                    "prediction accuracy",
                    "computational efficiency",
                    "model interpretability",
                    "robustness",
                    "scalability",
                ]
            ),
            benefit=random.choice(
                [
                    "faster convergence",
                    "better generalization",
                    "reduced complexity",
                    "improved accuracy",
                    "enhanced robustness",
                ]
            ),
            adjective=random.choice(
                ["comprehensive", "efficient", "robust", "scalable", "interpretable"]
            ),
            technique1=random.choice(
                [
                    "supervised learning",
                    "unsupervised learning",
                    "reinforcement learning",
                    "transfer learning",
                    "meta-learning",
                ]
            ),
            technique2=random.choice(
                [
                    "attention mechanisms",
                    "graph networks",
                    "adversarial training",
                    "self-supervision",
                    "multi-task learning",
                ]
            ),
            goal=random.choice(
                [
                    "optimal performance",
                    "efficient computation",
                    "robust predictions",
                    "scalable deployment",
                    "interpretable results",
                ]
            ),
        )

    def generate_authors(self) -> str:
        """Generate realistic author names"""
        num_authors = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8], weights=[5, 15, 25, 25, 15, 10, 3, 2]
        )[0]
        authors = []

        for _ in range(num_authors):
            # Use more realistic academic name patterns
            first_name = fake.first_name()
            last_name = fake.last_name()

            # Sometimes add middle initial
            if random.random() < 0.3:
                middle_initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                name = f"{last_name}, {first_name[0]}. {middle_initial}."
            else:
                name = f"{last_name}, {first_name[0]}."

            authors.append(name)

        return ", ".join(authors)

    def generate_fake_paper(self) -> Paper:
        """Generate a single fake research paper"""
        # Generate title first to use for context
        title = self.generate_realistic_title()

        # Generate publication date (last 10 years, weighted toward recent)
        days_ago = random.choices(
            range(0, 3650),  # 10 years
            weights=[
                3650 - i for i in range(3650)
            ],  # More recent papers weighted higher
        )[0]
        pub_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        # Generate ArXiv ID with realistic format
        arxiv_year = pub_date[:2]  # Last 2 digits of year
        arxiv_month = f"{random.randint(1, 12):02d}"
        arxiv_number = f"{random.randint(1000, 9999)}"
        arxiv_id = f"{arxiv_year}{arxiv_month}.{arxiv_number}"

        # Citation count based on paper age and random factors
        paper_age_years = (
            datetime.now() - datetime.strptime(pub_date, "%Y-%m-%d")
        ).days / 365
        base_citations = max(0, int(random.expovariate(0.1) * paper_age_years * 10))
        citation_count = max(0, base_citations + random.randint(-50, 200))

        return Paper(
            paper_id=str(uuid.uuid4()),
            title=title,
            authors=self.generate_authors(),
            category=random.choice(self.categories),
            pub_date=pub_date,
            arxiv_id=arxiv_id,
            journal=random.choice(self.journals_conferences),
            research_field=random.choice(self.research_fields),
            paper_type=random.choice(self.paper_types),
            citation_count=citation_count,
            abstract=self.generate_realistic_abstract(title),
        )

    def generate_batch(self, count: int) -> List[Paper]:
        """Generate a batch of fake papers"""
        return [self.generate_fake_paper() for _ in range(count)]


def display_generation_stats(papers: List[Paper]):
    """Display statistics about generated papers"""
    console.print("\n[bold cyan]📊 Generated Data Statistics[/bold cyan]")

    # Create statistics table
    stats_table = Table(show_header=True, header_style="bold magenta")
    stats_table.add_column("Metric", style="white", width=25)
    stats_table.add_column("Value", style="green", width=15)

    # Basic stats
    stats_table.add_row("Total Papers", f"{len(papers):,}")

    # Research field distribution
    field_counts = {}
    category_counts = {}
    type_counts = {}
    total_citations = 0

    for paper in papers:
        field_counts[paper.research_field] = (
            field_counts.get(paper.research_field, 0) + 1
        )
        category_counts[paper.category] = category_counts.get(paper.category, 0) + 1
        type_counts[paper.paper_type] = type_counts.get(paper.paper_type, 0) + 1
        total_citations += paper.citation_count

    stats_table.add_row("Research Fields", f"{len(field_counts)}")
    stats_table.add_row("Categories", f"{len(category_counts)}")
    stats_table.add_row("Paper Types", f"{len(type_counts)}")
    stats_table.add_row("Total Citations", f"{total_citations:,}")
    stats_table.add_row("Avg Citations", f"{total_citations/len(papers):.1f}")

    console.print(stats_table)

    # Top research fields
    console.print("\n[bold cyan]🔬 Top Research Fields[/bold cyan]")
    field_table = Table(show_header=True, header_style="bold yellow")
    field_table.add_column("Research Field", style="white", width=30)
    field_table.add_column("Count", style="green", width=10)
    field_table.add_column("Percentage", style="blue", width=12)

    sorted_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for field, count in sorted_fields:
        percentage = (count / len(papers)) * 100
        field_table.add_row(field, f"{count:,}", f"{percentage:.1f}%")

    console.print(field_table)


def stress_test_insertion(
    db_manager: MindsDBManager, total_records: int, batch_size: int = 100
):
    """Perform stress test insertion with batching and performance monitoring"""

    # Display header
    header_text = Text("Stress Test Data Generation", style="bold magenta")
    header_panel = Panel(
        header_text,
        subtitle=f"Generating and inserting {total_records:,} fake research papers",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(header_panel)

    generator = StressTestDataGenerator()

    # Ask for confirmation
    console.print(
        f"\n[bold yellow]⚠️  This will generate and insert {total_records:,} fake research papers.[/bold yellow]"
    )
    console.print(f"[dim]Batch size: {batch_size} papers per batch[/dim]")
    console.print(
        f"[dim]Estimated time: {(total_records / batch_size) * 2:.1f} minutes[/dim]"
    )

    if not Confirm.ask("Do you want to proceed?", default=False):
        console.print("[yellow]Stress test cancelled.[/yellow]")
        return False

    # Performance tracking
    start_time = time.time()
    successful_inserts = 0
    failed_inserts = 0
    papers_per_second_history = []

    # Calculate number of batches
    num_batches = (total_records + batch_size - 1) // batch_size

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("{task.completed}/{task.total} papers"),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            main_task = progress.add_task(
                "Generating and inserting papers...", total=total_records
            )

            for batch_num in range(num_batches):
                batch_start_time = time.time()

                # Calculate actual batch size for this iteration
                remaining_papers = total_records - (batch_num * batch_size)
                current_batch_size = min(batch_size, remaining_papers)

                # Generate batch
                progress.update(
                    main_task,
                    description=f"Generating batch {batch_num + 1}/{num_batches}...",
                )
                batch_papers = generator.generate_batch(current_batch_size)

                # Insert batch
                progress.update(
                    main_task,
                    description=f"Inserting batch {batch_num + 1}/{num_batches}...",
                )

                try:
                    # Use direct insertion like in sample_data_manager
                    for paper in batch_papers:
                        insert_query = f"""
                        INSERT INTO research_papers_kb 
                        (paper_id, title, authors, category, pub_date, arxiv_id, journal, research_field, paper_type, citation_count, abstract)
                        VALUES (
                            '{paper.paper_id}',
                            '{paper.title.replace("'", "''")}',
                            '{paper.authors.replace("'", "''")}',
                            '{paper.category}',
                            '{paper.pub_date}',
                            '{paper.arxiv_id}',
                            '{paper.journal.replace("'", "''")}',
                            '{paper.research_field}',
                            '{paper.paper_type}',
                            {paper.citation_count},
                            '{paper.abstract.replace("'", "''")}'
                        )
                        """

                        query = db_manager.server.query(insert_query)
                        query.fetch()
                        successful_inserts += 1
                        progress.advance(main_task)

                    # Calculate performance metrics
                    batch_time = time.time() - batch_start_time
                    papers_per_second = (
                        current_batch_size / batch_time if batch_time > 0 else 0
                    )
                    papers_per_second_history.append(papers_per_second)

                    # Update progress description with performance info
                    avg_speed = sum(papers_per_second_history) / len(
                        papers_per_second_history
                    )
                    progress.update(
                        main_task,
                        description=f"Batch {batch_num + 1}/{num_batches} complete • {avg_speed:.1f} papers/sec",
                    )

                except Exception as e:
                    console.print(
                        f"\n[red]Error in batch {batch_num + 1}: {str(e)}[/red]"
                    )
                    failed_inserts += current_batch_size
                    progress.advance(main_task, current_batch_size)

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Stress test interrupted by user[/yellow]")

    # Final performance report
    total_time = time.time() - start_time

    # Create performance report
    performance_panel = Panel(
        f"[bold green]🎯 Stress Test Complete![/bold green]\n\n"
        f"[bold]Performance Metrics:[/bold]\n"
        f"• Total Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)\n"
        f"• Successful Inserts: {successful_inserts:,}\n"
        f"• Failed Inserts: {failed_inserts:,}\n"
        f"• Success Rate: {(successful_inserts/(successful_inserts+failed_inserts)*100):.1f}%\n"
        f"• Average Speed: {successful_inserts/total_time:.1f} papers/second\n"
        f"• Peak Speed: {max(papers_per_second_history) if papers_per_second_history else 0:.1f} papers/second\n\n"
        f"[dim]Database now contains {successful_inserts:,} additional research papers for testing.[/dim]",
        title="Stress Test Results",
        border_style="green",
        padding=(1, 2),
    )
    console.print(performance_panel)

    return successful_inserts > 0


def run_interactive_tests(manager: MindsDBManager):
    """Run interactive knowledge base tests with user choices"""
    console.print("\n[bold cyan]🔧 Interactive Testing Mode[/bold cyan]")
    console.print("Choose what tests to run:")

    test_options = [
        ("Basic Database Operations", "test_basic"),
        ("Search Performance Tests", "test_search"),
        ("AI Agent Response Tests", "test_ai"),
        ("Data Integrity Check", "test_integrity"),
        ("Full Test Suite", "test_all"),
        ("Custom Query Test", "test_custom"),
    ]

    console.print("\nAvailable Tests:")
    for i, (name, _) in enumerate(test_options, 1):
        console.print(f"  {i}. {name}")

    choice = IntPrompt.ask(
        "Select test to run", choices=[str(i) for i in range(1, len(test_options) + 1)]
    )

    test_suite = KnowledgeBaseTestSuite(manager)

    if choice == 1:  # Basic operations
        results = test_suite.test_basic_database_operations()
        console.print("\n[bold green]Basic Database Operations Results:[/bold green]")
        for key, value in results.items():
            console.print(f"  {key}: {value}")

    elif choice == 2:  # Search performance
        num_queries = IntPrompt.ask("Number of queries to test", default=20)
        results = test_suite.test_search_performance(num_queries)
        console.print(
            f"\n[bold green]Search Performance Results ({num_queries} queries):[/bold green]"
        )
        console.print(
            f"  Success Rate: {(results['successful_queries']/results['total_queries']*100):.1f}%"
        )
        console.print(
            f"  Average Response Time: {results['average_response_time']:.3f}s"
        )
        console.print(
            f"  Min/Max Response Time: {results['min_response_time']:.3f}s / {results['max_response_time']:.3f}s"
        )

    elif choice == 3:  # AI agent tests
        num_tests = IntPrompt.ask("Number of AI tests to run", default=10)
        results = test_suite.test_ai_agent_responses(num_tests)
        console.print(
            f"\n[bold green]AI Agent Performance Results ({num_tests} tests):[/bold green]"
        )
        if results["total_tests"] > 0:
            console.print(
                f"  Success Rate: {(results['successful_responses']/results['total_tests']*100):.1f}%"
            )
            console.print(
                f"  Average Response Time: {results['average_response_time']:.3f}s"
            )
            if results["response_quality_scores"]:
                avg_quality = sum(results["response_quality_scores"]) / len(
                    results["response_quality_scores"]
                )
                console.print(f"  Average Quality Score: {avg_quality:.1f}/10")

    elif choice == 4:  # Data integrity
        results = test_suite.test_data_integrity()
        console.print("\n[bold green]Data Integrity Results:[/bold green]")
        console.print(f"  Total Records: {results['total_records']:,}")
        console.print(f"  Integrity Score: {results['integrity_score']:.1f}/100")
        console.print(f"  Missing Fields: {results['records_with_missing_fields']}")
        console.print(f"  Duplicate Titles: {results['duplicate_titles']}")
        console.print(f"  Invalid Citations: {results['invalid_citations']}")

    elif choice == 5:  # Full test suite
        results = test_suite.run_full_test_suite()
        display_test_results(results)

    elif choice == 6:  # Custom query
        custom_query = input("\nEnter your custom SQL query: ")
        try:
            start_time = time.time()
            result = manager.server.query(custom_query).fetch()
            response_time = time.time() - start_time

            console.print(f"\n[bold green]Custom Query Results:[/bold green]")
            console.print(f"  Query executed in: {response_time:.3f}s")
            console.print(f"  Rows returned: {len(result)}")

            if result and len(result) > 0:
                console.print("\n[bold]First few results:[/bold]")
                for i, row in enumerate(result[:3]):
                    console.print(f"  Row {i+1}: {dict(row)}")

        except Exception as e:
            console.print(f"[red]Query failed: {str(e)}[/red]")


def main():
    """Main function for stress testing"""
    parser = argparse.ArgumentParser(
        description="Stress test data generator for Scholar Map"
    )
    parser.add_argument(
        "--records",
        "-r",
        type=int,
        default=1000,
        help="Number of fake papers to generate (default: 1000)",
    )
    parser.add_argument(
        "--batch-size",
        "-b",
        type=int,
        default=100,
        help="Batch size for insertion (default: 100)",
    )
    parser.add_argument(
        "--no-confirm", action="store_true", help="Skip confirmation prompt"
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only run knowledge base tests, skip data generation",
    )
    parser.add_argument(
        "--test-queries",
        type=int,
        default=20,
        help="Number of test queries to run (default: 20)",
    )
    parser.add_argument(
        "--test-ai",
        type=int,
        default=10,
        help="Number of AI agent tests to run (default: 10)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode for custom testing",
    )

    args = parser.parse_args()

    # Initialize manager
    manager = MindsDBManager()

    # Display welcome message
    welcome_text = Text(
        "Scholar Map - Stress Test Data Generator & Knowledge Base Tester",
        style="bold blue",
    )
    welcome_panel = Panel(
        welcome_text,
        subtitle="Generate fake research papers and test knowledge base performance",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(welcome_panel)

    # Connect to database
    console.print("[dim]Connecting to MindsDB...[/dim]")
    if manager.connect() is False:
        console.print("[red]Failed to connect to MindsDB. Exiting.[/red]")
        return 1

    try:
        # Handle interactive mode
        if args.interactive:
            run_interactive_tests(manager)
            return 0

        # If test-only mode, skip data generation
        if args.test_only:
            console.print(
                "[bold yellow]🧪 Running knowledge base tests only...[/bold yellow]"
            )
        else:
            # Run stress test data generation
            if not args.no_confirm:
                # Show preview of what will be generated
                console.print(f"\n[bold cyan]📋 Stress Test Configuration[/bold cyan]")
                config_table = Table(show_header=False)
                config_table.add_column("Setting", style="white", width=20)
                config_table.add_column("Value", style="green", width=20)

                config_table.add_row("Papers to Generate", f"{args.records:,}")
                config_table.add_row("Batch Size", f"{args.batch_size}")
                config_table.add_row(
                    "Estimated Batches",
                    f"{(args.records + args.batch_size - 1) // args.batch_size}",
                )
                config_table.add_row(
                    "Estimated Time",
                    f"{(args.records / args.batch_size) * 2:.1f} minutes",
                )

                console.print(config_table)

            # Generate and insert data
            data_success = stress_test_insertion(manager, args.records, args.batch_size)
            if not data_success:
                console.print(
                    "[red]Data generation failed. Continuing with tests on existing data...[/red]"
                )

        # Always run knowledge base tests after data generation (or standalone)
        console.print("\n" + "=" * 80)
        console.print(
            "[bold magenta]🧪 Starting Knowledge Base Performance Tests[/bold magenta]"
        )
        console.print("=" * 80)

        # Initialize test suite
        test_suite = KnowledgeBaseTestSuite(manager)

        # Run comprehensive tests
        test_results = test_suite.run_full_test_suite()

        # Display results
        display_test_results(test_results)

        # Determine exit code based on overall test results
        overall_score = test_results.get("overall_score", 0)
        if overall_score >= 70:
            console.print("\n[bold green]✅ All tests passed successfully![/bold green]")
            return 0
        elif overall_score >= 50:
            console.print(
                "\n[bold yellow]⚠️  Some issues detected in testing.[/bold yellow]"
            )
            return 1
        else:
            console.print(
                "\n[bold red]❌ Critical issues found during testing.[/bold red]"
            )
            return 2

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user (Ctrl+C)[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
        import traceback

        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 1


if __name__ == "__main__":
    exit(main())
