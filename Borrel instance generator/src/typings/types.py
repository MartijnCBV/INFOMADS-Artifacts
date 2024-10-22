from typing import TypedDict
from enum import Enum

class Algorithm(Enum):
	RANDOM = 1
	EXACT = 2

class Config(TypedDict):
	debug: bool
	save_folder_name: str
	include_images: bool
	instances: int
	timeslots: int
	students: int
	borrel_length_range: tuple[int, int]
	borrel_amount: int
	can_overlap: bool
	is_flexible: bool

	# Random config
	obligation_max_length: tuple[int, int]
	obligation_probabilities: list[float] # Cycle through these probabilities for each student

	# Exact config
	obligations_per_student: int
	total_obligation_time_per_student: int

	algoritm: Algorithm

class Obligation(TypedDict):
	id: int
	start: int
	end: int
	length: int

class Student(TypedDict):
	obligations: list[Obligation]

class Instance(TypedDict):
	timeslots: int
	borrels: list[int]
	students: list[Student]