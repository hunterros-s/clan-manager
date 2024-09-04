# Clash of Clans Clan Manager

Welcome to the Clash of Clans Clan Manager project! This project is designed to provide a comprehensive management tool for Clash of Clans clan administrators. The application consists of two main components: the Clan Manager front-end and the Data Server back-end. Together, they provide real-time updates and analytics for clan members, utilizing Flask for the front-end and coc.py for interfacing with the Clash of Clans API.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip`

### Steps

1. Clone the repository:
    ```bash
    git clone git@github.com:hunterros-s/clan-manager.git
    cd clan-manager
    ```

2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables for the Data Server:
    ```bash
    export CLAN_TAG=YOUR_CLAN_TAG_HERE
    export DEV_SITE_EMAIL=YOUR_DEV_SITE_EMAIL
    export DEV_SITE_PASSWORD=YOUR_DEV_SITE_PASSWORD
    ```

## Usage

### Running the Data Server
```bash
./bin/dataserver start
```
Check the status with:
```bash
./bin/dataserver status
```
Stop the server with:
```bash
./bin/dataserver stop
```

### Running the Clan Manager Front-End
For development:
```bash
./bin/clanmanager start
```
For production:
```bash
./bin/clanmanager_prod
```

## Project Structure

```
.
├── README.md
├── bin
│   ├── clanmanager
│   ├── clanmanager_prod
│   └── dataserver
├── clanmanager
│   ├── __init__.py
│   ├── config.py
│   ├── model.py
│   ├── setup.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── images
│   │       ├── profile.svg
│   │       └── shield.svg
│   ├── templates
│   │   ├── index.html
│   │   └── member.html
│   ├── utils.py
│   └── views
│       ├── __init__.py
│       ├── index.py
│       ├── member.py
│       └── render_superlatives.py
├── clanmanager.pem
├── dataserver
│   ├── cocapi.py
│   ├── main.py
│   ├── model.py
│   ├── server.py
│   └── shared.py
└── requirements.txt
```

## Features

### Real-Time Clan and Member Updates

The data server handles real-time updates of clan and member data using coc.py. It automatically updates clan metrics, member activity, contributions, and other relevant statistics.

### Graphical Representation

Using Plotly.js, the project displays detailed graphs and statistics for each member. Historical data such as trophies, donations, and war stars are visualized, providing a clear and insightful view of a member’s performance over time.

### Superlatives

The project highlights top-performing clan members in various categories like "Supreme Conqueror" (most attacks won), "Trophy Maestro" (most trophies), and "Philanthropic Patron" (most troops donated). Superlatives are computed based on a 2-week time span.

### Web Interface

Leverages Flask to provide a responsive and intuitive web interface for viewing clan and member data. Includes detailed member profiles, clan descriptions, and superlative awards.
