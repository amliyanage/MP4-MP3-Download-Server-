# YouTube Video Downloader Backend

This repository contains the backend server for the YouTube Video Downloader project. The server is built using Node.js and Express, and it utilizes `ytdl-core` to fetch video details from YouTube.

## Project Overview

- **Repository**: [MP4-MP3-Download-Server](https://github.com/amliyanage/MP4-MP3-Download-Server-.git)
- **Technology Stack**:
  - Node.js
  - Express
  - ytdl-core

## API Endpoint

### GET /video-options/:videoId

Fetches available formats and details for a given YouTube video ID.

- **Parameters**:
  - `videoId` (string): The ID of the YouTube video.

- **Response**:
  - `formats` (array): List of available video formats.
  - `bestQuality` (object): Information about the best quality format (e.g., 1440p).

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (Node Package Manager)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/amliyanage/MP4-MP3-Download-Server-.git
    cd MP4-MP3-Download-Server-
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the server:

    ```bash
    npm start
    ```

   The server will be running on [http://localhost:3001](http://localhost:3001).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests if you have improvements or suggestions. Please follow the contributing guidelines if applicable.

## Contact

For any questions or inquiries, please reach out to ashenmliyanage@gmail.com.
