# `bevaring`

**Usage**:

```console
bevaring [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--endpoint TEXT`: The endpoint to use for the API  [default: bevaring.dev.digitalarkivet.no]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `auth`
* `datasett`
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
* `logout`: Login with Azure AD

### `bevaring auth debug-jwt`

Debug the JWT token

**Usage**:

```console
bevaring auth debug-jwt [OPTIONS]
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
bevaring auth login [OPTIONS]
```

**Options**:

* `--use-device-code`: Use device code flow, suitable for when running the CLI on a machine that does not have a browser installed.
* `--help`: Show this message and exit.

### `bevaring auth logout`

Login with Azure AD

By default this will use interactive authentication, but you can use the --device-code flag to use device code authentication,
which is suitable for when running the CLI on a machine that does not have a browser installed.

**Usage**:

```console
bevaring auth logout [OPTIONS]
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

### `bevaring datasett list`

**Usage**:

```console
bevaring datasett list [OPTIONS]
```

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

