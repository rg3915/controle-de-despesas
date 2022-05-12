from ninja import NinjaAPI

from backend.expense.api import router as expense_router

api = NinjaAPI()

api.add_router('/expense/', expense_router)
