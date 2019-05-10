## Elevator System Design.


###Usecase Diagram for Elevator System

![](images/usecase_diagram_ecs.png)

The above mentioned diagram depicts following usecases for a Elevator System.

Actors:

- Elevator system would consist of two actors passenger and maintainer 
- Maintainer does same tasks as user but additionally performs maintainence

Usecases:

- PressFloorButton: The passenger in this usecase presses the floor button requesting an elevator
- PressElevatorButton: The passenger here uses buttons inside elevator to select the floor they would like to go on
- CheckIndicator: The passenger checks indicator to see if the intended floor has arrived or not
- CheckDirection: The passenger checks the direction of lift from lobby, floors and from inside of the elevator
- PerformMaintainence: The maintainer performs maintainence tests on the elevator

Therefore, the usecase diagrams states that the passenger/maintainer is interacting with Elevator system by making elevator class and decide get on/off depending on indications from the system.


###Class Diagram for Elevator System (Software Architecture View)

![](images/class_diagram_ecs.png)

This diagram is used to potrait the object-oriented side of system which is scalabled and efficient. It also gives a view of whole system in detail.

In class diagram all the control objects are derived from the super class ElevatorControlSystem. The control objects share (some of) the property of ElevatorControlSystem, and has its own attributes and operations used for the object it controls.

- DoorControl controls the action of DoorMotor, each of the two DoorMotors on a car is controlled by a DoorControl object. DoorMotor can be commanded to open, close, or make a door reversal.
- DriveControl controls the elevator Drive, which acts as the main motor moving the car up and down, and stopping at floors when necessary.
- FloorIndicatorControl are in the number of two on each floor, each indicates the current moving direction of the car.
- LanternControl are in the number of two, each controls a CarLantern indicating the current moving direction of the car. 
- CarButtonControl is one for each floor and all locate in the car. The CarButtonControl accepts CarCallButton calls and is in charge of turning on/off the corresponding car call lights.
- CarPositionIndicator gives value to the CarPositionIndicator so that the passengers might know the current position of the car. 
- Safety is also an environmental object, which does not belong to the control software but is an important part of the system. In the real world, the safety actions vary if the 