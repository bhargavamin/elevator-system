#!/usr/bin/env python3.7

import os
import yaml
import ruamel.yaml
import logging as log
import datetime


class ElevatorControlSystem():
    def __init__(self, config_file):
        self.config_file = config_file
        self.time_per_floor = 15  # secs

    def loadElevatorConfigs(self):
        # load content from config file
        if self.config_file:
            config_path = os.path.expanduser(self.config_file)
            try:
                with open(config_path) as fh:
                    yaml_data = yaml.load(fh, Loader=ruamel.yaml.RoundTripLoader)
            except IOError:
                log.error("failed to load config: {}".format(config_path))
                raise
        else:
            raise FileNotFoundError("File not found {}'.format(self.config_path")
        return(yaml_data)

    def dumpElevatorConfigs(self, data):
        # dump new users in schema file
        if self.config_file:
            config_path = os.path.expanduser(self.config_file)
            try:
                with open(config_path, 'w') as write:
                    yaml.dump(data, write, Dumper=ruamel.yaml.RoundTripDumper, indent=2)
                    log.debug(" updated schema @ {}".format(config_path))
                    return True
            except IOError:
                log.error("failed to dump schema @ {}".format(config_path))
                raise
            return

    def getElevators(self):
        # get number of elevators
        elevator_list = []
        yaml_data = self.loadElevatorConfigs()

        if yaml_data:
            for configs in yaml_data['elevators']:
                elevator_list.append(configs['id'])
        else:
            raise FileNotFoundError("Config data not found ")
        return(elevator_list)

    def getFloors(self):
        # get number of floors

        yaml_data = self.loadElevatorConfigs()

        if yaml_data:
            floors = yaml_data['floors']
        else:
            raise FileNotFoundError("Config data not found ")
        return(int(floors))

    def getElevatorStatus(self):
        # get list of elevators and status
        config_data = self.loadElevatorConfigs()
        elevator_state = []

        if 'status' in config_data:
            print("No. of elevators {}".format(len(config_data['status'])))
            for status in config_data['status']:
                if status['state'] == "ready" or status['state'] == "transit":
                    print("Elevator {} is online...".format(status['id']))
                    response = self.compareTime(status['endtime'])
                    elevator_state.append({
                                        "id": status['id'],
                                        "floor": status['floor'],
                                        "state": response})
                else:
                    print(
                        "Elevator {} is in maintainence mode."
                        .format(status['id']))
        else:
            raise("No status configs found in configs.yaml")

        return(elevator_state)

    def determinDirection(self, elevator_id, requested_floor):
        data = self.loadElevatorConfigs()
        # determine the direction
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        for status in data['status']:
            if status['id'] == elevator_id:
                floor = status['floor']
                if floor < int(requested_floor):
                    direction = "up"
                elif floor > int(requested_floor):
                    direction = "down"
                else:
                    direction = "present"
        if direction == "up" or direction == "down":
            print(
                "elevator {} coming {} to pickup on floor {}"
                .format(elevator_id, direction, requested_floor))
        else:
            print(
                "elevator {} is already {} on same floor {}"
                .format(elevator_id, direction, requested_floor))
        return

    def pickBestElevator(self, selected_elevator, requested_floor):
        # algo to pick the most efficient elevator

        elevator_score = []
        for elevator in selected_elevator:
            if elevator['state']:
                distance = abs(int(elevator['floor']) - int(requested_floor))
                elevator_score.append({'id': elevator['id'], 'score': distance})
            else:
                print(
                    "Please wait Elevator {} is in transit state to floor {}"
                    .format(elevator['id'], elevator['floor']))

        if elevator_score:
            best_elevator = min(elevator_score, key=lambda x: x['score'])['id']
            print("Found the best and fastest elevator: ", best_elevator)
            self.determinDirection(best_elevator, requested_floor)
            return(best_elevator)

    def checkEta(self, id, desired_floor, requested_floor):
        # print the ETA
        strp_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        dstrp_time = datetime.datetime.strptime(strp_time, '%H:%M:%S')

        if id and dstrp_time:
            floor_difference = int(requested_floor) - int(desired_floor)
            travel_time = abs(floor_difference) * self.time_per_floor

            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(0, travel_time)
            eta_time = datetime.datetime.strftime(end_time, '%H:%M:%S')

            print("Eta for Elevator {}: {}".format(id, eta_time))

        return(start_time, end_time)

    def updateTime(self, id, requested_floor, desired_floor):
        # check and update time in config file
        config_data = self.loadElevatorConfigs()
        # check timestamp
        if id:
            for state in config_data['status']:
                if state['id'] == id:
                    end_time = state['endtime']
            response = self.compareTime(end_time)
        else:
            print("Error while updating time.")

        eta_time = self.checkEta(id, desired_floor, requested_floor)
        start_time = eta_time[0]
        end_time = eta_time[1]

        # update timestamp
        self.updateConfigs(
                        config_data,
                        id,
                        desired_floor,
                        response,
                        start_time,
                        end_time)
        return

    def compareTime(self, end_time):
        # compare time of elevators
        current_time = datetime.datetime.now()
        if end_time:
            if end_time < current_time:
                return True
            elif end_time > current_time:
                return False
            else:
                return False

    def printElevatorStatus(self, elevators_state):
        # print elevator state
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        print("          CURRENT STATE OF ELEVATORS          ")
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        for status in elevator_state:
            if status['state'] is True:
                print(
                    "Elevator {} is available on floor {}"
                    .format(status["id"], status['floor']))
            elif status['state'] is False:
                print(
                    "Elevator {} is in transit state to floor {}"
                    .format(status["id"], status['floor']))
            else:
                print(
                    "Elevator {} is in transit state on floor {}"
                    .format(status["id"], status['floor']))
        return

    def updateConfigs(
                    self,
                    data,
                    id,
                    desired_floor,
                    response,
                    start_time,
                    end_time):

        # print configs to file
        if response is True:
            for state in data['status']:
                if state['id'] == id:
                    state['state'] = 'transit'
                    state['floor'] = int(desired_floor)
                    state['starttime'] = start_time
                    state['endtime'] = end_time
                    self.dumpElevatorConfigs(data)


