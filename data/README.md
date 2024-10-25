# Data

This folder contains all the raw and processed data obtained from running the project.
The JSON files contain the raw data and are structured in the following way:
```json
{
    "instance name": {
        "measurement name": {
            "best": "some float",
            "average": "some float",
            "runs": [ "a series of floats" ]
        }
        ...
    }
    ...
}
```
The [plots folder](./plots/) contains processed data in the form of pdf images containing graphs/plots.