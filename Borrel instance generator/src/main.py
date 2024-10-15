import random
import datetime
import os
from typings.types import Student, Instance, Obligation
from config import config

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

def available_bounds(student: Student, timeslot: int) -> tuple[bool, int, int]:
	overlapping = []

	for obligation in student["obligations"]:
		if timeslot >= obligation["start"] and timeslot <= obligation["end"]:
			overlapping.append(obligation)

	if len(overlapping) == 0:
		return True, timeslot, config["timeslots"]
	elif config["can_overlap"] == False:
		return False, 0, 0

	total_length = 0
	outer_left = min([obligation["start"] for obligation in overlapping])
	outer_right = max([obligation["end"] for obligation in overlapping])

	# additional overlaps
	for obligation in student["obligations"]:
		if ((outer_left <= obligation["start"] <= outer_right) or \
			(outer_left <= obligation["end"] <= outer_right)) and \
			any([obligation["id"] == o["id"] for o in overlapping]) == False:
			overlapping.append(obligation)

	for obligation in overlapping:
		print(obligation["length"])
		total_length += obligation["length"]

	if outer_left + total_length - 1 >= timeslot:
		return False, 0, 0

	print(timeslot, total_length)
	total_length -= timeslot - outer_left

	bound_left = timeslot

	if total_length > 0:
		bound_right = outer_right - total_length
	else:
		bound_right = config["timeslots"]

	if bound_right < bound_left:
		return False, 0, 0
	else:
		return True, bound_left, bound_right

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
		id = 1

		for timeslot in range(1, config["timeslots"]):
			print(timeslot)
			can_add, bound_left, bound_right = available_bounds(student, timeslot)
			if can_add and random.random() < 0.5 and bound_left == timeslot:
				ob_max = config["obligation_max_length"]
				length = random.randint(1, min(bound_right, ob_max))

				end = min(timeslot + length - 1, config["timeslots"])
				length = random.randint(1, end - timeslot + 1) if config["is_flexible"] else end - timeslot + 1

				student["obligations"].append({
					"id": id,
					"start": timeslot,
					"end": end,
					"length": length,
				})
				id += 1
			print(student)

		new_instance["students"].append(student)

	return generate_instance_output(new_instance)

def run():
	os.makedirs("outputs", exist_ok=True)
	# timeNow = datetime.datetime.now().timestamp()
	timeNow = 1
	f = open(f'outputs/instances-{timeNow}.txt', "a")
	f.truncate(0)

	for i in range(config["instances"]):
		output = generate_instance()
		f.write(output + '\n\n')
		print(output)


	f.close()

# random.seed(500)
run()



# student_test = {
# 	"obligations": [
# 		{"start": 1, "end": 4, "length": 2},
# 		{"start": 2, "end": 3, "length": 1},
# 		{"start": 2, "end": 2, "length": 1},
# 	]
# }

student_test = {
	"obligations": [
		{"id": 1, "start": 5, "end": 9, "length": 2},
		{"id": 2, "start": 6, "end": 9, "length": 2},
	]
}

# print(available_bounds(student_test, 7))