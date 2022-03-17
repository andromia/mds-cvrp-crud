# solverstack-crud

![crud](https://github.com/cnpryer/solverstack-crud/workflows/crud/badge.svg)

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
- `stack_id`: integer

### Manage Geocodes

- **endpoint**: /geocode
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "stack_id": "",
    "geocodes": [{
      "id": "",
      "zipcode": "",
      "country": "",
      "latitude": "",
      "longitude": "",
      }
    ]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "stack_id": "",
    "geocodes": [{
      "zipcode": "",
      "country": "",
      "latitude": "",
      "longitude": "",
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
    "stack_id": "",
    "depots": [{
      "id": "",
      "latitude": "",
      "latitude": ""
    }]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "stack_id": "",
    "depots" : [{
    "latitude": "",
    "latitude": "",
    }]
  }
  ```

## Demand

`Demand` is each node with capacity to be routed:

- `id`: integer
- `latitude`: float
- `longitude`: float
- `quantity`: float
- `unit_id`: integer
- `stack_id`: integer

### Manage Demand

- **endpoint**: /demand
- **methods**: `GET`, `POST`
- **`GET` data expected:**

  ```json
  {
    "stack_id": "",
    "demand": [{
      "id": "",
      "latitude": "",
      "longitude": "",
      "quantity": "",
      "unit": ""
      }
    ]
  }
  ```

- **`POST` data required:**

  ```json
  {
    "stack_id": "",
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
- `stack_id`: integer

### Manage Routes

- **endpoint**: /route
- **methods**: `GET`
- **`GET` data expected:**

  ```json
  {
    "stack_id": "",
    "routes": [{
    "demand_id": "",
    "depot_id": "",
    "vehicle_id": "",
    "stop_number": "",
    "unit": ""
    }],
  }
  ```


- **`POST` data expected:**

  ```json
  {
    "stack_id": "",
    "routes": [{
    "demand_id": "",
    "depot_id": "",
    "vehicle_id": "",
    "stop_number": "",
    "unit": ""
    }],
  }
  ```
