import httpx
from typing import List, Dict, Optional

OPENALEX_API_BASE = "https://api.openalex.org"

async def search_papers(query: str, limit: int = 10) -> List[Dict]:
    """
    Search for papers in OpenAlex by query string.

    Args:
        query: Search term to look for in title, abstract, or fulltext
        limit: Maximum number of results to return (default 10)

    Returns:
        List of paper dictionaries with simplified structure
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OPENALEX_API_BASE}/works",
                params={"search": query, "per_page": limit},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # Transform OpenAlex format to our simplified format
            papers = []
            for work in data.get("results", []):
                paper = {
                    "openalex_id": work.get("id"),
                    "title": work.get("title"),
                    "authors": ", ".join([
                        author.get("author", {}).get("display_name", "Unknown")
                        for author in work.get("authorships", [])[:5]
                    ]),
                    "year": work.get("publication_year"),
                    "abstract": work.get("abstract"),
                    "url": work.get("doi") or work.get("id"),
                    "cited_by_count": work.get("cited_by_count", 0),
                }
                papers.append(paper)

            return papers

        except httpx.HTTPError as e:
            raise Exception(f"Error fetching from OpenAlex: {str(e)}")

async def get_paper_by_id(openalex_id: str) -> Optional[Dict]:
    """
    Fetch a single paper from OpenAlex by its OpenAlex ID.

    Args:
        openalex_id: The OpenAlex ID (URL format: https://openalex.org/W...)

    Returns:
        Paper dictionary with simplified structure, or None if not found
    """
    # Extract work ID from full URL if needed
    if openalex_id.startswith("https://openalex.org/"):
        work_id = openalex_id.split("/")[-1]
    else:
        work_id = openalex_id

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OPENALEX_API_BASE}/works/{work_id}",
                timeout=10.0
            )
            response.raise_for_status()
            work = response.json()

            paper = {
                "openalex_id": work.get("id"),
                "title": work.get("title"),
                "authors": ", ".join([
                    author.get("author", {}).get("display_name", "Unknown")
                    for author in work.get("authorships", [])
                ]),
                "year": work.get("publication_year"),
                "abstract": work.get("abstract"),
                "url": work.get("doi") or work.get("id"),
                "cited_by_count": work.get("cited_by_count", 0),
            }

            return paper

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f"Error fetching from OpenAlex: {str(e)}")
        except httpx.HTTPError as e:
            raise Exception(f"Error fetching from OpenAlex: {str(e)}")
