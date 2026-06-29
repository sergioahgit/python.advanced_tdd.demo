# TDD Walkthrough: Building a User Processing Workflow

## Overview

This document demonstrates how a user processing workflow was developed using the Test-Driven Development (TDD) cycle:

```text
Red → Green → Refactor
```

Where:

* **Red** = Write a failing test.
* **Green** = Write the minimum code required to pass the test.
* **Refactor** = Improve the design while keeping tests green.

The workflow consists of three steps:

1. Fetch user data
2. Clean user data
3. Save user data

---

# Iteration 1 - Creating a test case for each step.

Fetch User Data

## Requirement

The workflow should fetch user data and place it in the workflow context.
The **WorkflowContext** is used to store and share data between workflow steps during execution. It acts as a lightweight in-memory data structure that enables decoupled communication between steps.

---

## RED

Write the test first.

```python
import pytest


class WorkflowContext:

    def __init__(self):
        pass

def test_fetch_user_data_populates_context():
    context = WorkflowContext()

    step = FetchUserDataStep(user_id=123)

    step.execute(context)

    assert context.store["raw_user_data"] == {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

```

### Result

```text
FAILED
NameError: FetchUserDataStep is not defined


tests.py::test_fetch_user_data_populates_context 

============================== 1 failed in 0.13s ==============================
FAILED [100%]
tests.py:9 (test_fetch_user_data_populates_context)
def test_fetch_user_data_populates_context():
        context = WorkflowContext()
    
>       step = FetchUserDataStep(user_id=123)
               ^^^^^^^^^^^^^^^^^
E       NameError: name 'FetchUserDataStep' is not defined

tests:12: NameError

Process finished with exit code 1
```

---

## GREEN

Write the minimum code necessary to make the test pass.

At this stage, did a minimum implementation by creating a simple **FetchUserDataStep** class that takes in a **user_id** to fetch the user information and store it in the **WorkflowContext**.

```python
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

class FetchUserDataStep:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self, context: WorkflowContext) -> None:
        print(f"Fetching data for user {self.user_id}")

        # Simulates fetching data
        context.store["raw_user_data"] = {
            "id": self.user_id,
            "name": "Sergio",
            "email": "SERGIO@ADVANCED_TDD.COM"
        }

def test_fetch_user_data_populates_context():
    context = WorkflowContext()

    step = FetchUserDataStep(user_id=123)

    step.execute(context)

    assert context.store["raw_user_data"] == {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

```

### Result

```text
PASSED

============================= test session starts =============================
collecting ... collected 1 item

tests.py::test_fetch_user_data_populates_context PASSED [100%]Fetching data for user 123


============================== 1 passed in 0.39s ==============================

Process finished with exit code 0
```

---

# Clean Data

## Requirement

Email addresses should be normalized to lowercase.

---

## RED

```python
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

def test_clean_data_creates_cleaned_user_data():

    context = WorkflowContext()

    context.store["raw_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

    CleanDataStep().execute(context)

    assert context.store["cleaned_user_data"]["email"] == (
        "sergio@advanced_tdd.com"
    )
```

### Result

```text
FAILED
NameError: CleanDataStep is not defined

============================= test session starts =============================
collecting ... collected 1 item

tests.py::test_clean_data_creates_cleaned_user_data 

============================== 1 failed in 1.03s ==============================
FAILED [100%]
tests.py:55 (test_clean_data_creates_cleaned_user_data)
def test_clean_data_creates_cleaned_user_data():
    
        context = WorkflowContext()
    
        context.store["raw_user_data"] = {
            "id": 123,
            "name": "Sergio",
            "email": "SERGIO@ADVANCED_TDD.COM"
        }
    
>       CleanDataStep().execute(context)
        ^^^^^^^^^^^^^
E       NameError: name 'CleanDataStep' is not defined

tests.py:65: NameError

Process finished with exit code 1


```

---

## GREEN

Write the minimum code necessary to make the test pass.

At this stage, did a minimum implementation by creating a simple **CleanDataStep** class that given a context containing raw data, converts the user email into lower case and stores it in the **WorkflowContext**.

