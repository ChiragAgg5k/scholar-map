# Sample Data for Scholar Map

This document explains how to insert sample research papers into your Scholar Map database for testing and demonstration purposes.

## Overview

The sample data includes 10 high-quality research papers from various fields:
- **Machine Learning & AI**: Transformer architecture, BERT, GANs, GPT-3
- **Computer Vision**: ResNet, YOLO object detection
- **Natural Language Processing**: BERT, GPT-3, Transformer models
- **Information Retrieval**: Neural information retrieval
- **Emerging Fields**: Federated learning, quantum machine learning, explainable AI

## Methods to Insert Sample Data

### Method 1: Through Main Application Menu

1. Run the main application:
   ```bash
   python main.py
   ```

2. From the main menu, select option **2: Insert Sample Papers**

3. Review the preview of sample papers and confirm insertion

### Method 2: Standalone Script

Run the dedicated sample data script:
```bash
python run_sample_data.py
```

This method is useful for:
- Quick database population during development
- Automated testing setups
- Batch processing scenarios

### Method 3: Programmatic Usage

Import and use the sample data manager in your own scripts:

```python
from src.sample_data_manager import insert_sample_papers
from src.mindsdb_manager import MindsDBManager

# Initialize manager
manager = MindsDBManager()
manager.connect()

# Insert sample papers
success = insert_sample_papers(manager)
```

## Sample Papers Included

1. **Attention Is All You Need** - Foundational Transformer paper
2. **BERT** - Bidirectional transformer for language understanding  
3. **Generative Adversarial Networks** - Classic GAN paper
4. **ResNet** - Deep residual learning for image recognition
5. **GPT-3** - Large language model for few-shot learning
6. **YOLO** - Real-time object detection
7. **Neural Information Retrieval** - Survey of neural IR methods
8. **Federated Learning** - Distributed machine learning survey
9. **Quantum Machine Learning** - Intersection of quantum computing and ML
10. **Explainable AI** - Interpretable machine learning methods

## Features

- ✅ **Realistic Data**: All papers are based on actual influential research
- ✅ **Diverse Fields**: Covers multiple AI/ML research areas
- ✅ **Rich Metadata**: Includes authors, citations, categories, abstracts
- ✅ **Preview Mode**: Shows sample data before insertion
- ✅ **User Confirmation**: Asks for permission before inserting
- ✅ **Error Handling**: Graceful failure handling and reporting
- ✅ **Progress Tracking**: Visual progress indicators during insertion

## Prerequisites

Before inserting sample data, ensure:

1. **MindsDB Server is Running**: The database server must be accessible
2. **Environment Setup**: Required environment variables (like OpenAI API key) are configured
3. **Dependencies Installed**: All required Python packages are available

## Troubleshooting

### Connection Issues
- Verify MindsDB server is running on the correct port
- Check network connectivity and firewall settings

### API Key Issues  
- Ensure `OPENAI_API_KEY` is set in your environment or `.env` file
- Verify the API key has sufficient credits/permissions

### Permission Errors
- Check that the database user has write permissions
- Verify knowledge base creation privileges

## Data Persistence

Once inserted, the sample papers will be:
- Stored permanently in your MindsDB knowledge base
- Available for search and analysis operations  
- Indexed for efficient retrieval
- Enriched with embeddings for semantic search

## Cleaning Up

To remove sample data later, you can:
1. Delete specific papers using the MindsDB console
2. Drop and recreate the knowledge base
3. Use SQL DELETE statements with appropriate filters

---

For more information about Scholar Map, see the main project documentation. 