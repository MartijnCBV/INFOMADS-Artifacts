from typings.types import Config

config: Config = {
	"instances": 20,
	"timeslots": 10,
	"students": 4,

	"obligation_max_length": 6,
	"obligation_probability": 0.5,

	"borrel_length_range": (1, 3),
	"borrel_amount": 2,

	"can_overlap": True,
	"is_flexible": True,
}