import unicodecsv
from datetime import datetime as dt


#####################################
#                 1                 #
#####################################

## Read in the data from daily_engagement.csv and project_submissions.csv
## and store the results in the below variables.
## Then look at the first row of each table.
enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%d/%m/%y')

# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)



#####################################
#                 3                 #
#####################################

## Rename the "acct" column in the daily_engagement table to "account_key".
def renameDictKey(data, o_key, n_key):
    for d in data:
        d[n_key] = d[o_key]
        del d[o_key]
    return data

with open(enrollments_filename, 'rb') as f:
    reader = unicodecsv.DictReader(f)
    enrollments = list(reader)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'TRUE'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'TRUE'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

# print(enrollments[0])

with open(engagement_filename, 'rb') as f:
    reader = unicodecsv.DictReader(f)
    daily_engagement = list(reader)

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

# rename 'acct' -> 'account_key' to keep header uniform
renameDictKey(daily_engagement, 'acct', 'account_key')

# print(daily_engagement[0])

with open(submissions_filename, 'rb') as f:
    reader = unicodecsv.DictReader(f)
    project_submissions = list(reader)

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

# print(project_submissions[0])


#####################################
#                 2                 #
#####################################

## Find the total number of rows and the number of unique students (account keys)
## in each table.
def unique_list(data, key):
    unique_list = []
    for d in data:
        if d[key] not in unique_list:
            unique_list.append(d[key])
    return unique_list

def unique_set(data, key):
    unique_set = set()
    for d in data:
        if d[key] not in unique_set:
            unique_set.add(d[key])
    return unique_set

enrollment_unique_students_list = unique_list(enrollments, 'account_key')
enrollment_unique_students_set = unique_set(enrollments, 'account_key')
# engagement_unique_students_list = unique_list(daily_engagement, 'acct')
# engagement_unique_students_set = unique_set(daily_engagement, 'acct')
engagement_unique_students_list = unique_list(daily_engagement, 'account_key')
engagement_unique_students_set = unique_set(daily_engagement, 'account_key')
submission_unique_students_list = unique_list(project_submissions, 'account_key')
submission_unique_students_set = unique_set(project_submissions, 'account_key')

enrollment_num_rows = len(enrollments)       # Replace this with your code
enrollment_num_unique_students = len(enrollment_unique_students_set)  # Replace this with your code
print("====================================================================")
print("enrollment_num_rows " + str(enrollment_num_rows))
print("enrollment_num_unique_students " + str(enrollment_num_unique_students))

engagement_num_rows = len(daily_engagement)  # Replace this with your code
engagement_num_unique_students = len(engagement_unique_students_set)  # Replace this with your code
print("engagement_num_rows " + str(engagement_num_rows))
print("engagement_num_unique_students " + str(engagement_num_unique_students))

submission_num_rows = len(project_submissions) # Replace this with your code
submission_num_unique_students = len(submission_unique_students_set)  # Replace this with your code
print("submission_num_rows " + str(submission_num_rows))
print("submission_num_unique_students " + str(submission_num_unique_students))
print("====================================================================")


print("====================================================================")
#####################################
#                 4                 #
#####################################

## Find any one student enrollments where the student is missing from the daily engagement table.
## Output that enrollment.
unique_enrolled_not_engaged_set = enrollment_unique_students_set.difference(engagement_unique_students_set)
print("unique_enrolled_not_engaged_set " + str(len(unique_enrolled_not_engaged_set)))
# print(unique_enrolled_not_engaged_set)


non_engaged_enrollments = []
count_udacity_non_engaged_enrollments = 0
count_udacity_enrollments = 0
for enrollment in enrollments:
    if enrollment['is_udacity'] == True:
        count_udacity_enrollments += 1
    if enrollment['account_key'] not in engagement_unique_students_set:
        non_engaged_enrollments.append(enrollment)
        if enrollment['is_udacity'] == True:
            count_udacity_non_engaged_enrollments += 1

print("count_udacity_enrollments " + str(count_udacity_enrollments))
print("non_engaged_enrollments " + str(len(non_engaged_enrollments)))
print("count_udacity_non_engaged_enrollments " + str(count_udacity_non_engaged_enrollments))
# print(enrolled_not_engaged_list[0:19])

