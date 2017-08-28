#!/usr/bin/env python
# written by Miguel Hernandez and with help from
# stackoverflow, postgresql docs, and previous udacity lessons
import psycopg2
import datetime


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<unable to connect to database>")


def popular_articles():
    """
    Presents the top 3 articles that have been viewed the most as a sorted list
    No input, data will be gathered from database.
    Example output:
    "Princess Shellfish Marries Prince Handsome" - 1201 views
    "Baltimore Ravens Defeat Rhode Island Shoggoths" - 915 views
    "Political Scandal Ends In Political Scandal" - 553 views
    """
    # open connection
    db, cursor = connect()

    # one sql query to rule them all.
    sql = ("""
        SELECT title, views
        FROM articles
        INNER JOIN
            (SELECT path, count(path) AS views
             FROM log
             GROUP BY log.path) AS log
        ON log.path = '/article/' || articles.slug
        ORDER BY views DESC
        LIMIT 3;
        """)
    cursor.execute(sql)
    articles_result = cursor.fetchall()

    db.close()

    print("Most popular ARTICLES:")
    for result in articles_result:
        print('\"{}\" - {} views'.format(result[0], result[1]))


def popular_authors():
    """
    Presents the top article authors who have the most views as a sorted list
    No input, data will be gathered from database.
    Example output:
    Ursula La Multa - 2304 views
    Rudolf von Treppenwitz - 1985 views
    Markoff Chaney - 1723 views
    Anonymous Contributor - 1023 views
    """
    # open connection
    db, cursor = connect()

    sql = ("""
        SELECT authors.name, count(*) AS views
        FROM authors, articles, log
            WHERE authors.id = articles.author
            AND log.path = ('/article/' || articles.slug)
        GROUP BY authors.name
        ORDER BY views desc limit 3;
        """)
    cursor.execute(sql)
    authors_result = cursor.fetchall()

    # close connection
    db.close()

    print("Most popular AUTHORS:")
    for result in authors_result:
        print('{} - {} views'.format(result[0], result[1]))


def errors_analysis():
    """
    Presents the days where more than 1% of HTTP requests lead to errors
    No input, data will be gathered from database.
    Example output:
    July 29, 2016 - 2.5% errors
    August 2nd, 2016 - 5.4% errors
    December 7th, 2015 - 3.0% errors
    """

    # open connection
    db, cursor = connect()

    # get rows from db that have > 1.0 percentage error of http requests
    sql = ("""
        select total.date,
        100*(sum(error.http_requests)/(total.http_requests)) as percentage
           from
           (
           select
               date_trunc('day', log.time) as date,
               count(*) as http_requests
               from log where log.status = '404 NOT FOUND'
               group by date order by http_requests desc
           ) as error,
           (
           select
               date_trunc('day', log.time) as date,
               count(*) as http_requests
               from log group by date order by http_requests desc
           ) as total
        where error.date = total.date
        group by total.date, total.http_requests
        having 100*(sum(error.http_requests)/(total.http_requests)) > 1.0;
        """)

    cursor.execute(sql)
    # below is a list of tuples (str, datetime)
    error_list = cursor.fetchall()

    # close connection
    db.close()

    print("Dates where more than 1% of HTTP requests lead to errors:")
    for result in error_list:
        print('{0:%B %d, %Y} - {1:.2f}% errors'.format(result[0], result[1]))


if __name__ == "__main__":
    print("Question 1:")
    popular_articles()
    print("")
    print("Question 2:")
    popular_authors()
    print("")
    print("Question 3:")
    errors_analysis()
