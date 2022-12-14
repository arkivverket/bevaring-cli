import pytest


@pytest.fixture
def error_result():
    return {"error": "access_denied"}


@pytest.fixture
def login_result():
    return {
        "token_type": "Bearer",
        "scope": "https://bevaring.dev.digitalarkivet.no/User.Login",
        "expires_in": 3847,
        "ext_expires_in": 3847,
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSJ9.eyJhdWQiOiI2ZTc0MTcyYi1iZTU2LTQ4NDMtOWZmNC1lNjZhMzliYjEyZTMiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3L3YyLjAiLCJpYXQiOjE1MzcyMzEwNDgsIm5iZiI6MTUzNzIzMTA0OCwiZXhwIjoxNTM3MjM0OTQ4LCJhaW8iOiJBWFFBaS84SUFBQUF0QWFaTG8zQ2hNaWY2S09udHRSQjdlQnE0L0RjY1F6amNKR3hQWXkvQzNqRGFOR3hYZDZ3TklJVkdSZ2hOUm53SjFsT2NBbk5aY2p2a295ckZ4Q3R0djMzMTQwUmlvT0ZKNGJDQ0dWdW9DYWcxdU9UVDIyMjIyZ0h3TFBZUS91Zjc5UVgrMEtJaWpkcm1wNjlSY3R6bVE9PSIsImF6cCI6IjZlNzQxNzJiLWJlNTYtNDg0My05ZmY0LWU2NmEzOWJiMTJlMyIsImF6cGFjciI6IjAiLCJuYW1lIjoiQWJlIExpbmNvbG4iLCJvaWQiOiI2OTAyMjJiZS1mZjFhLTRkNTYtYWJkMS03ZTRmN2QzOGU0NzQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmVsaUBtaWNyb3NvZnQuY29tIiwicmgiOiJJIiwic2NwIjoiYWNjZXNzX2FzX3VzZXIiLCJzdWIiOiJIS1pwZmFIeVdhZGVPb3VZbGl0anJJLUtmZlRtMjIyWDVyclYzeERxZktRIiwidGlkIjoiNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3IiwidXRpIjoiZnFpQnFYTFBqMGVRYTgyUy1JWUZBQSIsInZlciI6IjIuMCJ9.pj4N-w_3Us9DrBLfpCt",  # noqa: E501
        "refresh_token": "0.AR8AbtU0Q0pNw1D4VeYN6TMic40lu2tzCJrMvHVukrU9BvJUfAH.QcI9FMKKU4T0sb4Q5dnlfhvs456iVyz9er+dio7sw4P5gT9M4Vua9D5FVB44b7X9dVxkK0y/dOU5r9yOwI1vep8dGbmVar9Cr8ZTV9OkdDK5ts7P0zNrEAidEDL8hFUUl1KKa55ZaFAkgx9TAPnCamkDDvvg3wDE0sv7hWFJwgK4sMpuGVfP6/JAjYpxxZUhcgqhLBh6bkLXQvK8O5yqsU58RjJFdpho+SitCWiLOSSIElVppNqOMlZxEbBlesH3/VO49MDm3xGci52N+smcC2iaEhdk0jNY/AH2lOyV8LR3IeX1mUqhHzoHchAUy2txngdN4+pgC6OoeP3t3KtrRHkuV4nGRryrYwhvFIoEOH9ZL/rLDZIW6ADAhjhld55F3lN8tO2pCI3EI1chCG46Y/JYSdsphFT1byP2ZCYqTN7rrlnehGWdh9R7ZbCYqlpjkk4lPLv2Nj17q6kuPsf58tqBvz+Xt8Ug+VQAceb06mrvqQ5jl8nrD3gjYB9aSXjMkPMUch/dLS4tw6jY3bdHFfN/W1npTUPwskkWP1HtlYhaBseWTdyqWzqS45fvMQgWERXaGA2uS0757NXUiWwE/QVehrR+jqWcjrk3tjrlZprcb10ZzHNDdQ2ULkDiKH/zn40xuiJFzY1T0LR2VzbGIWZ4ZhFH5TBT7E6kzC5WN3TWzUhEcx5xFm58lcmNWO8ZgpDYoZLJVmyju90f8vA3RkwvmS0xs+V9H0z90kvvh929AEviMrs6t4CluxD4q04rNFywwCPUE86RazAZ4zEp6vWYwNxn9Fhowwx34sDf4gLEnK/p/W1KjRiAA3TuMCBsIF/a9xqguKulPf03c6BHZlz+9us+7ezU08kW553rppzrpIC9VVTynBMtb896vqY",  # noqa: E501
        "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjFMVE16YWtpaGlSbGFfOHoyQkVKVlhlV01xbyJ9.eyJ2ZXIiOiIyLjAiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vOTEyMjA0MGQtNmM2Ny00YzViLWIxMTItMzZhMzA0YjY2ZGFkL3YyLjAiLCJzdWIiOiJBQUFBQUFBQUFBQUFBQUFBQUFBQUFJa3pxRlZyU2FTYUZIeTc4MmJidGFRIiwiYXVkIjoiNmNiMDQwMTgtYTNmNS00NmE3LWI5OTUtOTQwYzc4ZjVhZWYzIiwiZXhwIjoxNTM2MzYxNDExLCJpYXQiOjE1MzYyNzQ3MTEsIm5iZiI6MTUzNjI3NDcxMSwibmFtZSI6IkFiZSBMaW5jb2xuIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiQWJlTGlAbWljcm9zb2Z0LmNvbSIsIm9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC02NmYzLTMzMzJlY2E3ZWE4MSIsInRpZCI6IjkxMjIwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsIm5vbmNlIjoiMTIzNTIzIiwiYWlvIjoiRGYyVVZYTDFpeCFsTUNXTVNPSkJjRmF0emNHZnZGR2hqS3Y4cTVnMHg3MzJkUjVNQjVCaXN2R1FPN1lXQnlqZDhpUURMcSFlR2JJRGFreXA1bW5PcmNkcUhlWVNubHRlcFFtUnA2QUlaOGpZIn0.1AFWW-Ck5nROwSlltm7GzZvDwUkqvhSQpm55TQsmVo9Y59cLhRXpvB8n-55HCr9Z6G_31_UbeUkoz612I2j_Sm9FFShSDDjoaLQr54CreGIJvjtmS3EkK9a7SJBbcpL1MpUtlfygow39tFjY7EVNW9plWUvRrTgVk7lYLprvfzw-CIqw3gHC-T7IK_m_xkr08INERBtaecwhTeN4chPC4W3jdmw_lIxzC48YoQ0dB1L9-ImX98Egypfrlbm0IBL5spFzL6JDZIRRJOu8vecJvj1mq-IUhGt0MacxX8jdxYLP-KUu2d9MbNKpCKJuZ7p8gwTL5B7NlUdh_dmSviPWrw",  # noqa: E501
        "client_info": "eyJ1aWQiOiI4Mjg0NzcwMS1iOTc4LTRiNWQtYTMyMy04MmQ4ZmQyYzQ1NzciLCJ1dGlkIjoiOTlkM2QyOTgtNjBjZi00NjM2LTk3NzItNGExOTFiNmYwZDk0In0",  # noqa: E501
        "id_token_claims": {
            "aud": "6cb04018-a3f5-46a7-b995-940c78f5aef3",
            "iss": "https://login.microsoftonline.com/9122040d-6c67-4c5b-b112-36a304b66dad/v2.0",
            "exp": 1536361411,
            "iat": 1536274711,
            "nbf": 1536274711,
            "name": "Abe Lincoln",
            "preferred_username": "AbeLi@microsoft.com",
            "oid": "00000000-0000-0000-66f3-3332eca7ea81",
            "tid": "9122040d-6c67-4c5b-b112-36a304b66dad",
            "nonce": "123523",
            "aio": "Df2UVXL1ix!lMCWMSOJBcFatzcGfvFGhjKv8q5g0x732dR5MB5BisvGQO7YWByjd8iQDLq!eGbIDakyp5mnOrcdqHeYSnltepQmRp6AIZ8jY",  # noqa: E501
            "rh": "0.AR8AbtU0Q0pNw1D4VeYN6TMic40lu2tzCJrMvHVukrU9BvJUfAH.",
            "sub": "AAAAAAAAAAAAAAAAAAAAAIkzqFVrSaSaFHy782bbtaQ",
            "uti": "fqiBqXLPj0eQa82S-IYFAA",
            "ver": "2.0",
        }
    }


