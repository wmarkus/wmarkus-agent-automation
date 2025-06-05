from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.file import FileTools
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Simple LinkedIn Content Configuration
LINKEDIN_CONFIG = {
    "industry_focus": [
        "design engineering",
        "AI filmmaking", 
        "creative arts technology",
        "digital content creation"
    ],
    "target_audience": [
        "design professionals",
        "engineers", 
        "creative directors",
        "content creators",
        "filmmakers"
    ],
    "content_themes": [
        "innovation in creative tech",
        "productivity and efficiency",
        "industry trends and insights",
        "technology adoption",
        "creative process optimization",
        "future of creative work"
    ],
    "topics_per_session": 3,  # 3 high-quality options
    "posting_schedule": {
        "days": ["Monday", "Thursday"],
        "posting_time": "9:00 AM",
        "email_time": "8:00 AM"
    }
}

# Trend Discovery Agent
trend_agent = Agent(
    name="Trend Discovery Agent",
    role="Research trending topics in creative technology and design engineering",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[DuckDuckGoTools()],
    instructions=[
        f"Research current trends in: {', '.join(LINKEDIN_CONFIG['industry_focus'])}",
        "Find trending professional topics on LinkedIn",
        "Focus on topics from the last 7-14 days",
        "Look for discussion topics that resonate with creative professionals"
    ],
    add_datetime_to_instructions=True,
)

# Topic Creation Agent - Focused on Writing Complete Posts
topic_agent = Agent(
    name="LinkedIn Post Writer Agent", 
    role="Write 3 complete, engaging LinkedIn thought leadership posts ready for immediate posting",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[ReasoningTools()],
    instructions=[
        f"WRITE exactly {LINKEDIN_CONFIG['topics_per_session']} COMPLETE LinkedIn posts - not topic ideas, but full posts ready to publish",
        "CRITICAL: Write the actual post content, including the full text that will be posted",
        "Each post should be 150-300 words of engaging, professional content",
        "Include compelling opening hooks, substantive body content, and strong calls-to-action",
        "Write in first person with authentic professional voice and personal insights",
        "Structure: Hook → Key insights/story → Actionable takeaways → Engagement question",
        "Ensure each post establishes thought leadership through unique perspectives and expertise",
        "Vary post types: one tactical/how-to, one industry insight, one future-focused opinion",
        "Include strategic hashtags naturally within or at the end of each post",
        "Write posts that encourage meaningful comments and professional discussion",
        "Each post must be complete and ready to copy-paste directly into LinkedIn"
    ],
    add_datetime_to_instructions=True,
)

# Content Optimization Agent
optimization_agent = Agent(
    name="LinkedIn Post Optimization Agent",
    role="Polish and optimize complete LinkedIn posts for maximum engagement and professional impact",
    model=Claude(id="claude-opus-4-20250514"),
    tools=[ReasoningTools()],
    instructions=[
        "Optimize complete LinkedIn posts for maximum engagement and thought leadership positioning",
        "Refine opening hooks to stop scrolling and capture attention immediately", 
        "Ensure posts flow naturally from hook → insights → takeaways → call-to-action",
        "Optimize for LinkedIn's algorithm: authentic voice, meaningful content, engagement triggers",
        "Ensure posts are scannable with line breaks and emojis where appropriate",
        "Verify hashtags are strategically placed and relevant to the content",
        "Polish language for professional yet conversational tone",
        "Ensure each post demonstrates expertise and provides genuine value",
        "Optimize call-to-action questions to drive meaningful comments",
        "Final posts should be publication-ready with no further editing needed"
    ],
    add_datetime_to_instructions=True,
)

# Quality-Focused Team for Writing Complete Posts
linkedin_team = Team(
    name="LinkedIn Post Writing Team",
    mode="sequential",
    model=Claude(id="claude-opus-4-20250514"),
    members=[trend_agent, topic_agent, optimization_agent],
    tools=[ReasoningTools(), FileTools()],
    instructions=[
        f"Write {LINKEDIN_CONFIG['topics_per_session']} COMPLETE LinkedIn posts ready for immediate publishing",
        "CRITICAL: Generate full post content, not topic ideas - actual posts ready to copy-paste to LinkedIn",
        "Workflow: Research trending topics → Write complete posts → Optimize for engagement",
        f"Target audience: {', '.join(LINKEDIN_CONFIG['target_audience'])}",
        f"Content themes: {', '.join(LINKEDIN_CONFIG['content_themes'])}",
        "POST REQUIREMENTS: 150-300 words each, engaging hook, substantive content, clear CTA",
        "Write in authentic first-person voice with professional expertise and personal insights",
        "Ensure variety: tactical advice post, industry insights post, future-focused opinion post",
        "Include strategic hashtags naturally integrated into each post",
        "Output format: Complete LinkedIn posts ready for publication",
        "Each post must establish thought leadership and drive meaningful professional engagement"
    ],
    markdown=True,
    show_members_responses=True,
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria="Generated 3 complete, publication-ready LinkedIn posts that establish thought leadership, provide genuine value, and drive professional engagement."
)

