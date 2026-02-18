"""Retrieval evaluation: checks whether expected docs appear in top_k results."""

import os

import httpx

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
TOP_K = 5

# (question, expected filename prefix in doc_id)
CASES = [
    ("What should I focus on in my first week?", "first-week-playbook.md"),
    ("How do I open a pull request?", "pull-request-checklist.md"),
    ("How do I set up my development environment?", "onboarding.md"),
    ("How do I add authentication to an endpoint?", "authentication-and-authorization.md"),
    ("How do I handle errors in my service?", "error-handling-and-logging.md"),
    ("How do I write tests for a backend API?", "testing-backend-apis.md"),
    ("What does the overall system architecture look like?", "system-architecture-overview.md"),
    ("How do I add a new API endpoint?", "adding-a-new-api-endpoint.md"),
]


def run_eval() -> None:
    client = httpx.Client(base_url=API_BASE, timeout=30)

    hits = 0
    rows: list[tuple[str, str, bool, str]] = []

    for question, expected in CASES:
        resp = client.post("/retrieve", json={"query": question, "top_k": TOP_K})
        resp.raise_for_status()
        results = resp.json()["results"]

        top_docs = [r["doc_id"].split("::")[0] for r in results]
        found = expected in top_docs
        hits += found

        rank = str(top_docs.index(expected) + 1) if found else "-"
        rows.append((question, expected, found, rank))

    precision = hits / len(CASES)

    # Print results table
    q_width = max(len(r[0]) for r in rows)
    doc_width = max(len(r[1]) for r in rows)
    header = f"{'Question':<{q_width}}  {'Expected Doc':<{doc_width}}  Hit  Rank"
    print(header)
    print("-" * len(header))
    for question, expected, found, rank in rows:
        mark = "Y" if found else "N"
        print(f"{question:<{q_width}}  {expected:<{doc_width}}  {mark:>3}  {rank:>4}")

    print("-" * len(header))
    print(f"Precision@{TOP_K}: {precision:.0%} ({hits}/{len(CASES)})")


if __name__ == "__main__":
    run_eval()