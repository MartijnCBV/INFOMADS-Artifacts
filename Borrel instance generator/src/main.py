import random
import datetime
import os
from typings.types import Student, Instance, Obligation
from config import config
import numpy as np
from playwright.sync_api import sync_playwright, Playwright, Browser, Page

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

def fill_slots(timeslot: int, obligations: list[Obligation]) -> list[int]:
	filled_slots = []
	for obligation in sorted(obligations, key=lambda o: o["id"], reverse=True):
		obligation_fill = np.arange(obligation["start"], obligation["end"] + 1, step=1).tolist()
		obligation_fill = sorted(list(set(obligation_fill) - set(filled_slots)))

		diff = (obligation["end"] - obligation["start"] + 1) - len(obligation_fill)
		remove = (obligation["end"] - obligation["start"] + 1) - obligation["length"] - diff

		start = next((i for i, item in enumerate(obligation_fill) if item >= timeslot), obligation["end"] - remove)
		obligation_fill = list(set(obligation_fill) - set(obligation_fill[start:start+remove]))

		if len(obligation_fill) < obligation["length"]:
			return filled_slots
		else:
			filled_slots.extend(obligation_fill)

	return sorted(filled_slots)

def available_bounds_from_timeslot(student: Student, timeslot: int) -> tuple[bool, int, int]:
	overlapping = []
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

	filled_slots = fill_slots(timeslot, overlapping)

	# pick slot closest to left bound
	bound_right = outer_right \
		if filled_slots[len(filled_slots) - 1] < bound_left \
		else next(x for x in filled_slots if x >= bound_left) - 1

	if bound_right < bound_left:
		return False, 0
	else:
		bound_right = bound_right if outer_right is not bound_right else config["timeslots"]
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

		for timeslot in range(1, config["timeslots"] + 1):
			can_add, bound_right = available_bounds_from_timeslot(student, timeslot)
			if can_add and random.random() < config["obligation_probability"]:
				ob_max = config["obligation_max_length"]
				bound_max_length = random.randint(1, min(bound_right - timeslot + 1, ob_max))

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

def init_playwright(playwright: Playwright) -> tuple[Browser, Page]:
	browser = playwright.chromium.launch()
	page = browser.new_page()
	page.goto('https://martijncbv.github.io/INFOMADS-Visualiser/')

	return browser, page

def run():
	with sync_playwright() as playwright:
		if config["include_images"]:
			browser, page = init_playwright(playwright)

		os.makedirs("outputs", exist_ok=True)

		timeNow = datetime.datetime.now().timestamp()

		if config["debug"]:
			seed = 80
			random.seed(seed)
			timeNow = f'debug-{seed}'

		f = open(f'outputs/instances-{timeNow}.txt', "a")
		f.truncate(0)

		for i in range(config["instances"]):
			output = generate_instance()
			f.write(output + '\n\n')

			if config["include_images"]:
				page.locator('#problem-in').fill(output)
				page.locator('#problem-submit').click()
				page.locator('svg').screenshot(path=f'outputs/images/instance-{timeNow}-{i}.png')

		if config["include_images"]:
			browser.close()
		f.close()

run()