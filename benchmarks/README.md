# Benchmarks

Multiple benchmarks have been designed to test the performance of the model, these are as follows:
| Benchmark                                           | Description                                                                                                                                   |
| ----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| [general_no_overlap](./general_no_overlap/)         | Randomly generated instances where overlapping obligations were not allowed                                                                   |
| [general_overlap](./general_overlap/)               | Randomly generated instances where overlapping obligations were allowed                                                                       |
| [increasing_borrel_size](./increasing_borrel_size/) | Instances where each instance contains a larger borrel, other aspects of the instance are the same across all instances                       |
| [increasing_borrels](./increasing_borrels/)         | Instances where each instance contains a larger amount of unit sized borrels, other aspects of the instance are the same across all instances |
| [increasing_obligations](./increasing_obligations/) | Instances where each instance contains a higher obligation density, other aspects of the instance are the same across all instances           |
| [increasing_students](./increasing_students/)       | Instances where each instance contains larger amount of students, other aspects of the isntance are the same across all instances             |
| [increasing_timeslots](./increasing_timeslots/)     | Instances where each instance contains larger amount of timeslots, other aspects of the isntance are the same across all instances            |