import psycopg2

class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database='postgres',
            user='postgres',
            host='localhost',
            password='252208'
        )
        self.table_names = []

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        result = None
        with self.database as db:
            with db.cursor() as cursor:
                # Agar args bo'sh bo'lsa, parametrsiz execute ishlatiladi
                if args:
                    cursor.execute(sql, args)
                else:
                    cursor.execute(sql)
                
                if commit:
                    db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
        return result

    def create_departments(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS departments(
                department_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                department_name VARCHAR(50) NOT NULL
            );
        '''
        self.manager(sql, commit=True)
    
    def create_employees(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS employees(
                employee_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50), 
                position VARCHAR(20) NOT NULL,
                salary INTEGER NOT NULL,
                hire_date DATE,
                department_id INTEGER REFERENCES departments(department_id)
            );
        '''
        self.manager(sql, commit=True)

    def create_projects(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS projects(
                project_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                project_name VARCHAR(50) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE                 
            );
        '''
        self.manager(sql, commit=True)

    def insert_departments(self):
        departments = [
            ('Administration',),
            ('IT',),
            ('Design',),
        ]

        sql = '''
                INSERT INTO departments( department_name) VALUES
                (%s);
            '''
               
        for i in departments:
            self.manager(sql, *i, commit=True)
            
    def insert_projects(self):
        projects = [
            ('New Website', '2023-01-10', '2023-06-30', 50000),
            ('Mobile App', '2022-08-15', '2023-03-20', 30000),
            ('CRM System', '2024-02-01', None, 60000)  
        ]

        sql = '''
            INSERT INTO projects (project_name, start_date, end_date, budget) VALUES (%s, %s, %s, %s);
        '''

        for project in projects:
            self.manager(sql, *project, commit=True)


    def insert_employees(self):
        try:
            employees = [
                ('Ali', 'Karimov', 'Manager', 3000, '2020-03-15', 1),
                ('Nodira', 'Toirova', 'Developer', 2500, '2021-05-10', 2),
                ('Shoxruh', 'Abdullayev', 'Designer', 2200, '2022-01-22', 3),
                ('Zarina', 'Abdullayeva', 'HR Specialist', 1800, '2019-11-11', 1),
                ('Jasur', 'Aliyev', 'Developer', 2400, '2023-02-01', 2),
                ('Jamoliddin', 'Xolmatov', 'Backend developer', 2400, None, 2)
            ]
            
            sql = '''
                    INSERT INTO employees( first_name, last_name, position, salary, hire_date, department_id) VALUES
                    (%s, %s, %s, %s, %s, %s);
                '''
            
            for i in employees:
                self.manager(sql, *i, commit=True)
        except Exception as e:
            print(e)
            print("xato ketdi!!!")

    def select_full_name(self):
        sql = '''
            SELECT first_name ||' '|| last_name AS full_name FROM employees; 
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)
    
    def order_by(self):
        sql = '''
            SELECT first_name, salary FROM employees ORDER BY salary ASC; 
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)

    def where(self):
        sql = '''
            SELECT first_name, salary FROM employees WHERE salary >= 2500; 
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)

    def order_by_3(self):
        sql = '''
            SELECT first_name, salary FROM employees ORDER BY salary DESC LIMIT 3; 
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)


    def in_1(self):
        sql = '''
            SELECT first_name, salary FROM employees WHERE salary IN (2400, 3000);
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)


    def between(self):
        sql = '''
            SELECT first_name, salary FROM employees WHERE salary BETWEEN 2000 AND 3000;

        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)

    def like(self):
        sql = '''
            SELECT first_name, salary FROM employees WHERE first_name LIKE '%a%';
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)


    def is_null(self):
        sql = '''
            SELECT first_name, hire_date FROM employees WHERE hire_date IS NULL;
        '''
        select = self.manager(sql, fetchall=True)
        for i in select:
            print(i)

    def group_by(self):
        sql = '''
            SELECT department_id, AVG(salary) AS average_salary FROM employees GROUP BY department_id;
        '''
        select = self.manager(sql, fetchall=True)
        if not select:
            print("No data found for departments.")
        else:
            for department_id, average_salary in select:
                print(f"Department ID: {department_id}, Average Salary: {average_salary:.2f}")

        
    
    

































