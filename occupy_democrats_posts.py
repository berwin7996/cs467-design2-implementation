import csv
import datetime

date_index_status = 0
date_index_comment = 0
posts_by_week ={}
posts_by_day = {}

with open('occupy_democrats_all.csv', 'rb') as csvfile:
    file_reader = csv.reader(csvfile, delimiter=',')
    header = file_reader.next()
    for i in range (0, len(header)):
        if header[i] == "status_published":
            date_index_status = i

    for row in file_reader:
        post_date_string = row[date_index_status].split(" ")[0]
        post_day = datetime.datetime.strptime(post_date_string, '%m/%d/%Y')
        post_date = post_day.strftime('%m/%d/%Y')
        post_week = post_day.isocalendar()[1]
        if post_date not in posts_by_day:
            posts_by_day[post_date] = {}
            posts_by_day[post_date]['statuses'] = 1
            posts_by_day[post_date]['comments'] = 0
        else:
            posts_by_day[post_date]['statuses'] += 1
        if post_week not in posts_by_week:
            posts_by_week[post_week] = {}
            posts_by_week[post_week]['statuses'] = 1
            posts_by_week[post_week]['comments'] = 0
        else:
            posts_by_week[post_week]['statuses'] += 1

with open('occupy_democrats_comments.csv', 'rb') as csvfile:
    file_reader_comment = csv.reader(csvfile, delimiter=',')
    header = file_reader_comment.next()
    data_index_comment = 0

    for row in file_reader_comment:
        post_date_string = row[date_index_comment].split("T")[0]
        post_date = datetime.datetime.strptime(post_date_string, '%Y-%m-%d').strftime('%m/%d/%Y')
        post_day = datetime.datetime.strptime(post_date, '%m/%d/%Y')
        post_week = post_day.isocalendar()[1]
        if post_date not in posts_by_day:
            posts_by_day[post_date] = {}
            posts_by_day[post_date]['comments'] = 1
            posts_by_day[post_date]['statuses'] = 0
        else:
            posts_by_day[post_date]['comments'] += 1
        if post_week not in posts_by_week:
            posts_by_week[post_week] = {}
            posts_by_week[post_week]['comments'] = 1
            posts_by_week[post_week]['statuses'] = 0
        else:
            posts_by_week[post_week]['comments'] += 1


with open('occupy_democrats_day.csv', 'wb') as csvfile:
    file_writer_day = csv.writer(csvfile, delimiter=',')
    file_writer_day.writerow(['Day', 'Number of Statuses', 'Number of Comments'])
    for day in posts_by_day.keys():
        file_writer_day.writerow([str(day), str(posts_by_day[day]['statuses']), str(posts_by_day[day]['comments'])])

with open('occupy_democrats_week.csv', 'wb') as csvfile:
    file_writer_week = csv.writer(csvfile, delimiter=',')
    file_writer_week.writerow(['Week Number','Start Day', 'End Day', 'Number of Statuses', 'Number of Comments'])
    for week in posts_by_week.keys():
        d = "2016-" + str(week)
        start_date = datetime.datetime.strptime(d + '-1', "%Y-%W-%w")
        end_date = start_date + datetime.timedelta(days = 6)
        start_date_converted = start_date.strftime('%m/%d/%Y')
        end_date_converted = end_date.strftime('%m/%d/%Y')
        file_writer_week.writerow([str(week), str(start_date_converted), str(end_date_converted),str(posts_by_week[week]['statuses']), str(posts_by_week[week]['comments'])])

