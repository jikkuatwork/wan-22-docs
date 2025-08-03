#!/usr/bin/env python3

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def serve_docs(port=8080):
    """Serve the HTML documentation locally"""
    
    docs_dir = Path("../docs")
    if not docs_dir.exists():
        print("❌ docs directory not found. Please run generate_html_docs.py first.")
        return
    
    # Change to docs directory
    os.chdir(docs_dir)
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌐 Serving WAN 2.2 Documentation at http://localhost:{port}")
            print(f"📁 Serving from: {docs_dir.absolute()}")
            print(f"🔍 Access the documentation at: http://localhost:{port}/index.html")
            print(f"⏹️  Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{port}/index.html")
                print(f"🚀 Opened documentation in your default browser")
            except:
                print(f"💡 Please open http://localhost:{port}/index.html in your browser")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python3 serve_docs.py --port 8081")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] == "--port" and len(sys.argv) > 2:
                port = int(sys.argv[2])
            else:
                port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8080.")
    
    serve_docs(port)