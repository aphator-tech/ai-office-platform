from typing import Dict, Any, List
from app.agents.base import BaseAgent, AGENT_REGISTRY
import asyncio


class DesignerAgent(BaseAgent):
    """Designer Agent - creates UI/UX designs and specifications."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "designer"
        self.name = "Designer Agent"
        self.description = "UI/UX design, layouts, component specifications, and design systems"
        self.icon = "🎨"
    
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute design task.
        
        Steps:
        1. Analyze design requirements
        2. Plan visual structure
        3. Generate component specifications
        4. Create design system
        """
        await self._notify_update("working", "10%", "Analyzing design requirements...")
        await asyncio.sleep(1.5)
        
        # Determine design type
        design_type = self._determine_design_type(title, description)
        
        await self._notify_update("working", "25%", f"Planning {design_type} design...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "40%", "Creating visual structure...")
        await asyncio.sleep(1.5)
        
        # Generate layout structure
        layout = self._generate_layout(title, design_type)
        
        await self._notify_update("working", "60%", "Defining components...")
        await asyncio.sleep(1.5)
        
        # Generate component specs
        components = self._generate_components(design_type)
        
        for i, component in enumerate(components):
            progress = 60 + (i * 15 // len(components))
            await self._notify_update("working", f"{progress}%", f"Designing: {component['name']}...")
            await asyncio.sleep(1)
        
        await self._notify_update("working", "80%", "Building design system...")
        await asyncio.sleep(1.5)
        
        # Generate design system
        design_system = self._generate_design_system()
        
        await self._notify_update("working", "95%", "Finalizing specifications...")
        await asyncio.sleep(1)
        
        await self._notify_update("completed", "100%", "Design complete")
        
        return {
            "status": "success",
            "design_type": design_type,
            "layout": layout,
            "components": components,
            "design_system": design_system,
            "summary": f"Created {design_type} design with {len(components)} components"
        }
    
    def _determine_design_type(self, title: str, description: str) -> str:
        """Determine the type of design to create."""
        combined = f"{title} {description}".lower()
        
        if "landing page" in combined or "marketing" in combined:
            return "landing_page"
        elif "dashboard" in combined or "admin" in combined:
            return "dashboard"
        elif "mobile" in combined or "app" in combined:
            return "mobile_app"
        elif "blog" in combined:
            return "blog"
        else:
            return "website"
    
    def _generate_layout(self, title: str, design_type: str) -> Dict[str, Any]:
        """Generate layout structure."""
        return {
            "type": design_type,
            "page_sections": [
                {
                    "name": "Header",
                    "height": "80px",
                    "elements": ["Logo", "Navigation", "CTA Button"],
                    "position": "fixed top"
                },
                {
                    "name": "Hero Section",
                    "height": "80vh",
                    "elements": ["Headline", "Subheadline", "Primary CTA", "Hero Image"],
                    "position": "below header"
                },
                {
                    "name": "Features Section",
                    "height": "auto",
                    "elements": ["Section Title", "Feature Cards Grid"],
                    "position": "below hero"
                },
                {
                    "name": "About Section",
                    "height": "auto",
                    "elements": ["Section Title", "Content Block", "Image"],
                    "position": "below features"
                },
                {
                    "name": "Footer",
                    "height": "200px",
                    "elements": ["Links", "Social Icons", "Copyright"],
                    "position": "bottom"
                }
            ],
            "grid_system": {
                "columns": 12,
                "gutter": "24px",
                "max_width": "1440px"
            },
            "responsive_breakpoints": {
                "mobile": "320px",
                "tablet": "768px",
                "desktop": "1024px",
                "wide": "1440px"
            }
        }
    
    def _generate_components(self, design_type: str) -> List[Dict[str, Any]]:
        """Generate component specifications."""
        return [
            {
                "name": "Button",
                "type": "interactive",
                "variants": ["primary", "secondary", "outline", "ghost"],
                "states": ["default", "hover", "active", "disabled", "loading"],
                "specs": {
                    "primary": {
                        "background": "#58A6FF",
                        "text": "#0D1117",
                        "border_radius": "8px",
                        "padding": "12px 24px"
                    }
                }
            },
            {
                "name": "Card",
                "type": "container",
                "variants": ["default", "elevated", "outlined"],
                "specs": {
                    "background": "#161B22",
                    "border": "1px solid #30363D",
                    "border_radius": "12px",
                    "padding": "24px"
                }
            },
            {
                "name": "Input",
                "type": "form",
                "variants": ["text", "email", "password", "search"],
                "states": ["default", "focus", "error", "disabled"],
                "specs": {
                    "background": "#0D1117",
                    "border": "1px solid #30363D",
                    "border_radius": "8px",
                    "padding": "12px 16px"
                }
            },
            {
                "name": "Navigation",
                "type": "layout",
                "variants": ["horizontal", "vertical"],
                "specs": {
                    "background": "#161B22",
                    "item_spacing": "32px"
                }
            },
            {
                "name": "Hero",
                "type": "layout",
                "specs": {
                    "background": "linear-gradient(180deg, #161B22 0%, #0D1117 100%)",
                    "text_align": "center",
                    "max_width": "800px"
                }
            },
            {
                "name": "FeatureCard",
                "type": "container",
                "specs": {
                    "icon_size": "48px",
                    "title_size": "20px",
                    "grid_columns": "repeat(auto-fit, minmax(280px, 1fr))"
                }
            }
        ]
    
    def _generate_design_system(self) -> Dict[str, Any]:
        """Generate design system specifications."""
        return {
            "colors": {
                "primary": {
                    "main": "#58A6FF",
                    "light": "#79B8FF",
                    "dark": "#388BFD"
                },
                "secondary": {
                    "main": "#A371F7",
                    "light": "#BC8CFF",
                    "dark": "#8957E5"
                },
                "accent": {
                    "main": "#3FB950",
                    "light": "#56D364",
                    "dark": "#238636"
                },
                "neutral": {
                    "bg_dark": "#0D1117",
                    "bg_card": "#161B22",
                    "bg_elevated": "#21262D",
                    "border": "#30363D",
                    "text_primary": "#F0F6FC",
                    "text_secondary": "#8B949E"
                },
                "status": {
                    "success": "#3FB950",
                    "warning": "#D29922",
                    "error": "#F85149",
                    "info": "#58A6FF"
                }
            },
            "typography": {
                "fonts": {
                    "primary": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
                    "mono": "JetBrains Mono, monospace"
                },
                "sizes": {
                    "h1": "32px",
                    "h2": "24px",
                    "h3": "20px",
                    "body": "16px",
                    "small": "14px",
                    "caption": "12px"
                },
                "weights": {
                    "regular": 400,
                    "medium": 500,
                    "semibold": 600,
                    "bold": 700
                }
            },
            "spacing": {
                "unit": "4px",
                "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96]
            },
            "effects": {
                "shadows": {
                    "sm": "0 1px 2px rgba(0, 0, 0, 0.3)",
                    "md": "0 4px 12px rgba(0, 0, 0, 0.4)",
                    "lg": "0 8px 24px rgba(0, 0, 0, 0.5)"
                },
                "transitions": {
                    "fast": "150ms ease",
                    "normal": "250ms ease",
                    "slow": "400ms ease"
                },
                "animations": {
                    "pulse": "pulse 2s infinite",
                    "fade_in": "fadeIn 300ms ease"
                }
            }
        }


# Register the agent
AGENT_REGISTRY["designer"] = DesignerAgent
