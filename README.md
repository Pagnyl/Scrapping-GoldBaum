# Scrapping-GoldBaum
Software made for an intership's test for a company call GoldBaum


HOW TO RUN :

	1- To run the program called 'Data_ETF.py' you must have Chrome 

	2- Then, download a ChromeDriver at this address : 'https://chromedriver.chromium.org/' 
  which correspond to your Chrome versions.

	3- Put the .exe at the root of your Python IDE

	4- To run the programm, be aware that you have to run the script, not the file

HOW TO USE :

When you run the script a window appear and you have to choose which ETF you want to see ( notice that you can open each one individually. )

Then you have an interface where there are static data that I have choose in a table, the two main dynamic data in my opinion ( NAV et AUM ), and two button : the red one to quit the window
the green one to get the information of the different ETF.

If you want to get data, it will open a chrome page (you don't have to touch anything on the webpage), pass the first page and when it's passed the page is closed and the data is load in a .csv file in the folder 'File'.

HOW TO IMPROVE :

 - Wait to have better plot with more point
 - Complete the static data for Invesco
 - Find solution to have date on the X-axis for Invesco 
 - Use reactJS instead of tkinter to show value 
 - Use a library to run the script everyday, to get data automatically.