def generate_content():
    """Generate 3 complete LinkedIn posts ready for publishing"""
    prompt = f"""Write 3 COMPLETE LinkedIn thought leadership posts ready for immediate publication.
    
    Focus Areas: {', '.join(LINKEDIN_CONFIG['industry_focus'])}
    Target Audience: {', '.join(LINKEDIN_CONFIG['target_audience'])}
    Content Themes: {', '.join(LINKEDIN_CONFIG['content_themes'])}
    
    CRITICAL REQUIREMENTS:
    - Write FULL posts (150-300 words each), not topic ideas or outlines
    - Include complete post text ready to copy-paste into LinkedIn
    - Write in first person with authentic professional voice
    - Each post must establish thought leadership through unique insights
    - Include natural hashtag integration and engaging call-to-action questions
    
    POST VARIETY (exactly 3 posts):
    1. TACTICAL POST: How-to or practical advice with actionable steps
    2. INDUSTRY INSIGHT: Analysis of current trends or professional observations
    3. FUTURE-FOCUSED: Opinion on where the industry/technology is heading
    
    FORMAT for each complete post:
    ## Post Option [Number]: [Brief Theme Description]
    
    [COMPLETE LINKEDIN POST TEXT - ready to publish]
    [Include natural line breaks for readability]
    [Include strategic hashtags]
    [End with engaging question for comments]
    
    **Why This Post Works:** [Brief explanation of the strategy]
    
    ---
    
    Goal: 3 complete posts ready for copy-paste publishing at 9 AM on {LINKEDIN_CONFIG['posting_schedule']['days'][0]} or {LINKEDIN_CONFIG['posting_schedule']['days'][1]}.
    """
    
    return linkedin_team.print_response(prompt, stream=True, show_full_reasoning=True)

def send_email(content, email_config):
    """Send complete LinkedIn posts via email"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    day_name = datetime.datetime.now().strftime('%A')
    
    msg = MIMEMultipart()
    msg['From'] = email_config['from_email']
    msg['To'] = email_config['to_email']
    msg['Subject'] = f"📝 3 Complete LinkedIn Posts Ready - {day_name} {timestamp}"
    
    body = f"""Your 3 complete LinkedIn posts are ready for publishing at 9 AM! 

Each post is fully written and ready to copy-paste directly into LinkedIn.

{content}

📅 Posting Schedule: {', '.join(LINKEDIN_CONFIG['posting_schedule']['days'])} at {LINKEDIN_CONFIG['posting_schedule']['posting_time']}
📝 Ready to Publish: Complete posts, no editing needed
⏰ Generated: {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}

Simply choose your favorite post and copy-paste it directly to LinkedIn!
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_config['from_email'], email_config['password'])
    server.sendmail(email_config['from_email'], email_config['to_email'], msg.as_string())
    server.quit()
    
    print(f"✅ 3 complete LinkedIn posts emailed to {email_config['to_email']}")

def main():
    """Main function for GitHub Actions - generates 3 complete LinkedIn posts"""
    # Get email config from environment variables
    email_config = {
        'from_email': os.getenv('FROM_EMAIL'),
        'password': os.getenv('EMAIL_PASSWORD'), 
        'to_email': os.getenv('TO_EMAIL')
    }
    
    print("📝 Writing 3 complete LinkedIn posts ready for publishing...")
    content = generate_content()
    
    print("📧 Sending complete posts via email...")
    send_email(content, email_config)
    
    print("✅ Done! 3 complete LinkedIn posts ready to copy-paste and publish.")

def create_github_workflow():
    """Create GitHub Actions workflow file"""
    workflow_content = """name: LinkedIn Content Generation

on:
  schedule:
    # Runs at 8:00 AM UTC on Mondays and Thursdays (1 hour before 9 AM posting time)
    - cron: '0 8 * * 1,4'
  workflow_dispatch:  # Manual trigger button

jobs:
  generate-content:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install agno anthropic
    
    - name: Generate 3 Quality LinkedIn Options
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        FROM_EMAIL: ${{ secrets.FROM_EMAIL }}
        EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
        TO_EMAIL: ${{ secrets.TO_EMAIL }}
      run: |
        python linkedin_agent.py
"""
    
    os.makedirs('.github/workflows', exist_ok=True)
    with open('.github/workflows/linkedin_automation.yml', 'w') as f:
        f.write(workflow_content)
    
    print("✅ Created GitHub Actions workflow at .github/workflows/linkedin_automation.yml")
    print("\n📋 Setup Summary:")
    print("📅 Schedule: Mondays and Thursdays at 8:00 AM UTC")
    print("📧 Email: Sends 3 complete posts 1 hour before 9 AM posting time")
    print("📝 Output: Full LinkedIn posts ready to copy-paste and publish")
    print("\n🔧 Next steps:")
    print("1. Push this code to GitHub")
    print("2. Go to repo Settings → Secrets and variables → Actions")
    print("3. Add these secrets:")
    print("   - ANTHROPIC_API_KEY (your Claude API key)")
    print("   - FROM_EMAIL (your Gmail address)")
    print("   - EMAIL_PASSWORD (Gmail app password)")
    print("   - TO_EMAIL (where to send content)")
    print("4. Test with Actions → LinkedIn Content Generation → Run workflow")
    print("\n⏰ Perfect workflow: Email at 8 AM → Review → Copy-paste at 9 AM → Publish!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        create_github_workflow()
    else:
        main()