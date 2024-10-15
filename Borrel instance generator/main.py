from typing import TypedDict
import math
import random
import datetime
import os
import json

class Config(TypedDict):
	instances: int
	timeslots: int
	students: int
	obligation_length_range: tuple[int, int]
	borrel_length_range: tuple[int, int]
	borrel_amount: int
	is_overlapping: bool
	is_flexible: bool

class Obligation(TypedDict):
	start: int
	end: int
	length: int

class Student(TypedDict):
	obligations: list[Obligation]

class Instance(TypedDict):
	timeslots: int
	borrels: list[int]
	students: list[Student]

config: Config = {
	"instances": 2,
	"timeslots": 10,
	"students": 4,

	"obligation_length_range": (1, 6),

	"borrel_length_range": (1, 3),
	"borrel_amount": 2,

	"is_overlapping": False,
	"is_flexible": True,
}

test_instance: Instance = {
	"timeslots": 10,
	"borrels": [1, 3],
	"students": [
		{
			"obligations": [
				{"start": 1, "end": 4, "length": 3},
				{"start": 5, "end": 10, "length": 6},
			]
		},
		{
			"obligations": [
				{"start": 2, "end": 5, "length": 1},
			]
		},
		{
			"obligations": [
				{"start": 4, "end": 10, "length": 3},
			]
		},
		{
			"obligations": [
				{"start": 1, "end": 3, "length": 1},
				{"start": 1, "end": 6, "length": 5},
				{"start": 3, "end": 9, "length": 2},
				{"start": 8, "end": 8, "length": 1},
			]
		},
	]
}

def generate_student_output(student_index: int, instance: Instance) -> str:
	student = instance["students"][student_index]
	output = []
	output.append(f'{len(student["obligations"])}')

	for obligation in student["obligations"]:
		output.append(f'{obligation["start"]}, {obligation["end"]}, {obligation["length"]}')

	return ', '.join(output)


def generate_students_output(instance: Instance) -> str:
	students = []

	for i in range(config["students"]):
		students.append(generate_student_output(i, instance))

	return '\n'.join(students)

def generate_instance_output(instance: Instance) -> str:
	return '\n'.join(
		str(num) for num in
		[
			instance["timeslots"],
			len(instance["borrels"]),
			', '.join(str(e) for e  in instance["borrels"]),
			len(instance["students"]),
			generate_students_output(instance),
		]
	)

def can_add_obligation(student: Student, timeslot: int) -> bool:
	for obligation in student["obligations"]:
		if timeslot >= obligation["start"] and timeslot <= obligation["end"]:
			return False

	return True

def generate_instance() -> str:
	new_instance: Instance = {
		"timeslots": config["timeslots"],
		"borrels": [],
		"students": [],
	}

	for i in range(config["borrel_amount"]):
		new_instance["borrels"].append(random.randint(*config["borrel_length_range"]))

	for i in range(config["students"]):
		student: Student = {"obligations": []}

		for timeslot in range(1, config["timeslots"]):
			if can_add_obligation(student, timeslot) and random.random() < 0.5:
				length = random.randint(*config["obligation_length_range"])

				end = min(timeslot + length - 1, config["timeslots"])
				student["obligations"].append({
					"start": timeslot,
					"end": end,
					"length": end - timeslot + 1,
				})

		new_instance["students"].append(student)

	return generate_instance_output(new_instance)

def run():
	os.makedirs("outputs", exist_ok=True)
	f = open(f'outputs/instances-{datetime.datetime.now().timestamp()}.txt', "a")

	for i in range(config["instances"]):
		f.write(generate_instance() + '\n\n')

	f.close()

run()