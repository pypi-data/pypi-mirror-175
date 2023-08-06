# Network Health Check

Configurable command line application that can be used to test network conditions are as expected.

Very early work in progress version!

poetry 

Example:

```
$ poetry run netcheck check --type=dns --should-fail
Passed but was expected to fail.
{'type': 'dns', 'nameserver': None, 'host': 'github.com', 'A': ['20.248.137.48']}
```

### Individual Assertions

```
./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-fail
./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-pass
./netcheck check --type=http --method=get --url=https://s3.ap-southeast-2.amazonaws.com --should-pass
```

Output is quiet by default, json available with `--json` (TODO).

python -m netcheck.cli --help

## Configuration via file

A json file can be provided with a list of assertions to be checked:

```json
{
  "assertions": [
    {"name":  "deny-cloudflare-dns", "rules": [{"type": "dns", "server":  "1.1.1.1", "host": "github.com", "expected": "pass"}] }
  ]
}
```

And the command can be called:

$ poetry run netcheck run --config config.json 

