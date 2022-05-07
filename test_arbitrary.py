import json
import subprocess
import pytest


PLAYBOOK = """
---
- hosts: localhost
  tasks:{}
      register: result
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
        subprocess.check_call(command)

        with output_path.open("r") as f:
            result = f.read()

        return json.loads(result)

    return inner


def test_run(run_task):
    res = run_task("""
    - name: Print hello world
      debug:
        msg: Hello, world!
    """)
    assert not res["changed"]
    assert res["msg"] == "Hello, world!"
