from typings.types import Instance

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