
# Scalable Online Judge

## Current Todo With priorities

- [x] Deploy for once.
- [ ] Add some CSS, and make the design at least look like mediocre. 
- [ ] Add some CSS, and make website responsive.
- [ ] Add TLE and MLE detection mechanism.
- [ ] Add more test cases and test problems.
- [ ] Add 4-5 new problems.
- [ ] Creating Demo video and code walkthrough video.
- [ ] Adding proper documentation in ReadMe.md

## Prerequisites to run

## How to run locally (for windows)

0. Make sure ??? is installed

1. make user temp_executables directory exist in /data/submissions 

2. Open oj_django_project/problems/backend/config.py
   - Make sure that Python compiler path and C++ compiler path is mentioned

## How to run locally (for linux)

0. Open terminal in ./oj_django_project directory

1. Start virtual environment (for bash shell)
`source ./venv/bin/activate`

2. Install required packagess
`pip install -r requirements.txt`

3. Start the server 
`python3 manage.py runserver 8000`

4. Go to `https://127.0.0.1:8000/` .
- Can use username = `dummy` and password = `dummy` .

## screenshots
![image](https://github.com/nitin12384/online_judge/blob/main/docs/screenshots/version1/ss%20(1).png?raw=true)
![image]()
![image]()
![image]()
![image]()
![image]()
![image]()


# Detailed Todo list (Most of that is not gonna happen now. )
- [x] Add user log in
- [ ] put in docker
- [ ] Add Time, Memory limit, Network security, ....
- [ ] deploy on firebase, heroku, AWS
- [ ] Option to see compiler error 
- [ ] Add multiple testcases for problems (big IO testcases)
- [ ] Add More problems. Have 7-8 good and (nowhere else you could find) problems.
- [ ] Improve the UI
- [ ] Testing including NFR
- [ ] Django . gets logged out automatically 
- [ ] send Friends
- [ ] Forgot password/change password thing
- [ ] CSRF protection in Submit code. Learn how CSRF works, what kind of thing a hacker do with it.
- [ ] User Login success, user signup success message/alert
- [ ] Put validation in username and password and email . Cross Sire Scripting attacks!!
- [ ] Put db handling code in models
 
* ToDo List
✔️ Done
▶️ In progress

## Part 1

-- Learning Basics (1 week)

- ✔️1a. Finish Django Learning Part 3,4
- ✔️1b. Finish React Learning basic
- ▶️1c. Learn MySQL + Django integration basics
- ▶️1d. Learn React + Django integration basics 
- *1e. Learn/Try docker basics and how to send and recieve files from docker .
- *1f. Learn/Try user authentication in a website
- *1g. Try using timeout, and running and compiling a code file, from a program.

-- Design (1-2 day)

- ✔️2a. Decide the database architect, all tables, primary keys, foreign keys
- ✔️2b. Decide the UI, 
- ✔️2c. Decide the backend architecture : dataflow, api, etc.

-- Database ( 2-3 hour )

- ✔️3a. Create the database.

-- Implementing the Backend (1-1.5 week )

- ✔️4a. Getting List of problems 
- ✔️4b. Getting a problem details 
- ✔️4c. Submitting the code 
- ✔️4d. Getting the verdict
- ✔️4e. Getting n recent submissions 

-- Implement the UI + backend finalizing (1 week )

- ✔️5a. Home page : List of problems
- ✔️5b. Problem page : problem details
- ✔️5c. Submit Page 
- ✔️5d. Submissions page : 

- ✔️6a. Integrate all things ( 2-3 days)

-- ✔️MVP done

## Part 2 

- Add user authentication (1-2 days)
- Add docker (2-3 days)

- Add C, Ruby, Java 11, Kotlin
- Add multiple testcases for problems (big IO testcases)
- Add More problems. Have 7-8 good and (nowhere else you could find) problems.
- Add support of custom output checker program instead of simple file matcher (2-3 days)

- Deploy on heroku(1 day)
- Deploy using AWS 

- Get envioronment variable / VM args. like env, problem_data_path, etc.

- Add Unit Testing
- Add UI Testing
- Add Functional and NFR Testing 

- Make design more scalable : Put multiple docker instances, 
- Use Ngnix and Gunicorn
- Migrate to postgreSQL ( ?? 3 days or more )

- Vague : Improve the UI ( 2 days )
- Use React
- Better Design of Table 

- Vague : Improve the backend ( 2 days )
- Todo Part in backend
- Function based views to class based views
- more SOLID code.
- divide code into more modules

- Add run code with custom testcase feature
- Add contests
- User is able to see his old submissions
- User is able to see which test case failed.
- Syntax Highlighting in you text editor
- Cache : Store most recent code to local storage (like leetcode)
- copy button near sample IO



