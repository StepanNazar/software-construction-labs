from employee import FakeEmployeeFactory


def main():
    employees = (FakeEmployeeFactory.random_employee() for _ in range(15))
    employees_data = []
    for employee in employees:
        salary = employee.calculate_salary()
        tax = employee.calculate_tax(salary)
        employees_data.append((employee, salary, tax))
    employees_data.sort(key=lambda x: (-x[1], x[0].last_name))
    for employee, salary, tax in employees_data:
        print(
            f"{employee.ipn} {employee.last_name} - salary: {salary:.2f}, tax: {tax:.2f}"
        )


if __name__ == "__main__":
    main()