```python
import copy
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

class CleanDataStep:

    def execute(self, context: WorkflowContext) -> None:

        print("Cleaning user data...")

        raw_data = context.store.get("raw_user_data")
        if raw_data:

            # Normalize email to lower case.
            cleaned_user_data = copy.deepcopy(raw_data)
            cleaned_user_data["email"] = cleaned_user_data["email"].lower()

            context.store["cleaned_user_data"] = cleaned_user_data

def test_clean_data_creates_cleaned_user_data():

    context = WorkflowContext()

    context.store["raw_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

    CleanDataStep().execute(context)

    assert context.store["cleaned_user_data"]["email"] == (
        "sergio@advanced_tdd.com"
    )
```

### Result

```text
PASSED

============================= test session starts =============================
collecting ... collected 1 item

tests.py::test_clean_data_creates_cleaned_user_data PASSED [100%]Cleaning user data...

============================== 1 passed in 0.04s ==============================

Process finished with exit code 0

```

---

# Save User Data

## Requirement

The workflow should save user data in the database.

At the stage, we assumed the data has been fetched and cleaned up prior to saving the user data.

---

## RED

```python
import copy
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

def test_save_user_step_success():

    mock_db_repository = None
    
    context = WorkflowContext()

    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SaveUserStep(mock_db_repository)

    step.execute(context)

    assert context.store["saved_user_id"] == 123
```

### Result

```text
FAILED
NameError: SaveUserStep is not defined

FAILED [100%]
tests.py:36 (test_save_user_step_success)
def test_save_user_step_success():
    
        mock_db_repository = None
    
        context = WorkflowContext()
    
        context.store["cleaned_user_data"] = {
            "id": 123,
            "name": "Sergio",
            "email": "sergio@advanced_tdd.com"
        }
    
>       step = SaveUserStep(mock_db_repository)
               ^^^^^^^^^^^^
E       NameError: name 'SaveUserStep' is not defined

tests.py:48: NameError

Process finished with exit code 1

```

---

## GREEN

Write the smallest implementation possible to make the test pass.


```python
import copy
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

class SaveUserStep:

    def __init__(self, db_repository):
        pass

    def execute(self, context):

        user_id = context.store["cleaned_user_data"]["id"]

        print(f"Updated user {user_id} entry in database.")

        context.store["saved_user_id"] = user_id

def test_save_user_step_success():

    mock_db_repository = None

    context = WorkflowContext()

    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SaveUserStep(mock_db_repository)

    step.execute(context)

    assert context.store["saved_user_id"] == 123
```

### Result

```text
PASSED

============================= test session starts =============================
collecting ... collected 1 item

tests.py::test_save_user_step_success PASSED PASSED [100%]Updated user 123 entry in database.

============================== 1 passed in 0.34s ==============================

Process finished with exit code 0
```

### Observation

The implementation is ugly, but it passes.

This is acceptable in TDD because the goal is to make the test green as quickly as possible. At this stage, 3 test cases were created that covered the 3 core steps of the workflow:

1. Fetch user data
2. Clean user data
3. Save user data

```python
import copy
import pytest
from typing import List, Any, Dict

class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

class FetchUserDataStep:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self, context: WorkflowContext) -> None:
        print(f"Fetching data for user {self.user_id}")

        # Simulates fetching data
        context.store["raw_user_data"] = {
            "id": self.user_id,
            "name": "Sergio",
            "email": "SERGIO@ADVANCED_TDD.COM"
        }

class CleanDataStep:
    
    def execute(self, context: WorkflowContext) -> None:

        print("Cleaning user data...")

        raw_data = context.store.get("raw_user_data")
        if raw_data:

            # Normalize email to lower case.
            cleaned_user_data = copy.deepcopy(raw_data)
            cleaned_user_data["email"] = cleaned_user_data["email"].lower()

            context.store["cleaned_user_data"] = cleaned_user_data

class SaveUserStep:

    def __init__(self, db_repository):
        pass

    def execute(self, context):

        user_id = context.store["cleaned_user_data"]["id"]

        print(f"Updated user {user_id} entry in database.")

        context.store["saved_user_id"] = user_id

def test_save_user_step_success():

    mock_db_repository = None

    context = WorkflowContext()

    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SaveUserStep(mock_db_repository)

    step.execute(context)

    assert context.store["saved_user_id"] == 123

def test_clean_data_creates_cleaned_user_data():

    context = WorkflowContext()

    context.store["raw_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

    CleanDataStep().execute(context)

    assert context.store["cleaned_user_data"]["email"] == (
        "sergio@advanced_tdd.com"
    )

def test_fetch_user_data_populates_context():
    context = WorkflowContext()

    step = FetchUserDataStep(user_id=123)

    step.execute(context)

    assert context.store["raw_user_data"] == {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }
```
---

