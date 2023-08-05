import logging, os
from inspect import ismethod

from .utils import (
    log_detailed,
    logging_error_handler,
    notify_state,
    system_log_transition,
    get_headers,
    parse_config
    )

from statemachine import StateMachine
from statemachine import State as _State

from .tags import CVTEngine, TagBinding, GroupBinding
from .logger import DataLoggerEngine
from .models import FloatType, IntegerType, BooleanType, StringType
import requests

APP_EVENT_LOG = bool(int(os.environ.get('APP_EVENT_LOG') or "0"))
EVENT_LOGGER_SERVICE_HOST = os.environ.get('EVENT_LOGGER_SERVICE_HOST') or "127.0.0.1"
EVENT_LOGGER_SERVICE_PORT = os.environ.get('EVENT_LOGGER_SERVICE_PORT') or "5004"
AUTH_SERVICE_HOST = os.environ.get('AUTH_SERVICE_HOST') or "127.0.0.1"
AUTH_SERVICE_PORT = os.environ.get('AUTH_SERVICE_PORT') or "5000"

FLOAT = "float"
INTEGER = "int"
BOOL = "bool"
STRING = "str"

READ = "read"
WRITE = "write"

class State(_State):

    """
    Class used to define custom states in a state machine.

    This class is used to define custom states in a state machine.

    **Parameters:**

    * **name** (str): state machine name.
    * **interval** (float): machine loop time for this state in seconds.

    Usage:

    ```python
    state1  = State('State1', initial=True)
    state2  = State('State2', interval=0.5)
    """

    def __init__(self, *args, **kwargs):

        super(State, self).__init__(*args, **kwargs)
        self._trigger = None

        if "interval" in kwargs:
            self._interval = kwargs["interval"]
        else:
            self._interval = float('inf')

        self._transition = None

    def to(self, another, trigger=None):

        """
        This method allows to create transitions between states,
        you can also define trigger conditions in order to execute
        transitions
        """

        self._transition = super(State, self).to(another)
        self._trigger = trigger

        return self._transition

    @property
    def interval(self):

        return self._interval

    def attach_all(self):

        if not self._trigger:
            return


