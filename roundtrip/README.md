# Setting up Google Cloud Translate API

Set the following environment variable:

```sh
GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'
```

Make sure that all lyrics files have a trailing newline:

```bash
for x in *; do if [ -n "$(tail -c 1 <"$x")" ]; then echo >>"$x"; fi; done
```