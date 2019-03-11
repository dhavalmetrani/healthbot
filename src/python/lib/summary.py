"""
Calculate the steps and return details.
"""

import sys
import os
import csv
import datetime
import logging
from os import walk
from dateutil.parser import parse
from collections import OrderedDict

import lib.util as util

TYPE="type"
UNIT="unit"
START_DATE="startDate"
VALUE="value"

def get_daily_workout_details(exercise_rows, start_date=START_DATE, value=VALUE):
  """
  Get average steps.
  :exercise_rows: List of steps
  """
  # util.log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  # print(exercise_rows)
  count = 0
  start_date_utc = None
  str_start_date = None
  dict_exercise = {}
  for row in exercise_rows[1:]:
    # count = int(row[8])
    # str_start_date = row[6]
    index_start_date = exercise_rows[0].index(start_date)
    index_count = exercise_rows[0].index(value)
    str_start_date = row[index_start_date]
    count = float(row[index_count])
    start_date_utc = parse(str_start_date)
    str_date_format = "{:04d}-{:02d}-{:02d}".format(start_date_utc.year, start_date_utc.month, start_date_utc.day)
    if str_date_format not in dict_exercise:
      dict_exercise[str_date_format] = count
    else:
      dict_exercise.update({str_date_format:dict_exercise[str_date_format]+count})

    count = 0
  od = OrderedDict(sorted(dict_exercise.items(), key=lambda x: x[0]))
  return od


def get_last_days_details(dict_exercise, days=7):
  """
  Get steps of last few days
  """
  count_total = 0
  for k, v in sorted(dict_exercise.items(), key=lambda x: x[0], reverse=True)[:days]:
    count_total += v
  average_value = count_total//days

  return count_total, average_value


def main(file_path):
    """
    Main logic resides here.
    """
    # util.log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
    exercise_rows = util.get_csv_rows(file_path)
    dict_exercise = get_daily_workout_details(exercise_rows)
    index_type = exercise_rows[0].index(TYPE)
    index_unit = exercise_rows[0].index(UNIT)

    exercise_type = exercise_rows[1][index_type]
    exercise_unit = exercise_rows[1][index_unit]
    # print(exercise_rows[0])
    # print(index_type)
    # print(index_unit)
    # print(exercise_type)
    # print(exercise_unit)

    # for days in [1, 7, 30]:
    for days in [1]:
      count_total_exercise, average_exercise = get_last_days_details(dict_exercise, days)
      # print("```Exercise Type: `{}`\nTotal: `{}` {}\nAverage: {}\nDays: {}```".format(exercise_type, count_total_exercise, exercise_unit, average_exercise, days))
      # print("Exercise Type: `{}`\nTotal: `{}` {}\nAverage: {}\nDays: {}\n".format(exercise_type, count_total_exercise, exercise_unit, average_exercise, days))
      print("Total `{}` for the day: {} {}\n".format(exercise_type, average_exercise, exercise_unit))

    # print("You took `{}` steps in last `{}` days. Average `{}` per day".format(count_total_exercise, days, average_exercise))
    # days = 7
    # count_total_exercise, average_exercise = get_last_days_details(dict_exercise, days)
    # print("You took `{}` steps in last `{}` days. Average `{}` per day".format(count_total_exercise, days, average_exercise))
    # days = 30
    # count_total_exercise, average_exercise = get_last_days_details(dict_exercise, days)
    # print("You took `{}` steps in last `{}` days. Average `{}` per day".format(count_total_exercise, days, average_exercise))
    # days = 60
    # count_total_exercise, average_exercise = get_last_days_details(dict_exercise, days)
    # print("You took `{}` steps in last `{}` days. Average `{}` per day".format(count_total_exercise, days, average_exercise))


    pass

