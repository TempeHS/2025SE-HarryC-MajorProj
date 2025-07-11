# Overview

This is a pilot implementation of a progressive web application for an Acupuncturist. The website includes static user features such as a home page, booking page, blog page and about me page, which can be configured through the admin dashboard.

## Dependencies

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

- Go to the VS Code extension marketplace and download the following
  - ![Database examples](readme_files/sqlite.png)

## How to use the website as an enduser

Use this codespace in google chrome

- Run main.py

```bash
python main.py
```

- Run api.py

```bash
python api.py
```

- Now you can navigate the site as usual

[Watch: Website Navigation Demo](readme_files/vid%20of%20le%20acupuncture.mp4)

## How to use the website as an adminastrator

- In the browser url when you're on the home page of the webiste type in /admin_login.html
- Use the following credentials
  - Username: AdminUser
  - Password: P@ssword12345
- ## For the OTP refer to the main.py terminal
  - ![OTP Code Example](readme_files/otp_code.png)
- Watch the video for instructions
  - In the video u can see me go to my email, only reason I did that is to prove that the 2FA email successfully sent

[Watch: Admin Usage Tutorial](readme_files/instructional%20admin%20usage%20website%20tut.mp4)

## If you wish to test the 2FA

- Change the email manually in the admin_users in table in the database.db and you can change password though it will require you to go the admin_change_password.html and input the current password which is P@ssword12345 (email could be in spam)
  - ![Changing Email](readme_files/changing_email_db.png)
  - [Watch: Change password example.mov](readme_files/Change%20password%20example.mov)

## Version History

- 0.3 (https://github.com/TempeHS/2025SE-HarryC-MajorProj/tree/sprint_3)
  - Added CSS, responsive buttons
  - Created Admin Blog and Blog Editor
  - Implemented Security Features
- 0.2 (https://github.com/TempeHS/2025SE-HarryC-MajorProj/tree/sprint_2)
  - Added Admin Dashboard
  - Ability to make testimonials and change about me
- 0.1 (https://github.com/TempeHS/2025SE-HarryC-MajorProj/tree/sprint_1)
  - Added Admin Login, 2FA and Session Management
  - Created layout and basic versions of all pages

## View the full Systems Report Template

[Download: Task 4 - Systems Report Template (1).docx](<readme_files/Task%204%20-%20Systems%20Report%20Template%20(1).docx>)
