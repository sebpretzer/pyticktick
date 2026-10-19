# Running the Documentation Server Locally

??? question "Have you set up your local environment?"

    Make sure your local environment is set up by following the steps in the [Setting Up the Local Environment](setup_local_environment.md) guide.

By running the documentation locally, you can create a dev server that updates itself as the documentation and code changes. This allows for better visualization of what the endstate will look like.

To run the Zensical dev server, you simply have to run:

```bash
make zensical-dev
```

This will then serve the documentation at [`http://localhost:8000/`](http://localhost:8000/).

If you make changes to any files in `docs/`, you should see the documentation refresh, it may just take a second to rebuild. Changes to the code in `src/pyticktick/` need a restart of the dev server to show up.
