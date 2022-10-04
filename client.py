import grpc

from definitions.builds.service_pb2 import Appointment, AppointmentRequest
from definitions.builds.service_pb2_grpc import AppointmentServiceStub


def main():
    with grpc.insecure_channel("localhost:3000") as channel:
        client = AppointmentServiceStub(channel)
        print("To book an apointment, print \"book <NAME> <SERVICE-CODE>\"")
        print("To cancel an apointment, print \"cancel <QUEUE-ID>\"")
        print("To check status of existing apointment, print \"check <QUEUE-ID>\"")
        print("To exit this tool, print \"exit\"")

        while True:
            commands = input().split()
            if len(commands) == 0:
                print("Invalid command")
                continue
            if commands[0] == 'book':
                if (len(commands) != 3):
                    print("Invalid command")
                    continue
                response = client.BookAppointment(AppointmentRequest(
                    name=commands[1],
                    service_code=commands[2]
                ))
                print("A new appointment is created for " + commands[1])
                print("Your queue ID is " + response.queue_id)
            elif commands[0] == 'cancel':
                if (len(commands) != 2):
                    print("Invalid command")
                    continue
                client.CancelAppointment(Appointment(
                    queue_id=commands[1]
                ))
                print("Appointment " + commands[1] + " is cancelled.")
            elif commands[0] == 'check':
                if (len(commands) != 2):
                    print("Invalid command")
                    continue
                response = client.CheckAppointment(Appointment(
                    queue_id=commands[1]
                ))
                print(response.response_message)
            elif commands[0] == 'exit':
                break
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()