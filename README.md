# Run arbitrary python code in your ansible roles and playbooks

`arbitrary` is an ansible module that allows you to run arbitray python code.

```yaml
---
- hosts: localhost
  vars:
    things:
      - 0: "lorem"
        1: "ipsum"
      - 0: "something"
        1: "entirely"
        2: "new"
  tasks:
    - arbitrary:
        statements: |
          def transform(item):
              return {
                  "first": item[0],
                  "second": item[1],
              }

        expression: |
          [transform(i) for i in {{ things }}]
```

```shell
$ ansible-playbook playbook.yml -v
Using /home/julius/code/arbitrary/ansible.cfg as config file
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [localhost] ******************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************
ok: [localhost]

TASK [arbitrary] ******************************************************************************************************
changed: [localhost] => {"changed": true, "result": [{"first": "lorem", "second": "ipsum"}, {"first": "something", "second": "entirely"}]}

PLAY RECAP ************************************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Why?

I don't like to use jinja filters for data manipulation.
Also this module allows me to rapidly develop behavior for which I would
need to write my own module otherwise (which might be a good idea later).

## How does it work?

The string optionally passed as `statements` is executed via
[python's `exec` function](https://docs.python.org/3/library/functions.html#exec).
The string passed as `expression` is evaluated via
[python's `eval` function](https://docs.python.org/3/library/functions.html#eval).
`globals` are shared between the two and the expression's result
is returned by the module.