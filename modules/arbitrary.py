from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec = dict(
            code      = dict(required=True, type='str'),
        )
    )
    module.exit_json(changed=True, msg="Hello, world!")


if __name__ == '__main__':
    main()

