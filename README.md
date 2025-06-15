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

## Checklist

### 🛠️ Build an app with KBs

1. Your app executes `CREATE KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L78) ✅
2.  Your app ingests data using `INSERT INTO knowledge_base` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L161) ✅
3. Your app retrieves relevant data based on on semantic queries `SELECT` ... `FROM` ... `WHERE` `content` `LIKE` `<query>` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L253) ✅
4. Your app uses `CREATE INDEX ON KNOWLEDGE_BASE` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L116) ✅

### 🛠️ Use metadata columns

1. Define `metadata_columns` during ingestion and use WHERE clauses that combine semantic search with SQL attribute filtering on `metadata_columns` - [here](https://github.com/ChiragAgg5k/scholar-map/blob/9dc1420c07d0231c9f039f09e8eb681fff5dc5d3/src/mindsdb_manager.py#L90) ✅