def activity_summary(file_path="./src/python/config/ActivitySummary.csv"):
  """
  Get the activity summary for the day.
  :param file_path: Path to csv file.
  """
  # util.log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
  exercise_rows = util.get_csv_rows(file_path)
  dict_exercise = {}
  for row in exercise_rows[1:]:
    index_start_date = exercise_rows[0].index("dateComponents")
    index_energy_burned = exercise_rows[0].index("activeEnergyBurned")
    index_energy_burned_goal = exercise_rows[0].index("activeEnergyBurnedGoal")
    index_exercise_time = exercise_rows[0].index("appleExerciseTime")
    index_exercise_time_goal = exercise_rows[0].index("appleExerciseTimeGoal")
    index_stand_hours = exercise_rows[0].index("appleStandHours")
    index_stand_hours_goal = exercise_rows[0].index("appleStandHoursGoal")

    start_date = row[index_start_date]
    energy_burned = row[index_energy_burned]
    energy_burned_goal = row[index_energy_burned_goal]
    exercise_time = row[index_exercise_time]
    exercise_time_goal = row[index_exercise_time_goal]
    stand_hours = row[index_stand_hours]
    stand_hours_goal = row[index_stand_hours_goal]

    dict_temp = {
      "dateComponents": start_date,
      "activeEnergyBurned": energy_burned,
      "activeEnergyBurnedGoal": energy_burned_goal,
      "appleExerciseTime": exercise_time,
      "appleExerciseTimeGoal": exercise_time_goal,
      "appleStandHours": stand_hours,
      "appleStandHoursGoal": stand_hours_goal
    }

    if start_date not in dict_exercise:
      dict_exercise[start_date] = dict_temp
    else:
      dict_exercise.update(dict_temp)

  od = OrderedDict(sorted(dict_exercise.items(), key=lambda x: x[0]))
  key = list(od.keys())[-1]
  str_eb = "*[ {} / {} ]* :white_check_mark: "
  str_et = "*[ {} / {} ]* :white_check_mark: "
  str_sh = "*[ {} / {} ]* :white_check_mark: "

  # CUSTOM:
  od[key]["activeEnergyBurnedGoal"] = 106
  if float(od[key]["activeEnergyBurned"]) < float(od[key]["activeEnergyBurnedGoal"]):
    str_eb = "`[ {} / {} ]` :warning: "
  if float(od[key]["appleExerciseTime"]) < float(od[key]["appleExerciseTimeGoal"]):
    str_et = "`[ {} / {} ]` :warning: "
  if float(od[key]["appleStandHours"]) < float(od[key]["appleStandHoursGoal"]):
    str_sh = "`[ {} / {} ]` :warning: "

  str_msg = "*Summary* [ *{}*: ] \n*Energy burned:* " + str_eb + " calories\n" + \
                                  "*Exercise time:* " + str_et + " mins\n" + \
                                  "*Standing hours:* " + str_sh + " hours"
  # print(str_msg)
  print(str_msg.format(key, \
  od[key]["activeEnergyBurned"], od[key]["activeEnergyBurnedGoal"], \
  od[key]["appleExerciseTime"], od[key]["appleExerciseTimeGoal"], \
  od[key]["appleStandHours"], od[key]["appleStandHoursGoal"]))

  # util.pprint(od)
  # return od


if __name__ == '__main__':
    """
    Main guard.
    """
    util.init_logging(logging.ERROR)
    # util.log.info("Module: {} Function: {}".format(__name__, sys._getframe().f_code.co_name))
    # file_path = os.getcwd()
    file_path = "./src/python/config/ActivitySummary.csv"
    try:
      activity_summary(file_path)
    except Exception as ex:
      print(ex)
    # print(os.getcwd())
    # f = []
    # if len(sys.argv) != 2:
    #   # file_path += "/src/python/config/StepCount.csv"
    #   for (dirpath, dirnames, filenames) in walk("./src/python/config/"):
    #     f.extend(filenames)
    #     # break
    #   for file in sorted(f):
    #     print(file)
    #     file_path = "./src/python/config/" + file
    #     try:
    #       main(file_path)
    #     except Exception as ex:
    #       print(ex)
    # else:
    #   file_path = sys.argv[1]
    #   main(file_path)
