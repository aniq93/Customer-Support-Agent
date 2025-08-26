import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our API routes
from intelligagent.api import users, tickets

app = FastAPI(title="IntelliAgent", version="0.1.0")

# Include our API routers
app.include_router(users.router)
app.include_router(tickets.router)

@app.get("/")
async def root():
    return {"message": "Hello from IntelliAgent!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test-groq")
async def test_groq():
    """Test endpoint to verify Groq configuration"""
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=400, 
            detail="Groq API key not configured. Please set GROQ_API_KEY in your .env file"
        )
    
    return {
        "message": "Groq API key is configured!",
        "api_key_length": len(groq_api_key),
        "api_key_preview": f"{groq_api_key[:8]}..."
    }

@app.get("/env-info")
async def env_info():
    """Show current environment configuration"""
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": os.getenv("PORT", "8000"),
        "debug": os.getenv("DEBUG", "false"),
        "groq_configured": bool(os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "your_groq_api_key_here")
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Starting IntelliAgent server...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🔑 Groq API Key: {'✅ Configured' if os.getenv('GROQ_API_KEY') and os.getenv('GROQ_API_KEY') != 'your_groq_api_key_here' else '❌ Not configured'}")
    
    if debug:
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        uvicorn.run(app, host=host, port=port)