#####################################
#                 5                 #
#####################################

## Find the number of surprising data points (enrollments missing from
## the engagement table) that remain, if any.
surprising_data_points = []
for enrollment in enrollments:
    if enrollment['account_key'] in unique_enrolled_not_engaged_set and enrollment['days_to_cancel'] != 0:
        surprising_data_points.append(enrollment)

print("count_surprising_data_points " + str(len(surprising_data_points)))
# print(surprising_data_points)
print("====================================================================")

print("====================================================================")
# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
print("udacity_test_accounts " + str(len(udacity_test_accounts)))

# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data


# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print("non_udacity_enrollments " + str(len(non_udacity_enrollments)))
print("non_udacity_engagement " + str(len(non_udacity_engagement)))
print("non_udacity_submissions " + str(len(non_udacity_submissions)))
# print("enrollments " + str(len(enrollments)))
# print("daily_engagement " + str(len(daily_engagement)))
# print("project_submissions " + str(len(project_submissions)))
print("====================================================================")


#####################################
#                 6                 #
#####################################

# Create a dictionary named paid_students containing all students who either
# haven't canceled yet or who remained enrolled for more than 7 days. The keys
# should be account keys, and the values should be the date the student enrolled.
def get_paid_students(enrollments):
    paid_students = {}
    for enrollment in enrollments:
        if enrollment['days_to_cancel'] == None or int(enrollment['days_to_cancel']) > 7:
            key = enrollment['account_key']
            enrollment_date = enrollment['join_date']
            if key not in paid_students or enrollment_date > paid_students[key]:
                paid_students[key] = enrollment['join_date']
    return paid_students
print("====================================================================")
paid_students = get_paid_students(non_udacity_enrollments)
print("paid_students " + str(len(paid_students)))


# Given some data with an account_key field, removes any records corresponding to free trial/non-paying accounts
def remove_free_trial_accounts(data):
    paid_non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            paid_non_udacity_data.append(data_point)
    return paid_non_udacity_data


# Remove Udacity test accounts from all three tables
paid_non_udacity_enrollments = remove_free_trial_accounts(enrollments)
paid_non_udacity_engagement = remove_free_trial_accounts(daily_engagement)
paid_non_udacity_submissions = remove_free_trial_accounts(project_submissions)

print("paid_non_udacity_enrollments " + str(len(paid_non_udacity_enrollments)))
print("paid_non_udacity_engagement " + str(len(paid_non_udacity_engagement)))
print("paid_non_udacity_submissions " + str(len(paid_non_udacity_submissions)))
print("====================================================================")



# Add has_visited field
for engagement in paid_non_udacity_engagement:
    if engagement['num_courses_visited'] > 0:
        engagement['has_visited'] = 1
    else:
        engagement['has_visited'] = 0

#####################################
#                 7                 #
#####################################

print("====================================================================")
# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.
paid_engagement_in_first_week = []
for engagement in paid_non_udacity_engagement:
    student = engagement['account_key']
    engage_date = engagement['utc_date']
    join_date = paid_students[student]
    if within_one_week(join_date, engage_date):
        paid_engagement_in_first_week.append(engagement)

print("paid_engagement_in_first_week " + str(len(paid_engagement_in_first_week)))
# print(paid_engagement_in_first_week[0:3])


print("====================================================================")





#####################################
#                 8                 #
#####################################

## Go through a similar process as before to see if there is a problem.
## Locate at least one surprising piece of data, output it, and take a look at it.

print("====================================================================")

from collections import defaultdict
import numpy as np


# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)
print("engagement_by_account " + str(len(engagement_by_account)))

# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0

    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes
print("total_minutes_by_account " + str(len(total_minutes_by_account)))

#
# sorted_engagement_by_account_by_key = sorted(engagement_by_account.items(), key=operator.itemgetter(0))
# print(sorted_engagement_by_account_by_key[0])
# print(sorted_engagement_by_account_by_key[-1])
# print(len(engagement_by_account['108']))


# Summarize the data about minutes spent in the classroom
# total_minutes = total_minutes_by_account.values() # Original returns dict_values.  Need to convert to list in python3.5 below.
total_minutes = list(total_minutes_by_account.values())

