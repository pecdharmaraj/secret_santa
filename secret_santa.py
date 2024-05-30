
import csv
import random
#import unittest

class Employee:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Employee(name={self.name}, email={self.email})"

class SecretSanta:
    def __init__(self, employees, previous_assignments):
        self.employees = employees
        self.previous_assignments = previous_assignments
        self.assignments = {}

    def is_valid_assignment(self, giver, receiver):
        if giver == receiver:
            return False
        if self.previous_assignments.get(giver.email) == receiver.email:
            return False
        return True

    def assign(self):
        available_receivers = self.employees[:]
        random.shuffle(available_receivers)

        for giver in self.employees:
            for receiver in available_receivers:
                if self.is_valid_assignment(giver, receiver):
                    self.assignments[giver] = receiver
                    available_receivers.remove(receiver)
                    break
            else:
                raise Exception("No valid assignment found. Please check the constraints and try again.")

        return self.assignments

def read_employees(file_path):
    employees = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                employees.append(Employee(row['Employee_Name'], row['Employee_EmailID']))
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")
    return employees

def read_previous_assignments(file_path):
    previous_assignments = {}
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                previous_assignments[row['Employee_EmailID']] = row['Secret_Child_EmailID']
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")
    return previous_assignments

def write_assignments(assignments, file_path):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID'])
            for giver, receiver in assignments.items():
                writer.writerow([giver.name, giver.email, receiver.name, receiver.email])
    except Exception as e:
        print(f"Error: {e}")

def main():
    employees = read_employees('employees.csv')
    previous_assignments = read_previous_assignments('previous_assignments.csv')

    if not employees:
        print("No employees found. Exiting.")
        return

    secret_santa = SecretSanta(employees, previous_assignments)
    try:
        assignments = secret_santa.assign()
        write_assignments(assignments, 'new_assignments.csv')
        print("Secret Santa assignments successfully created.")
    except Exception as e:
        print(f"Error: {e}")

'''class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        self.employees = [Employee("Abi", "abi@example.com"), Employee("Dharma", "dharma@example.com")]
        self.previous_assignments = {"abi@example.com": "dharma@example.com", "dharma@example.com": "abi@example.com"}

    def test_no_self_assignment(self):
        secret_santa = SecretSanta(self.employees, {})
        assignments = secret_santa.assign()
        for giver, receiver in assignments.items():
            self.assertNotEqual(giver, receiver)

    def test_no_repeat_assignment(self):
        secret_santa = SecretSanta(self.employees, self.previous_assignments)
        assignments = secret_santa.assign()
        for giver, receiver in assignments.items():
            self.assertNotEqual(self.previous_assignments[giver.email], receiver.email)'''

if __name__ == "__main__":
    main()
    #unittest.main(argv=[''], verbosity=2, exit=False)

