# alexa-lol-esports-skill
alexa-lol-esports-skill

This project uses an Alexa skill that triggers Lambda to give the user information about League of Legends League
Championship Series (LCS) matches.  It is not affiliated with nor endorsed by Riot Games in any way.

This is just a project that I wanted to run when I needed to find out when Cloud 9 played, and it's evolving as we go.

Expected features/roadmap:

1. Ask Alexa when NA LCS teams play for 2018 Summer Split only. Uses LoL eSports API. Times in PDT only. DONE
2. Speed up the response by storing the match info for each team's next four matches in S3 bucket. DONE
3. Develop python script to pull API data and update DynamoDB on demand. DONE
4. Store match data in a database and query as needed. DONE
5. Develop Lambda function to pull API data weekly and update Dynamo DB.
-- It turns out that Riot doesn't update the team "nextScheduled" field after the game, so I'm unable to use that as a
-- field. Instead, I will just check if the next match is scheduled for before today, and if so, move to the next scheduled item.
6. Ask Alexa when EU LCS teams play for 2018 Summer Split only.
7. Have Alexa give match time in local time zone.
8. Ask Alexa when all region teams play for 2018 summer split only.
9. Develop script to create and fill DynamoDB table.
10. Store data for 2018 Summer Split Playoffs.
11. Use datetime.isoformat() instead of multiple formats.