class Elevator():
    def __init__(self, elevator_id, requested_floor, desired_floor):
        self.id = elevator_id
        self.requested_floor = requested_floor
        self.desired_floor = desired_floor
        self.direction = "up"

    def setElevatorInMotion(self):
        # set elevator in motion
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        if self.direction == "up" or self.direction == "down":
            print(
                "Elevator {} now in transit to floor {}"
                .format(self.id, self.desired_floor))
        else:
            print(
                "Elevator {} remains still on floor {}"
                .format(self.id, self.desired_floor))
        return


if __name__ == '__main__':
    print("----------------------------------")
    print("-------PRESS CTRL+C TO STOP-------")
    print("----------------------------------")

    ecs = ElevatorControlSystem("configs/configs.yaml")
    no_of_elevators = len(ecs.getElevators())
    no_of_floors = ecs.getFloors()

    if no_of_floors and no_of_elevators:
        print("--Configs loaded!--")
        print("Checking elevator status..")
        elevator_state = ecs.getElevatorStatus()
        ecs.printElevatorStatus(elevator_state)

        # while(True)
        print("+++++++++++++++++++++++++++++++++++++++++++")
        print("               SELECT OPTIONS              ")
        print("+++++++++++++++++++++++++++++++++++++++++++")
        requested_floor = input("Which floor you are on? ")
        desired_floor = input("Which floor you want to go? ")
        if requested_floor != "" and desired_floor != "":

            # check range of input
            requested_floor_limit = 1 <= int(requested_floor) <= int(no_of_floors)
            desired_floor_limit = 1 <= int(desired_floor) <= int(no_of_floors)

            if requested_floor != desired_floor:
                if requested_floor_limit and desired_floor_limit:
                    print(
                        "Checking for the most efficient elevator you can take...")
                    best_elevator = ecs.pickBestElevator(elevator_state, requested_floor)
                    if best_elevator:
                        e = Elevator(
                                    int(best_elevator),
                                    requested_floor,
                                    desired_floor)
                        e.setElevatorInMotion()
                        ecs.updateTime(best_elevator, requested_floor, desired_floor)
                else:
                    print(
                        "Input is out of range: min 1 and max {} allowed"
                        .format(no_of_floors))
            else:
                print("You're on same floor as your request.")
