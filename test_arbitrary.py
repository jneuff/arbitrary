import json
import subprocess
import pytest


PLAYBOOK = """
---
- hosts: localhost
  gather_facts: false
  vars: {}
  tasks:{}
      register: result
      ignore_errors: true
    - name: Dump result
      shell:
        cmd: "echo '{{{{ result|to_nice_json }}}}' > {}"
"""


@pytest.fixture
def run_task(tmp_path):
    playbook_path = tmp_path / "playbook.yml"
    output_path = tmp_path / "output.json"

    def inner(task, set_vars={}):
        with playbook_path.open("w") as f:
            contents = PLAYBOOK.format(set_vars, task, output_path)
            f.write(contents)

        command = ["ansible-playbook", playbook_path]
        _proc = subprocess.run(command)

        with output_path.open("r") as f:
            result = f.read()

        return json.loads(result)

    return inner


def test_evaluate_str(run_task):
    actual = run_task(
        """
    - name: Print hello world
      arbitrary:
        expression: |
          "Hello, world!"
    """
    )
    assert not actual["failed"]
    assert actual["result"] == "Hello, world!"


def test_reports_error_in_expression(run_task):
    actual = run_task(
        """
    - arbitrary:
        expression: |
          print(undefined_var)
    """
    )
    assert actual["failed"]
    assert "msg" in actual


def test_reports_error_in_statements(run_task):
    actual = run_task(
        """
    - arbitrary:
        statements: |
          this = undefined
        expression: |
          "no problem here"
    """
    )
    assert actual["failed"]
    assert "msg" in actual


def test_transform_items(run_task):
    actual = run_task(
        """
    - arbitrary:
        statements: |
          def transform(item):
              return {
                  "first": item[0],
                  "second": item[1],
              }

        expression: |
          [transform(i) for i in {{ things }}]
    """,
        set_vars="""
    things:
      - 0: "lorem"
        1: "ipsum"
      - 0: "something"
        1: "entirely"
        2: "new"
    """,
    )
    assert not actual["failed"]
    assert actual["result"] == [
        {
            "first": "lorem",
            "second": "ipsum",
        },
        {
            "first": "something",
            "second": "entirely",
        },
    ]
