// getTwitterTrends.js
const TwitterTrends = require('twittertrendsapi.js');

(async () => {
  const tt = new TwitterTrends({ expire: 15 * 60 * 1000 });
  const topics = await tt.getTopics({ id: '1', limit: 5 });  // Worldwide trends
  topics.forEach(t => console.log(t.name));  // prints trending topic names
})();
