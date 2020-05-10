# txtLab-music

This repository contains code used for .txtLAB @ McGill's research on Spotify's playlist curation process.

The root folder is organized in the following fashion:
- `/analysis`: folder with Python scripts and Jupyter notebooks used for analysis of the data.
- `/scraping`: folder with Python scripts to scrape Spotify's API and Chartmetric. This folder contains its own README with scraping instructions.
- `/spotify_data`: a copy of all of the scraped Spotify data from the scraping folder. This folder is referenced by scripts in `/analysis`.
- `/billboard_data`: a copy of all of the scraped Billboard data from the scraping folder. This folder is also referenced by scripts in `/analysis`.
- `requirements.txt`: contains python packages needed for this project.
