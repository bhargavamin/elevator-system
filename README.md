# elevator+system

## Pre-requesite
- python 3.7
- ruamel.yaml (`pip install ruamel.yaml`)
- `configs.yaml` file

## Sample config file code

```
elevators:
- name: ElevatorA
  id: 1
- name: ElevatorB
  id: 2

floors: 5

status:
- id: 1
  state: ready
  starttime: 2019-05-12 04:39:05.698757
  endtime: 2019-05-12 08:39:35.698757
  floor: 1
- id: 2
  state: ready
  starttime: 2019-05-12 08:39:10.186604
  endtime: 2019-05-12 08:39:55.186604
  floor: 1

```

### Running the script

- command : `python elevator.py`

# Inputs

Following inputs required:
```
Which floor you are on?
Which floor you want to go?
```

**Notes:**
- floor 1 is considered as lobby.
- no. of floor can be adjusted from `config.yaml`.
- copy `starttime` and `endtime` from above example config file.
- after every execution the `starttime` and `endtime` will be updated automatically.
- maintainence mode can be set from `config.yaml` by change state of any elevator to `stopped`

### Things can be included in future

- tuning of algorithm - compare remaining elevator transit time with pickup time if less then recommend elevator in transit
- process threads in python to manage elevator request
- advanced elevator request management using queues(priority or heap queues)
- improvise code <> class diagram - extend implementation (introduce classes like door, button, light etc.)
