import sqlite3
from typing import Union
from debugging_benchmark.refactory import RefactoryBenchmarkProgram
from debugging_benchmark.student_assignments import StudentAssignmentBenchmarkProgram

from debugging_benchmark.core import BenchmarkProgram

#Singleton
class DatabaseHelper:
    _instance = None

    #vllt mache ich das nicht so sondern immer neu auf in den funktionen, da man die connection wieder schließen soll
    _database = None
    _cursor = None

    def __init__(self):
        raise RuntimeError("Use DatabaseHelper.instance() instead")
    
    def _init_db(self):
        self._database = sqlite3.connect("inputs.db")
        self._cursor = self._database.cursor()

        #hier tabs hinzugefügt vllt klappts nicht
        self._cursor.execute(""" CREATE TABLE IF NOT EXISTS programs (
                             id integer PRIMARY KEY,
                             name text
                            ); """)
        
        #jeder input einzeln vllt gibts da ne bessere möglichkeit
        self._cursor.execute(""" CREATE TABLE IF NOT EXISTS failing_input(
                             id integer PRIMARY KEY,
                             program_id integer,
                             failing_input1 text,
                             failing_input2 text,
                             failing_input3 text,
                             failing_input4 text,
                             failing_input5 text
                            ); """)
        
        self._cursor.execute(""" CREATE TABLE IF NOT EXISTS passing_input(
                             id integer PRIMARY KEY,
                             program_id integer,
                             passing_input1 text,
                             passing_input2 text,
                             passing_input3 text,
                             passing_input4 text,
                             passing_input5 text
                            ); """)
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            #initialization here f.e. database init? mache ich ja schon in get_db
        return cls._instance    

    def get_database(self):
        if self._database is None:
            self._init_db()

        return self._database
    
    #wie kann man das noch machen, wenn es in zukunft mehr Types of BenchmarkProgramme gibt?
    #erben ja alle von BenchmarkProgram kann man da vllt irgendwas machen?
    def insert_program(self, program: BenchmarkProgram) -> int:
        try:
            db = self.get_database()
            cursor = db.cursor()
            name = program.get_name()
            program_id = len(cursor.execute("select * from programs").fetchall()) + 1
            
            cursor.execute(""" INSERT INTO programs
                           (id, name)
                           VALUES (?, ?); """, (program_id, name))
            
            
        
        except sqlite3.Error as error:
            print("Failed to insert program into db", error)

        return program_id



