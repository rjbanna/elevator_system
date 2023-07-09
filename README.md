# Elevator System

### APIs

1. Initialize elevator system
2. List the elevator systems
3. Open the elevator door
4. Close the elevator door
5. Mark the elevator as 'In maintenance'
6. Mark the elevator as 'Operational'
7. Request elevator for floor
8. Get all the requests for the given elevator

### Video walkthrough

* https://drive.google.com/file/d/1cyk4MA5jtu720-mqST88whBmg_ULcGNZ/view?usp=share_link

### Steps to run this project

1. Create virtual environment according to your PC/laptop OS
2. Clone the repo ```git clone https://github.com/rjbanna/elevator_system.git```
3. Install the requirements using command
   ```pip install -r requirements.txt```
4. Run the server ```python manage.py runserver```

### Assumptions

* All the new initialized elevators will be at the ground floor (0) with door closed and operational
* Lift won't be called when it's door is open or it is in maintenance

### API endpoints

* ```/systems/``` - Initializes the elevator system
* ```/systems``` - Lists all the elevator systems
* ```/elevators/<pk>/door/open``` - Opens the door of elevator ```<pk>```
* ```/elevators/<pk>/door/close``` - Closes the door of elevator ```<pk>```
* ```/elevators/<pk>/maintenance/start``` - Marks the elevator ```<pk>``` as 'In maintenance'
* ```/elevators/<pk>/maintenance/stop``` - Marks the elevator ```<pk>``` as 'Operational'
* ```/elevators/call/``` - Calls the nearest elevator to the requested floor and the elevator goes to the destination floor
* ```/elevators/<pk>/requests``` - Lists the user requests for ```<pk>``` elevator

### Deployment

* This project can be deployed to any cloud services like AWS, GCP or Azure
* Create the docker image for more reliability
