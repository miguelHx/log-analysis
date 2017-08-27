# Log Analysis Project
Purpose is to answer three questions based on data from a postgresql database called _news_
There are three tables:
* articles
* authors
* logs

## Questions that the program answers
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## Setting up the database
1. Install VirtualBox from [this link](https://www.virtualbox.org/wiki/Downloads) (Install package for your OS)
  * **Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.
2. Install Vagrant from [this link](https://www.vagrantup.com/downloads.html)
  * **Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
3. Download this repository as a zip file and then unzip to wherever
4. Open up a terminal and run `cd log-analysis` and then `cd vagrant`
  * vagrant setup file will be in there
5. Inside the **vagrant** subdirectory, run the command `vagrant up`
  * This will cause Vagrant to download the Linux operating system and install it
  * May take a while (many minutes) depending on your internet connection speed
6. When `vagrant up` finishes running and the shell prompt is back, run `vagrant ssh` to log in to the Linux VM
  * Files in the VM's /vagrant directory are shared with the vagrant folder on your computer. But other data inside the VM is not.
  * For instance, the PostgreSQL database itself lives only inside the VM.
  * If you exit the terminal or reboot the computer, you will need to run `vagrant up` to restart the VM
7. Now that you are logged in, run `cd /vagrant` to gain access to the shared directory
8. The sql file should be in the folder, so run `psql -d news -f newsdata.sql` to populate the database
9. Once the data is loaded, connect to the database using `psql -d news` and explore the tables using `\dt` and `\d table` commands and `select` statements.
10. Setup is complete! Now it is time to run the log analysis program I wrote.


## Steps to Run Log Analysis
1. Make sure you are logged in to the VM
2. cd into /vagrant: `cd /vagrant`
3. run `python log-analysis.py`

## Performance
* Each question will happen quickly thanks to the speed of SQL queries.

## Notes
* Views were used for testing, but not in the final code.  
* Subqueries were used in place of views instead.
* You can see some of the views in sql_query_notebook.txt
* sql_query_notebook.txt just contains queries that I wanted to have as notes.

## Links that helped me on this project
* https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string
* https://stackoverflow.com/questions/120926/why-does-python-pep-8-strongly-recommend-spaces-over-tabs-for-indentation
* https://stackoverflow.com/questions/5648210/postgresql-self-join
* https://dba.stackexchange.com/questions/23778/count-and-sum-at-the-same-time-after-removing-duplicate-rows/23788#23788?newreg=fbc32b4ea43b4a108ac8722191727590
* https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting
* https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
* postgresql documentation
* https://stackoverflow.com/questions/16269394/how-to-get-count-and-percentage-comparing-two-tables-in-mysql
* https://stackoverflow.com/questions/7376072/postgresql-calculate-sum-of-a-resultset
* https://stackoverflow.com/questions/6832566/postgresql-group-by-timestamp-values
