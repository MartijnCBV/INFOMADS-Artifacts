from typings.types import Config

config: Config = {
	"debug": False,
	"instances": 1,
	"timeslots": 10,
	"students": 4,

	"obligation_max_length": 6,
	"obligation_probability": 1,

	"borrel_length_range": (1, 3),
	"borrel_amount": 2,

	"can_overlap": True,
	"is_flexible": True,
}