## REFACTOR - Improve the Implementation

At the stage, the refactor work involved on:
1. Separating the code in a defined directory structures:
   * core files that define the **WorkflowContext** and **WorkflowStep**.
   * step files that define the 3 Steps (**FetchUserDataStep**, **CleanDataStep**, **SaveUserStep**).
   * test files that define the test cases. 
2. Since the **SaveUserStep** depended on the mock_db_repository to save the step, a fixture was introduced to create a Mock DB Repository object. 


**Project directory structure**
```text
advanced_tdd
|-- README.md
|-- workflow_app/
|   |-- src/
|       |-- core/
|           |-- __init__.py
|           |-- context.py
|           |-- step.py
|       __init__.py
|       |-- steps/
|           |-- user_steps.py
|           __init__.py
|       __init__.py
|   |-- tests/
|       |-- test_steps/
|           |-- tests_fetch_user_data_steps.py
|           |-- tests_clean_data_steps.py
|           |-- tests_save_user_steps.py
|           |-- __init__.py
|       |-- conftest.py


```

**workkflow_app/src/core/context.py**
```python
from typing import List, Any, Dict

__all__ = ["WorkflowContext"]


class WorkflowContext:

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.errors: List[Exception] = []

```
**workkflow_app/src/core/step.py**
```python
from abc import ABC, abstractmethod

from workflow_app.src.core.context import WorkflowContext

__all__ = ["WorkflowStep"]


class WorkflowStep(ABC):

    @abstractmethod
    def execute(self, context: WorkflowContext) -> None:
        pass

```

**workkflow_app/src/steps/user_steps.py**
```python
import copy

from workflow_app.src.core.step import WorkflowStep
from workflow_app.src.core.context import WorkflowContext

__all__ = ["FetchUserDataStep", "CleanDataStep", "SaveUserStep" ]


class FetchUserDataStep(WorkflowStep):

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self, context: WorkflowContext) -> None:

        print(f"Fetching data for user {self.user_id}")

        # Simulates fetching data
        context.store["raw_user_data"] = {
            "id": self.user_id,
            "name": "Sergio",
            "email": "SERGIO@ADVANCED_TDD.COM"
        }

class CleanDataStep(WorkflowStep):

    def execute(self, context: WorkflowContext) -> None:

        print("Cleaning user data...")

        raw_data = context.store.get("raw_user_data")
        if raw_data:

            # Normalize email to lower case.
            cleaned_user_data = copy.deepcopy(raw_data)
            cleaned_user_data["email"] = cleaned_user_data["email"].lower()

            context.store["cleaned_user_data"] = cleaned_user_data

class SaveUserStep(WorkflowStep):

    def __init__(self, db_repository):
        self.db_repository = db_repository

    def execute(self, context: WorkflowContext) -> None:
        
        cleaned_data = context.store.get("cleaned_user_data")

        if not cleaned_data:
            raise ValueError("No cleaned user data found in context")

        #TODO: Replace this line to later to simulate saving data to database through the db_repository.
        user_id = cleaned_data["id"]

        context.store["saved_user_id"] = user_id
```

**workkflow_app/tests/tests_steps/test_fetch_user_data_steps.py**
```python
import pytest
from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import FetchUserDataStep


def test_fetch_user_data_populates_context():
    """Verify that FetchUserDataStep correctly populates raw user data in context.

    This test ensures that the FetchUserDataStep simulates retrieving user data
    and stores the expected structured result in the WorkflowContext.

    It validates that:
    - The step uses the provided user_id correctly
    - The full user payload is created as expected
    - The result is stored under 'raw_user_data' in the context

    This test confirms the correctness of the initial data-fetching step in the
    workflow pipeline.
    """

    context = WorkflowContext()

    step = FetchUserDataStep(user_id=123)

    step.execute(context)

    assert context.store["raw_user_data"] == {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

```

**workkflow_app/tests/tests_steps/test_clean_data_steps.py**
```python
from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import CleanDataStep

def test_clean_data_creates_cleaned_user_data():
    """Verify that CleanDataStep correctly creates normalized user data.

    This test ensures that CleanDataStep transforms raw user data into a
    cleaned version stored in the WorkflowContext.

    It validates that:
    - Raw user data is read from 'raw_user_data'
    - Email addresses are normalized to lowercase
    - The result is stored under 'cleaned_user_data'
    - The transformation preserves all existing user fields

    This test confirms the correctness of the data cleaning transformation
    step in the workflow pipeline.
    """
    context = WorkflowContext()

    context.store["raw_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "SERGIO@ADVANCED_TDD.COM"
    }

    CleanDataStep().execute(context)

    assert context.store["cleaned_user_data"]["email"] == (
        "sergio@advanced_tdd.com"
    )
```

