# `bevaring`

**Usage**:

```console
bevaring [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--endpoint=TEXT`: The endpoint to use for the API [default: bevaring.digitalarkivet.no]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `auth`
* `datasett`
* `session`
* `version`: Prints the version

## `bevaring auth`

**Usage**:

```console
bevaring auth [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `debug-jwt`: Debug the JWT token
* `login`: Login with Azure AD
* `logout`: Logout from Azure AD

### `bevaring auth debug-jwt`

Debug the JWT token

**Usage**:

```console
bevaring auth [OPTIONS] debug-jwt
```

**Options**:

* `-y, --yes`: Do not prompt for confirmation
* `--help`: Show this message and exit.

### `bevaring auth login`

Login with Azure AD

By default this will use interactive authentication, but you can use the --device-code flag to use device code authentication,
which is suitable for when running the CLI on a machine that does not have a browser installed.

**Usage**:

```console
bevaring auth [OPTIONS] login
```

**Options**:

* `--endpoint=TEXT`: The endpoint to use for the API. You might also overwrite default with e.g. export.
* `--use-device-code`: Use device code flow, suitable for when running the CLI on a machine that does not have a browser installed.
* `--help`: Show this message and exit.

### `bevaring auth logout`

Logout from Azure AD

**Usage**:

```console
bevaring auth [OPTIONS] logout
```

**Options**:

* `--help`: Show this message and exit.

## `bevaring datasett`

**Usage**:

```console
bevaring datasett [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`
* `copies`
* `copy`
* `aws`

### `bevaring datasett list`

Prints out the list of datasetts

**Usage**:

```console
bevaring datasett list [OPTIONS]
```

**Options**:

* `--limit=INTEGER`: Max amount of datasetts to list
* `--endpoint=TEXT`: The endpoint to use for the API [default: bevaring.digitalarkivet.no]
* `--help`: Show this message and exit.

### `bevaring datasett copies`

Prints all locally stored credentials from copy operations

**Usage**:

```console
bevaring datasett copies [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `bevaring datasett copy`

Initiates copying of a chosen generation of a datasett into a target bucket. 
If the user has no bucket, a temporary bucket with credentials is created.

**Usage**:

```console
bevaring datasett copy [ARGS] [OPTIONS]
```

**Arguments**:

* `datasett_id`: Identifier of the datasett to copy

**Options**:
* `--id=TEXT`: User defined id for locally stored credentials
* `--bucket-name=TEXT`: Name of the target bucket. If not specified a temporary bucket will be created
* `--iam-access-key-id=TEXT`: IAM access key id if user has a bucket
* `--iam-secret-access-key=TEXT`: IAM secret access key if user has a bucket
* `--s3-path=TEXT`: Root-folder within bucket where the datasett should be copied
* `--generation-name=TEXT`: Which generation to copy
* `--receipt-email=TEXT`: Email address for progress notifications
* `--endpoint=TEXT`: The endpoint to use for the API [default: bevaring.digitalarkivet.no]
* `--help`: Show this message and exit.

### `bevaring datasett aws`

Prints out the locally stored credentials generated from a specific copy operation

**Usage**:

```console
bevaring datasett aws [ARGS]
```

**Arguments**:
* `id`: Id of the aws credentials to print

**Options**:

* `--help`: Show this message and exit.

## `bevaring version`

Prints the version

**Usage**:

```console
bevaring version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

