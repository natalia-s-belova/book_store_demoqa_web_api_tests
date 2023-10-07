## Training project with Web and API autotests for [BookStore DemoQa](https://demoqa.com/books) service

<img src="readme_images/logo.png" height="100"/>&nbsp;

### Tools and technologies used
<p>
<a href="https://www.python.org/"><img src="readme_images/technologies/python.png" width="40" height="40"  alt="PYTHON"/></a>
<a href="https://docs.pytest.org/en/"><img src="readme_images/technologies/pytest.png" width="40" height="40"  alt="PYTEST"/></a>
<a href="https://www.jetbrains.com/pycharm/"><img src="readme_images/technologies/pycharm.png" width="40" height="40"  alt="PYCHARM"/></a>
<a href="https://www.selenium.dev/"><img src="readme_images/technologies/selenium.png" width="40" height="40"  alt="SELENIUM"/></a>
<a href="https://github.com/yashaka/selene/"><img src="readme_images/technologies/selene.png" width="40" height="40"  alt="SELENE"/></a>
<a href="https://python-poetry.org/"><img src="readme_images/technologies/poetry.png" width="40" height="40"  alt="POETRY"/></a>
<a href="https://docs.pydantic.dev/latest/"><img src="readme_images/technologies/pydantic.png" width="40" height="40"  alt="PYDANTIC"/></a>
<a href="https://pypi.org/project/requests/"><img src="readme_images/technologies/requests.png" width="40" height="40"  alt="REQUESTS"/></a>
<a href="https://www.jenkins.io/"><img src="readme_images/technologies/jenkins.png" width="40" height="40"  alt="JENKINS"/></a>
<a href="https://allurereport.org/"><img src="readme_images/technologies/allure_report.png" width="40" height="40"  alt="ALLUREREPORT"/></a>
<a href="https://qameta.io/"><img src="readme_images/technologies/allure_testops.png" width="40" height="40"  alt="ALLURETESTOPS"/></a>
<a href="https://aerokube.com/selenoid/"><img src="readme_images/technologies/selenoid.png" width="40" height="40"  alt="SELENOID"/></a>
<a href="https://www.atlassian.com/software/jira"><img src="readme_images/technologies/jira.png" width="40" height="40"  alt="JIRA"/></a>
</p>

### Test coverage
UI-tests (web application):
* User's authorization
* Bookstore: search, navigate, view book details, add book to user's collection
* Profile: View, navigate, search, remove book(s) from the collection

API-tests:
* Account creation/deletion
* Token generation
* Receiving information about book's details
* Adding book(s) to user's collection
* Response's status codes
* Response's schemas

*Note: some web-tests are hybrid and use API requests (for example, to create/log in/delete user in order to reduce tests' running time and/or avoid CAPTCHA at registration).*

Example of Web test's running (successful login):

<img src="readme_images/bookstore_web_test.gif"/>&nbsp;

Example of API request's test:

<img src="readme_images/bookstore_api_test.png" height="400"/>&nbsp;

### Test Launch
Tests are launching using **Jenkins service**.
To run tests, open the [configured job](https://jenkins.autotests.cloud/job/C06-natalya_s_belova_bookstore_web_api_main/), click 'Build with parameters', select browser + version (for example, firefox 98.0) and tests directory (web/api tests can be launched in the same run or separately), click 'Build'.

<img src="readme_images/bookstore_jenkins_1.png"/>&nbsp;
<img src="readme_images/bookstore_jenkins_2.png"/>&nbsp;

Also, since the integration with **Allure Test Ops** is implemented, it is possible to run tests with this service. 
In Allure Test Ops is also an additional ability to configure test scope by choosing specific test cases.

<img src="readme_images/bookstore_testops_jobs.png"/>&nbsp;
<img src="readme_images/bookstore_testops_parameters.png"/>&nbsp;

### Test Report and Test Documentation

Reporting is implemented using **Allure services**.

[Allure Report](https://jenkins.autotests.cloud/job/C06-natalya_s_belova_bookstore_web_api_main/allure/) can be opened on Jenkins page (see Jenkins screenshot in the section above) and contains graphics, detalization of test executions, different kinds of attachments (screenshots, logs, video, html code).
<img src="readme_images/bookstore_allure_1.png"/>&nbsp;
<img src="readme_images/bookstore_allure_2.png"/>&nbsp;

**Allure Test Ops** also contains such information and in addition it has generated Test Documentation that can be imported to Jira.
<img src="readme_images/bookstore_testops_dashboard.png"/>&nbsp;
<img src="readme_images/bookstore_testops_tc.png"/>&nbsp;

### Integration with Jira

Test Launches and Test Cases are integrated with Jira Task:
<img src="readme_images/bookstore_jira.png"/>&nbsp;

### Test Results Notifications
As soon as Test Launch is completed, telegram message with the following information is sent:
* total amount of tests and run duration
* percentage of passed/failed/skipped/etc. tests
* link to the allure report

<img src="readme_images/bookstore_telegram.png" height="300"/>&nbsp;

For such messages to be sent, [notifications library](https://github.com/qa-guru/allure-notifications) was used, telegram bot was created and added to a specific telegram group.
