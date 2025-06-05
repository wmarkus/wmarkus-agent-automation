from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.file import FileTools
from agno.tools.email import EmailTools
from typing import List
import datetime
import os
import io
import sys

# Configuration for newsletter topics and sources
NEWSLETTER_CONFIG = {
    "newsletter_title": "Top of Mind: AI Filmmaking & Creative Arts",
    "categories": [
        "Industry News",
        "Technical Insights", 
        "Project Updates",
        "Tools and Resources",
        "Events and Conferences"
    ],
    "search_keywords": [
        "AI filmmaking",
        "AI creative arts", 
        "artificial intelligence film production",
        "AI video editing",
        "generative AI art",
        "AI animation",
        "neural rendering film",
        "AI special effects",
        "machine learning creative tools"
    ],
    "target_sources": [
        "venturebeat.com",
        "techcrunch.com", 
        "wired.com",
        "aitimes.com",
        "creativebloq.com",
        "variety.com",
        "hollywoodreporter.com"
    ]
}

# Research Agent - Finds and collects articles
research_agent = Agent(
    name="Content Research Agent",
    role="Research and collect articles about AI filmmaking and creative arts",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[DuckDuckGoTools()],
    instructions=[
        f"Search for recent articles about: {', '.join(NEWSLETTER_CONFIG['search_keywords'])}",
        f"Focus on content from these preferred sources: {', '.join(NEWSLETTER_CONFIG['target_sources'])}",
        "Look for articles published within the last 7 days",
        "Collect article titles, URLs, publication dates, sources, and brief summaries",
        "Prioritize high-quality, authoritative sources",
        "Avoid duplicate content",
        "Include both breaking news and in-depth analysis pieces",
        "Always verify article relevance to AI filmmaking and creative arts"
    ],
    add_datetime_to_instructions=True,
)

# Categorization Agent - Organizes content by topic
categorization_agent = Agent(
    name="Content Categorization Agent", 
    role="Categorize and organize collected articles into newsletter sections",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[ReasoningTools()],
    instructions=[
        f"Categorize articles into these sections: {', '.join(NEWSLETTER_CONFIG['categories'])}",
        "Each article should be placed in the most appropriate single category",
        "Consider the primary focus and target audience of each article",
        "Industry News: Company announcements, funding, partnerships, market trends",
        "Technical Insights: How-to guides, technical deep dives, algorithm explanations",
        "Project Updates: New product launches, software updates, feature releases", 
        "Tools and Resources: New tools, software, hardware, educational content",
        "Events and Conferences: Upcoming events, conference reports, webinars",
        "If an article doesn't fit well in any category, place it in 'Industry News'",
        "Provide reasoning for categorization decisions"
    ],
    add_datetime_to_instructions=True,
)

# Curation Agent - Summarizes and refines content
curation_agent = Agent(
    name="Content Curation Agent",
    role="Summarize articles and create engaging newsletter content",
    model=Claude(id="claude-opus-4-20250514"), 
    tools=[ReasoningTools()],
    instructions=[
        "Create concise, engaging 2-3 sentence summaries for each article",
        "Highlight key insights and their relevance to AI filmmaking professionals",
        "Maintain an informative yet accessible tone",
        "Focus on practical implications and actionable insights",
        "Identify the most newsworthy and impactful articles in each category",
        "Limit to top 5 articles per category to keep newsletter focused",
        "Ensure summaries are original and not direct copies from source material",
        "Add context about why each article matters to the target audience"
    ],
    add_datetime_to_instructions=True,
)

# Newsletter Generation Agent - Creates final formatted output
newsletter_agent = Agent(
    name="Newsletter Generation Agent",
    role="Generate the final formatted newsletter from curated content",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[FileTools()],
    instructions=[
        f"Create a professionally formatted newsletter titled '{NEWSLETTER_CONFIG['newsletter_title']}'",
        "Use markdown format for clean, readable output",
        "Include an engaging introduction paragraph",
        "Organize content by categories with clear section headers", 
        "Format each article with: title (linked), source, date, and summary",
        "Add visual separators between articles",
        "Include a closing note and call-to-action",
        "Ensure consistent formatting throughout",
        "Add issue number and publication date",
        "Keep the overall length appropriate for email distribution (not too long)"
    ],
    add_datetime_to_instructions=True,
)

# Distribution Agent - Handles newsletter delivery  
distribution_agent = Agent(
    name="Newsletter Distribution Agent",
    role="Handle newsletter distribution and delivery logistics",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[EmailTools(), FileTools()],
    instructions=[
        "Save newsletter to file with timestamp in filename",
        "Prepare newsletter for email distribution if requested",
        "Generate both markdown and HTML versions if needed", 
        "Create archive of past newsletters for reference",
        "Handle any distribution logistics and delivery confirmation",
        "Maintain subscriber list if provided",
        "Generate delivery reports and metrics if requested"
    ],
    add_datetime_to_instructions=True,
)

