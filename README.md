# Instagram Follower Management Tool
This project is a Python-based application that automates interactions with Instagram to help users analyze their follower and following lists. It provides a simple, user-friendly interface to log in, fetch follower data, and identify accounts that the user follows but do not follow back. The tool operates in a headless browser environment using Selenium and presents results through a GUI built with Tkinter.

### Key Features
-Automated Login: Securely log in to Instagram by providing a username and password.
-Data Fetching: Retrieve followers and following lists in real-time.
-Unfollow Analysis: Identify accounts that you follow but are not following you back.
-Headless Browser: Operates in the background without displaying the browser window, making it efficient and unobtrusive.
-Graphical User Interface (GUI): An intuitive Tkinter-based interface for easy interaction.

### How It Works
-Login: Enter your Instagram credentials through the GUI. The tool securely logs you into your account.
-Data Collection: It navigates to your followers and following pages, scrolling through the lists to collect all account data.
-Comparison: The tool compares the lists to determine which accounts are not following you back.
-Results Display: Presents the analysis in a clear and concise message, showing the total followers, total following, and the list of non-reciprocal accounts.
