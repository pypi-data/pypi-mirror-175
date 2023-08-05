from .core import BaseModel
from peewee import *
from datetime import datetime
from .tags import Tags


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class AlarmTypes(BaseModel):

    name = CharField(unique=True)                       # high-high , high , bool , low , low-low

    @classmethod
    def create(cls, name:str)-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsType.create(name='High-High')
        {
            'message': (str)
            'data': (dict) {
                'name': 'HIGH-HIGH'
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """
        result = dict()
        data = dict()
        name = name.upper()

        if not cls.name_exist(name):

            query = cls(name=name)
            query.save()
            
            message = f"Alarm type {name} created successfully"
            data.update(query.serialize())

            result.update(
                {
                    'message': message, 
                    'data': data
                }
            )
            return result

        message = f"Alarm type {name} is already into database"
        result.update(
            {
                'message': message, 
                'data': data
            }
        )
        return result

    @classmethod
    def read_by_name(cls, name:str)->bool:
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name.upper())
        
        if query is not None:

            return query.serialize()
        
        return None

    @classmethod
    def name_exist(cls, name:str)->bool:
        r"""
        Verify is a name exist into database

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name.upper())
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """

        return {
            "id": self.id,
            "name": self.name
        }


class AlarmsDB(BaseModel):

    name = CharField(unique=True)
    tag = ForeignKeyField(Tags, backref='alarms', on_delete='CASCADE')
    description = CharField()
    alarm_type = ForeignKeyField(AlarmTypes, backref='alarms', on_delete='CASCADE')
    trigger = FloatField(null=True)


    @classmethod
    def create(cls, name:str, tag:str, description:str, alarm_type:str="NOT DEFINED")-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsDB.create(name='alarm_PT_01_H', tag='PT-01', description='Inlet Pressure Alarm', alarm_type='High-High', trigger=250.0)
        {
            'message': (str)
            'data': (dict) {
                'id': 1,
                'name': 'alarm_PT_01_H',
                'tag': 'PT-01',
                'description': 'Inlet Pressure Alarm',
                'alarm_type': 'high-high',
                'trigger': 250.0
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """

        if not cls.name_exist(name):
            
            _tag = Tags.read_by_name(name=tag)

            if _tag:

                _alarm_type = AlarmTypes.read_by_name(name=alarm_type)

                if _alarm_type is not None:

                    alarm_type_id = _alarm_type['id']

                    query = cls(name=name, tag=_tag.id, description=description, alarm_type=alarm_type_id)
                    query.save()
                    
                    return query
                    

    def set_trigger(self, alarm_type:str, trigger:float):
        r"""
        Documentation here
        """
        _alarm_type = AlarmTypes.read_by_name(name=alarm_type)

        if _alarm_type is not None:

            alarm_type_id = _alarm_type['id']

            _fields = {
                'alarm_type': alarm_type_id,
                'trigger': trigger
            }

            AlarmsDB.put(self.id, **_fields )

    @classmethod
    def read_by_name(cls, name:str):
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        return cls.get_or_none(name=name)
        
    @classmethod
    def name_exist(cls, name:str)->bool:
        r"""
        Verify is a name exist into database

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """
        trigger = self.trigger
        if self.alarm_type.name.upper()=='BOOL':

            trigger = bool(trigger)

        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag.name,
            "description": self.description,
            "alarm_type": self.alarm_type.name,
            "trigger": trigger
        }


