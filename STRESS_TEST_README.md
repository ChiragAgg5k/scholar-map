# Scholar Map - Stress Testing & Knowledge Base Testing

This comprehensive testing suite allows you to generate large amounts of fake research data and thoroughly test the Scholar Map knowledge base performance.

## Features

### 📊 Data Generation
- Generate thousands of realistic fake research papers
- Configurable batch sizes and record counts
- Performance monitoring during insertion
- Rich progress indicators and statistics

### 🧪 Knowledge Base Testing
- **Basic Database Operations**: Connection, record count, sample retrieval tests
- **Search Performance**: Query response times and success rates
- **AI Agent Testing**: Test the Scholar Agent's ability to answer research questions
- **Data Integrity**: Check for missing fields, duplicates, and data quality issues
- **Interactive Testing**: Custom test modes for specific scenarios

### 📈 Performance Metrics
- Query response times (min, max, average)
- Success/failure rates
- Data quality scores
- Citation pattern analysis
- Category and field distribution analysis

## Usage

### Quick Start
```bash
# Generate 1000 papers and run full test suite
python src/stress_test_data.py

# Generate 5000 papers with custom batch size
python src/stress_test_data.py --records 5000 --batch-size 200

# Run tests only (no data generation)
python src/stress_test_data.py --test-only

# Interactive testing mode
python src/stress_test_data.py --interactive
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--records` | `-r` | Number of fake papers to generate | 1000 |
| `--batch-size` | `-b` | Batch size for insertion | 100 |
| `--test-only` | | Skip data generation, run tests only | False |
| `--test-queries` | | Number of search queries to test | 20 |
| `--test-ai` | | Number of AI agent tests to run | 10 |
| `--interactive` | `-i` | Run in interactive testing mode | False |
| `--no-confirm` | | Skip confirmation prompts | False |

### Examples

#### 1. Large Scale Stress Test
```bash
# Generate 10,000 papers and test performance
python src/stress_test_data.py --records 10000 --batch-size 500
```

#### 2. Quick Performance Check
```bash
# Test existing data with 50 queries
python src/stress_test_data.py --test-only --test-queries 50
```

#### 3. AI Agent Evaluation
```bash
# Focus on AI agent testing with 25 questions
python src/stress_test_data.py --test-only --test-ai 25
```

#### 4. Interactive Testing Session
```bash
# Run custom tests interactively
python src/stress_test_data.py --interactive
```

## Test Suite Details

### 🔧 Basic Database Operations
- **Connection Test**: Verifies database connectivity
- **Record Count**: Counts total papers in knowledge base
- **Sample Retrieval**: Tests data retrieval functionality
- **Response Time**: Measures basic query performance

### ⚡ Search Performance Tests
Tests various search patterns:
- Basic keyword searches
- Complex semantic queries
- Technical term searches
- Citation-based queries
- Cross-domain research queries

**Metrics Tracked:**
- Query success rate
- Average response time
- Min/Max response times
- Result relevance

### 🤖 AI Agent Response Tests
Evaluates the Scholar Agent's capabilities:
- Research trend analysis
- Paper summarization
- Technical question answering
- Citation pattern analysis

**Quality Scoring:**
- Response length and coherence
- Technical accuracy
- Relevance to question
- Response time

### 🔍 Data Integrity Checks
- **Missing Fields**: Identifies records with empty required fields
- **Duplicate Detection**: Finds papers with identical titles
- **Data Validation**: Checks for invalid citation counts
- **Distribution Analysis**: Analyzes category and field distributions
- **Integrity Score**: Overall data quality rating (0-100)

## Generated Data Characteristics

### Realistic Paper Properties
- **Titles**: Technical titles using ML/AI terminology
- **Authors**: Academic naming conventions with initials
- **Abstracts**: Context-aware abstracts matching titles
- **Categories**: Standard arXiv categories (cs.AI, cs.LG, etc.)
- **Citations**: Age-weighted citation counts
- **Journals**: Real conference and journal names

### Data Distribution
- Research fields weighted toward popular areas
- Publication dates favor recent papers
- Citation counts follow realistic patterns
- Author counts follow academic collaboration patterns

## Output and Reporting

### Test Results Display
The testing suite provides comprehensive visual reports:

1. **Overall Score**: Aggregate performance rating
2. **Basic Operations Table**: Connection and retrieval metrics
3. **Search Performance Table**: Query timing and success rates
4. **AI Agent Performance**: Response quality and timing
5. **Data Integrity Report**: Quality checks and distributions
6. **Category Distribution**: Top research areas
7. **Sample Query Results**: Example search outcomes

### Performance Benchmarks

| Score Range | Status | Recommendation |
|-------------|--------|----------------|
| 80-100 | 🟢 Healthy | System ready for production |
| 60-79 | 🟡 Issues Detected | Review performance metrics |
| 0-59 | 🔴 Critical Issues | Address issues before deployment |

### Exit Codes
- `0`: All tests passed successfully (score ≥ 70)
- `1`: Some issues detected (score 50-69)
- `2`: Critical issues found (score < 50)

## Interactive Mode

Interactive mode provides a menu-driven interface for custom testing:

1. **Basic Database Operations** - Quick connectivity check
2. **Search Performance Tests** - Configurable query testing
3. **AI Agent Response Tests** - Evaluate AI capabilities
4. **Data Integrity Check** - Comprehensive data validation
5. **Full Test Suite** - Complete testing workflow
6. **Custom Query Test** - Execute custom SQL queries

## Performance Optimization Tips

### For Large Datasets (10,000+ papers)
- Use larger batch sizes (500-1000)
- Run tests during off-peak hours
- Monitor system resources
- Consider database indexing

### For Testing
- Use `--test-only` for repeated testing
- Adjust query counts based on dataset size
- Use interactive mode for focused testing
- Save results for performance tracking

## Troubleshooting

### Common Issues

**Connection Errors:**
- Verify MindsDB server is running
- Check connection credentials
- Ensure knowledge base exists

**Performance Issues:**
- Reduce batch size for memory constraints
- Check database server resources
- Consider network latency

**Test Failures:**
- Verify data exists in knowledge base
- Check SQL query syntax
- Review error messages in traceback

### Debugging

Enable detailed error reporting:
```bash
python src/stress_test_data.py --test-only 2>&1 | tee test_log.txt
```

## Dependencies

Required Python packages:
- `faker` - Fake data generation
- `rich` - Rich terminal formatting
- `mindsdb_sdk` - MindsDB integration

Install dependencies:
```bash
pip install faker rich mindsdb_sdk
```

## Integration with Scholar Map

This testing suite integrates with the Scholar Map system:
- Uses the same `MindsDBManager` class
- Tests the actual knowledge base structure
- Validates the Scholar Agent functionality
- Provides production readiness assessment

## Contributing

To add new test types:
1. Add methods to `KnowledgeBaseTestSuite` class
2. Update `run_interactive_tests()` for menu integration
3. Add command-line options if needed
4. Update this documentation

## License

Part of the Scholar Map project. See main project license. 