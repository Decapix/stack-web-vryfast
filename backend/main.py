import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", "8000")), log_level="info")
