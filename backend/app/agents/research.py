from typing import Dict, Any, List
from app.agents.base import BaseAgent, AGENT_REGISTRY
import asyncio


class ResearchAgent(BaseAgent):
    """Research Agent - gathers information and performs web research."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "research"
        self.name = "Research Agent"
        self.description = "Information gathering, web research, and data analysis"
        self.icon = "🔍"
    
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute research task.
        
        Steps:
        1. Understand the research goal
        2. Identify key research areas
        3. Gather information (simulated)
        4. Synthesize findings
        """
        await self._notify_update("working", "10%", "Understanding research goal...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "25%", "Identifying key research areas...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "40%", "Gathering information from sources...")
        await asyncio.sleep(1.5)
        
        # Simulate research topics
        research_topics = self._identify_topics(title, description)
        
        for i, topic in enumerate(research_topics):
            progress = 40 + (i * 20 // len(research_topics))
            await self._notify_update("working", f"{progress}%", f"Researching: {topic}...")
            await asyncio.sleep(1.2)
        
        await self._notify_update("working", "85%", "Analyzing and synthesizing findings...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "95%", "Generating research summary...")
        await asyncio.sleep(1)
        
        # Generate research report
        research_report = self._generate_report(title, description, research_topics)
        
        await self._notify_update("completed", "100%", "Research complete")
        
        return {
            "status": "success",
            "findings": research_report,
            "summary": f"Research completed on {len(research_topics)} topics",
            "topics_covered": research_topics
        }
    
    def _identify_topics(self, title: str, description: str) -> List[str]:
        """Identify key research topics from the task."""
        combined = f"{title} {description}".lower()
        topics = []
        
        # Extract keywords as research topics
        keywords = ["technology", "market", "competitors", "features", 
                   "pricing", "users", "implementation", "challenges",
                   "opportunities", "trends", "solutions"]
        
        for kw in keywords:
            if kw in combined:
                topics.append(kw)
        
        if not topics:
            topics = ["general overview", "key concepts", "best practices"]
        
        return topics[:5]  # Limit to 5 topics
    
    def _generate_report(self, title: str, description: str, topics: List[str]) -> Dict[str, Any]:
        """Generate a comprehensive research report."""
        return {
            "title": f"Research Report: {title}",
            "overview": f"This report provides comprehensive research on {title}.",
            "findings": [
                {
                    "topic": topic,
                    "summary": f"Key findings related to {topic} in the context of {title}.",
                    "sources": [
                        {"name": f"Source A - {topic}", "url": "https://example.com/1"},
                        {"name": f"Source B - {topic}", "url": "https://example.com/2"}
                    ],
                    "key_insights": [
                        f"Insight 1 about {topic}",
                        f"Insight 2 about {topic}",
                        f"Insight 3 about {topic}"
                    ]
                }
                for topic in topics
            ],
            "conclusion": f"Based on the research, {title} presents significant opportunities.",
            "recommendations": [
                "Focus on core features that differentiate from competitors",
                "Consider target audience preferences",
                "Implement best practices from industry leaders"
            ]
        }


# Register the agent
AGENT_REGISTRY["research"] = ResearchAgent