# Newsletter Production Team - Coordinates the entire workflow
newsletter_team = Team(
    name="AI Filmmaking Newsletter Team",
    mode="sequential",  # Execute agents in order for newsletter workflow
    model=Claude(id="claude-opus-4-20250514"),
    members=[
        research_agent,
        categorization_agent, 
        curation_agent,
        newsletter_agent,
        distribution_agent
    ],
    tools=[ReasoningTools(add_instructions=True), FileTools()],
    instructions=[
        "Collaborate to produce a high-quality weekly newsletter about AI filmmaking and creative arts",
        "Follow this workflow: Research → Categorize → Curate → Generate → Distribute",
        "Research Agent: Find 15-25 recent, relevant articles from quality sources",
        "Categorization Agent: Organize articles into the defined categories",
        "Curation Agent: Summarize articles and select the best 3-5 per category",
        "Newsletter Agent: Create the final formatted newsletter",
        "Distribution Agent: Save files and prepare for delivery",
        "Ensure each step builds upon the previous agent's work",
        "Maintain quality standards throughout the process",
        "Focus on content that serves AI filmmaking professionals and enthusiasts",
        "Only output the final newsletter, not individual agent responses unless debugging"
    ],
    markdown=True,
    show_members_responses=False,  # Set to True for debugging
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria="The team has produced a complete, well-formatted newsletter with curated articles organized by category, including summaries and proper attribution, ready for distribution to subscribers."
)

# Utility functions for newsletter management
def generate_weekly_newsletter():
    """Generate the weekly newsletter"""
    prompt = f"""Generate this week's '{NEWSLETTER_CONFIG['newsletter_title']}' newsletter.
    
    Research recent articles (last 7 days) about:
    {', '.join(NEWSLETTER_CONFIG['search_keywords'])}
    
    Organize content into these categories:
    {', '.join(NEWSLETTER_CONFIG['categories'])}
    
    Create a professional newsletter ready for distribution to AI filmmaking professionals.
    """
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    newsletter_team.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True
    )
    sys.stdout = old_stdout
    return mystdout.getvalue()

def generate_themed_newsletter(theme: str, keywords: List[str] = None):
    """Generate a themed newsletter on a specific topic"""
    if keywords is None:
        keywords = NEWSLETTER_CONFIG['search_keywords']
    
    prompt = f"""Generate a themed newsletter about: {theme}
    
    Focus your research on: {', '.join(keywords)}
    
    Follow the standard newsletter format but emphasize content related to {theme}.
    Ensure all articles are relevant to both the theme and AI filmmaking/creative arts.
    """
    
    return newsletter_team.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True
    )

def analyze_newsletter_topics():
    """Analyze current trends and suggest newsletter topics"""
    prompt = """Research current trends in AI filmmaking and creative arts to suggest topics for upcoming newsletters.
    
    Identify:
    1. Emerging technologies and tools
    2. Industry developments and announcements  
    3. Important upcoming events or releases
    4. Trending discussion topics in the community
    
    Provide 5-7 suggested themed newsletter topics based on your research.
    """
    
    return newsletter_team.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True
    )

# Configuration for scheduled execution
class NewsletterScheduler:
    """Simple scheduler for newsletter generation"""
    
    def __init__(self, team: Team):
        self.team = team
        self.schedule_day = "Thursday"
        self.schedule_time = "09:00"
    
    def generate_and_save(self, output_dir: str = "newsletters"):
        """Generate newsletter and save to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate newsletter
        newsletter_content = generate_weekly_newsletter()
        
        # Save with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"newsletter_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(newsletter_content)
        
        print(f"Newsletter saved to: {filepath}")
        return filepath

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Filmmaking Newsletter Generator')
    parser.add_argument('--mode', choices=['weekly', 'themed', 'trends'], default='weekly',
                      help='Newsletter generation mode')
    parser.add_argument('--theme', type=str, help='Theme for themed newsletter')
    parser.add_argument('--keywords', nargs='+', help='Custom keywords for research')
    parser.add_argument('--save', action='store_true', help='Save newsletter to file')
    
    args = parser.parse_args()
    
    if args.mode == 'weekly':
        print("Generating weekly newsletter...")
        if args.save:
            scheduler = NewsletterScheduler(newsletter_team)
            scheduler.generate_and_save()
        else:
            generate_weekly_newsletter()
            
    elif args.mode == 'themed':
        if not args.theme:
            print("Please provide a theme with --theme")
        else:
            print(f"Generating themed newsletter: {args.theme}")
            generate_themed_newsletter(args.theme, args.keywords)
            
    elif args.mode == 'trends':
        print("Analyzing trends for newsletter topics...")
        analyze_newsletter_topics() 