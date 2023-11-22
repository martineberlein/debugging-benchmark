from typing import List, Union, Callable
from debugging_framework.oracle import OracleResult

import sqlite3

from debugging_framework.benchmark import BenchmarkProgram

#Singleton
class DatabaseHelper:
    '''
    Creation:   db = DatabaseHelper().instance() to create an DatabaseHelper.
    Insertion:  db.insert_program() returns the prog_id. Gets used for assigning the Inputs to the correct Program.
                db.insert_input() and db.insert_many_inputs() are the preferred ways of adding new Inputs to the db
    Query Data: db.get_failing_inputs_from_program()
                db.get_passing_inputs_from_program()
                db.get_inputs_from_program()
    '''
    #TODO: Everywhere program is accepted, accept prog_id aswell
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
        '''
        Returns the program_id. 
        The ID is used for correctly assigning programs to their corresponding inputs in the db
        '''
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
        '''
        Returns a List of the passing inputs of the program.
        '''
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
        '''
        Returns a List of the failing inputs of the program.
        '''
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
        '''
        Returns a List of all inputs of the program.
        '''
        failing_inputs = self.get_failing_inputs_from_program(program)
        passing_inputs = self.get_passing_inputs_from_program(program)

        return [*failing_inputs, *passing_inputs]
    
    def insert_program(self, program: BenchmarkProgram) -> int:
        '''
        Inserts a Program to the db and returns its prog_id.
        The prog_id gets used to identify the corresponding inputs to the program.
        It is IMPORTANT that the programs have distinct NAMES.
        Because if a program with the same name is already in the db the new program does NOT get added
        and instead the prog_id of the former program is returned!
        '''
        #maybe add more comparing factors for programs -> oracle, grammar
        #but for now name should be enough if BenchmarkProgram and BenchmarkRepository are used like intended
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
        '''
        Inserts a passing input in the db.
        Only used internally.
        Please use insert_inputs() or insert_many_inputs()
        '''
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
        '''
        Inserts a failing input in the db.
        Only used internally.
        Please use insert_inputs() or insert_many_inputs()
        '''
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

    def insert_input(self, program_id: int, inp: str, oracle: Union[Callable, OracleResult]):
        '''
        Preferred way of inserting a Input into the db
        '''
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                if isinstance(oracle, Callable):
                    oracle_result = oracle(inp)
                elif isinstance(oracle, OracleResult):
                    oracle_result = oracle
                else:
                    raise TypeError("hallo")
                
                match oracle_result:
                    case OracleResult.PASSING:
                        self.insert_passing_input(program_id, inp)

                    case OracleResult.FAILING:
                        self.insert_failing_input(program_id, inp)

        except sqlite3.Error as error:
            print("Failed to insert failing input into db:", error)
        
        finally:
            cursor.close()
            conn.close()

    def get_count_inputs(self, program_id: int) -> dict:
        '''
        Only used internally.
        Returns the counts for passing and failing inputs as a dict.
        Keys: "pass" and "fail"
        '''
        try:
            conn = self.get_conn()
            with conn:
                cursor = conn.cursor()
                data = cursor.execute("SELECT * FROM failing_inputs WHERE program_id = ?", (program_id,)).fetchall()
                count_fail = len(data)

                data = cursor.execute("SELECT * FROM passing_inputs WHERE program_id = ?", (program_id,)).fetchall()

                count_pass = len(data)

                return {"pass": count_pass, "fail": count_fail}

        except sqlite3.Error as error:
            print("Failed to insert failing input into db:", error)
        
        finally:
            cursor.close()
            conn.close()
    
    def insert_many_inputs(self, program_id: int, inputs: List[str], oracle: Union[Callable, OracleResult], max_pass:int = 5, max_fail:int = 5):
        '''
        Preferred way of inserting many inputs into the db.
        Checks if the input is passing or failing and stops if max_pass and max_fail are reached.
        '''
        for inp in inputs:
            counts = self.get_count_inputs(program_id)
            
            if isinstance(oracle, Callable):
                oracle_result = oracle(inp)
            elif isinstance(oracle, OracleResult):
                oracle_result = oracle
            
            if counts["pass"] < max_pass and oracle_result == OracleResult.PASSING:
                self.insert_passing_input(program_id, inp)
            elif counts["fail"] < max_fail and oracle_result == OracleResult.FAILING:
                self.insert_failing_input(program_id, inp)

            if counts["pass"] >= max_pass and counts["fail"] >= max_fail:
                break

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
