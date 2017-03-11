# Similar-Shooter
Find basketball players with similar shot charts

# Examples

A live version of this flask app can be seen at: https://similar-shooter.herokuapp.com/.  Note, I am not paying anything to host this, so it could take forever to run...

Here are some static examples, though.

Who is most similar to **DeAndre Jordan**? Top shot-chart match: **Rody Gobert**
![Jordan](http://i.imgur.com/dB6cT2s.png?1)
![Gobert](http://i.imgur.com/Lt64djC.png?1)

Who is most similar to **Buddy Hield**? Top shot-chart match: **Tim Hardaway**
![Hield](http://i.imgur.com/yfHK0kL.png?1)
![Hardaway](http://i.imgur.com/BzG8mBI.png?1)

# How does it work?

I played around with a lot of different algorithms to define what makes shot charts similar.  It's an interesting question: **what does it mean for two shot charts to be similar?**

I made the following assumptions:
* If two shot charts are the exact same, but with different densities, they are still very similar.  Players with different usage rates shouldn't be penalized as being different.
* The most important features are distance from the hoop, and 2PT vs 3PT shots.  I largely disregard things like which side of the court players shoot from.

Using these assumptions, I compare the [Kullback-Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) of each players shot distributions.  Players with low KL divergence have high similarity.

# What data are used?

Shot data and shot charts are scrapped seperately (design flaw).  These data were scraped March 7 2017, so they contain data from the 2017 season up until this data.  

To get up-to-date data, rerun `scraper/scraper.py` and `shotchart/shotchart.py`.

To get historic data, change global parameter `YEAR` before scraping.


