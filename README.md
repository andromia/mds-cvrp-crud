# solverstack-crud

![crud](https://github.com/andromia/solverstack-crud/workflows/crud/badge.svg)
[![Discord](https://img.shields.io/discord/721862473132540007?label=discord&style=plastic)](https://discord.gg/wg7xSAf)
[![Slack](https://img.shields.io/badge/slack-workspace-orange)](https://join.slack.com/t/andromiasoftware/shared_invite/zt-felqfjhs-Tvma8OYuCExxdmQgHOIGsg)

[Under Development]

CRUD service for solverstack.

## MVP

`/api/<version>/`

## User

- `id`: integer
- `username`: string
- `email`: string
- `password_hash`: hashed-string

### Manage Users

- **endpoint**: /user
- **methods**: `GET`, `POST`
- **`GET` data expected:**

**NOTE**: `password_hash` will not be returned in regular `User` `GET`s

  ```json
  {
    "user": {
      "id": "",
      "username": "",
      "email": "",
      "password_hash": ""
    }
  }
  ```

- **`POST` data required:**

  ```json
  {
    "user" : {
    "username": "",
    "email": "",
    "password": ""
  }
  ```

## Unit

`Unit`s are different _unit of measures_ used (pallets, weight, miles).

- `id`: integer
- `name`: string ('pallets', 'weight', 'miles')
- `user_id`: integer

## Depot

`Depot`s are points of origin consisting of:

- `id`: integer
- `latitude`: float
- `latitude`: float
- `user_id`: integer

### Manage Depots

- **endpoint**: /depot
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "depot": {
      "id": "",
      "latitude": "",
      "latitude": "",
      "user_id": ""
    }
  }
  ```

- **`POST` data required:**

  ```json
  {
    "depot" : {
    "latitude": "",
    "latitude": "",
    "user_id": ""
  }
  ```

## Demand

`Demand` is each node with capacity to be routed:

- `id`: integer
- `latitude`: float
- `longitude`: float
- `quantity`: float
- `unit_id`: integer
- `user_id`: integer

### Manage Demand

- **endpoint**: /demand
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "demand": [{
      "id": "",
      "latitude": "",
      "longitude": "",
      "quantity": "",
      "unit": "",
      "user_id": ""
      }
    ]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "demand": [{
      "latitude": "",
      "longitude": "",
      "quantity": "",
      "unit": "",
      "user_id": ""
      }
    ]
  }
  ```

## Vehicle

`Vehicle`s are resources describing vehicle capacity and its availability:

- `id`: integer
- `capacity`: integer
- `unit_id`: integer,
- `user_id`: integer

### Manage Vehicles

- **endpoint**: /vehicles
- **methods**: `GET`, `POST`, `CREATE`
- **`GET` data expected:**

  ```json
  {
    "vehicles" : [{
      "capacity": "",
      "unit": "", 
      "user_id": ""
    }]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "vehicles" : [{
      "capacity": "",
      "unit": "", 
      "user_id": ""
    }]
  }
  ```

- **`CREATE`**
  This creates a default set of vehicles for the model to use.

## Routes

`Routes` define inputs and their outputs via vrp service.

- `id`: integer
- `demand_id`: integer
- `depot_id`: integer
- `vehicle_id`: integer
- `stop_number`: integer
- `unit_id`: integer
- `user_id`: integer

### Manage Routes

- **endpoint**: /routes
- **methods**: `GET`
- **`GET` data expected:**

  ```json
  {
    "routes": [{
    "demand_id": "",
    "depot_id": "",
    "vehicle_id": "",
    "stop_number": "",
    "unit": "",
    "user_id": ""
    }],
  }
  ```
