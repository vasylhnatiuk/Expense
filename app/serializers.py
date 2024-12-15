from django.db.models import Sum
from rest_framework import serializers
from app.models import User, Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'title', 'amount', 'date', 'category']

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value


class FilterSerializerBase(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def filter_expenses(self):
        """
        This method should be overridden in the subclass to provide the specific filtering logic.
        """
        raise NotImplementedError("Subclasses must implement the `filter_expenses` method.")

    def get_user(self):
        """
        Helper method to get the validated user.
        """
        return self.validated_data['user']


class DateRangeFilterSerializer(FilterSerializerBase):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        """
        Custom validation to check that the start date is before the end date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be after end date.")
        return data

    def filter_expenses(self):
        """
        Filters expenses based on the validated user, start_date, and end_date.
        """
        user = self.validated_data['user']
        start_date = self.validated_data['start_date']
        end_date = self.validated_data['end_date']

        expenses = Expense.objects.filter(user=user, date__range=[start_date, end_date])
        return expenses


class CategorySummaryFilterSerializer(FilterSerializerBase):
    month = serializers.IntegerField(required=True, min_value=1, max_value=12)

    def filter_expenses(self):
        """
        Filters the expenses for the given user and month, then calculates the category summary.
        """
        user = self.validated_data['user']
        month = self.validated_data['month']

        expenses = Expense.objects.filter(user=user, date__month=month)

        summary = expenses.values('category').annotate(total=Sum('amount'))
        return summary
