# mds-cvrp-crud

![Python application](https://github.com/andromia/mds-cvrp-crud/workflows/Python%20application/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

[Under Development]

REST API implementation for cvrp-app CRUD abstracted microserice to dynamically support [cvrp-app-rpc](https://github.com/andromia/cvrp-app-rpc).

## MVP

```/api/<version>/```

## Unit

```Unit```s are different *unit of measures* used (pallets, weight, miles).

- ```id```: integer
- ```name```: string ('pallets', 'weight', 'miles')

## Origin

```Origin```s are the node users want to generate routes from (routes are sequences of stops):

- ```id```: integer
- ```latitude```: float
- ```latitude```: float

### Manage Origins

- **endpoint**: /origin
- **methods**: ```GET```, ```POST```
- **```GET``` data expected:**

  ```json
  {
    "id": "",
    "latitude": "",
    "latitude": ""
  }
  ```

- **```POST``` data required:**

  ```json
  {
    "latitude": "",
    "longitude": ""
  }
  ```

## Demand

```Demand``` is each node with capacity to route:

- ```id```: integer
- ```latitude```: float
- ```longitude```: float
- ```units```: float
- ```unit_id```: integer
- ```cluster_id```: integer

### Manage Demand

- **endpoint**: /demand
- **methods**: ```GET```, ```POST```
- **```GET``` data expected:**

  ```json
  {
    "demands": [ {
      "id": ,
      "latitude": ,
      "longitude": ,
      "units": ,
      "unit_name": ,
      "cluster_id":
      }
    ]
  }
  ```

- **```POST``` data required:**

  ```json
  {
    "demands": [
      {
      "latitude": ,
      "longitude": ,
      "units": ,
      "unit_name": ,
      "cluster_id":
      }
    ]
  }
  ```

## Vehicle

```Vehicle```s are resources describing vehicle capacity and number of vehicles:

- ```id```: integer
- ```max_capacity_units```: integer
- ```unit_id```: integer

### Manage Vehicles

- **endpoint**: /vehicles
- **methods**: ```GET```, ```POST```, ```CREATE```
- **```GET``` data expected:**

  ```json
  {
    "max_capacity_units": [],
    "unit_name": ""
  }
  ```

- **```POST``` data required:**

  ```json
  {
    "max_capacity_units": [],
    "uom": ""
  }
  ```

- **```CREATE```**
This creates a default set of vehicles for the model to use.

## Solution

```Solution```s define inputs and their outputs via cvrp rpc.

- ```id```: integer
- ```demand_id```: integer
- ```origin_id```: integer
- ```vehicle_id```: float
- ```stop_num```: integer
- ```stop_distance_units```: float
- ```unit_id```: integer

### Manage Solutions

This is what the end goal of the service is for our client.

- **endpoint**: /solution
- **methods**: ```GET```
- **```GET``` data expected:**

  ```json
  {
    "demand_id": [],
    "origin_id": [],
    "vehicle_id": [],
    "stop_num": [],
    "[uom name]": []
  }
  ```
