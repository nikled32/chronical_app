import flet as ft


# views
from views.index_view import IndexView
from views.doctor_view import DoctorView
from views.patient_view import PatientView


class Router:
    def __init__(self, page, ft):
        self.page = page
        self.ft = ft
        self.routes = {
            "/": IndexView(page),
            "/doctor_page": DoctorView(page),
            "/patient_page": PatientView(page)
        }
        self.body = ft.Container(content=self.routes['/'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()