class AlarmStates(BaseModel):
    r"""
    Based on ISA 18.2
    """

    name = CharField(unique=True)
    mnemonic = CharField(max_length=20)
    condition = CharField(max_length=20)
    status = CharField(max_length=20)

    @classmethod
    def create(cls, name:str, mnemonic:str, condition:str, status:str)-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsType.create(name='Unacknowledged', mnemonic='UNACKED', description='Alarm unacknowledged')
        {
            'message': (str)
            'data': (dict) {
                'id': 1,
                'name': 'unacknowledged',
                'mnemonic': 'UNACKED',
                'description': 'Alarm unacknowledged'
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """

        if not cls.name_exist(name):

            query = cls(name=name, mnemonic=mnemonic, condition=condition, status=status)
            query.save()
            
            return query

    @classmethod
    def read_by_name(cls, name:str)->bool:
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        return cls.get_or_none(name=name)

    @classmethod
    def name_exist(cls, name:str)->bool:
        r"""
        Verify is a name exist into database

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        query = cls.get_or_none(name=name)
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """

        return {
            "id": self.id,
            "name": self.name,
            "mnemonic": self.mnemonic,
            "condition": self.condition,
            "status": self.status
        }


class AlarmPriorities(BaseModel):
    r"""
    Based on ISA 18.2
    """

    value = IntegerField(unique=True)
    description = CharField()

    @classmethod
    def create(cls, value:int, description:str)-> dict:
        r"""
        You can use Model.create() to create a new model instance. This method accepts keyword arguments, where the keys correspond 
        to the names of the model's fields. A new instance is returned and a row is added to the table.

        ```python
        >>> AlarmsType.create(value=1, description='Low priority')
        {
            'message': (str)
            'data': (dict) {
                'id': 1,
                'value': 1,
                'description': 'Low priority'
            }
        }
        ```
        
        This will INSERT a new row into the database. The primary key will automatically be retrieved and stored on the model instance.

        **Parameters**

        * **name:** (str), Industrial protocol name

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (dict) row serialized}

        """

        if not cls.value_exist(value):

            query = cls(value=value, description=description)
            query.save()
            
            return query

    @classmethod
    def read_by_value(cls, value:int)->dict:
        r"""
        Get instance by its value

        **Parameters**

        * **value:** (str) Alarm priority value

        **Returns**

        * **bool:** If True, priority exist into database 
        """
        return cls.get_or_none(value=value)

    @classmethod
    def value_exist(cls, value:int)->bool:
        r"""
        Verify is a priority value exist into database

        **Parameters**

        * **value:** (str) Alarm priority value

        **Returns**

        * **bool:** If True, priority value exist into database 
        """
        query = cls.get_or_none(value=value)
        
        if query is not None:

            return True
        
        return False

    def serialize(self)-> dict:
        r"""
        Serialize database record to a jsonable object
        """

        return {
            "id": self.id,
            "value": self.value,
            "description": self.description
        }


class AlarmLogging(BaseModel):
    
    timestamp = DateTimeField(default=datetime.now)
    alarm = ForeignKeyField(AlarmsDB, backref='logging', on_delete='CASCADE')
    state = ForeignKeyField(AlarmStates, backref='logging', on_delete='CASCADE')
    priority = ForeignKeyField(AlarmPriorities, backref='logging', on_delete='CASCADE')
    value = FloatField()

    @classmethod
    def create(cls, name:str, state:str, priority:int, value:float):

        alarm = AlarmsDB.read_by_name(name=name)

        if alarm:
            
            state = AlarmStates.read_by_name(name=state)

            if state:

                priority = AlarmPriorities.read_by_value(value=priority)

                if priority:
        
                    query = cls(alarm=alarm.id, state=state.id, priority=priority.id, value=value)
                    query.save()

                    return query

    @classmethod
    def read_lasts(cls, lasts:int=1):
        r"""
        Documentation here
        """
        alarms = cls.select().where(cls.id > cls.select().count() - int(lasts)).order_by(cls.id.desc())

        result = [alarm.serialize() for alarm in alarms]

        return result

    def serialize(self):
        r"""
        Documentation here
        """
        result = {
            "timestamp": self.timestamp.strftime(DATETIME_FORMAT),
            "name": self.alarm.name,
            "state": self.state.name,
            "description": self.alarm.description,
            "priority": self.priority.value,
            "value": self.value
        }

        return result


class AlarmSummary(BaseModel):
    
    alarm = ForeignKeyField(AlarmsDB, backref='summary', on_delete='CASCADE')
    state = ForeignKeyField(AlarmStates, backref='summary', on_delete='CASCADE')
    alarm_time = DateTimeField(default=datetime.now)
    ack_time = DateTimeField(null=True)
    out_of_service_time = DateTimeField(null=True)
    return_to_service_time = DateTimeField(null=True)
    active = BooleanField(default=True)

    @classmethod
    def create(cls, name:str, state:str):
        _alarm = AlarmsDB.read_by_name(name=name)
        _state = AlarmStates.read_by_name(name=state)

        if _alarm:

            if _state:
            
                # Set Active old alarms False
                old_query = cls.select().where(cls.alarm==_alarm.id).get_or_none()
                if old_query:
                    old_query.active = False
                    old_query.save()


                # Create record
                query = cls(alarm=_alarm.id, state=_state.id)
                query.save()
                
                return query

    @classmethod
    def read_by_name(cls, name:str)->bool:
        r"""
        Get instance by its a name

        **Parameters**

        * **name:** (str) Alarm type name

        **Returns**

        * **bool:** If True, name exist into database 
        """
        alarm = AlarmsDB.read_by_name(name=name)
        return cls.get_or_none(alarm=alarm)

    @classmethod
    def read_all(cls):
        r"""
        Select all records

        You can use this method to retrieve all instances matching in the database. 

        This method is a shortcut that calls Model.select() with the given query.

        **Parameters**

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (list) row serialized}
        """

        # result = dict()
        data = list()
        
        try:
            data = [query.serialize() for query in cls.select().order_by(cls.id.desc())]

            return data

        except Exception as _err:

            return data

    @classmethod
    def read_lasts(cls, lasts:int=1):
        r"""
        Documentation here
        """
        alarms = cls.select().where(cls.id > cls.select().count() - int(lasts)).order_by(cls.id.desc())

        result = [alarm.serialize() for alarm in alarms]

        return result

    def serialize(self):
        r"""
        Documentation here
        """
        ack_time = None
        if self.ack_time:

            ack_time = self.ack_time.strftime(DATETIME_FORMAT)

        out_of_service_time = None
        if self.out_of_service_time:

            out_of_service_time = self.out_of_service_time.strftime(DATETIME_FORMAT)

        return_to_service_time = None
        if self.return_to_service_time:

            return_to_service_time = self.return_To_service_time.strftime(DATETIME_FORMAT)

        return {
            'id': self.id,
            'name': self.alarm.name,
            'state': self.state.name,
            'mnemonic': self.state.mnemonic,
            'status': self.state.status,
            'condition': self.state.condition,
            'description': self.alarm.description,
            'alarm_time': self.alarm_time.strftime(DATETIME_FORMAT),
            'ack_time': ack_time,
            'out_of_service_time': out_of_service_time,
            'return_to_service_time': return_to_service_time,
            'active': self.active
        }