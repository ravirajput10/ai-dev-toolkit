"""
API Tools — Phase 3 Tools
===========================
Async tools that call external APIs: GitHub search, weather lookup, URL fetcher.
"""

import json
import httpx

from app import mcp


# ============================================================
# TOOL: GitHub Repository Search
# ============================================================
# This is our first ASYNC tool — it calls an external API
# Notice: async def (not def) and await (for network calls)
# FastMCP handles the async event loop — you just write the code

@mcp.tool()
async def search_github(query: str, max_results: int = 5) -> str:
    """Search GitHub repositories by keyword.

    Find open-source projects, libraries, and tools on GitHub.
    Returns repository name, stars, description, and URL.

    Args:
        query: Search query (e.g., "mcp server python")
        max_results: Number of results to return (default: 5, max: 10)
    """
    max_results = min(max_results, 10)  # Cap at 10 to avoid huge responses

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "per_page": max_results, "sort": "stars"},
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # Uncomment for debugging:
            # logger.debug(f"GitHub API Response: {json.dumps(data, indent=2)[:1000]}")

            if data["total_count"] == 0:
                return f"🔍 No repositories found for: {query}"

            results = [f"🔍 GitHub Search: '{query}' ({data['total_count']} total results)\n"]
            for i, repo in enumerate(data["items"], 1):
                results.append(
                    f"{i}. ⭐ {repo['stargazers_count']:,} | "
                    f"**{repo['full_name']}**\n"
                    f"   {repo['description'] or 'No description'}\n"
                    f"   🔗 {repo['html_url']}\n"
                )

            return "\n".join(results)

        except httpx.TimeoutException:
            return "❌ Request timed out. GitHub API might be slow — try again."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                return "❌ GitHub API rate limit exceeded. Wait a minute and try again."
            return f"❌ GitHub API error: {e.response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)}"


# ============================================================
# TOOL: Weather Lookup
# ============================================================
# Uses wttr.in — a free weather API (no API key needed!)
# Demonstrates: async HTTP call with different response format

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city.

    Returns temperature, conditions, humidity, and wind speed.
    Works for any city worldwide.

    Args:
        city: City name (e.g., "London", "New York", "Mumbai")
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://wttr.in/{city}",
                params={"format": "j1"},
                headers={"User-Agent": "MCP-DevToolkit"},
                timeout=10.0,
                follow_redirects=True
            )
            response.raise_for_status()
            data = response.json()

            current = data["current_condition"][0]
            location = data["nearest_area"][0]

            city_name = location["areaName"][0]["value"]
            country = location["country"][0]["value"]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]
            feels_like = current["FeelsLikeC"]

            return f"""🌤️ Weather for {city_name}, {country}:

🌡️ Temperature: {temp_c}°C ({temp_f}°F)
🤔 Feels like: {feels_like}°C
☁️ Condition: {desc}
💧 Humidity: {humidity}%
💨 Wind: {wind_kmph} km/h"""

        except httpx.TimeoutException:
            return f"❌ Weather request timed out for '{city}'. Try again."
        except Exception as e:
            return f"❌ Could not get weather for '{city}': {str(e)}"


# ============================================================
# TOOL: URL Content Fetcher
# ============================================================
# Fetches text content from a URL — useful for reading docs,
# checking API responses, or grabbing page content

@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch text content from a URL.

    Retrieves the content of a webpage or API endpoint.
    Returns the first 2000 characters to keep responses manageable.

    Args:
        url: The URL to fetch (must start with http:// or https://)
    """
    if not url.startswith(("http://", "https://")):
        return "❌ Invalid URL. Must start with http:// or https://"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={"User-Agent": "MCP-DevToolkit/1.0"},
                timeout=10.0,
                follow_redirects=True
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            content = response.text[:2000]  # Limit to 2000 chars

            return f"""🌐 URL: {url}
📊 Status: {response.status_code}
📄 Content-Type: {content_type}
📏 Length: {len(response.text):,} characters

Content (first 2000 chars):
{content}"""

        except httpx.TimeoutException:
            return f"❌ Request timed out for: {url}"
        except httpx.HTTPStatusError as e:
            return f"❌ HTTP Error {e.response.status_code} for: {url}"
        except Exception as e:
            return f"❌ Error fetching URL: {str(e)}"
