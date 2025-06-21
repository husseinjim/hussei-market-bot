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

// Get top trending topic worldwide
T.get('trends/place', { id: 1 }, function(err, data, response) {
  if (err) {
    console.error("Twitter error:", err);
    return;
  }

  const trends = data[0].trends.slice(0, 5); // Get top 5 trends
  trends.forEach((trend, index) => {
    console.log(`${index + 1}. ${trend.name}`);
  });
});
