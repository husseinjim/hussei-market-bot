// getTwitterTrends.js
const Twit = require('twit');

const T = new Twit({
  consumer_key:         process.env.TWITTER_CONSUMER_KEY,
  consumer_secret:      process.env.TWITTER_CONSUMER_SECRET,
  access_token:         process.env.TWITTER_ACCESS_TOKEN,
  access_token_secret:  process.env.TWITTER_ACCESS_SECRET,
  timeout_ms:           60 * 1000,
  strictSSL:            true,
});

// Fetch worldwide Twitter trends (WOEID 1)
T.get('trends/place', { id: 1 }, function (err, data, response) {
  if (err) {
    console.error('Twitter API error:', err);
  } else {
    const topTrend = data[0].trends[0].name;
    console.log('Top trend:', topTrend);
  }
});
