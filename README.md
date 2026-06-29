# Test-Driven Development Demo: Building a User Processing Workflow

# TDD Demo Introduction — Workflow Engine

## What This Demo Is About

Today I’ll demonstrate **Test-Driven Development (TDD)** by building a small workflow engine in Python.

The goal is not to build a production system, but to show how TDD influences **design, structure, and correctness** as code evolves.

```text
Note: If you wish to skip demo the introduction, you can jump straight into the written demo walk-through guide - tdd_walkthrough.md (file)
```
---

## The Problem We Are Solving

We are simulating a simple user onboarding workflow:

1. Fetch user data
2. Clean and normalize the data
3. Save the user to a database
4. Send a welcome email

Although simple, this pattern appears frequently in real systems such as:

* User onboarding pipelines
* Background job systems
* Event-driven workflows

---

## High-Level Workflow

The system executes a sequence of steps:

```text id="w3p8qk"
Fetch User Data
        ↓
Clean Data
        ↓
Save User
        ↓
Send Welcome Email
```

Each step is independent and focuses on a single responsibility.

---

## Core Design Concepts

### 1. Workflow Engine

The workflow engine is responsible for executing steps in sequence.

It does not know *how* each step works — only that each step can be executed.

Its responsibilities:

* Run steps in order
* Handle errors
* Stop execution on failure

---

### 2. Workflow Context

The `WorkflowContext` is shared memory across all steps.

It allows steps to communicate without directly depending on each other.

Example:

```python id="k9x0ad"
context.store["raw_user_data"]
context.store["cleaned_user_data"]
context.store["saved_user_id"]
```


---

### 3. Workflow Steps

Each step is an independent unit of behavior.

All steps implement the same interface (contract):

```python id="q8x1lw"
class WorkflowStep:
    def execute(self, context):
        pass
```

This allows the workflow engine to treat all steps uniformly.

---

## The Steps in This Demo

### FetchUserDataStep

Simulates retrieving user data.

Outputs a dictionary containing:

* id
* name
* email

---

### CleanDataStep

Normalizes user data.

Example transformation:

```text id="9p2vnm"
SERGIO@ADVANCED_TDD.COM
→
sergio@advanced_tdd.com
```

---

### SaveUserStep

Simulates saving a user to a database.

* Uses a repository dependency (mocked in tests)
* Returns saved user id.
* Stores the result in the context

---

### SendWelcomeEmailStep

Simulates sending a welcome email.

In this demo it simply prints a message, but in a real system it would call an external email service.

---

## Why This Is a Good TDD Example

This project is intentionally small and focused.

The goal is to show how **design emerges through tests**, not upfront planning.

As we write tests, we will:

* Define behavior before implementation
* Build code incrementally
* Refactor safely
* Discover design improvements naturally

---

## What You Will See During the Demo

As the demo progresses, you will see:

### 1. Red → Green → Refactor in action

We always start with a failing test and only write enough code to pass it.

---

### 2. Design emerging from tests

Classes and responsibilities are not pre-planned — they evolve based on test requirements.

---

### 3. Use of mocking

We simulate external dependencies like databases using mocks.

---

### 4. Integration testing

We will intentionally connect all steps together and observe integration tests.

---

### 5. A real workflow system built incrementally

By the end, we will have a fully working pipeline built entirely from test-driven design decisions.

---

## Expected Outcome

By the end of this demo, we will have:

* A working workflow engine
* Independent, testable workflow steps
* Unit tests for each behavior
* Integration tests for the full pipeline
* Mocked external dependencies
* A clear demonstration of TDD in practice
