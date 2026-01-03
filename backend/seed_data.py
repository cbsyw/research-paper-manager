import asyncio
import httpx
from app.database import SessionLocal, engine, Base
from app.models import Paper

OPENALEX_API_BASE = "https://api.openalex.org"

async def fetch_biology_papers():
    """Fetch biology papers from OpenAlex API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{OPENALEX_API_BASE}/works",
                params={
                    "search": "biology",
                    "per_page": 15,
                    "sort": "cited_by_count:desc"
                },
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()

            papers = []
            for work in data.get("results", []):
                paper = Paper(
                    title=work.get("title", "Unknown Title"),
                    authors=", ".join([
                        author.get("author", {}).get("display_name", "Unknown")
                        for author in work.get("authorships", [])[:5]
                    ]),
                    year=work.get("publication_year"),
                    abstract=work.get("abstract"),
                    url=work.get("doi") or work.get("id"),
                    notes=f"Cited by: {work.get('cited_by_count', 0)} papers"
                )
                papers.append(paper)

            return papers

        except Exception as e:
            print(f"Error fetching from OpenAlex: {e}")
            return []

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    db = SessionLocal()

    # Check if data already exists
    existing_papers = db.query(Paper).count()
    if existing_papers > 0:
        print(f"Database already contains {existing_papers} papers. Skipping seed.")
        db.close()
        return

    # Fetch papers from OpenAlex
    print("Fetching biology papers from OpenAlex...")
    papers = asyncio.run(fetch_biology_papers())

    if not papers:
        print("Failed to fetch papers from OpenAlex. Exiting.")
        db.close()
        return

    # Add papers to database
    for paper in papers:
        db.add(paper)

    db.commit()
    print(f"Successfully seeded database with {len(papers)} biology papers from OpenAlex")
    db.close()

if __name__ == "__main__":
    seed_database()