**workkflow_app/tests/tests_steps/test_save_user_steps.py**
```python
import pytest

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.users_steps import SaveUserStep
from workflow_app.tests.conftest import mock_db_repository


def test_save_user_step_success(mock_db_repository):
    """Verify that SaveUserStep successfully saves user data using a
    repository.

    This test ensures that SaveUserStep correctly interacts with the provided
    database repository and updates the WorkflowContext with the returned ID.

    It also demonstrates pytest fixture injection behavior, where the fixture
    name 'mock_db_repository' is automatically resolved and injected into the
    test.

    Args:
        mock_db_repository:
            A pytest fixture providing a mocked repository. It simulates the
            persistence layer and allows verification of method calls without
            using a real database.

    Validations:
        - The user ID returned by the repository is stored in the context
        - The repository's save_user method is called exactly once
        - The correct user payload is passed to the repository
    """

    context = WorkflowContext()
    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SaveUserStep(db_repository=mock_db_repository)
    step.execute(context)

    # These checks both:
    # 1. The result was stored correctly.
    # 2. SaveUserStep actually attempted to save the expected data.
    assert context.store["saved_user_id"] == 123


```

**workkflow_app/tests/conftest.py**
```python
"""This code is intended to define a reusable pytest fixture that
provides a mocked database repository."""

import pytest
from unittest.mock import Mock

__all__ = ["mock_db_repository"]


@pytest.fixture
def mock_db_repository():
    """
    A pytest fixture is a function that provides setup objects for tests.
    In this case, this fixture should create a mock object that behaves
    like a database repository.  Providing a reusable mock database
    repository for step tests.

    In tests, you usually don't want to connect to a real database.
    A mock lets you:
        1. control return values
        2. simulate failures
        3. verify method calls
        4. keep tests fast and isolated
    """

    # A Mock object will automatically create mock attributes and methods
    # when you access them.
    mock = Mock()

    # During test, we don't care about actually saving a user. You just want
    # to return a predictable value.  This will ensure the code under test
    # behaves as if the database returned user ID 123.
    mock.save_user.return_value = 123

    return mock


```
---

# Iteration 2 - Creating a test case for sending a welcome email to user.

Send Welcome Email

## Requirement

A welcome email should be sent to the newly saved user. Simulating a sending a welcome email via a print message.

```text
Sending email to user: Sergio, email: sergio@advanced_tdd.com
```

---

## RED

Write the test first.  This involved first learning how to test a print message via assert.  Luckily, there is a mock decorator for testing print messages.

**workflow_app/tests/test_steps/test_send_email_steps.py**
```python
from unittest.mock import patch

from workflow_app.src.core.context import WorkflowContext


@patch("builtins.print")
def test_execute_prints_welcome_email(mock_print):
    """Verify that the workflow step prints the expected welcome email message.

    The ``@patch("builtins.print")`` decorator temporarily replaces
    Python's built-in ``print()`` function with a ``Mock`` object for
    the duration of this test. The injected ``mock_print`` argument
    records calls made to ``print()`` so the test can verify the
    expected output without writing anything to the console.

    Args:
        mock_print:
            Mock object that replaces Python's built-in ``print()``
            function during the execution of this test.
    """

    context = WorkflowContext()
    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SendWelcomeEmailStep()

    step.execute(context)

    mock_print.assert_called_once_with(
        "Sending email to user: Sergio, "
        "email: sergio@advanced_tdd.com"
    )


```

### Result

