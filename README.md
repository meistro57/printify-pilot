# Printify Pilot

This repository collects scripts and experiments for working with the Printify API.  It now contains a variety of helper utilities for generating images, interacting with Printify, and reviewing product data.

## Installation

Create a virtual environment and install the required Python packages:

```bash
pip install -r requirements.txt
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
`google-upload` and `fetch-products`.
