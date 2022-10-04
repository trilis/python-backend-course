from asyncio import queues
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import re
from urllib import response

import grpc

from definitions.builds.service_pb2 import Appointment, Null, CheckResponse
from definitions.builds.service_pb2_grpc import AppointmentServiceServicer, add_AppointmentServiceServicer_to_server


class Service(AppointmentServiceServicer):

    appointments = dict()
    queues_ids = dict()
    cancelled = dict()

    def BookAppointment(self, request, context):
        if not (request.service_code in self.queues_ids):
            self.queues_ids[request.service_code] = 1
        id = request.service_code + str(self.queues_ids[request.service_code])
        self.queues_ids[request.service_code] += 1
        self.appointments[id] = request.name
        response = Appointment(queue_id=id)
        return response

    def CancelAppointment(self, request, context):
        if not (request.queue_id in self.appointments):
            return Null()
        self.cancelled[request.queue_id] = self.appointments[request.queue_id]
        self.appointments.pop(request.queue_id)
        return Null()

    def CheckAppointment(self, request, context):
        if not (request.queue_id in self.appointments):
            if request.queue_id in self.cancelled:
                name = self.cancelled[request.queue_id]
                cancelled_message = "Dear " + name + ", your appointment " + request.queue_id + " is successfully cancelled."
                return CheckResponse(response_message=cancelled_message)
            else:
                fail_message = "We can't find appointment with ID " + request.queue_id + \
                                ". Please check your ID or try to book an apointment again"
                return CheckResponse(response_message=fail_message)
        name = self.appointments[request.queue_id]
        ok_message = "Dear " + name + ", your appointment " + request.queue_id + " is valid."
        return CheckResponse(response_message=ok_message)

def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_AppointmentServiceServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:3000")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()