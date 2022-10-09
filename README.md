# Abhi-YTscrapper
This project helps the user to scrape the useful information of a YouTube channel such as Video title, Subscriber, Latest videos links, its comments and views.
For front end, i used HTML, CSS and JAVASCRIPT to design the webpage.
For scrapping, I used SELENIUM and BEAUTIFULSOUP library of python. 
For webapp, i used FLASK framework of python.
For database, I used MYSQL and MONGOdb database to store the required information.

**Step 1**: _First enter the channel name in the input box as shown below and click the submit button._

![ytscrappermain](https://user-images.githubusercontent.com/95995839/194746698-688c1d6b-5d6c-4248-8d23-d35cbffef27a.PNG)

**Step 2**: _Once submit button clicked, selenium and Beautifulsoup start working their task that is scrapping the content of that YouTube channel. After scarpping, all the information are displayed on the webpage as shown below:_

![ytsecond display](https://user-images.githubusercontent.com/95995839/194746766-c95c15df-4429-49f9-a2f8-c31d2c4c6b6b.PNG)

![yt-3](https://user-images.githubusercontent.com/95995839/194746795-8861585a-4766-42cc-a77c-6bbb064b4ae8.PNG)

When You hover any card, a small white box appear below the car which shows the number of views that the channel have. Also, there is a small "view comments" button. When we click on this button, it will display the all comments of that particulr video. But right now, this button will not work as comments are not loaded yet.

**Step 3**: _There is "comment" button at the top. When I click on thi button, all the comments of each and every displayed video start scrapping one by one. This is a very time taking process. Once all the comments are scraped, it will be displayed using the HTML table as shown below. Now, i can also view the comments of any particular video by just cicking the view comments button below the displayed video._

![comment1](https://user-images.githubusercontent.com/95995839/194746823-eeb8bec8-ceed-4521-9c63-05f95f47e23c.PNG)

![comment2](https://user-images.githubusercontent.com/95995839/194746837-f988510c-148b-4fb8-9248-b8bb1805ba49.PNG)

Now everything is done, all the scrapped information will store in the MYSQL and MONGODB database.This means if someone tries to scrape the content of the same channel that already scraped, then this time the scrapper load the information from the database instead of scrapping all the things again from the internet. But suppose if someone wants to scrape the content again of the same YouTube channel, then there is a reload button. After clicking on this button, the scrapper start again scrapping the content and again the fresh data will stored in the databases.

One of the main challenge that I face in this project to scrape the comments of YT Shorts video because in YT Shorts video, we have to click on the comment button then a pop up box will appear which show all the comments of that YT Shorts comment. Keeping this issue in mind, I designed my code in such a way that is also scrape all the relevant information of the YT shorts video as well.

