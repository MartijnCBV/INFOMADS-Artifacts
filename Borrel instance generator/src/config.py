from typings.types import Config

config: Config = {
	"debug": False,
	"include_images": False,
	"instances": 100,
	"timeslots": 20,
	"students": 10,

	"obligation_max_length": 6,
	"obligation_probabilities": [1, 0.5, 0.25, 0.1],

	"borrel_length_range": (1, 3),
	"borrel_amount": 2,

	"can_overlap": True,
	"is_flexible": True,
}