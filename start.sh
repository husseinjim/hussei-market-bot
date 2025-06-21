#!/bin/bash

# Run Python bot in the background
python3 bot.py &

# Run Twitter fetcher
node getTwitterTrends.js
