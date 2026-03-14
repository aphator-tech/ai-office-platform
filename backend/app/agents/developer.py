from typing import Dict, Any, List
from app.agents.base import BaseAgent, AGENT_REGISTRY
import asyncio


class DeveloperAgent(BaseAgent):
    """Developer Agent - generates code and builds projects."""
    
    def __init__(self):
        super().__init__()
        self.agent_type = "developer"
        self.name = "Developer Agent"
        self.description = "Code generation, project building, and software development"
        self.icon = "💻"
    
    async def execute(self, task_id: str, title: str, description: str) -> Dict[str, Any]:
        """
        Execute development task.
        
        Steps:
        1. Analyze requirements
        2. Plan technical implementation
        3. Generate code structure
        4. Write code modules
        """
        await self._notify_update("working", "10%", "Analyzing technical requirements...")
        await asyncio.sleep(1.5)
        
        # Determine project type
        project_type = self._determine_project_type(title, description)
        
        await self._notify_update("working", "25%", f"Planning {project_type} implementation...")
        await asyncio.sleep(1.5)
        
        await self._notify_update("working", "40%", "Generating project structure...")
        await asyncio.sleep(1.5)
        
        # Generate project structure
        project_structure = self._generate_structure(title, project_type)
        
        await self._notify_update("working", "60%", "Writing code modules...")
        await asyncio.sleep(1.5)
        
        # Generate code files
        code_files = self._generate_code(title, description, project_type)
        
        for i, file in enumerate(code_files):
            progress = 60 + (i * 25 // len(code_files))
            await self._notify_update("working", f"{progress}%", f"Writing: {file['name']}...")
            await asyncio.sleep(1)
        
        await self._notify_update("working", "90%", "Finalizing project setup...")
        await asyncio.sleep(1)
        
        await self._notify_update("completed", "100%", "Development complete")
        
        return {
            "status": "success",
            "project_type": project_type,
            "structure": project_structure,
            "files": code_files,
            "summary": f"Generated {project_type} with {len(code_files)} files"
        }
    
    def _determine_project_type(self, title: str, description: str) -> str:
        """Determine the type of project to build."""
        combined = f"{title} {description}".lower()
        
        if "landing page" in combined or "website" in combined:
            return "website"
        elif "api" in combined:
            return "api"
        elif "app" in combined or "application" in combined:
            return "webapp"
        elif "script" in combined:
            return "script"
        else:
            return "website"
    
    def _generate_structure(self, title: str, project_type: str) -> Dict[str, Any]:
        """Generate project directory structure."""
        if project_type == "website":
            return {
                "root": "/",
                "files": [
                    {"path": "index.html", "type": "file"},
                    {"path": "styles.css", "type": "file"},
                    {"path": "script.js", "type": "file"},
                    {"path": "README.md", "type": "file"}
                ]
            }
        elif project_type == "webapp":
            return {
                "root": "/",
                "files": [
                    {"path": "src/index.js", "type": "file"},
                    {"path": "src/App.js", "type": "file"},
                    {"path": "src/components/", "type": "directory"},
                    {"path": "public/index.html", "type": "file"},
                    {"path": "package.json", "type": "file"}
                ]
            }
        else:
            return {
                "root": "/",
                "files": [
                    {"path": "main.py", "type": "file"},
                    {"path": "requirements.txt", "type": "file"},
                    {"path": "README.md", "type": "file"}
                ]
            }
    
    def _generate_code(self, title: str, description: str, project_type: str) -> List[Dict[str, Any]]:
        """Generate code files."""
        if project_type == "website":
            return [
                {
                    "name": "index.html",
                    "language": "html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + title + """</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">""" + title + """</div>
            <ul class="nav-links">
                <li><a href="#features">Features</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <h1>""" + title + """</h1>
            <p>""" + description[:100] + """</p>
            <button class="cta-button">Get Started</button>
        </section>
        
        <section id="features" class="features">
            <h2>Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>Feature 1</h3>
                    <p>Description of feature 1</p>
                </div>
                <div class="feature-card">
                    <h3>Feature 2</h3>
                    <p>Description of feature 2</p>
                </div>
                <div class="feature-card">
                    <h3>Feature 3</h3>
                    <p>Description of feature 3</p>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 """ + title + """. All rights reserved.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "styles.css",
                    "language": "css",
                    "content": """/* Global Styles */
:root {
    --primary-color: #58A6FF;
    --secondary-color: #A371F7;
    --bg-dark: #0D1117;
    --bg-card: #161B22;
    --text-primary: #F0F6FC;
    --text-secondary: #8B949E;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-primary);
    line-height: 1.6;
}

header {
    padding: 1rem 2rem;
    background-color: var(--bg-card);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 100;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary-color);
}

.hero {
    padding: 8rem 2rem 4rem;
    text-align: center;
    background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-dark) 100%);
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem;
}

.cta-button {
    padding: 1rem 2rem;
    background-color: var(--primary-color);
    color: var(--bg-dark);
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(88, 166, 255, 0.3);
}

.features {
    padding: 4rem 2rem;
}

.features h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 3rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.feature-card {
    background-color: var(--bg-card);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid #30363D;
    transition: transform 0.2s;
}

.feature-card:hover {
    transform: translateY(-4px);
}

.feature-card h3 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.feature-card p {
    color: var(--text-secondary);
}

footer {
    padding: 2rem;
    text-align: center;
    color: var(--text-secondary);
    border-top: 1px solid #30363D;
}"""
                },
                {
                    "name": "script.js",
                    "language": "javascript",
                    "content": """// Main JavaScript for """ + title + """
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // CTA button interaction
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', () => {
            alert('Thank you for your interest! We will be in touch soon.');
        });
    }
    
    // Add scroll effect to header
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.3)';
        } else {
            header.style.boxShadow = 'none';
        }
    });
    
    console.log('""" + title + """ - Loaded successfully');
});"""
                }
            ]
        else:
            return [
                {
                    "name": "main.py",
                    "language": "python",
                    "content": f'''"""Main application file for {title}"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="{title}")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int = 1

@app.get("/")
async def root():
    return {{"message": "Welcome to {title}"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
                }
            ]


# Register the agent
AGENT_REGISTRY["developer"] = DeveloperAgent
