# alexa-lol-esports-skill
alexa-lol-esports-skill

This project uses an Alexa skill that triggers Lambda to give the user information about League of Legends League
Championship Series (LCS) matches.  It is not affiliated with nor endorsed by Riot Games or LoL eSports in any way.

This is just a project that I wanted to run when I needed to find out when Cloud 9 played, and it's evolving as we go.

Expected features/roadmap:

1. Ask Alexa when NA LCS teams play for 2018 Summer Split only. Uses LoL eSports API. Times in PDT only. DONE

2. Speed up the response by storing the match info for each team's next four matches in S3 bucket. DONE

3. Develop python script to pull API data and update DynamoDB on demand. DONE

4. Store match data in a database and query as needed. DONE

5. Develop Lambda function to pull API data weekly and update Dynamo DB.
-- It turns out that Riot doesn't update the team "nextScheduled" field after the game, so I'm unable to use that as a
-- field. Instead, I will just check if the next match is scheduled for before today, and if so, move to the next scheduled item.
--DONE

6. Ask Alexa when EU LCS teams play for 2018 Summer Split only. -- DONE

7. Have Alexa give match time in REQUESTED (not local) time zone.
--Getting the user's time zone is difficult.  I can support asking for a specific timezone right now, but
--I'll have to work on being able to set the timezone as a variable (perhaps in a customer database?) - In Progress, testing

8. Lambda timing out on updating DDB.  No errors, just taking too long to get through the whole thing.  -- DONE
-- I need to split this into a handler function that queues leagues/teams and a second function that pulls each
-- team/league and updates it.
-- I switched to a handler function that creates SQS messages for each team/league to update.  The SQS messages will
-- trigger another function that updates each team individually.  This has removed the time out issue.

9. Store data for 2018 Summer Split Playoffs.

10. Add opponent to data.

11. Ask Alexa when all region teams play for 2018 summer split only.

12. Develop script to create and fill DynamoDB table.

13. Use datetime.isoformat() instead of multiple formats.