# Web Blog
Basic WebBlog web applicaiton using Bootstrap for frontend and Django for backend.

## Motivation
This application was done as my first project to test out my skills in Django.

## Features
* Responsive Web Design
* Markdown is supported when writing blog posts
* User registration and login
* Comments
* All the data is saved using a database
* Admin panel

## How to use?

**Requirements (not tested with other versions)**:  
Python v3.7.4, Django v3.1.7, markdown2 v2.4.0

Starting the web application:  
`python manage.py runserver`

Some demo data (admin, users, posts, comments) is availabe in the database. Admin panel can be accessed at '/admin' link with `login: admin`, `password: admin`.  
The demo data can be cleaned by deleting blogapp/migrations and db.sqlite3. After the cleaning it is required to make the migrations:  
`python manage.py makemigrations blogapp`  
`python manage.py migrate`  

*config.py needs to be properly configured and "canWriteBlogs" checkbox needs to be removed when the web application is used in production*

## Existing issues
* There is an HTML injection vulnerability if writing posts is allowed to untrusted users.

## Future improvements
* Support for editing and deleting posts by post authors
* Support for images in posts and comments
* Support for pagination in the index page and for comments
* JavaScript input validation for input fields
