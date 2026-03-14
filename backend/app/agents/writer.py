from typing import Dict, Any, List
from app.agents.base import BaseAgent, AGENT_REGISTRY
import asyncio


class WriterAgent(BaseAgent):
    """Writer Agent - creates written content, articles, documentation."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "writer"
        self.name = "Writer Agent"
        description = "Content creation, articles, reports, documentation, and social media"
        self.icon = "✍️"
    
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute writing task.
        
        Steps:
        1. Analyze content requirements
        2. Plan content structure
        3. Generate content sections
        4. Review and refine
        """
        await self._notify_update("working", "10%", "Analyzing content requirements...")
        await asyncio.sleep(1.5)
        
        # Determine content type
        content_type = self._determine_content_type(title, description)
        
        await self._notify_update("working", "25%", f"Planning {content_type} structure...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "40%", "Generating content sections...")
        await asyncio.sleep(1.5)
        
        # Generate content sections
        sections = self._generate_sections(title, description, content_type)
        
        for i, section in enumerate(sections):
            progress = 40 + (i * 20 // len(sections))
            await self._notify_update("working", f"{progress}%", f"Writing: {section['title']}...")
            await asyncio.sleep(1.2)
        
        await self._notify_update("working", "85%", "Reviewing and refining content...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "95%", "Finalizing document...")
        await asyncio.sleep(1)
        
        # Generate final content
        content = self._compile_content(title, sections)
        
        await self._notify_update("completed", "100%", "Content creation complete")
        
        return {
            "status": "success",
            "content": content,
            "content_type": content_type,
            "summary": f"Created {content_type} with {len(sections)} sections",
            "word_count": len(content.split())
        }
    
    def _determine_content_type(self, title: str, description: str) -> str:
        """Determine the type of content to create."""
        combined = f"{title} {description}".lower()
        
        if "thread" in combined or "twitter" in combined:
            return "twitter_thread"
        elif "article" in combined or "blog" in combined:
            return "article"
        elif "report" in combined:
            return "report"
        elif "documentation" in combined or "docs" in combined:
            return "documentation"
        elif "landing page" in combined or "website" in combined:
            return "web_copy"
        else:
            return "article"
    
    def _generate_sections(self, title: str, description: str, content_type: str) -> List[Dict[str, Any]]:
        """Generate content sections based on type."""
        if content_type == "twitter_thread":
            return [
                {"title": "Hook", "content": f"🚨 {title}\n\nHere's what you need to know:"},
                {"title": "Point 1", "content": "1/ The problem we're solving:\n\n" + description[:100]},
                {"title": "Point 2", "content": "2/ Why it matters:\n\nKey insight about the topic."},
                {"title": "Point 3", "content": "3/ The solution:\n\nHow it works and why it's innovative."},
                {"title": "Conclusion", "content": "4/ Bottom line:\n\nThis is just the beginning. Follow for more updates 🚀"}
            ]
        elif content_type == "report":
            return [
                {"title": "Executive Summary", "content": f"This report covers: {title}\n\n{description}"},
                {"title": "Introduction", "content": f"Background and context for {title}."},
                {"title": "Key Findings", "content": "Analysis of the main findings from research."},
                {"title": "Detailed Analysis", "content": "In-depth examination of the topic."},
                {"title": "Conclusions", "content": "Summary of key takeaways."},
                {"title": "Recommendations", "content": "Actionable recommendations based on findings."}
            ]
        else:  # article
            return [
                {"title": "Introduction", "content": f"Welcome to this article about {title}.\n\n{description}"},
                {"title": "Background", "content": "Understanding the context and background of this topic."},
                {"title": "Main Content", "content": "The core content and analysis."},
                {"title": "Key Points", "content": "Important takeaways and insights."},
                {"title": "Conclusion", "content": "Wrapping up the key insights and next steps."}
            ]
    
    def _compile_content(self, title: str, sections: List[Dict[str, Any]]) -> str:
        """Compile all sections into final content."""
        content_lines = [f"# {title}\n"]
        
        for section in sections:
            content_lines.append(f"\n## {section['title']}\n")
            content_lines.append(section['content'])
        
        return "\n".join(content_lines)


# Register the agent
AGENT_REGISTRY["writer"] = WriterAgent
