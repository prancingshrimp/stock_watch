import argparse
import datetime
import json
import subprocess
import sys
import threading
import time
import os

from concurrent.futures import thread



def run(scriptPath, data):
    executePath = os.path.join(scriptPath, data['scriptName'])
    p = subprocess.Popen(['python.exe', executePath, '-f', data['inputCSV'], '-t', str(data['timeIntervall'])])
    while True:
        if stop_threads:
            p.terminate()
            break



def check_json_data(data, scriptPath):
    executePath = os.path.join(scriptPath, data['scriptName'])
    if os.path.isfile(executePath) == False:
        print('Can not find ' + executePath + '!')
        progQuit()

    csvPath = os.path.join(scriptPath, data['inputCSV'])
    if os.path.isfile(csvPath) == False:
        print('Can not find ' + csvPath + '!')
        progQuit()

    try:
        data['timeIntervall'] = int(data['timeIntervall'])
    except:
        print('Can not get the time intervall: ' + data['timeIntervall'] + '!')
        progQuit()

    try:
        data['startTime'] = datetime.datetime.strptime(data['startTime'], '%H:%M').time()
    except:
        print('Can not get the starting time: ' + data['startTime'] + '!')
        progQuit()

    try:
        data['endTime'] = datetime.datetime.strptime(data['endTime'], '%H:%M').time()
    except:
        print('Can not get the end time: ' + data['endTime'] + '!')
        progQuit()



def check_in_time(startTime, endTime):
    currentTime = datetime.datetime.now().time()
    if currentTime > startTime and currentTime < endTime:
        return True
    else:
        return False



def main():
    PROOF_TIME = 60

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='JSON_FILE', action='store')
    args = parser.parse_args()

    scriptPath = os.path.dirname(os.path.abspath(__file__))
    jsonFilePath = os.path.join(scriptPath, args.JSON_FILE)

    if os.path.isfile(jsonFilePath):
        with open(jsonFilePath, 'r') as file:
            try:
                jsonData = json.load(file)
            except:
                print('Can not read ' + args.JSON_FILE + '!')
                progQuit()

            check_json_data(jsonData, scriptPath)

        global stop_threads
        while True:
            in_time_window = check_in_time(jsonData['startTime'], jsonData['endTime'])
            
            if in_time_window == True:
                while in_time_window:
                    stop_threads = False
                    thread0 = threading.Thread(target = run, args=[scriptPath, jsonData])
                    thread0.start()
                    print('thread started at:', datetime.datetime.now().time())
                    still_in_time_window = True
                    while still_in_time_window:
                        time.sleep(PROOF_TIME)
                        still_in_time_window = check_in_time(jsonData['startTime'], jsonData['endTime'])
                    stop_threads = True
                    thread0.join()
                    print('thread killed at:', datetime.datetime.now().time())
                    in_time_window = False

            time.sleep(PROOF_TIME)



def progQuit():
    progName = sys.argv[0]
    sys.exit(0)



if __name__ == '__main__':
    main()