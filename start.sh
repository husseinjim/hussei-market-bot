#!/bin/bash

# Start the Python bot
python3 bot.py &

# Start the Twitter trends fetcher
node getTwitterTrends.js
