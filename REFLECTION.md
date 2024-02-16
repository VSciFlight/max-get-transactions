# Reflection

>__*"The way is more important than the outcome"*__

## Difficulties in the project:

1. Max is a closed system which doesn't support open-banking methods so any try to access it without the user himself is unwanted.
2. Max doesn't support API for private accounts (they do have API for businesses)
3. Locators in the website are obscure and not clear or unique when it comes to dates selections.
4. First time using CLI command with arguments to do different tasks which may require different parameters
5. Max's limits
6. Security with uploading to git
7. Python best practices
8. Testing a CLI program

## Solutions

1. At first I needed to think a way around so I will have to access the website using my user credentials. I did similar things with Selenium so I decided to go ahead and use it. Max allows a user login with 2 methods:
    1. One time SMS code which requires ID and bank account or last eight digits of credit card.
    2. Email and Password.

    since option 1 requires user involvement through the process I decided to go with option 2
2. I accidentally asked for the API for business and got a phone call from Max themselves telling me about it. At that time I spoke with them the customer support told me that the API currently under maintenance and doesn't answer my request - it cannot extract data from my personal account.
3. Collecting locators may be the fun thing at the start of the project. Using the browser DevTools I extracted the locators with xPath and then cleaned them to match my exact locator. The main difficulties were their attributes which sometimes were multiple elements for the same locator so I had to improvise and be more specific about them. Selecting the first element the locator answer, selecting by text... <br>
When I got to the point I needed to search transactions by range I couldn't find the right locators as they weren't unique anymore and selecting specific dates became a mess. Some time later I noticed the URL parameters (GET request) was based on the range I was looking for. I have been looking at it more and tried more until I understood how it worked. Using that information I found a better and faster way to get to my transactions using URL method instead the buttons.
4. This was the first project I used flags within a CLI program. It was nice and felt like magic when it happened properly. I had to go through naming flags and their funcionalities. Filtering and making sure they are in the correct format so the program won't crash for this particular reason.
5. Max has its own limitations within their website when it comes to transactions information. For example I can view this month next year under month view but not under range view. When I tried to do so it showed me an error box. I wanted to deny the option to get into this view from the first place so I built filter to allow only the dates that can be proceeded properly. In case where the user tries to enter a date that doesn't match the program will show the error and asks the user to try again.
6. At the start of the project I didn't know exactly where it will end and only at about the end I thought about uploading it to GitHub and share it with others. I hard-coded credentials for testing methods which later was forgotten. Later I tried to rebase but decided to transfer my files to a new repository as needed.
7. Since I decided to share the repository with others I had to make sure repository is readable, written properly and follows best practices.
I used Pylint to lint the repository and fix issues it rose.
8. The program runs with the CLI with flags and arguments. The testing practice was to run the project with different parameters. It is small projects which can be devided into two parts:
    1. When user tries wrong parameters to test the filtering methods of the program.
    2. When user enters correct parameters so the selenium driver will run and then test the program results (the CSV file).

    In order to test a program that runs on CLI I had to use python subprocess to run the program aside the testing process. The tests related to the filtering relied on raised exceptions messages from the program (stderr). The tests related to the successfull cases of the program relied on the file created and its information.

    Using pytest to sharpen the results and then be extracted to other formats and analysis tools such as Allure.


## Conclusion

In my head at start I thought it would be easy and fast solution to my need. When I started to develop I stumbled upon things I didn't think about such as going to a specific date. The solutions I found were good enough for me to work with and yielded my expectations. I sharpened my skills related to python development and testing and hopefully Max won't be mad at me for creating this tool.

## Future?

Ideas for continues development:

- GUI
- Analysis tools for the data
- Making it faster
