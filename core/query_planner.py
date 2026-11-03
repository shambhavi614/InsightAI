
import json

import requests
from pydantic import ValidationError

from core.ai_engine import OLLAMA_URL, MODEL_NAME
from core.analysis_engine import AnalysisPlan


def create_analysis_plan(question, df):
    columns = [
        {
            "name": str(column),
            "dtype": str(df[column].dtype),
        }
        for column in df.columns
    ]

    prompt = f"""
You are InsightAI's query planner.

Translate the user question into ONE JSON object.

Dataset columns:
{json.dumps(columns)}

JSON structure:
{{
  "operation": "sum",
  "group_by": "Product",
  "target_column": "Sales",
  "sort": "desc",
  "limit": 10,
  "filters": []
}}

Supported operations:
sum, mean, count, max, min

Supported filter operators:
eq, ne, gt, gte, lt, lte

Example filter:
{{
  "column": "Region",
  "operator": "eq",
  "value": "South"
}}

Rules:
1. Use exact dataset column names.
2. Total sales means sum.
3. Average means mean.
4. Number of records means count.
5. Highest total by category means sum and desc.
6. Lowest total by category means sum and asc.
7. Use null when no grouping or target is needed.
8. Use limit 10 for grouped comparisons.
9. Use filters only when the user specifies a condition.
10. Do not invent dataset results.
11. Return only JSON.
12. If the question cannot be represented, return
    an unsupported operation so validation fails.

Question:
{question}
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 256,
                    "num_ctx": 2048,
                },
                "keep_alive": "10m",
            },
            timeout=(10, 180),
        )

        response.raise_for_status()

        content = response.json()["message"]["content"]
        plan_data = json.loads(content)

        plan = AnalysisPlan.model_validate(plan_data)

        return plan, None

    except (
        requests.RequestException,
        ValueError,
        ValidationError,
        KeyError,
        TypeError,
    ) as error:
        return None, str(error)
