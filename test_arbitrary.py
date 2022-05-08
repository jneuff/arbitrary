import json
import subprocess
import pytest


PLAYBOOK = """
---
- hosts: localhost
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

    def inner(task):
        with playbook_path.open("w") as f:
            contents = PLAYBOOK.format(task, output_path)
            f.write(contents)

        command = ["ansible-playbook", playbook_path]
        _proc = subprocess.run(command)

        with output_path.open("r") as f:
            result = f.read()

        return json.loads(result)

    return inner


def test_evaluate_str(run_task):
    res = run_task("""
    - name: Print hello world
      arbitrary:
        eval: |
          "Hello, world!"
    """)
    print(res)
    assert res["changed"]
    assert res["result"] == "Hello, world!"


def test_return_errors(run_task):
    res = run_task("""
    - name: Print hello world
      arbitrary:
        eval: |
          print(undefined_var)
    """)
    print(res)
    assert res["failed"]
    assert "msg" in res
    assert "code" in res
