# Printify Pilot

This repository collects scripts and experiments for working with the Printify API.  It now contains a variety of helper utilities for generating images, interacting with Printify, and reviewing product data.

## Installation

Create a virtual environment and install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

Run the setup script to save your API keys in `config.py`:

```bash
python setup.py
```

## Status

The project is still a work in progress and the tools are provided as-is.

## Unified command interface

Use `toolkit.py` to launch any of the available utilities from a single entry
point:

```bash
python toolkit.py <command>
```

Available commands include `data-viewer`, `tshirt-automation`,
`blueprint-review`, `product-reviewer`, `awakening-shirt`,
`google-upload`, `fetch-products` and `creator-portal`.

## Webpack Frontend

The `webpack-app` directory contains a small React application that fetches
product data from the Flask backend.

### Setup

Run the convenience script to install dependencies and launch both the Flask
backend and the React development server:

```bash
./start.sh
```

This starts the backend on `http://localhost:5000` and serves the frontend at
`http://localhost:8080`.

If you prefer to build the frontend manually:

```bash
cd webpack-app
npm install
npm run build
```

This creates `webpack-app/dist` containing the compiled bundle. Start the Flask
backend (`python app.py`) and open `dist/index.html` or use `npm start` for
live development.

## Creator Portal

The `creator_portal` directory implements a new FastAPI backend with modular
agents for parsing blueprints, generating prompts and metadata, and optionally
creating products on Printify. Launch it with:

```bash
python toolkit.py creator-portal
```

## Roadmap

A list of upcoming features is maintained in [roadmap.md](roadmap.md).
Contributions and feedback are welcome!
