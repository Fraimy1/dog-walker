# Dog walker project

This is a small project I am using to practice Docker (You don't have to write anything related to docker, that's my job).

In the first stage of development there will be just two components
1. Telegram bot in python using AIogram library
2. SQLite database using SQLAlchemy for native python support

File structure:
- src/bot/file1 ... file2 etc. Each file should be responsible for its own functionality
- data/database

Functionality: 
    bot:
        - When you open an app you press the regular button to start, then you use the buttons above your keyboard (one of two types of buttons you can add to telegram)
        - There is only one main button that will log that you "username" walked the dog
        - On backend it will log it into database and put a timer for 5 minutes. 
        - On frontend you'd be presented with buttons like "Didn't poop" "Long walk" and "Send". 
        - Then either if the button "Send" was pressed or the time has passed, we update the database value with the parameters if they were changed. 
        - Then a message to all members is sent that "username: <username> has walked the dog at <time when the message was sent>." +  "Additional parameters:" if they selected anything from the options/buttons
        - Database of course should track all of these options. 

Additional notes:
    - Use all the best practices for code style and project style e.g. keep a clear database structure etc.