```text
FAILED
NameError: name 'SendWelcomeEmailStep' is not defined


============================== 1 failed in 0.10s ==============================
FAILED [100%]
workflow_app\tests\test_steps\test_send_email_steps.py:6 (test_execute_prints_welcome_email)
mock_print = <MagicMock name='print' id='1325472886672'>

    @patch("builtins.print")
    def test_execute_prints_welcome_email(mock_print):
        """Verify that the workflow step prints the expected welcome email message.
    
        The ``@patch("builtins.print")`` decorator temporarily replaces
        Python's built-in ``print()`` function with a ``Mock`` object for
        the duration of this test. The injected ``mock_print`` argument
        records calls made to ``print()`` so the test can verify the
        expected output without writing anything to the console.
    
        Args:
            mock_print:
                Mock object that replaces Python's built-in ``print()``
                function during the execution of this test.
        """
    
        context = WorkflowContext()
        context.store["cleaned_user_data"] = {
            "id": 123,
            "name": "Sergio",
            "email": "sergio@advanced_tdd.com"
        }
    
>       step = SendWelcomeEmailStep()
               ^^^^^^^^^^^^^^^^^^^^
E       NameError: name 'SendWelcomeEmailStep' is not defined

workflow_app\tests\test_steps\test_send_email_steps.py:29: NameError

Process finished with exit code 1
```

---

## GREEN

Write the minimum code necessary to make the test pass.

At this stage, did a minimum implementation by creating a simple **SendWelcomeEmailStep** class that takes in the cleaned user data and simulates sending an email.

**workflow_app/core/steps/notification_steps.py**
```python
from workflow_app.src.core.step import WorkflowStep
from workflow_app.src.core.context import WorkflowContext

__all__ = ["SendWelcomeEmailStep"]


class SendWelcomeEmailStep(WorkflowStep):
    
    def execute(self, context: WorkflowContext) -> None:
        
        cleaned_data = context.store["cleaned_user_data"]

        # Simulate sending a welcome email.
        print(
            f"Sending email to user: {cleaned_data['name']}, "
            f"email: {cleaned_data['email']}"
        )

```

Then proceeded to import the SendWelcomeEmailStep into the test case:
```python
from unittest.mock import patch

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.notification_steps import SendWelcomeEmailStep


@patch("builtins.print")
def test_execute_prints_welcome_email(mock_print):

    context = WorkflowContext()
    context.store["cleaned_user_data"] = {
        "id": 123,
        "name": "Sergio",
        "email": "sergio@advanced_tdd.com"
    }

    step = SendWelcomeEmailStep()

    step.execute(context)

    mock_print.assert_called_once_with(
        "Sending email to user: Sergio, "
        "email: sergio@advanced_tdd.com"
    )

```

### Result

```text
PASSED

============================== test session starts =============================
collecting ... collected 1 item

workflow_app/tests/test_steps/test_send_email_steps.py::test_execute_prints_welcome_email PASSED [100%]

============================== 1 passed in 0.35s ==============================

Process finished with exit code 0

```

---

# Iteration 3 — Final Step - Creating Integration Test to verify all steps working together.

Test Workflow

## Requirement
Verify that the full user onboarding workflow executes successfully end-to-end.

1. Fetch user data
2. Clean user data
3. Save user data
4. Send a Welcome email to the user.

**Project directory structure**
```text
advanced_tdd
|-- README.md
|-- workflow_app/
|   |-- src/
|       |-- core/
|           |-- __init__.py
|           |-- context.py
|           |-- orchestrator.py
|           |-- step.py
|       __init__.py
|       |-- steps/
|           |-- user_steps.py
|           __init__.py
|       __init__.py
|   |-- tests/
|       |-- test_steps/
|           |-- tests_fetch_user_data_steps.py
|           |-- tests_clean_data_steps.py
|           |-- tests_save_user_steps.py
|           |-- __init__.py
|       |-- test_integration/
|           |-- test_workflow.py
|           |-- __init__.py
|       |-- conftest.py
```

---

## RED

Write the test first.

**workflow_app/tests/test_integration/test_workflow.py**
```python
def test_full_workflow_orchestration(mock_db_repository):
    
    workflow = UserOnboardingWorkflow(
        user_id=123, db_repository=mock_db_repository
    )
    result_context = workflow.run()

    print("Final Store State:", result_context.store)

    assert result_context.store == {
        'raw_user_data': {
            'id': 123,
            'name': 'Sergio',
            'email': 'sergio@advanced_tdd.com'
        },
        'cleaned_user_data': {
            'id': 123,
            'name': 'Sergio',
            'email': 'sergio@advanced_tdd.com'
        },
        'saved_user_id': 123
    }


```

### Result

