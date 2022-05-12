from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            "statements": dict(required=False, type="str"),
            "expression": dict(required=True, type="str"),
        }
    )
    statements = module.params.get("statements")
    expression = module.params["expression"]
    globals_and_locals = {}
    try:
        if statements is not None:
            exec(statements, globals_and_locals)
        result = eval(expression, globals_and_locals)
    except Exception as e:
        module.fail_json(msg=f"{e}", code=statements)

    module.exit_json(changed=True, result=result)


if __name__ == "__main__":
    main()
