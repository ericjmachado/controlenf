from __future__ import unicode_literals

from django.conf.urls import url, include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_nested import routers

from core.api.v1 import views

router = routers.DefaultRouter()

router.register("users", views.UserViewSet, basename="users")
router.register("companies", views.CompanyViewSet, basename="companies")

company_router = routers.NestedSimpleRouter(router, "companies", lookup="companies")
company_router.register("categories", views.CategoryViewSet, basename="categories")
company_router.register("customers", views.CustomerViewSet, basename="customers")
company_router.register("revenues", views.RevenueViewSet, basename="revenues")
company_router.register("expenses", views.RevenueViewSet, basename="expenses")
company_router.register(
    "reports/total-revenue", views.TotalRevenueViewSet, basename="total-revenue"
)
company_router.register(
    "reports/revenue-by-month",
    views.TotalRevenueByMonthViewSet,
    basename="revenue-by-month",
)
company_router.register(
    "reports/revenue-by-customer",
    views.TotalRevenueByCustomerViewSet,
    basename="revenue-by-customer",
)

company_router.register(
    "reports/total-expense", views.TotalExpenseViewSet, basename="total-expense"
)
company_router.register(
    "reports/expense-by-month",
    views.TotalExpenseByMonthViewSet,
    basename="expense-by-month",
)
company_router.register(
    "reports/expense-by-customer",
    views.TotalExpenseByCustomerViewSet,
    basename="expense-by-customer",
)
urlpatterns = [
    url("", include(router.urls)),
    url("", include(company_router.urls)),
    path("auth/", obtain_jwt_token),
    path("auth/sso/", refresh_jwt_token),
]
