import http.server
import socketserver
import yt_dlp as youtube_dl
import json
from urllib.parse import urlparse, parse_qs

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8').strip()

        # Ensure the URL doesn't have extra quotes
        youtube_url = post_data.strip('"')

        try:
            # Set up yt-dlp options to get info without downloading the file
            ydl_opts = {
                'skip_download': True,  # Don't download the video
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # Get video info without downloading
                video_info = ydl.extract_info(youtube_url, download=False)

            mp4_sizes = {}
            mp3_size_mb = None

            # Extract file sizes in bytes (may not always be available)
            if 'formats' in video_info:
                for fmt in video_info['formats']:
                    resolution = fmt.get('height')  # Get video resolution
                    if fmt.get('ext') == 'mp4' and fmt.get('vcodec') != 'none' and resolution:
                        # Convert video size to MB if available
                        filesize_bytes = fmt.get('filesize', 0)
                        filesize_mb = filesize_bytes / 1_048_576 if filesize_bytes else None
                        if filesize_mb:
                            mp4_sizes[f"{resolution}p"] = round(filesize_mb, 2)
                    elif fmt.get('ext') == 'm4a' and fmt.get('acodec') != 'none':
                        # Get audio size (MP3 equivalent)
                        mp3_size_bytes = fmt.get('filesize', 0)
                        mp3_size_mb = mp3_size_bytes / 1_048_576 if mp3_size_bytes else None

            # Build the response structure
            response_data = {
                "mp3": f"{round(mp3_size_mb, 2)} MB" if mp3_size_mb else None,
                "mp4": mp4_sizes
            }

            # Convert response to JSON format
            response_json = json.dumps(response_data)

            # Send response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_json.encode())
        except Exception as e:
            # Handle errors if URL is invalid or other exceptions occur
            error_message = json.dumps({"error": str(e)})
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_message.encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        youtube_url = query_params.get('url', [None])[0]
        format = query_params.get('format', [None])[0]

        if not youtube_url or not format:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_message = json.dumps({"error": "URL and format are required"})
            self.wfile.write(error_message.encode())
            return

        try:
            # Set up yt-dlp options to get info without downloading the file
            ydl_opts = {
                'skip_download': True,  # Don't download the video
                'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best'
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # Get video info without downloading
                video_info = ydl.extract_info(youtube_url, download=False)

            if format == 'mp3':
                # Extract the download link for MP3
                formats = video_info.get('formats', [])
                for fmt in formats:
                    if fmt.get('ext') == 'm4a' and fmt.get('acodec') != 'none':
                        download_link = fmt.get('url')
                        response_data = {
                            "response": download_link
                        }
                        break
                else:
                    response_data = {"error": "MP3 format not found"}
            elif format in ['1440p', '1080p', '720p', '480p', '360p']:
                # Extract the download link for MP4
                formats = video_info.get('formats', [])
                for fmt in formats:
                    if fmt.get('height') == int(format.replace('p', '')) and fmt.get('ext') == 'mp4':
                        download_link = fmt.get('url')
                        response_data = {
                            "response": download_link
                        }
                        break
                else:
                    response_data = {"error": "MP4 format not found"}
            else:
                response_data = {"error": "Unsupported format or resolution"}

            # Convert response to JSON format
            response_json = json.dumps(response_data)

            # Send response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_json.encode())
        except Exception as e:
            # Handle errors if URL is invalid or other exceptions occur
            error_message = json.dumps({"error": str(e)})
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_message.encode())

# Start the server
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
