<div align="center">
<img src="catalog/static/images/logo.png" alt="NotInk Logo" style="height: 90px; display: block; margin: 0 auto"/>
<h1>LocalLibrary (Reader)</h1>
</div>


## Overview
Reader is a project that allows anonymous users to view a list of available books on the homepage and search for books based on title, author, or summary. If an anonymous user wants to borrow a book, they are redirected to the login page. Logged-in users can borrow books from the available collection. On the project, admin users have additional privileges to manage authors, books, and renewals.

The app is also tested extensively, making sure most parts of the app behave as expected.

<p><strong> Live link </strong></p>

Follow the link below to view the deployed version of the app
[Live](https://reader-production-eb1.up.railway.app/catalog/)

## Reader Preview
![Reader_Home_Page](https://raw.githubusercontent.com/DanAdewole/LocalLibrary/main/catalog/static/images/home-page.jpg)

<p>The page fro logged in users to borrow books.</p>

![Reader_Borrow-page](https://raw.githubusercontent.com/DanAdewole/LocalLibrary/main/catalog/static/images/borrow-page.jpg)

<p>The admin users have the permission to add books and add authors to the site, they can also renew book instances for the user.</p>

![Reader_Add_author_Page](https://raw.githubusercontent.com/DanAdewole/LocalLibrary/main/catalog/static/images/home-page.jpg)


## Getting Started with the Project
* First clone this repository from Github to your local machine
```
git clone https://github.com/DanAdewole/LocalLibrary.git
```

* Change your directory to where you cloned the repository
```
cd localLibrary
```

* Create a virtual environment in the localLibrary Directory
```
python -m venv .\venv
```

* Activate the virtual environment
```
venv\scripts\activate
```
Note: Upon running the command **venv\scripts\activate**, if this error shows up:
```
venv\scripts\activate : File C:\Users\Training\Documents\New folder\venv\scripts\Activate.ps1 cannot be loaded because running scripts is 
disabled on this system. For more information, see about_Execution_Policies at http://go.microsoft.com/fwlink/?LinkID=135170.
```
Run this command: 
``` 
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted 
```
Then run the command to activate the virtual environment

* Install all the necessary packages
```
pip install -r requirements.txt
```

* Make migrations
Run the following commands separately to make migrations
```
python manage.py makemigrations
python manage.py migrate
```

* Create a new superuser
Run the following command to create a new superuser
```
python manage.py createsuperuser
```

Update debug settings in the project settings file
Go to **locallibrary/settings.py** and change DEBUG to True
```
DEBUG = True
```

* Run the project
```
python manage.py runserver
```


