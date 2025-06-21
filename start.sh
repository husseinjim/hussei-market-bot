#!/bin/bash

# Run Python bot in the background using python3
python3 bot.py &

# Run Node.js script
node getTwitterTrends.js