class PyHadesStateMachine(StateMachine):

    """
    Class used to define custom state machines.

    This class is used to define custom machines,
    by defining parameters, states, transitions and
    by defining methods state behaviour can de defined.

    **Parameters:**

    * **name** (str): state machine name.

    **Attributes**

    * **tag_engine** (CVTEngine Object)
    * **logger_engine** (DataLoggerEngine Object)

    """
    tag_engine = CVTEngine()
    logger_engine = DataLoggerEngine()


    def __init__(self, name:str, **kwargs):

        super(PyHadesStateMachine, self).__init__()
        self.name = name
        self._tag_bindings = list()
        self._group_bindings = list()
        self._machine_interval = list()

        attrs = self.get_attributes()

        for key, value in attrs.items():

            try:
                if isinstance(value, TagBinding):
                    self._tag_bindings.append((key, value))
                    _value = self.tag_engine.read_tag(value.tag)

                    setattr(self, key, _value)

                if isinstance(value, GroupBinding):
                    self._group_bindings.append((key, value))
                    _value = value.values

                    setattr(self, key, _value)

                if key in kwargs:
                    default = kwargs[key]
                else:
                    default = value.default
                    _type = value._type

                if default:
                    setattr(self, key, default)
                else:
                    if _type == FLOAT:
                        setattr(self, key, 0.0)
                    elif _type == INTEGER:
                        setattr(self, key, 0)
                    elif _type == BOOL:
                        setattr(self, key, False)
                    elif _type == STRING:
                        setattr(self, key, "")
            except Exception as e:
                continue

        self.attrs = attrs

        DAQ_SERVICE_HOST = os.environ.get('DAQ_SERVICE_HOST') or "127.0.0.1"
        DAQ_SERVICE_PORT = os.environ.get('DAQ_SERVICE_PORT') or "5001"
        self.DAQ_SERVICE_URL = f"http://{DAQ_SERVICE_HOST}:{DAQ_SERVICE_PORT}"

    def info(self)->str:
        r"""
        Gets general information of the state machine

        **Returns**

        * **(str)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> info = machine.info()
        ```
        """
        return f'''\nState Machine: {self.name} - Interval: {self.get_interval()} seconds - States: {self.get_states()} - Transitions: {self.get_transitions_name()}'''

    def get_states(self)->list:
        r"""
        Gets a list of state machine's names

        **Returns**

        * **(list)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> states = machine.get_states()
        ```
        """
        return [state.identifier for state in self.states]

    def get_state_interval(self)->float:
        r"""
        Gets current state interval

        **Returns**

        * **(float)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> current_interval = machine.get_state_interval()
        ```

        """
        return self.current_state.interval

    def get_interval(self)->float:
        r"""
        Gets overall state machine interval

        **Returns**

        * **(float)**

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> interval = machine.get_interval()
        ```
        """
        return self._machine_interval

    def set_interval(self, interval):
        r"""
        Sets overall machine interval

        **Parameters**

        * **interval:** (float) overal machine interval in seconds

        Usage

        ```python
        >>> machine = app.get_machine(name)
        >>> machine.set_interval(0.5)
        ```
        """
        self._machine_interval = interval

    @classmethod
    def get_attributes(cls):
        r"""
        Gets class attributes defined by [model types]()

        **Returns**

        * **(dict)**
        """
        result = dict()

        props = cls.__dict__

        forbidden_attributes = (
            "states",
            "transitions",
            "states_map",
            "_loop",
            "get_attributes",
            "_tag_bindings",
            "_get_active_transitions",
            "_activate_triggers",
            "get_state_interval",
            "get_interval",
            "set_interval",
            "_machine_interval"
        )

        for key, value in props.items():


            if key in forbidden_attributes:
                continue
            if hasattr(value, '__call__'):
                continue
            if isinstance(value, PyHadesStateMachine):
                continue
            if isinstance(value, State):
                continue
            if not ismethod(value):

                if not "__" in key:
                    result[key] = value

        return result

    def _get_active_transitions(self):
        r"""
        Gets allowed transitions based on the current state

        **Returns**

        * **(list)**
        """
        result = list()

        current_state = self.current_state

        transitions = self.transitions

        for transition in transitions:

            if transition.source == current_state:

                result.append(transition)

        return result

    def get_transitions_name(self):
        r"""
        Get all transitions name define in the state machine

        **Returns**

        * **(list)** of string
        """
        transitions = self.transitions

        _transitions = list()

        for transition in transitions:
            _transitions.append(transition.identifier)

        return _transitions

    def _activate_triggers(self):
        r"""
        Allows to execute the on_ method in transitions when it's necesary

        """
        transitions = self._get_active_transitions()

        for transition in transitions:
            method_name = transition.identifier
            method = getattr(self, method_name)

            try:
                source = transition.source
                if not source._trigger:
                    continue
                if source._trigger.evaluate():
                    method()
            except Exception as e:
                error = str(e)
                logging.error("Machine - {}:{}".format(self.name, error))

    def _update_tags(self, direction=READ):

        for attr, _binding in self._tag_bindings:

            try:
                if direction == READ and _binding.direction == READ:

                    tag = _binding.tag
                    value = self.tag_engine.read_tag(tag)
                    value = setattr(self, attr, value)

                elif direction == WRITE and _binding.direction == WRITE:
                    tag = _binding.tag
                    value = getattr(self, attr)
                    self.tag_engine.write_tag(tag, value)

            except Exception as e:
                message = "Machine - {}: Error on machine tag-bindings".format(self.name)
                log_detailed(e, message)

    def _update_groups(self, direction=READ):

        for attr, _binding in self._group_bindings:

            try:
                if direction == READ and _binding.direction == READ:

                    _binding.update()

                    setattr(self, attr, _binding.values)

                elif direction == WRITE and _binding.direction == WRITE:

                    values = getattr(self, attr)

                    _binding.values = values

                    _binding.update()

            except Exception as e:
                message = "Machine - {}: Error on machine group-bindings".format(self.name)
                log_detailed(e, message)

    def _loop(self):
        r"""
        Documentation in construction
        """
        try:
            state_name = self.current_state.identifier.lower()
            method_name = "while_" + state_name

            if method_name in dir(self):
                update_tags = getattr(self, '_update_tags')
                update_groups = getattr(self, '_update_groups')
                method = getattr(self, method_name)

                # update tag read bindings
                update_tags()
                update_groups()

                # loop machine
                try:
                    method()
                except Exception as e:
                    message = "Machine - {}: Error on machine loop".format(self.name)
                    log_detailed(e, message)

                #update tag write bindings
                update_tags("write")
                update_groups("write")

            self.log_to_db()
            self._activate_triggers()

        except Exception as e:
            error = str(e)
            logging.error("Machine - {}:{}".format(self.name, error))

    def loop(self):
        r"""
        Starts state machine thread and it allows to execute the correct while_ method
        in the state machine loop execution
        """
        self._loop()

    def serialize(self)->dict:
        r"""
        Gets state machine attributes serialized
        """
        def is_serializable(value):

            if isinstance(value, float):
                return True

            if isinstance(value, int):
                return True

            if isinstance(value, bool):
                return True

            if isinstance(value, str):
                return True

            return False

        result = {
            'name': {
                'value': self.name,
                'unit': None,
            },
            'state': {
                'value': self.current_state.identifier,
                'unit': None
            }
        }

        states = self.get_states()
        checkers = ["is_" + state for state in states]
        methods = ["while_" + state for state in states]

        attrs = self.get_attributes()

        for key in attrs.keys():

            obj = attrs[key]

            if key in checkers:
                continue
            if key in methods:
                continue


            value = getattr(self, key)
            if isinstance(obj, (FloatType, IntegerType, BooleanType, StringType)):

                value = obj.value
                unit = obj.unit

                result[key] = {
                    'value': value,
                    'unit': unit
                }

        return result

    def get_state(self):
        r"""
        Gets current state of the state machine

        **Returns**

        * **state:** (str) current state of the state machine
        """

        return self.current_state.identifier

    def init_socketio_for_variables(self):
        r"""
        Documentation here
        """
        states = self.get_states()
        checkers = ["is_" + state for state in states]
        methods = ["while_" + state for state in states]

        attrs = self.get_attributes()

        for key in attrs.keys():

            obj = attrs[key]

            if key in checkers:
                continue
            if key in methods:
                continue

            if isinstance(obj, (FloatType, IntegerType, BooleanType, StringType)):

                obj.init_socketio(machine=self)

    @logging_error_handler
    def get_tag_name_to_log(self):
        r"""
        Documentation here
        """
        tag_names = list()
        states = self.get_states()
        checkers = ["is_" + state for state in states]
        methods = ["while_" + state for state in states]

        attrs = self.get_attributes()
        
        for key in attrs.keys():

            obj = attrs[key]
            
            if key in checkers:
                continue
            if key in methods:
                continue
            
            if isinstance(obj, (FloatType, IntegerType, BooleanType, StringType)):

                if obj.is_logged():

                    tag_names.append(key)

        return tag_names

    @logging_error_handler
    def log_to_db(self):
        r"""
        Documentation here
        """
        tag_names = self.get_tag_name_to_log()
        response = requests.post(f"{self.DAQ_SERVICE_URL}/api/tags/read_tag_id_by_name", json=tag_names)
        tags = list()

        if response.status_code==200:

            tag_names_ids = response.json()

            for tag_name, tag_id in tag_names_ids.items():

                tag_attr = getattr(self, tag_name)


                tags.append({
                    'tag': tag_id,
                    'value': tag_attr.value
                })

            response = requests.post(f"{self.DAQ_SERVICE_URL}/api/tags/write_tags", json=tags)

