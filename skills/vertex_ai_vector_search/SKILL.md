---
name: vertex-ai-vector-search
description: Create and manage Vertex AI Vector Search indexes.
---

# Vertex AI Vector Search Skill

This skill provides instructions and scripts to create a Vector Search index on Google Cloud Vertex AI, using text embeddings generated from source data.

## Workflow

1.  **Prepare Data**: Generate embeddings for your text data and save them in JSONL format with a `.json` extension.
2.  **Upload to GCS**: Upload the `.json` file to a dedicated folder in a GCS bucket.
3.  **Create Index**: Use `gcloud` or a script to create the Vertex AI Vector Search index, pointing to the GCS folder.

## Scripts

### [generate_embeddings.py](file:///usr/local/google/home/bdpanigrahi/a9y/agent_demo/skills/vertex_ai_vector_search/scripts/generate_embeddings.py)

Script to generate embeddings using Vertex AI and save as JSONL (with `.json` extension required by Vertex AI).

## Usage Example

### 1. Generate Embeddings
```bash
python3 skills/vertex_ai_vector_search/scripts/generate_embeddings.py \
  --input_dir path/to/text/files \
  --output_file path/to/output/incidents_embeddings.json \
  --project_id your-project-id \
  --region your-region
```

### 2. Upload to GCS
```bash
gcloud storage cp path/to/output/incidents_embeddings.json gs://your-bucket/embeddings/
```

### 3. Create Index
Create a metadata file `index_metadata.json`:
```json
{
  "contentsDeltaUri": "gs://your-bucket/embeddings/",
  "config": {
    "dimensions": 768,
    "approximateNeighborsCount": 10,
    "distanceMeasureType": "DOT_PRODUCT_DISTANCE"
  }
}
```
Run the gcloud command:
```bash
gcloud ai indexes create \
  --display-name=my-index \
  --metadata-file=index_metadata.json \
  --project=your-project-id \
  --region=your-region
```
