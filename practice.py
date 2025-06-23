class Room:
    length = 0.0
    breadth = 0.0

    def calculate_area(self):
        print("area of Room =", self.length * self.breadth)

study_room = Room()

study_room.length = 45.3
study_room.breadth = 20.3

study_room.calculate_area()