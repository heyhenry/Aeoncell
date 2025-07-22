class Person():
    def __init__(self, gender, age, height, name):
        self.gender = gender
        self.age = age
        self.height = height
        self.name = name
    
person_a = Person("Male", 26, "175cm", "Henry")

attr_name = "gender"
asked_info = getattr(person_a, attr_name)
print(asked_info)