print('Mean Time Spent : ' + str(np.mean(total_minutes)))
print('Standard deviation Time Spent :' + str(np.std(total_minutes)))
print('Minimum Time Spent :' + str(np.min(total_minutes)))
print('Maximum Time Spent :' + str(np.max(total_minutes)))
print("====================================================================")


#####################################
#                 9                 #
#####################################

## Adapt the code above to find the mean, standard deviation, minimum, and maximum for
## the number of lessons completed by each student during the first week. Try creating
## one or more functions to re-use the code above.
print("====================================================================")

def dict_by_account(data):
    dict_by_account = defaultdict(list)
    for d in data:
        account_key = d['account_key']
        dict_by_account[account_key].append(d)
    return dict_by_account

def sum_by_account(data, key):
    sum_by_account = {}
    for account_key, data_list in data.items():
        data_sum = 0
        for data_point in data_list:
            data_sum += data_point[key]
        sum_by_account[account_key] = data_sum
    return sum_by_account

def data_stats(data, name):
    data_list = list(data)
    print('Mean ' + name + ' :' + str(np.mean(data_list)))
    print('Standard Deviation ' + name + ' :' + str(np.std(data_list)))
    print('Minimum ' + name + ' :' + str(np.min(data_list)))
    print('Maximum ' + name + ' :' + str(np.max(data_list)))

print("====================================================================")

engagement_by_account = dict_by_account(paid_engagement_in_first_week)
print("engagement_by_account " + str(len(engagement_by_account)))

print("====================================================================")
total_minutes_by_account = sum_by_account(engagement_by_account, 'total_minutes_visited')
print("total_minutes_by_account " + str(len(total_minutes_by_account)))

data_stats(total_minutes_by_account.values(), 'Time Spent')

print("====================================================================")

lessons_completed_by_account = sum_by_account(engagement_by_account, 'lessons_completed')
print("lessons_completed_by_account " + str(len(lessons_completed_by_account)))

data_stats(lessons_completed_by_account.values(), 'Lessons Completed')

print("====================================================================")


######################################
#                 10                 #
######################################

## Find the mean, standard deviation, minimum, and maximum for the number of
## days each student visits the classroom during the first week.

print("====================================================================")

days_visited_course_by_account = sum_by_account(engagement_by_account, 'has_visited')
print("days_visited_course_by_account " + str(len(days_visited_course_by_account)))

data_stats(days_visited_course_by_account.values(), 'Days Visited Course(s)')
print("====================================================================")
######################################
#                 11                 #
######################################

## Create two lists of engagement data for paid students in the first week.
## The first list should contain data for students who eventually pass the
## subway project, and the second list should contain data for students
## who do not.

# paid_non_udacity_enrollments = remove_free_trial_accounts(enrollments)
# paid_non_udacity_engagement = remove_free_trial_accounts(daily_engagement)
# paid_non_udacity_submissions = remove_free_trial_accounts(project_submissions)
print("====================================================================")
subway_project_lesson_keys = ['746169184', '3176718735']

project_ratings_set = unique_set(project_submissions, 'assigned_rating')
print(project_ratings_set)

def project_submissions_by_lessons_ratings(lesson_keys,ratings):
    project_submissions = []
    for submission in paid_non_udacity_submissions:
        if submission['lesson_key'] in lesson_keys and submission['assigned_rating'] in ratings:
            project_submissions.append(submission)
    return project_submissions

passed_subway_project_submissions = project_submissions_by_lessons_ratings(['746169184','3176718735'], ['PASSED', 'DISTINCTION'])
passed_subway_project_submissions_account = dict_by_account(passed_subway_project_submissions)
print("passed_subway_project_submissions " + str(len(passed_subway_project_submissions)))
print("passed_subway_project_submissions_account " + str(len(passed_subway_project_submissions_account)))


passing_engagement = []
non_passing_engagement = []

print("paid_non_udacity_engagement " + str(len(paid_non_udacity_engagement)))
print("paid_engagement_in_first_week " + str(len(paid_engagement_in_first_week)))

for engagement in paid_engagement_in_first_week:
    if engagement['account_key'] in passed_subway_project_submissions_account:
        passing_engagement.append(engagement)
    else:
        non_passing_engagement.append(engagement)
