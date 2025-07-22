class Person():
    def __init__(self, gender, age, height, name):
        self.gender = gender
        self.age = age
        self.height = height
        self.name = name
   
person_1_info = Person("Male", 26, "175cm", "Henry")
person_2_info = Person("Male", 26, "175cm", "Jake")
person_3_info = Person("Male", 26, "175cm", "Ray")
person_4_info = Person("Male", 26, "175cm", "Henson")

people = {
    1: person_1_info,
    2: person_2_info,
    3: person_3_info,
    4: person_4_info
}

for i in range(1, 5):
    print(getattr(people[i], "name"))

