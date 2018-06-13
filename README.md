# alexa-lol-esports-skill
alexa-lol-esports-skill

This project uses an Alexa skill that triggers Lambda to give the user information about League of Legends League
Championship Series (LCS) matches.  It is not affiliated with nor endorsed by Riot Games in any way.

This is just a project that I wanted to run when I needed to find out when Cloud 9 played, and it's evolving as we go.

Expected features/roadmap:

1. Ask Alexa when NA LCS teams play for 2018 Summer Split only. Uses LoL eSports API. Times in PDT only. DONE
2. Speed up the response by storing the match info for each team's next four matches in S3 bucket. DONE
3. Ask Alexa when EU LCS teams play for 2018 Summer Split only. Uses S3 bucket. Times in PDT only.
4. Have Alexa give match time in local time zone.
5. Develop Lambda function to pull API data weekly and update S3 bucket data.
6. Store match data in a database and query as needed.
7. Ask Alexa when LCK teams play for 2018 Summer Split only. Uses database.
