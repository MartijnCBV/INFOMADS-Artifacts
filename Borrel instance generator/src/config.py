from typings.types import Config, Algorithm

config: Config = {
	"debug": True,
	"save_folder_name": "output",
	"include_images": False,
	"instances": 1,
	"timeslots": 700,
	"students": 1,
	"algorithm": Algorithm.EXACT,

	# Exact config
	"obligations_per_student": 400,
	"total_obligation_time_per_student": 420,

	# Random config
	"obligation_max_length": 6,
	"obligation_probabilities": [1, 0.5, 0.25, 0.1],

	"borrel_length_range": (1, 3),
	"borrel_amount": 2,

	"can_overlap": True,
	"is_flexible": True,
}