from typing import TypedDict

class Config(TypedDict):
	instances: int
	timeslots: int
	students: int
	obligation_max_length: tuple[int, int]
	borrel_length_range: tuple[int, int]
	borrel_amount: int
	can_overlap: bool
	is_flexible: bool

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