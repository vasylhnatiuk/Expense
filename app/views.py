from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer, CategorySummaryFilterSerializer, DateRangeFilterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related("user")
    serializer_class = ExpenseSerializer

    @swagger_auto_schema(
        operation_summary="List Expenses by Date Range",
        operation_description="Retrieve all expenses for a specific user within a date range.",
        query_serializer=DateRangeFilterSerializer,
        responses={200: ExpenseSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='date-range', url_name='date_range')
    def list_by_date_range(self, request):
        serializer = DateRangeFilterSerializer(data=request.query_params)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        expenses = serializer.filter_expenses()

        expense_serializer = self.get_serializer(expenses, many=True)
        return Response(expense_serializer.data)

    @swagger_auto_schema(
        operation_summary="Category Summary for a Given Month",
        operation_description="Retrieve the total expenses per category for a specific user in a given month.",
        query_serializer=CategorySummaryFilterSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "category": openapi.Schema(type=openapi.TYPE_STRING, description="Expense category"),
                        "total": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                description="Total amount spent in the category"),
                    },
                ),
            ),
        },
    )
    @action(detail=False, methods=['get'], url_path='category-summary', url_name='category_summary')
    def category_summary(self, request):
        filter_serializer = CategorySummaryFilterSerializer(data=request.query_params)
        if not filter_serializer.is_valid():
            raise ValidationError(filter_serializer.errors)
        summary = filter_serializer.filter_expenses()
        return Response(summary)
