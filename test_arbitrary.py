import pytest


def run_task(task):
    return {
        "changed": True,
        "output": "Hello, world!"
    }



def test_run():
    res = run_task("""
    - name: Print hello world
      debug:
        msg: Hello, world!
    """)
    assert res["changed"]
    assert res["output"] == "Hello, world!"
