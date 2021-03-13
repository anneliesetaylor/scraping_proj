
# JOU4364: web-scraping-project
## Scraping Rotten Tomatoes and Box Office Mojo

For this project, I scraped the Rotten Tomatoes list of the [Top 100 Movies of All Time](https://www.rottentomatoes.com/top/bestofrt/) to compare the stats of some of the best movies to have been produced. My goal with this project was to compare each movie's Tomatometer score and Audience score after noticing that multiple films on the list with high Tomatometer scores lacked the same level of positive feedback from viewers, given their significantly lower Audience scores. I wanted to compare these two metrics in hopes of discovering whether this is a trend across all highly rated movies, or just the few that I happened to find. I also decided to incorporate each film's production budget and worldwide box office earnings, gathered from [Box Office Mojo](https://www.boxofficemojo.com/), since I thought that data could aid in understanding why certain movies rank higher than others or received better ratings (in the aspect of the film being higher quality or having a noticeably higher production value.)

I think that this data could explain whether critics collectively give movies higher ratings as a result of their more holistically evaluative approach when watching them, or if everyday viewers possibly have higher expectations and are more critical than the experts.


## Data Points Collected:

-	Title
-	Release year
-	Tomatometer score, in percentage
-	Audience score, in percentage
-	Production budget (denoted as ‘budget’ on Box Office Mojo website)
-	Worldwide box office earnings


## Scraping Process:

First, I used the [Top 100 Movies of All Time](https://www.rottentomatoes.com/top/bestofrt/) webpage to generate two lists: rt_movie_titles, holding all the movies' titles and release years, and rt_movie_links, holding each movie's partial URL to its specific Rotten Tomatoes page. I scraped each movie's partial URL so that I would be able to use them to later scrape each film's Tomatometer score and Audience score.
  - See get_titles_from_rt(url) and get_links_from_rt(url) functions

Then, I used that list of partial URLs in conjunction with Selenium to visit each movie's unique Rotten Tomatoes page and scrape both the film's Tomatometer score and Audience score. I did end up having to do these as two different functions, which I will explain more in depth down below, but doing so enabled me to get two distinct lists of each metric: tomatometer_scores, holding all the films' Tomatometer scores, and audience_scores, holding all the films' Audience scores.
  - See scrape_tm_scores(movie_partials) and scrape_aud_scores(partialurls) functions

Next, I focused on using the [Box Office Mojo](https://www.boxofficemojo.com/) site to search each film for its production budget and worldwide box office earnings. Using Selenium and the list of movie titles I already acquired from Rotten Tomatoes, I automated my browser to search each movie title with release year on the site, click the first search result, and then scrape the page for my last two data points: production_budget and ww_boxoffice. As I tested this code, I discovered that some of the titles from the Rotten Tomatoes page did not match the exact title the film was filed under on the Box Office Mojo site. To rectify this issue and avoid my code from terminating every time these particular titles were searched, I made a list of them myself and wrote conditional statements within the function's for loop to either search a different spelling of the title, or search for the film without its release year included in the search.
  - See scrape_wwbo(titles) and scrape_movie_budget(movietitles) functions.

Lastly, I created a new CSV file that, using the function def write_csv(), took each list I had acquired and matched each film to its accompanying stats before capturing the data in the file.

## Obstacles Faced:

Aside from occasionally struggling to determine what HTML element I needed to scrape to obtain the specific data points I wanted, the only major obstacle I faced was struggling to get my code to completely run. After testing each function individually before gradually combining them together to make a cohesive program, I realized that I was sending too many requests to the Rotten Tomatoes webpage in rapid succession and was being met with 'HTTP error 504' as a result of it. Since I scraped each film's Tomatometer score and Audience score in two separate functions, I was sending 200 requests to the Rotten Tomatoes site in the span of roughly 20 minutes and was most likely being rejected by the site for doing so. Therefore, I decided to reorganize my code to start with scraping the Tomatometer scores first before switching over to scraping Box Office Mojo to give the Rotten Tomatoes site a break before I needed to scrape the films' Audience scores. This allowed my code to run through completely, rather than terminating thanks to a Gateway Timeout.