@pytest.fixture
def refresh_result():
    return {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSJ9.eyJhdWQiOiI2ZTc0MTcyYi1iZTU2LTQ4NDMtOWZmNC1lNjZhMzliYjEyZTMiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3L3YyLjAiLCJpYXQiOjE1MzcyMzEwNDgsIm5iZiI6MTUzNzIzMTA0OCwiZXhwIjoxNTM3MjM0OTQ4LCJhaW8iOiJBWFFBaS84SUFBQUF0QWFaTG8zQ2hNaWY2S09udHRSQjdlQnE0L0RjY1F6amNKR3hQWXkvQzNqRGFOR3hYZDZ3TklJVkdSZ2hOUm53SjFsT2NBbk5aY2p2a295ckZ4Q3R0djMzMTQwUmlvT0ZKNGJDQ0dWdW9DYWcxdU9UVDIyMjIyZ0h3TFBZUS91Zjc5UVgrMEtJaWpkcm1wNjlSY3R6bVE9PSIsImF6cCI6IjZlNzQxNzJiLWJlNTYtNDg0My05ZmY0LWU2NmEzOWJiMTJlMyIsImF6cGFjciI6IjAiLCJuYW1lIjoiQWJlIExpbmNvbG4iLCJvaWQiOiI2OTAyMjJiZS1mZjFhLTRkNTYtYWJkMS03ZTRmN2QzOGU0NzQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmVsaUBtaWNyb3NvZnQuY29tIiwicmgiOiJJIiwic2NwIjoiYWNjZXNzX2FzX3VzZXIiLCJzdWIiOiJIS1pwZmFIeVdhZGVPb3VZbGl0anJJLUtmZlRtMjIyWDVyclYzeERxZktRIiwidGlkIjoiNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3IiwidXRpIjoiZnFpQnFYTFBqMGVRYTgyUy1JWUZBQSIsInZlciI6IjIuMCJ9.pj4N-w_3Us9DrBLfpCt",  # noqa: E501
        "token_type": "Bearer",
        "expires_in": 3899,
    }


