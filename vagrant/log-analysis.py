#!/usr/bin/env python
# written by Miguel Hernandez and with help from
# stackoverflow, postgresql docs, and previous udacity lessons
import psycopg2
import datetime
import calendar


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
    sql = (
        'select title, count(*) as views '
        '   from '
        '   ('
        '   select '
        '       articles.title, articles.slug, log.path, log.status '
        '       from articles join log '
        '       on log.path = (\'/article/\' || articles.slug) '
        '   ) as result '
        'group by title order by views desc limit 3;'
        )
    cursor.execute(sql)
    articles_result = cursor.fetchall()

    db.close()

    print("Most popular ARTICLES:")
    for i in range(0, len(articles_result)):
        print("\"" + articles_result[i][0] + "\" - " +
              str(articles_result[i][1]) + " views")


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

    sql = (
        'select authors.name, count(*) as views '
        '   from authors, articles, log '
        '       where authors.id = articles.author '
        '       and log.path = (\'/article/\' || articles.slug) '
        'group by authors.name '
        'order by views desc limit 3;'
    )
    cursor.execute(sql)
    authors_result = cursor.fetchall()

    # close connection
    db.close()

    print("Most popular AUTHORS:")
    for i in range(0, len(authors_result)):
        print(
            authors_result[i][0] + " - " + str(authors_result[i][1]) + " views"
            )


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
    sql = (
        'select total.date, '
        '100*(sum(error.http_requests)/(total.http_requests)) as percentage '
        '   from '
        '   ('
        '   select '
        '       date_trunc(\'day\', log.time) as date, '
        '       count(*) as http_requests '
        '       from log where log.status = \'404 NOT FOUND\''
        '       group by date order by http_requests desc'
        '   ) as error, '
        '   ('
        '   select '
        '       date_trunc(\'day\', log.time) as date, '
        '       count(*) as http_requests '
        '       from log group by date order by http_requests desc'
        '   ) as total '
        'where error.date = total.date '
        'group by total.date, total.http_requests '
        'having 100*(sum(error.http_requests)/(total.http_requests)) > 1.0 '
        'limit 3;'
    )

    cursor.execute(sql)
    # below is a list of tuples (str, datetime)
    error_list = cursor.fetchall()

    # close connection
    db.close()

    print("Dates where more than 1% of HTTP requests lead to errors:")
    for i in range(0, len(error_list)):
        error_date = str(calendar.month_name[error_list[i][0].month]) \
            + " " + str(error_list[i][0].day) \
            + ", " + str(error_list[i][0].year)
        print(
            error_date + " - " + str(error_list[i][1]) + "% errors"
            )


if __name__ == "__main__":
    print("Question 1:")
    popular_articles()
    print("")
    print("Question 2:")
    popular_authors()
    print("")
    print("Question 3:")
    errors_analysis()