```text
FAILED
NameError: name 'UserOnboardingWorkflow' is not defined


============================= test session starts =============================
collecting ... collected 1 item

workflow_app/tests/test_integration/test_workflow.py::test_full_workflow_orchestration 

============================== 1 failed in 0.10s ==============================
FAILED [100%]
workflow_app\tests\test_integration\test_workflow.py:1 (test_full_workflow_orchestration)
mock_db_repository = <Mock id='1635025367600'>

    def test_full_workflow_orchestration(mock_db_repository):
    
>       workflow = UserOnboardingWorkflow(
                   ^^^^^^^^^^^^^^^^^^^^^^
            user_id=123, db_repository=mock_db_repository
        )
E       NameError: name 'UserOnboardingWorkflow' is not defined

workflow_app\tests\test_integration\test_workflow.py:3: NameError

Process finished with exit code 1

```

---

## GREEN

Write the minimum code necessary to make the test pass.

At this stage, did a minimum implementation by creating a simple **UserOnboardingWorkflow** class that takes in the user_id and db_repository.  It also involved creating a **BaseWorkflow** orchestration pipeline to drive the test.

**workflow_app/core/steps/notification_steps.py**
```python
from workflow_app.src.core.orchestrator import BaseWorkflow
from workflow_app.src.steps.users_steps import (
    FetchUserDataStep,
    CleanDataStep,
    SaveUserStep
)
from workflow_app.src.steps.notification_steps import SendWelcomeEmailStep

__all__ = ["UserOnboardingWorkflow"]


class UserOnboardingWorkflow(BaseWorkflow):

    def __init__(self, user_id: int, db_repository):

        """Defines the exact pipeline of steps for this specific workflow"""
        steps = [
            FetchUserDataStep(user_id=user_id),
            CleanDataStep(),
            SaveUserStep(db_repository),
            SendWelcomeEmailStep()
        ]

        super().__init__(steps=steps)


```

Introduced Orchestration pipeline that will run the workflow steps.

**workkflow_app/src/core/orchestrator.py**
```python
from typing import List

from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.core.step import WorkflowStep

__all__ = ["BaseWorkflow"]


class BaseWorkflow:

    def __init__(self, steps: List[WorkflowStep]):
        self.steps = steps

    def run(self) -> WorkflowContext:

        context = WorkflowContext()
        for step in self.steps:

            try:
                step.execute(context)

            except Exception as e:
                context.errors.append(e)

                # Here we could implement rollback logic or break the loop
                break

        return context

```

Then proceeded to import the UserOnboardingWorkflow into the test case:
```python
from workflow_app.src.core.context import WorkflowContext
from workflow_app.src.steps.notification_steps import SendWelcomeEmailStep
from workflow_app.src.steps.users_steps import (
    FetchUserDataStep,
    CleanDataStep,
    SaveUserStep
)
from workflow_app.src.workflows.onboarding import UserOnboardingWorkflow


def test_full_orchestration_workflow_success(mock_db_repository):

    workflow = UserOnboardingWorkflow(
        user_id=123, db_repository=mock_db_repository
    )
    result_context = workflow.run()

    print("Final Store State:", result_context.store)

    assert result_context.store['raw_user_data'] == {
        'id': 123,
        'name': 'Sergio',
        'email': 'SERGIO@ADVANCED_TDD.COM'
    }
    assert result_context.store['cleaned_user_data'] == {
        'id': 123,
        'name': 'Sergio',
        'email': 'sergio@advanced_tdd.com'
    }
    assert "saved_user_id" in result_context.store

```

### Result

```text
PASSED

============================= test session starts =============================
collecting ... collected 1 item

workflow_app/tests/test_integration/test_workflow_temp.py::test_full_orchestration_workflow_success PASSED [100%]Fetching data for user 123
Cleaning user data...
Updated user 123 entry in database.
Sending email to user: Sergio, email: sergio@advanced_tdd.com
Final Store State: {'raw_user_data': {'id': 123, 'name': 'Sergio', 'email': 'SERGIO@ADVANCED_TDD.COM'}, 'cleaned_user_data': {'id': 123, 'name': 'Sergio', 'email': 'sergio@advanced_tdd.com'}, 'saved_user_id': 123}


============================== 1 passed in 0.04s ==============================

Process finished with exit code 0
```

---

# Final Takeaway

* Unit tests verified behavior for each step.
* Integration verified the workflow behavior during user onboarding.

TDD is not about writing tests after development.  TDD is a development process where:

1. A failing test defines the next requirement.
2. Minimal code is written to satisfy that requirement.
3. The design is improved safely through refactoring.
4. The cycle repeats.

By following this process, the workflow evolved incrementally into a fully tested and maintainable solution while continuously providing feedback and confidence.
