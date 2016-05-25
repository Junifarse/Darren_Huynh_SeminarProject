Author: Darren Huynh
Credits: SeaofBTC

Overview:
	This inventory program is written in Python 2.7, and uses SQLite3 for database management, and TkInter for user interface. Functions are written in Python to execute SQL commands to communicate with the SQL database, which are called upon button press in the GUI. The program includes a self created Database upon initial usage, and generates a changelog as well. 
Technical Description:
	The program consists of multiple frames (pages henceforth) that have data entry fields for accessible user interaction. User input is collected upon user interaction( entering data, selecting options, button presses), and used in functions that execute included functions (create, edit , view) by passing said input into SQL execute statements (Insert, Update, Select). Widgets are appropriately placed and labeled for easy navigation via Grid/Pack widget management. A summary page is dynamically created upon request, such that it includes all changes made to the database upon creation. An admin delete function is included for deleting entries, which is username and password protected. All transactions are logged within the included changelog.txt file. 
