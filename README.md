# solverstack-crud

![crud](https://github.com/andromia/solverstack-crud/workflows/crud/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

[Under Development]

CRUD service for solverstack service modules.

## MVP

`/api/<version>/`

## Unit

`Unit`s are different _unit of measures_ used (pallets, weight, miles).

- `id`: integer
- `name`: string ('pallets', 'weight', 'miles')

## Origin

`Origin`s are the node users want to generate routes from (routes are sequences of stops):

- `id`: integer
- `latitude`: float
- `latitude`: float

### Manage Origins

- **endpoint**: /origin
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "origin": {
      "id": "",
      "latitude": "",
      "latitude": ""
    }
  }
  ```

- **`POST` data required:**

  ```json
  {
    "origin" : {
    "latitude": "",
    "latitude": ""
  }
  ```

## Demand

`Demand` is each node with capacity to route:

- `id`: integer
- `latitude`: float
- `longitude`: float
- `quantity`: float
- `unit_id`: integer
- `cluster_id`: integer

### Manage Demand

- **endpoint**: /demand
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "demands": [{
      "id": ,
      "latitude": ,
      "longitude": ,
      "quantity": ,
      "unit": ,
      "cluster_id":
      }
    ]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "demands": [{
      "latitude": ,
      "longitude": ,
      "quantity": ,
      "unit": ,
      "cluster_id":
      }
    ]
  }
  ```

## Vehicle

`Vehicle`s are resources describing vehicle capacity and number of vehicles:

- `id`: integer
- `capacity`: integer
- `unit_id`: integer

### Manage Vehicles

- **endpoint**: /vehicles
- **methods**: `GET`, `POST`, `CREATE`
- **`GET` data expected:**

  ```json
  {
    "vehicles" : [{
      "capacity": ,
      "unit": ""
    }]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "vehicles" : [{
      "capacity": ,
      "unit": ""
    }]
  }
  ```

- **`CREATE`**
  This creates a default set of vehicles for the model to use.

## Solution

`Solution`s define inputs and their outputs via cvrp rpc.

- `id`: integer
- `demand_id`: integer
- `origin_id`: integer
- `vehicle_id`: float
- `stop_number`: integer
- `stop_distance`: float
- `unit_id`: integer

### Manage Solutions

This is what the end goal of the service is for our client.

- **endpoint**: /solution
- **methods**: `GET`
- **`GET` data expected:**

  ```json
  {
    "solutions":[{
    "demand_id": ,
    "origin_id": ,
    "vehicle_id": ,
    "stop_number": ,
    "unit": ""
    }],
  }
  ```
