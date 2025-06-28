# Scholar Map CLI 🧠

**AI-Powered Research Assistant using MindsDB Knowledge Bases with Multi-Step AI Workflow**

ScholarMind is a command-line interface that transforms how researchers discover and explore academic papers. Instead of traditional keyword searches, use natural language queries to find contextually relevant research papers through semantic search powered by MindsDB. The system now includes a multi-step AI workflow that automatically generates summaries for research papers using AI tables.

## 🚀 New Features: Multi-Step AI Workflow

### 🤖 AI-Powered Paper Summarization
- **Automatic Summary Generation**: When papers are inserted, the system automatically generates AI-powered summaries using GPT-4
- **AI Table Integration**: Uses MindsDB AI tables to create intelligent summaries from paper abstracts
- **Enhanced Search Results**: View AI-generated summaries alongside search results
- **Standalone Summary Generation**: Generate summaries for papers without inserting them into the knowledge base

### 🔗 Multi-Step Workflow
1. **Knowledge Base Creation**: Sets up research papers knowledge base with semantic search
2. **AI Table Setup**: Creates `paper_summarizer_model` for automatic summarization
3. **Paper Insertion**: Automatically generates summaries during insertion
4. **Enhanced Search**: Displays summaries in search results with summary indicators
5. **Summary Viewing**: Dedicated interface to view detailed paper information with AI summaries

## How to run

