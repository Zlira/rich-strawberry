def test_query_without_errors(default_schema):
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = default_schema.execute_sync(query=query, variable_values={"id": 1})
    assert result.data == {"user": {"name": "Solpavchek", "age": 100}}
    assert not result.errors


def test_error_in_the_query(default_schema, get_stripped_stderr):
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = default_schema.execute_sync(query=query)

    assert result.data is None
    assert result.errors
    assert len(result.errors) == 1

    err_output = get_stripped_stderr()
    graphql_err = result.errors[0]

    assert "GRAPHQL ERROR" in err_output
    assert graphql_err.message in err_output
    assert str(graphql_err) in err_output


def test_error_in_resolver_code(default_schema, get_stripped_stderr):
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = default_schema.execute_sync(query=query, variable_values={"id": 5})

    assert result.data == {"user": None}
    assert result.errors
    assert len(result.errors) == 1

    err_output = get_stripped_stderr()

    graphql_err = result.errors[0]
    assert "GRAPHQL ERROR" in err_output
    assert graphql_err.message in err_output
    assert str(graphql_err) in err_output
    assert "Traceback (most recent call last)" in err_output
    assert "ValueError: User not found" in err_output


def test_multiple_errors(default_schema, get_stripped_stderr):
    query = """
      query GetUsers {
        missingUser: user(id: 3) { name }
        secretUser: user(id: 2) { name }
      }
    """
    result = default_schema.execute_sync(query=query, variable_values={"id": 2})

    assert result.data == {"missingUser": None, "secretUser": None}
    assert result.errors
    assert len(result.errors) == 2

    err_output = get_stripped_stderr()

    assert err_output.count("GRAPHQL ERROR") == 2
    assert result.errors[0].message in err_output
    assert str(result.errors[0]) in err_output
    assert result.errors[1].message in err_output
    assert str(result.errors[1]) in err_output
    assert err_output.count("Traceback (most recent call last)", 2)
    assert "ValueError: User not found" in err_output
    assert "ValueError: This is a secret user!" in err_output