class AutomationStateMachine(PyHadesStateMachine):
    r"""
    Documentation here
    """
    # States definition
    starting = State('start', initial=True)
    waiting = State('wait')
    running = State('run')
    restarting = State('restart')
    resetting = State('reset')
    sleeping = State('sleep')
    testing = State('test')
    con_restart = State('confirm_restart')
    con_reset = State('confirm_reset')

    # Main transitions
    start_to_wait = starting.to(waiting)
    wait_to_run = waiting.to(running)
    reset_to_confirm_reset = resetting.to(con_reset)
    restart_to_confirm_restart = restarting.to(con_restart)
    confirm_restart_to_wait = con_restart.to(waiting)
    confirm_reset_to_start = con_reset.to(starting)

    # Transitions to Testing
    run_to_test = running.to(testing)
    wait_to_test = waiting.to(testing)

    # Transitions to Sleeping
    run_to_sleep = running.to(sleeping)
    wait_to_sleep = waiting.to(sleeping)

    # Transitions to Restart
    run_to_restart = running.to(restarting)
    wait_to_restart = waiting.to(restarting)
    test_to_restart = testing.to(restarting)
    sleep_to_restart = sleeping.to(restarting)

    # Transitions to Reset
    run_to_reset = running.to(resetting)
    wait_to_reset = waiting.to(resetting)
    test_to_reset = testing.to(resetting)
    sleep_to_reset = sleeping.to(resetting)

    criticity = IntegerType(default=1)
    priority = IntegerType(default=1)
    classification = StringType(default='')
    description = StringType(default='')
    states_for_users = ['restart', 'reset', 'test', 'sleep', 'confirm_restart', 'confirm_reset']

    def __init__(self, app, name:str):
        """
        """
        super(AutomationStateMachine, self).__init__(name)
        # DAQ_SERVICE_HOST = os.environ.get('DAQ_SERVICE_HOST') or "127.0.0.1"
        # DAQ_SERVICE_PORT = os.environ.get('DAQ_SERVICE_PORT') or "5001"
        # self.DAQ_SERVICE_URL = f"http://{DAQ_SERVICE_HOST}:{DAQ_SERVICE_PORT}"
        self.system_tags = dict()
        self.default_tags = list()
        self.default_alarms = list()
        self.app = app
        self.ready_to_run = False
        self.default_alarms = list()
        self.default_tags = list()
        self.buffer = dict()
        self.event_name = "machine_event"
        self.time_window = 10


    def while_starting(self):
        """

        """
        self.app_mode = self.app.get_mode()
        self.headers = get_headers(auth_service_host=AUTH_SERVICE_HOST, auth_service_port=AUTH_SERVICE_PORT)
        self.sio = self.app.get_socketio()
        self.config_file_location = self.app.config_file_location
        self.init_configuration()
        self.init_socketio_for_variables()
        self.start_to_wait()

    def while_waiting(self):
        r"""
        Documentation here
        """
        data = self.read_data()
        self.fill_buffer(data)
        if self.ready_to_run:
            self.wait_to_run()

    def while_running(self):
        r"""
        Documentation here
        """
        data = self.read_data()
        self.fill_buffer(data)
        self.criticity = 1

    def while_sleeping(self):
        """
        ## **sleeping** state

        Only set priority and classification to notify in the front end
        """
        self.criticity = 4

    def while_testing(self):
        """
        ## **testing** state

        Only set priority and classification to notify in the front end
        """
        self.criticity = 3

    def while_resetting(self):
        r"""
        ## **resetting** state

        Only set priority and classification to notify in the front end
        """

        self.reset_to_confirm_reset()

    def while_con_reset(self):
        r"""
        ## **confirm_reset** state

        Only set priority and classification to notify in the front end
        """
        self.criticity = 3

    def while_restarting(self):
        r"""
        ## **resetting** state

        Only set priority and classification to notify in the front end
        """

        self.restart_to_confirm_restart()

    def while_con_restart(self):
        r"""
        ## **confirm_restart** state

        Only set priority and classification to notify in the front end
        """
        self.criticity = 3

    # Transitions definitions
    @notify_state
    @system_log_transition(
        log=APP_EVENT_LOG,
        event_logger_service_host=EVENT_LOGGER_SERVICE_HOST,
        event_logger_service_port=EVENT_LOGGER_SERVICE_PORT,
        auth_service_host=AUTH_SERVICE_HOST,
        auth_service_port=AUTH_SERVICE_PORT,
        )
    def on_start_to_wait(self):
        r"""
        ## **Transition**

        * **from: *start* ** state
        * **to: *waiting* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to waiting state, no problems.
        * **classification:** system (Transition triggered automatically).

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 1

    @notify_state
    @system_log_transition(
        log=APP_EVENT_LOG,
        event_logger_service_host=EVENT_LOGGER_SERVICE_HOST,
        event_logger_service_port=EVENT_LOGGER_SERVICE_PORT,
        auth_service_host=AUTH_SERVICE_HOST,
        auth_service_port=AUTH_SERVICE_PORT,
        )
    def on_wait_to_run(self):
        """
        ## **Transition**

        * **from: *waiting* ** state
        * **to: *running* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to running state, no problems.
        * **classification:** system (Transition triggered automatically).

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 1

    @notify_state
    def on_confirm_restart_to_wait(self):
        """
        ## **Transition**

        * **from: *confirm_restart* ** state
        * **to: *waiting* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to waiting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        data_to_log = {
            'engine': self.serialize(),
            'tags': [
                {
                    'tag_name': self.name,
                    'value': 0.0
                }
            ]
        }
        self.sio.emit('tags_logging', data_to_log)
        self.criticity = 1

    @notify_state
    def on_confirm_reset_to_start(self):
        """
        ## **Transition**

        * **from: *confirm_reset ** state
        * **to: *starting* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to starting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        data_to_log = {
            'engine': self.serialize(),
            'tags': [
                {
                    'tag_name': self.name,
                    'value': 0.0
                }
            ]
        }
        self.sio.emit('tags_logging', data_to_log)
        self.criticity = 1

    @notify_state
    def on_restart_to_confirm_restart(self):
        """
        ## **Transition**

        * **from: *confirm_reset ** state
        * **to: *starting* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to starting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 3

    @notify_state
    def on_reset_to_confirm_reset(self):
        """
        ## **Transition**

        * **from: *confirm_reset ** state
        * **to: *starting* ** state

        ### **Settings**

        * **priority:** 1 (low priority) machine to starting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 3

    @notify_state
    def on_wait_to_restart(self):
        """
        ## **Transition**

        * **from: *waiting* ** state
        * **to: *restarting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to restarting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_run_to_restart(self):
        """
        ## **Transition**

        * **from: *running* ** state
        * **to: *restarting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to restarting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_test_to_restart(self):
        """
        ## **Transition**

        * **from: *testing* ** state
        * **to: *restarting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to restarting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_sleep_to_restart(self):
        """
        ## **Transition**

        * **from: *sleeping* ** state
        * **to: *restarting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to restarting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4


    @notify_state
    def on_wait_to_reset(self):
        """
        ## **Transition**

        * **from: *running* ** state
        * **to: *resetting* ** state

        ### **Settings**

        * **priority:** 5 (high priority) machine to resetting state, danger
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 5

    @notify_state
    def on_run_to_reset(self):
        """
        ## **Transition**

        * **from: *running* ** state
        * **to: *resetting* ** state

        ### **Settings**

        * **priority:** 5 (high priority) machine to resetting state, danger
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 5

    @notify_state
    def on_test_to_reset(self):
        """
        ## **Transition**

        * **from: *testing* ** state
        * **to: *resetting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to resetting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_sleep_to_reset(self):
        """
        ## **Transition**

        * **from: *sleeping* ** state
        * **to: *resetting* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to resetting state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4


    @notify_state
    def on_run_to_test(self):
        """
        ## **Transition**

        * **from: *running* ** state
        * **to: *testing* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to testing state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_wait_to_test(self):
        """
        ## **Transition**

        * **from: *waiting* ** state
        * **to: *testing* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to testing state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_run_to_sleep(self):
        """
        ## **Transition**

        * **from: *running* ** state
        * **to: *sleeping* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to sleeping state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    @notify_state
    def on_wait_to_sleep(self):
        """
        ## **Transition**

        * **from: *waiting* ** state
        * **to: *sleeping* ** state

        ### **Settings**

        * **priority:** 4 (high-middle priority) machine to sleeping state, warning
        * **classification:** user (Transition triggered by the operator)

        This method is decorated by @notify_transition to register this event in the database.
        """
        self.criticity = 4

    # Auxiliary Methods
    @logging_error_handler
    def init_configuration(self):
        r"""
        Documentation here
        """
        self.parse_config_file()
        self.restart_buffer()

    @logging_error_handler
    def define_tag(self, **payload):
        r"""
        Documentation here
        """
        requests.post(f'{self.DAQ_SERVICE_URL}/api/tags/add', headers=self.headers, json=payload)

        return payload

    @logging_error_handler
    def define_alarm(self, **payload):
        r"""
        Documentation here
        """
        requests.post(f'{self.DAQ_SERVICE_URL}/api/alarms/append', headers=self.headers, json=payload)

        return payload

    @logging_error_handler
    def get_allowed_transitions(self):
        r"""
        Documentation here
        """
        _transitions = self.allowed_transitions
        transitions = {
            'reset': False,
        }
        for transition in _transitions:

            t = transition.destinations[0].name
            current_state = self.current_state.name.lower()

            if current_state=="confirm_restart":

                transitions["confirm restart"] = True

                continue

            if current_state=="confirm_reset":

                transitions["confirm reset"] = True

                continue

            if t in self.states_for_users:

                transitions[t] = True

        return transitions

    @logging_error_handler
    def transition(
        self,
        to
        ):
        r"""
        Documentation here
        """
        _from = self.current_state.name.lower()
        _transition = getattr(self, '{}_to_{}'.format(_from, to))
        _transition()

    @logging_error_handler
    def read_data(self):
        r"""
        Documentation here
        """
        payload = {
            'tags': list(self.system_tags.keys())
        }
        data = dict()

        response = requests.post(f'{self.DAQ_SERVICE_URL}/api/daq/read_current_tags', json=payload, headers=self.headers)

        if response:

            tags = response.json()

            for tag_name, value in tags.items():

                data[tag_name] = value

        return data

    @logging_error_handler
    def parse_config_file(self):
        r"""
        Documentation here
        """
        if self.config_file_location:

            config = parse_config(self.config_file_location)

            if 'modules' in config and config['modules'] is not None:

                if 'engine' in config['modules'] and config['modules']['engine'] is not None:

                    if 'tags' in config['modules']['engine'] and config['modules']['engine']['tags'] is not None:

                        tags = config['modules']['engine']['tags']
                        self.default_tags = [self.define_tag(**tag) for key, tag in tags.items()]


                    if 'alarms' in config['modules']['engine'] and config['modules']['engine']['alarms'] is not None:

                        alarms = config['modules']['engine']['alarms']
                        self.default_alarms = [self.define_alarm(**alarm)for key, alarm in alarms.items()]

                    if 'event_name' in config['modules']['engine'] :

                        self.event_name = config['modules']['engine']['event_name']

                    if 'time_window' in config['modules']['engine']:
                        _time_window = config['modules']['engine']['time_window']
                        self.time_window = int(_time_window / self.get_interval())

                    if 'system_tags' in config['modules']['engine']:

                        self.system_tags = config['modules']['engine']['system_tags']

    @logging_error_handler
    def restart_buffer(self):
        r"""
        Documentation here
        """
        for tag in list(self.system_tags.keys()):

            location = None
            if 'location' in self.system_tags[tag]:

                location = self.system_tags[tag]['location']

            self.buffer[tag] = {
                'data': list(),
                'location': location
                            }

    @logging_error_handler
    def get_default_tags(self):
        r"""
        Documentation here
        """
        return self.default_tags

    @logging_error_handler
    def get_default_alarms(self):
        r"""
        Documentation here
        """
        return self.default_alarms

    @logging_error_handler
    def fill_buffer(self, data:dict)->dict:
        r"""
        Documentation here
        """
        for tag_name, value in data.items():

            if len(self.buffer[tag_name]['data']) < self.time_window:

                _value = self.buffer[tag_name]['data']
                _value.append(value['y'])
                self.buffer[tag_name]['data'] = _value
                self.ready_to_run = False

            else:

                _value = self.buffer[tag_name]['data']
                _value = _value[1:] + _value[:1]
                _value[-1] = value['y']
                self.buffer[tag_name]['data'] = _value
                self.ready_to_run = True
