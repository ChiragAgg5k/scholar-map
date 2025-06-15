# Scholar Map CLI 🧠

**AI-Powered Research Assistant using MindsDB Knowledge Bases**

ScholarMind is a command-line interface that transforms how researchers discover and explore academic papers. Instead of traditional keyword searches, use natural language queries to find contextually relevant research papers through semantic search powered by MindsDB.

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
    uv run src/main.py
    ```

## Usage

To start off, you can insert some sample papers by using the `d` or `demo` command. It will include some sample papers like:

```bash
╭─────────────────────────────────────────────────────────────────────────────────── Sample Paper 1 ───────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                      │
│  Title: Attention Is All You Need: A Comprehensive Study of Transformer Architecture                                                                                                 │
│  Authors: Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kai...                                                                                        │
│  Category: cs.LG                                                                                                                                                                     │
│  Research Field: Natural Language Processing                                                                                                                                         │
│  Citations: 45,230                                                                                                                                                                   │
│  Abstract: The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The b...                 │
│                                                                                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

After addition, it should look like this:

```bash
╭───────────────────────────────────────────────────────────────────────────────── Operation Complete ─────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                      │
│  Sample Data Inserted Successfully!                                                                                                                                                  │
│                                                                                                                                                                                      │
│  Successfully inserted 10 sample research papers.                                                                                                                                    │
│  These papers span multiple research fields including:                                                                                                                               │
│  • Machine Learning & AI                                                                                                                                                             │
│  • Computer Vision                                                                                                                                                                   │
│  • Natural Language Processing                                                                                                                                                       │
│  • Data Science                                                                                                                                                                      │
│                                                                                                                                                                                      │
│  You can now test search and analysis features with this data.                                                                                                                       │
│                                                                                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

You can query in natural language using the `adv` search option. It will show a table of results like this:

```bash
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Relevance  ┃ Title                                    ┃ Authors                   ┃ Field                ┃ Category   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 0.810      │ Attention Is All You Need: A Comprehe... │ Vaswani, A., Shazeer, ... │ Natural Language ... │ cs.LG      │
│ 0.536      │ BERT: Pre-training of Deep Bidirectio... │ Devlin, J., Chang, M.W... │ Natural Language ... │ cs.CL      │
│ 0.434      │ ResNet: Deep Residual Learning for Im... │ He, K., Zhang, X., Ren... │ Computer Vision      │ cs.CV      │
│ 0.391      │ GPT-3: Language Models are Few-Shot L... │ Brown, T.B., Mann, B.,... │ Natural Language ... │ cs.CL      │
│ 0.317      │ Neural Information Retrieval: At the ... │ Mitra, B., Craswell, N.   │ Artificial Intell... │ cs.IR      │
│ 0.291      │ Explainable AI: Interpreting, Explain... │ Samek, W., Montavon, G... │ Artificial Intell... │ cs.AI      │
│ 0.254      │ You Only Look Once: Unified, Real-Tim... │ Redmon, J., Divvala, S... │ Computer Vision      │ cs.CV      │
│ 0.251      │ Generative Adversarial Networks          │ Goodfellow, I., Pouget... │ Machine Learning     │ cs.LG      │
│ 0.250      │ Federated Learning: Challenges, Metho... │ Li, T., Sahu, A.K., Ta... │ Machine Learning     │ cs.LG      │
│ 0.250      │ Quantum Machine Learning: What Quantu... │ Biamonte, J., Wittek, ... │ Data Science         │ physics    │
└────────────┴──────────────────────────────────────────┴───────────────────────────┴──────────────────────┴────────────┘
```

## Checklist

### 🛠️ Build an app with KBs

1. Your app executes `CREATE KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L78) ✅
2.  Your app ingests data using `INSERT INTO knowledge_base` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L161) ✅
3. Your app retrieves relevant data based on on semantic queries `SELECT` ... `FROM` ... `WHERE` `content` `LIKE` `<query>` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L253) ✅
4. Your app uses `CREATE INDEX ON KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L116) ✅

### 🛠️ Use metadata columns

1. Define `metadata_columns` during ingestion and use WHERE clauses that combine semantic search with SQL attribute filtering on `metadata_columns` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L90) ✅