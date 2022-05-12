from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            "exec": dict(required=False, type='str'),
            "eval": dict(required=True, type='str'),
        }
    )
    code = module.params.get("exec")
    final_expr = module.params["eval"]
    globals_and_locals = {}
    try:
        if code is not None:
            exec(code, globals_and_locals)
        result = eval(final_expr, globals_and_locals)
    except Exception as e:
        module.fail_json(msg=f"{e}", code=code)

    module.exit_json(changed=True, result=result)


if __name__ == '__main__':
    main()