@pytest.fixture
def copy_response():
    return {
        'datasett_id': 'di',
        'session_id': 'si',
        'bucket_name': 'bn',
        'iam_access_key_id': 'ik',
        'iam_secret_access_key': 'is',
        'target_s3_uri': 's3://bn/di/ip0',
        's3_path': None,
    }


@pytest.fixture
def copy_response_with_s3_path():
    return {
        'datasett_id': 'di',
        'session_id': 'si',
        'bucket_name': 'bn',
        'iam_access_key_id': 'ik',
        'iam_secret_access_key': 'is',
        'target_s3_uri': 's3://bn/sp/di/ip0',
        's3_path': 'sp',
    }


@pytest.fixture
def expected_creds():
    return {
        'target_s3_uri': 's3://bn/di/ip0',
        'iam_access_key_id': 'ik',
        'iam_secret_access_key': 'is',
    }


@pytest.fixture
def expected_creds_with_s3_path():
    return {
        'target_s3_uri': 's3://bn/sp/di/ip0',
        'iam_access_key_id': 'ik',
        'iam_secret_access_key': 'is',
    }


@pytest.fixture
def command_input():
    return [
        "datasett",
        "copy",
        "123",
    ]


@pytest.fixture
def command_input_id():
    return [
        "datasett",
        "copy",
        "123",
        "--id=test1",
    ]


@pytest.fixture
def command_input_id_with_s3_path():
    return [
        "datasett",
        "copy",
        "123",
        "--id=test2",
        "--bucket-name=bn",
        "--iam-access-key-id=ik",
        "--iam-secret-access-key=is",
        "--s3-path=sp",
        "--generation-name=gn",
        "--receipt-email=test@test",
    ]


@pytest.fixture
def command_input_index_increment_test():
    return [
        "datasett",
        "copy",
        "123",
    ]


@pytest.fixture
def command_input_print_copies_file():
    return [
        "datasett",
        "copies",
    ]


@pytest.fixture
def command_input_aws_export():
    return [
        "datasett",
        "aws",
        "test1"
    ]


@pytest.fixture
def command_input_aws_export_id_not_found():
    return [
        "datasett",
        "aws",
        "wrongid",
    ]
