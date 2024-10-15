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

def available_bounds_from_timeslot(student: Student, timeslot: int) -> tuple[bool, int, int]:
	overlapping = []
	total_length = 0
	bound_left = timeslot

	for obligation in student["obligations"]:
		start, end = obligation["start"], obligation["end"]
		if start <= bound_left <= end:
			overlapping.append(obligation)

	if len(overlapping) == 0:
		return True, config["timeslots"]
	elif config["can_overlap"] == False:
		return False, 0

	outer_left = min([obligation["start"] for obligation in overlapping])
	outer_right = max([obligation["end"] for obligation in overlapping])

	# additional overlaps from other obligations
	for obligation in student["obligations"]:
		start, end = obligation["start"], obligation["end"]
		if ((outer_left <= start <= outer_right) or \
			(outer_left <= end <= outer_right)) and \
			any([obligation["id"] == o["id"] for o in overlapping]) == False:
			overlapping.append(obligation)

	for i in range(len(overlapping)):
		# check if gap between obligations is larger than the length of the obligations
		if i + 1 < len(overlapping):
			total_length += max(overlapping[i+1]["start"] - overlapping[i]["start"], overlapping[i]["length"])
		else:
			total_length += overlapping[i]["length"]

	# check if the total length of the obligations exceeds our left bound
	if outer_left + total_length - 1 >= bound_left:
		return False, 0

	total_length -= bound_left - outer_left

	if total_length > 0:
		bound_right = outer_right - total_length
	else:
		bound_right = config["timeslots"]

	if bound_right < bound_left:
		return False, 0, 0
	else:
		return True, bound_right

def generate_instance() -> str:
	instance: Instance = {
		"timeslots": config["timeslots"],
		"borrels": [],
		"students": [],
	}

	for _ in range(config["borrel_amount"]):
		instance["borrels"].append(random.randint(*config["borrel_length_range"]))

	for _ in range(config["students"]):
		student: Student = {"obligations": []}
		id = 1

		for timeslot in range(1, config["timeslots"]):
			can_add, bound_right = available_bounds_from_timeslot(student, timeslot)
			if can_add and random.random() < config["obligation_probability"]:
				ob_max = config["obligation_max_length"]
				bound_max_length = random.randint(1, min(bound_right - timeslot, ob_max))

				end = min(timeslot + bound_max_length - 1, config["timeslots"])
				length = random.randint(1, end - timeslot + 1) if config["is_flexible"] else end - timeslot + 1

				student["obligations"].append({
					"id": id,
					"start": timeslot,
					"end": end,
					"length": length,
				})
				id += 1

		instance["students"].append(student)

	return generate_instance_output(instance)

def run():
	os.makedirs("outputs", exist_ok=True)
	timeNow = datetime.datetime.now().timestamp()
	f = open(f'outputs/instances-{timeNow}.txt', "a")
	f.truncate(0)

	for _ in range(config["instances"]):
		output = generate_instance()
		f.write(output + '\n\n')

	f.close()

run()