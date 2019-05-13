## Elevator System Design.


### Usecase Diagram for Elevator System

![](images/usecase_diagram_ecs.png)

The above mentioned diagram depicts following usecases for a Elevator System.

**Actors:**

- Elevator system would consist of two actors passenger and maintainer
- Maintainer does same tasks as user but additionally performs maintainence

**Usecases:**

- PressFloorButton: The passenger in this usecase presses the floor button requesting an elevator
- PressElevatorButton: The passenger here uses buttons inside elevator to select the floor they would like to go on
- CheckIndicator: The passenger checks indicator to see if the intended floor has arrived or not
- CheckDirection: The passenger checks the direction of lift from lobby, floors and from inside of the elevator

Environment controlled:
- EmergencyBrakes: The passenge can apply for emergency stop
- PerformMaintainence: The maintainer performs maintainence tests on the elevator

Therefore, the usecase diagrams states that the passenger/maintainer is interacting with Elevator system by making elevator class and decide get on/off depending on indications from the system.


### Class Diagram for Elevator System (Software Architecture View)

![](images/class_diagram_ecs.png)

This diagram is used to portrait the object-oriented side of system which is scalable and efficient. It tries to give a static view of whole system at once.

In class diagram, all the control objects are derived from the super class `ElevatorControlSystem`. The control objects share (some of) the property of `ElevatorControlSystem`, and has its own attributes and operations used for the object it controls.

- `DoorControl` controls the action of DoorMotor, each of the two `DoorMotors` on the elevator is controlled by a `DoorControl` object. `DoorMotor` can be commanded to open, close, or make a door reversal.
- `DriveControl` controls the elevator Drive, which acts as the main motor moving the car up and down, and stopping at floors when necessary.
- `FloorLightControl` are in the number of two on each floor, each indicates the current moving direction of the elevator.
- `ButtonControl` is one for each floor and in the elevators. The `ElevatorButtonControl` accepts `ElevatorRequestButton` calls and is in charge of turning on/off the corresponding elevator call lights.
- ElevatorControl controls elevator actions like start, stop and reset elevetors, also the `ElevatorPositionIndicator/Status` helps passengers to know current position of the elevator.
- `Safety` and `Maintenance` are also an environmental object, which does not belong to the control software but is an important part of the system. In the real world, the safety and maintenance actions vary.


- **What’s the most effective way to move people?**

  - The most effective way will be have an efficient algorithm like having separate queues for up and down requests or implement priority queues or heap queue.

- **How will your system scale?**

  - The system as showed in class diagram will scale horizontally - the requests will be handled by respective control classes which manage the object
  - where there can more than ``ElevatorControlSystem`` class to scale vertically.
  - The having separate control classes will avoid issues like compute shortage, single point of failure and under utilized resources

- **What can fail? How will your system recover?**

  - The elevator system is can be prone to a various issues:
    - power outages:  it is important to have a backup power supply for each elevator so that it can safely reach nearest floors
    - button/indicator or external hardware device failures: buttons and indicator failure can be man made or natural, therefore, it is suggested that each button/indicator are replaced as an when possible. This can also lead to users breaking the button/indicators while they attempt to fix it on their own which can also may lead to issues with other system devices.
    - sensor failures : sensor failures are critical for elevator to open/close doors and to stop therefore it is important that the maintainence of sensors are done on regular basis
  Once can recover from all above issues by making sure that elevator is bought from a certified authority with all safety certificates and manuals - users can be trained on how to use elevators during emergency.

- **What are the security concerns?**

  - Security concerns can be following:
    - Outdated firmware and software update/upgrades - it is important that the firmware and software are patched on time to time basis to avoid any security vulnerabilities
    - Physical security - sometimes like movies peopled try to hack into elevator softwares to control them - that can only happy if elevators and its sockets are not protected, therefore, it is important that all the sockets and connections to elevator are protected/sealed.
    - Unauthorised access - People not belonging to certain premises can access elevators easily once they manage to get in premises, therefore, to protect that one can implement access card based elevator function so that only authorised users can use elevators with there access card.
