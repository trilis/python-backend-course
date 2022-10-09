# Queue management system 

Tiny electronic appointment management system, can be used in banks or other institutions with appointment queue. Supported operations:
* Booking appointment for service with code `Code` and client `Name`: `/book/?name=Name&service_code=Code`. Returns json `{"queue_id": Id}`, where `Id` is id for your appointment.
* Checking status of appointment with id `Id`: `/check/Id`. Returns json `{"message": Msg}`, where `Msg` is human-readable status message.
* Cancelling pre-booked appointment with id `Id`: `/cancel/Id`. Returns empty json.


## Building

```
poetry install
```

## Testing

```
poetry run pytest
```

## Launching

```
poetry run uvicorn src.app:app
```
After launching, auto-generated docs can be found at `http://127.0.0.1:8000/docs`