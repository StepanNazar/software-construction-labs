"""Module to represent employees and calculate their month average salaries and taxes."""

import random
from abc import ABC, abstractmethod
from typing import cast

import faker

from descriptors import NonNegative

PDFO_RATE = 0.18
MILITARY_RATE = 0.015
SINGLE_TAX_RATE = 0.05
SINGLE_SOCIAL_CONTRIBUTION = 1760
_fake = faker.Faker(["uk_UA"])


class Employee(ABC):
    """
    Abstract base class to represent an employee and calculate their month average salary and taxes.

    Attributes:
        ipn (int): 10-digit individual personal number.
        first_name (str): First name of the employee.
        last_name (str): Last name of the employee.

    Example:
        >>> class TestEmployee(Employee):
        ...     def calculate_salary(self):
        ...         return 10
        ...
        ...     def calculate_tax(self, salary):
        ...         return 1
        ...
        >>> emp = TestEmployee(1234567890, "John", "Doe")
        >>> emp.ipn
        1234567890
        >>> emp.first_name
        'John'
        >>> emp.last_name
        'Doe'
        >>> emp
        TestEmployee(ipn=1234567890, first_name='John', last_name='Doe')
        >>> emp.calculate_taxed_salary()
        9
        >>> class TaxBiggerThanSalaryEmployee(Employee):
        ...     def calculate_salary(self):
        ...         return 1
        ...     def calculate_tax(self, salary):
        ...         return 10
        ...
        >>> emp = TaxBiggerThanSalaryEmployee(1234567890, "John", "Doe")
        >>> emp.calculate_taxed_salary()
        0
        >>> emp.ipn = 123
        Traceback (most recent call last):
            ...
        ValueError: IPN must be 10 digits long
    """

    def __init__(self, ipn: int, first_name: str, last_name: str):
        self.ipn = ipn
        self.first_name = first_name
        self.last_name = last_name

    @property
    def ipn(self) -> int:
        return self.__ipn

    @ipn.setter
    def ipn(self, value: int):
        if not 1000000000 <= value <= 9999999999:
            raise ValueError("IPN must be 10 digits long")
        self.__ipn = value

    @abstractmethod
    def calculate_salary(self) -> float:
        """Calculate month average salary without taxes."""

    def calculate_taxed_salary(self) -> float:
        """Calculate month average salary after taxes."""
        salary = self.calculate_salary()
        return max(salary - self.calculate_tax(salary), 0)

    @abstractmethod
    def calculate_tax(self, salary: float) -> float:
        """Calculate taxes based on the salary."""

    def __repr__(self):
        return f"{self.__class__.__name__}(ipn={self.ipn}, first_name={repr(self.first_name)}, last_name={repr(self.last_name)})"


class HourlyPaidEmployee(Employee):
    """
    Class to represent an hourly paid employee.

    Attributes:
        hourly_rate (float): Hourly rate paid to the employee.
        worked_hours (int): Total hours worked by the employee.

    Example:
        >>> emp = HourlyPaidEmployee(1234567890, "Jane", "Doe", hourly_rate=100, worked_hours=160)
        >>> emp.calculate_salary()
        16000
        >>> emp.calculate_tax(emp.calculate_salary())
        3120.0
        >>> HourlyPaidEmployee(1234567890, "Jane", "Doe", hourly_rate=-100, worked_hours=160)
        Traceback (most recent call last):
            ...
        ValueError: hourly_rate value must be non-negative
        >>> HourlyPaidEmployee(1234567890, "Jane", "Doe", hourly_rate=100, worked_hours=-160)
        Traceback (most recent call last):
            ...
        ValueError: worked_hours value must be non-negative
    """

    DEFAULT_WORK_HOURS = 20.8 * 8
    hourly_rate = NonNegative()
    worked_hours = NonNegative()

    def __init__(
        self,
        ipn: int,
        first_name: str,
        last_name: str,
        hourly_rate: float,
        worked_hours: int = DEFAULT_WORK_HOURS,
    ):
        super().__init__(ipn, first_name, last_name)
        self.hourly_rate = hourly_rate
        self.worked_hours = worked_hours

    def calculate_salary(self) -> float:
        return self.hourly_rate * self.worked_hours

    def calculate_tax(self, salary: float) -> float:
        return salary * (PDFO_RATE + MILITARY_RATE)


class FixedSalaryEmployee(Employee):
    """Class to represent an employee with a fixed salary.

    Attributes:
        salary (float): Fixed salary paid to the employee.

    Example:
        >>> emp = FixedSalaryEmployee(1234567890, "John", "Doe", salary=10000)
        >>> emp.calculate_salary()
        10000
        >>> emp.calculate_tax(emp.calculate_salary())
        1950.0
        >>> FixedSalaryEmployee(1234567890, "John", "Doe", salary=-10000)
        Traceback (most recent call last):
            ...
        ValueError: salary value must be non-negative
    """

    salary = NonNegative()

    def __init__(self, ipn: int, first_name: str, last_name: str, salary: float):
        super().__init__(ipn, first_name, last_name)
        self.salary = salary

    def calculate_salary(self) -> float:
        return self.salary

    def calculate_tax(self, salary: float) -> float:
        return salary * (PDFO_RATE + MILITARY_RATE)


