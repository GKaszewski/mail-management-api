from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from .endpoints import router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/", router)


urlpatterns = [
    path('', api.urls),
]