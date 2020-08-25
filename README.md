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

## Stacks

- `id`: integer
- `name`: string
- `user_id`: integer

### Manage Stacks

- **endpoint**: /stacks
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "stacks": [{
      "id": "",
      "name": "",
      "user_id": ""
    }]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "stack" : {
      "name": ""
    },
    "chain": [{
      "id": "",
      "name": ""
    }]
  }
  ```

## Geocodes

`Geocodes` is a location with latitude and longitudes:

- `id`: integer
- `zipcode`: string
- `country`: string
- `latitude`: float
- `longitude`: float
- `user_id`: integer

### Manage Geocodes

- **endpoint**: /geocodes
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "geocodes": [{
      "id": "",
      "zipcode": "",
      "country": "",
      "latitude": "",
      "longitude": "",
      "user_id": ""
      }
    ]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "geocodes": [{
      "zipcode": "",
      "country": "",
      "latitude": "",
      "longitude": "",
      "user_id": ""
      }
    ]
  }
  ```

## Depot

`Depot`s are points of origin consisting of:

- `id`: integer
- `latitude`: float
- `latitude`: float

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
    "latitude": ""
  }
  ```

## Demand

`Demand` is each node with capacity to be routed:

- `id`: integer
- `latitude`: float
- `longitude`: float
- `quantity`: float
- `unit_id`: integer

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
      "unit": ""
    }]
  }
  ```

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


- **`POST` data expected:**

  ```json
  {
    "routes": [{
    "demand_id": "",
    "depot_id": "",
    "vehicle_id": "",
    "stop_number": "",
    "unit": ""
    }],
  }
  ```
