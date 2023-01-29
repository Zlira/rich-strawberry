def test_context_not_logged_by_default(default_schema, get_stripped_stderr):
    query = """
      query GetUsers {
        missingUser: user(id: 3) { name }
        secretUser: user(id: 2) { name }
      }
    """
    result = default_schema.execute_sync(
        query=query,
        variable_values={"id": 5},
        context_value={
            "request": "this is request from context",
            "other_val": "this is other val",
        },
    )

    assert result.data == {"missingUser": None, "secretUser": None}
    assert result.errors
    assert len(result.errors) == 2

    err_output = get_stripped_stderr()

    print(err_output)
    assert "CONTEXT" not in err_output
    assert "this is request from context" not in err_output
    assert "this is other val" not in err_output


def test_can_configure_context_keys_to_log(
    get_stripped_stderr, get_schema_with_logger_params
):
    schema = get_schema_with_logger_params(
        log_context_keys=("request", "other_val")
    )
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = schema.execute_sync(
        query=query,
        variable_values={"id": 5},
        context_value={
            "request": "this is request from context",
            "other_val": "this is other val",
        },
    )

    assert result.data == {"user": None}
    assert result.errors
    assert len(result.errors) == 1

    err_output = get_stripped_stderr()
    # print(err_output)

    assert err_output.count("CONTEXT") == 1
    assert err_output.count("this is request from context") == 1
    assert err_output.count("this is other val") == 1


def test_warn_about_missing_context_key(
    get_stripped_stderr, get_schema_with_logger_params
):
    schema = get_schema_with_logger_params(log_context_keys=("request",))
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = schema.execute_sync(
        query=query,
        variable_values={"id": 5},
        context_value={"other_val": 2},
    )

    assert result.data == {"user": None}
    assert result.errors
    assert len(result.errors) == 1

    err_output = get_stripped_stderr()

    assert err_output.count("CONTEXT") == 1
    assert "Warning: missing context key 'request'" in err_output


def test_warn_about_context_not_being_mapping():
    # TBD
    pass