class SoleEntrepreneurEmployee(Employee):
    """
    Class to represent a sole entrepreneur employee. Due to lower taxes, they get a bonus.

    Attributes:
        hourly_rate (float): Hourly rate paid to the employee.
        worked_hours (int): Total hours worked by the employee.

    Example:
        >>> emp = SoleEntrepreneurEmployee(1234567890, "Jane", "Doe", hourly_rate=100, worked_hours=160)
        >>> emp.calculate_salary()
        17600.0
        >>> emp.calculate_tax(emp.calculate_salary())
        2640.0
        >>> SoleEntrepreneurEmployee(1234567890, "Jane", "Doe", hourly_rate=-100, worked_hours=160)
        Traceback (most recent call last):
            ...
        ValueError: hourly_rate value must be non-negative
        >>> SoleEntrepreneurEmployee(1234567890, "Jane", "Doe", hourly_rate=100, worked_hours=-160)
        Traceback (most recent call last):
            ...
        ValueError: worked_hours value must be non-negative
    """

    DEFAULT_WORK_HOURS = 20.8 * 8
    BONUS = 1.1
    hourly_rate = NonNegative()
    worked_hours = NonNegative()

    def __init__(
        self,
        ipn: int,
        first_name: str,
        last_name: str,
        hourly_rate: float,
        worked_hours: int = DEFAULT_WORK_HOURS,
    ):
        super().__init__(ipn, first_name, last_name)
        self.hourly_rate = hourly_rate
        self.worked_hours = worked_hours

    def calculate_salary(self) -> float:
        return self.hourly_rate * self.worked_hours * SoleEntrepreneurEmployee.BONUS

    def calculate_tax(self, salary: float) -> float:
        return salary * SINGLE_TAX_RATE + SINGLE_SOCIAL_CONTRIBUTION


class ContractorEmployee(Employee):
    """Class to represent a contractor employee. They get paid based on the number of code lines they write.

    Attributes:
        code_line_rate (float): Rate paid per code line.
        code_lines (int): Total number of code lines written by the employee.

    Example:
        >>> emp = ContractorEmployee(1234567890, "John", "Doe", code_line_rate=0.05, code_lines=10000)
        >>> emp.calculate_salary()
        500.0
        >>> emp.calculate_tax(emp.calculate_salary())
        1857.5
        >>> ContractorEmployee(1234567890, "John", "Doe", code_line_rate=-0.05, code_lines=10000)
        Traceback (most recent call last):
            ...
        ValueError: code_line_rate value must be non-negative
        >>> ContractorEmployee(1234567890, "John", "Doe", code_line_rate=0.05, code_lines=-10000)
        Traceback (most recent call last):
            ...
        ValueError: code_lines value must be non-negative
    """

    code_line_rate = NonNegative()
    code_lines = NonNegative()

    def __init__(
        self,
        ipn: int,
        first_name: str,
        last_name: str,
        code_line_rate: float,
        code_lines: int,
    ):
        super().__init__(ipn, first_name, last_name)
        self.code_line_rate = code_line_rate
        self.code_lines = code_lines

    def calculate_salary(self) -> float:
        return self.code_line_rate * self.code_lines

    def calculate_tax(self, salary: float) -> float:
        return salary * (PDFO_RATE + MILITARY_RATE) + SINGLE_SOCIAL_CONTRIBUTION


class FakeEmployeeFactory:
    """Factory class to generate random employees."""

    @staticmethod
    def random_employee() -> Employee:
        employee_type = random.choice(
            [
                HourlyPaidEmployee,
                FixedSalaryEmployee,
                SoleEntrepreneurEmployee,
                ContractorEmployee,
            ]
        )
        return cast(
            Employee,
            employee_type(
                ipn=random.randint(1000000000, 9999999999),
                first_name=_fake.first_name(),
                last_name=_fake.last_name(),
                **FakeEmployeeFactory.get_employee_kwargs(employee_type),
            ),
        )

    @staticmethod
    def get_employee_kwargs(employee_type: type[Employee]) -> dict[str, float]:
        if issubclass(employee_type, HourlyPaidEmployee):
            return {
                "hourly_rate": _fake.random_int(50, 200),
                "worked_hours": _fake.random_int(0, 20) * 8,
            }
        if issubclass(employee_type, FixedSalaryEmployee):
            return {"salary": _fake.random_int(5000, 10000)}
        if issubclass(employee_type, SoleEntrepreneurEmployee):
            return {
                "hourly_rate": _fake.random_int(50, 200),
                "worked_hours": _fake.random_int(0, 20) * 8,
            }
        if issubclass(employee_type, ContractorEmployee):
            return {
                "code_line_rate": _fake.random_int(2, 10) / 100,
                "code_lines": _fake.random_int(5000, 200000),
            }


if __name__ == "__main__":
    import doctest

    doctest.testmod()
