import sqlite3
from typing import Union, List
from debugging_benchmark.refactory import RefactoryBenchmarkProgram
from debugging_benchmark.student_assignments import StudentAssignmentBenchmarkProgram

from debugging_benchmark.benchmark import BenchmarkProgram

#Singleton
class DatabaseHelper:
    _instance = None

    def __init__(self):
        raise RuntimeError("Use DatabaseHelper.instance() instead")
    
    def _init_db(self):
        conn = sqlite3.connect("inputs.db")
        cursor = conn.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS programs (
                             id integer PRIMARY KEY,
                             name text
                            ); """)
        
        #jeder input einzeln vllt gibts da ne bessere möglichkeit
        cursor.execute(""" CREATE TABLE IF NOT EXISTS failing_inputs(
                             id integer PRIMARY KEY,
                             program_id integer,
                             failing_input text
                            ); """)
        
        cursor.execute(""" CREATE TABLE IF NOT EXISTS passing_inputs(
                             id integer PRIMARY KEY,
                             program_id integer,
                             passing_input text
                            ); """)
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def get_conn(self):
        return sqlite3.connect("inputs.db")
    
    def get_program_id(self, program: BenchmarkProgram) -> int:
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                name = program.get_name()
                data = cursor.execute("SELECT * FROM programs WHERE name = ?", (name,)).fetchone()
                print(data)
                if data is None:
                    return -1
                else:
                    return data[0]
        
        except sqlite3.Error as error:
            print("Error in get_program_id:", error)

        finally:
            cursor.close()
            conn.close()
    
    def get_passing_inputs_from_program(self, program: BenchmarkProgram) -> List[str]:
        try:
            conn = self.get_conn()
            inputs = []
            with conn:
                cursor = conn.cursor()
                program_id = self.get_program_id(program)
                data = cursor.execute("SELECT * from passing_inputs WHERE program_id = ?", (program_id,)).fetchall()
                for entry in data:
                    inputs.append(entry[2])

                return inputs

        except sqlite3.Error as error:
            print("Error in get_passing_inputs:", error)

        finally:
            cursor.close()
            conn.close()

    def get_failing_inputs_from_program(self, program: BenchmarkProgram) -> List[str]:
        try:
            conn = self.get_conn()
            inputs = []
            with conn:
                cursor = conn.cursor()
                program_id = self.get_program_id(program)
                data = cursor.execute("SELECT * from failing_inputs WHERE program_id = ?", (program_id,)).fetchall()
                for entry in data:
                    inputs.append(entry[2])

                return inputs

        except sqlite3.Error as error:
            print("Error in get_failing_inputs:", error)

        finally:
            cursor.close()
            conn.close()
    
    def get_inputs_from_program(self, program: BenchmarkProgram) -> List[str]:
        failing_inputs = self.get_failing_inputs_from_program(program)
        passing_inputs = self.get_passing_inputs_from_program(program)

        return [*failing_inputs, *passing_inputs]
    
    def insert_program(self, program: BenchmarkProgram) -> int:
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                name = program.get_name()
                data = cursor.execute("SELECT * FROM programs WHERE name = ?", (name,)).fetchone()

                if data is None:
                    cursor.execute(""" INSERT INTO programs
                                    (name)
                                    VALUES (?); """, (name,))
                    program_id = cursor.lastrowid
                    return program_id
                else:
                    program_id = data[0]
                    return program_id
        
        except sqlite3.Error as error:
            print("Failed to insert program into db:", error)

        finally:
            cursor.close()
            conn.close()
    
    def insert_passing_input(self, program_id: int, passing_input: str):
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                data = cursor.execute("SELECT * FROM passing_inputs WHERE passing_input = ? AND program_id = ?", (passing_input, program_id)).fetchone()

                if data is None:
                    cursor.execute(""" INSERT INTO passing_inputs
                                    (program_id, passing_input)
                                    VALUES (?, ?); """, (program_id, passing_input))
        
                else:
                    print("Input bereits in DB vorhanden")
        except sqlite3.Error as error:
            print("Failed to insert passing input into db:", error)
        
        finally:
            cursor.close()
            conn.close()

    def insert_failing_input(self, program_id: int, failing_input: str):
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                data = cursor.execute("SELECT * FROM failing_inputs WHERE failing_input = ? AND program_id = ?", (failing_input, program_id)).fetchone()

                if data is None:
                    cursor.execute(""" INSERT INTO failing_inputs
                                    (program_id, failing_input)
                                    VALUES (?, ?); """, (program_id, failing_input))
                else:
                    print("Input bereits in DB vorhanden")

        except sqlite3.Error as error:
            print("Failed to insert failing input into db:", error)
        
        finally:
            cursor.close()
            conn.close()

    def delete_program(self, program: BenchmarkProgram):
        '''
        Deletes Program and all corresponding Inputs from db
        '''
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                name = program.get_name()
                data = cursor.execute("SELECT * FROM programs WHERE name = ?", (name,)).fetchone()
                if data is None:
                    raise NotImplementedError
                else:
                    program_id = data[0]
                    cursor.execute("DELETE from programs WHERE name = ?", (name,))
                    cursor.execute("DELETE from passing_inputs WHERE program_id = ?", (program_id,))
                    cursor.execute("DELETE from failing_inputs WHERE program_id = ?", (program_id,))

        except sqlite3.Error as error:
                print("Failed to delete program from db:", error)