print("passing_engagement " + str(len(passing_engagement)))
print("non_passing_engagement " + str(len(non_passing_engagement)))

print("====================================================================")

######################################
#                 12                 #
######################################

## Compute some metrics you're interested in and see how they differ for
## students who pass the subway project vs. students who don't. A good
## starting point would be the metrics we looked at earlier (minutes spent
## in the classroom (minutes_spent), lessons completed (lessons_completed),
## and days visited (has_visited), or others such as numbers of courses
## visited (num_courses_visited), project competed (projects_completed)
print("====================================================================")

passing_engagement_by_account = dict_by_account(passing_engagement)
non_passing_engagement_by_account = dict_by_account(non_passing_engagement)




# Time Spent
passing_engagement_time_spent_by_account = sum_by_account(passing_engagement_by_account, 'total_minutes_visited')
non_passing_engagement_time_spent_by_account = sum_by_account(non_passing_engagement_by_account, 'total_minutes_visited')
data_stats(passing_engagement_time_spent_by_account.values(), 'Passing Time Spent')
print("--------------------------------------------------------------------")
data_stats(non_passing_engagement_time_spent_by_account.values(), 'Non-Passing Time Spent')
print("====================================================================")


# Completed lessons
passing_engagement_lessons_completed_by_account = sum_by_account(passing_engagement_by_account, 'lessons_completed')
non_passing_engagement_lessons_completed_by_account = sum_by_account(non_passing_engagement_by_account, 'lessons_completed')
data_stats(passing_engagement_lessons_completed_by_account.values(), 'Passing Lesson Completed')
print("--------------------------------------------------------------------")
data_stats(non_passing_engagement_lessons_completed_by_account.values(), 'Non-Passing Lesson Completed')
print("====================================================================")


# Days Visited

passing_days_visited_lessons_completed_by_account = sum_by_account(passing_engagement_by_account, 'has_visited')
non_passing_days_visited_lessons_completed_by_account = sum_by_account(non_passing_engagement_by_account, 'has_visited')
data_stats(passing_days_visited_lessons_completed_by_account.values(), 'Passing Days Visited')
print("--------------------------------------------------------------------")
data_stats(non_passing_days_visited_lessons_completed_by_account.values(), 'Non-Passing Days Visited')
print("====================================================================")

passing_time_spent_filename = 'passing_time_spent.txt'
non_passing_time_spent_filename = 'non_passing_time_spent.txt'
passing_lessons_completed_filename = 'passing_lessons_completed.txt'
non_passing_lessons_completed_filename = 'non_passing_lessons_completed.txt'
passing_daily_visits_filename = 'passing_daily_visits.txt'
non_passing_daily_visits_filename = 'non_passing_daily_visits.txt'

import json
def write_dict_values_to_filename(data, filename):
    data_list = list(data)
    with open(filename, 'w') as fobj: # 'w' denote writing mode
        json.dump(data_list, fobj)
    fobj.close()

write_dict_values_to_filename(passing_engagement_time_spent_by_account.values(), passing_time_spent_filename)
write_dict_values_to_filename(non_passing_engagement_time_spent_by_account.values(), non_passing_time_spent_filename)
write_dict_values_to_filename(passing_engagement_lessons_completed_by_account.values(), passing_lessons_completed_filename)
write_dict_values_to_filename(non_passing_engagement_lessons_completed_by_account.values(), non_passing_lessons_completed_filename)
write_dict_values_to_filename(passing_days_visited_lessons_completed_by_account.values(), passing_daily_visits_filename)
write_dict_values_to_filename(non_passing_days_visited_lessons_completed_by_account.values(), non_passing_daily_visits_filename)

######################################
#                 13                 #
######################################

## Make histograms of the three metrics we looked at earlier for both
## students who passed the subway project and students who didn't. You
## might also want to make histograms of any other metrics you examined.

# ######################################
# #                 14                 #
# ######################################

import seaborn
# ## Make a more polished version of at least one of your visualizations
# ## from earlier. Try importing the seaborn library to make the visualization
# ## look better, adding axis labels and a title, and changing one or more
# ## arguments to the hist() function.
