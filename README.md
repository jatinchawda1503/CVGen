# Cover Letter Generator

## Overview

This application is a Chrome extension that helps you to gerate cover letter instantly without switching from application to another. 

## Installation

### Chrome Extension

1. Navigate to `chrome://extensions` in your Chrome browser.
2. Enable Developer mode by ticking the checkbox in the upper-right corner.
3. Click on the "Load unpacked" button.
4. Select the `plugin` directory from your project.

### Backend Setup

1. Navigate to the `backend` directory.
2. Upgrade pip by running `python -m pip install --upgrade pip`.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Start the application by running `python app.py`.

## Configuration

To configure the application, you need to set the OpenAI API key in the `.env` file:

1. Copy the `.env.example` file and rename it to `.env`.
2. Open the `.env` file and replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