1. Install `uv` package manager by following the instructions [here](https://docs.astral.sh/uv/getting-started/installation/)

2. Make sure you have docker installed and running. For more information, see [here](https://docs.docker.com/get-docker/)

3. Self-host mindsdb by running:
    ```bash
    docker run --name mindsdb_container \
    -p 47334:47334 -p 47335:47335 mindsdb/mindsdb
    ```

4. Install the dependencies by running:
    ```bash
    uv sync
    ```

5. Make sure to set the `OPENAI_API_KEY` environment variable. For more information, see [here](https://platform.openai.com/docs/api-reference/introduction)

6. Run the app by running:
    ```bash
    uv run main.py
    ```

## Usage

### Main Menu Options
- **`i` or `insert`**: Add new research papers with automatic AI summary generation
- **`s` or `search`**: Search papers using semantic queries
- **`a` or `ai`**: Access AI features (view summaries, generate summaries)
- **`d` or `demo`**: Load sample papers with AI-generated summaries
- **`j` or `job`**: Manage periodic paper insertion jobs
- **`q` or `quit`**: Exit the application

### AI Features Menu
- **`s` or `summary`**: View AI-generated summaries for specific papers
- **`g` or `generate`**: Generate AI summaries for papers without inserting them
- **`b` or `back`**: Return to main menu

### Enhanced Search Results
Search results now include a summary indicator column:
- **📝**: Paper has an AI-generated summary
- **❌**: No summary available

### Sample Data with AI Summaries
To start off, you can insert some sample papers by using the `d` or `demo` command. It will include sample papers with AI-generated summaries like:

```bash
╭─────────────────────────────────────────────────────────────────────────────────── Sample Paper 1 ───────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                      │
│  Title: Attention Is All You Need: A Comprehensive Study of Transformer Architecture                                                                                                 │
│  Authors: Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kai...                                                                                        │
│  Category: cs.LG                                                                                                                                                                     │
│  Research Field: Natural Language Processing                                                                                                                                         │
│  Citations: 45,230                                                                                                                                                                   │
│  Abstract: The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The b...                 │
│  🤖 AI Summary: This paper introduces the Transformer architecture, which uses attention mechanisms instead of recurrence or convolutions for sequence transduction. The model achieves superior performance on machine translation tasks while being more parallelizable and faster to train than previous approaches. │
│                                                                                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Enhanced Search Results with Summary Indicators
```bash
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Relevance  ┃ Title                                    ┃ Authors                   ┃ Field                ┃ Category   ┃ Summary  ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 0.810      │ Attention Is All You Need: A Comprehe... │ Vaswani, A., Shazeer, ... │ Natural Language ... │ cs.LG      │ 📝       │
│ 0.536      │ BERT: Pre-training of Deep Bidirectio... │ Devlin, J., Chang, M.W... │ Natural Language ... │ cs.CL      │ 📝       │
│ 0.434      │ ResNet: Deep Residual Learning for Im... │ He, K., Zhang, X., Ren... │ Computer Vision      │ cs.CV      │ 📝       │
└────────────┴──────────────────────────────────────────┴───────────────────────────┴──────────────────────┴────────────┴──────────┘
```

## Testing the AI Workflow

Run the test script to verify the AI workflow functionality:

```bash
uv run test_ai_workflow.py
```

This will test:
- AI table creation for summarization
- Automatic summary generation during paper insertion
- Enhanced search results with summary indicators
- Summary viewing functionality

## Technical Implementation

### AI Table Creation
The system creates a MindsDB AI table for summarization:

```sql
CREATE MODEL paper_summarizer_model
PREDICT summary
USING
    engine = 'openai_engine',
    model_name = 'gpt-4o',
    api_key = 'your_openai_api_key',
    prompt_template = 'Generate a concise summary of the following research paper abstract. Focus on the key contributions, methodology, and findings. Keep the summary under 200 words and make it accessible to researchers in the field.

    Abstract: {{abstract}}
    Title: {{title}}
    Authors: {{authors}}
    Research Field: {{research_field}}
    
    Summary:';
```

### Multi-Step Workflow Process
1. **Setup Phase**: Creates knowledge base and AI table simultaneously
2. **Insertion Phase**: Generates summaries using AI table before inserting papers
3. **Storage Phase**: Stores papers with summaries in the knowledge base
4. **Retrieval Phase**: Displays summaries in search results and dedicated views

## Checklist

### 🛠️ Build an app with KBs

1. Your app executes `CREATE KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L78) ✅
2.  Your app ingests data using `INSERT INTO knowledge_base` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L161) ✅
3. Your app retrieves relevant data based on on semantic queries `SELECT` ... `FROM` ... `WHERE` `content` `LIKE` `<query>` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L253) ✅
4. Your app uses `CREATE INDEX ON KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L116) ✅

### 🛠️ Use metadata columns

1. Define `metadata_columns` during ingestion and use WHERE clauses that combine semantic search with SQL attribute filtering on `metadata_columns` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L90) ✅

### 🛠️ Integrate JOBS

Set up a 🔗 MindsDB JOB that periodically checks a data source and inserts new data into the KB (using LAST or similar logic) - [here](https://github.com/ChiragAgg5k/scholar-map/blob/2631f1818607633c780c4b8b734bc26c4b37d979/src/job_manager.py#L36) ✅

### Upload a video and write a nice README

1. You upload a short video demo explaining the app & showcasing the KB interaction - [here](https://www.youtube.com/watch?v=4ZksrrIPWp4) ✅
2. Your project has a README.md with clear setup instructions. - (done) ✅

### Document the process and showcase your app

DevTo article - [here](https://dev.to/chiragagg5k/creating-knowledge-bases-using-mindsdb-1a33) ✅

### Give feedback and suggest features

Submitted the feedback form ✅

### 🛠️ Integreate CREATE Agent

Projects that integrate CREATE Agent will be rewarded with an additional 10 points. - [here](https://github.com/ChiragAgg5k/scholar-map/blob/2631f1818607633c780c4b8b734bc26c4b37d979/src/mindsdb_manager.py#L241) ✅

### 🛠️ Evaluate the relevancy and accuracy of the documents returned by KB

Use EVALUATE KNOWLEDGE_BASE to evaluate the relevancy and accuracy of the documents and data returned by the knowledge base. - [here](https://github.com/ChiragAgg5k/scholar-map/blob/2631f1818607633c780c4b8b734bc26c4b37d979/src/mindsdb_manager.py#L756) ✅

### Bug-hunt & stress-testing

Stess-Testing report can be found in this [google doc](https://docs.google.com/document/d/1eNg6RNxV-PNjDIxybGkUDtmlBq7Uk1hJ2HK6-heTeHY/edit?usp=sharing).