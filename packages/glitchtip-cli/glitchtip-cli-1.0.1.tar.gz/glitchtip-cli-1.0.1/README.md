# Glitchtipcli
Glitch-tip Error tracking software command-line tool in python click. 



## Prerequisites 
- Please review glitchtip [API Documentation](https://app.glitchtip.com/docs/)
- Python 3.8
- Click 
- Docker

## Features Remaining - (TODO)

- Push to PyPi
- Containerized cli tool.
- Make upstream changes to glitchtip backend to enable api token removal feature flag.
- Create a reporting feature flag
- Create a Jira integration


## Glitchtip commandline tool local setup.

- **Step 1.** Run the following commands to set up a virtual environment.

```
python3 -m venv env  # 'venv' is a module, 'env' is the target directory
source env/bin/activate
```

- **Step 2.** Install the glitchtip-cli package using pip, this will add the `gtc` command to your virtual environment.

```
pip install glitchtip-cli
```

- **Step 3.** Generate a Gltich-tip API Token from your Glitchtip instance. Login into your hosted or self hosted Glitchtip instance in the appropriate organization.

  - **Step 3.1**  **Goto** --> **Profile** --> **Auth Tokens**

  - **Step 3.2** Click `Create New Token` button and give your `Auth Token` a name and apply the appropriate permissions.

    ![alt text](images/auth_token.png "Glitchtip Auth Token")

- **Step 4.** You will be prompted for the API token and your Glitch-tip instance url the first time you run the command.

- **Example output** (output may differ due to future updates to the CLI)

```
$ gtc 
   _________ __       __    __  _     
  / ____/ (_) /______/ /_  / /_(_)___ 
 / / __/ / / __/ ___/ __ \/ __/ / __ \
/ /_/ / / / /_/ /__/ / / / /_/ / /_/ /
\____/_/_/\__/\___/_/ /_/\__/_/ .___/ 
                             /_/      

GT, Open Source Error Tracking Software! ☕ By Mark Freer

Looks like you don't have a `.env` file set up yet. Let's do it!
GlitchTip project API key: my-api-key  
GlitchTip instance url (https://glitchtip.example.net): my-gt-instance-url
Config successfully written to `.env` file.
Do you want to add `.env` to your `.gitignore` file? (y/n): y
`.gitignore` file successfully updated.

Usage: glitchtipcli.py [OPTIONS] COMMAND [ARGS]...

  A Glitch-tip Command line tool to query the Glitch-tip Error tracking
  software API.

Options:
  --help  Show this message and exit.

Commands:
  create   Create a new glitchtip organization
  delete   Delete a glitchtip organization
  list     Print the list of glitchtip organizations
  members  Print the list of a glitchtip organization's members
```

- **ASCIINEMA setup demo**
[![asciicast](https://asciinema.org/a/rNjivM0dhFkDBGUtEg09400oK.svg)](https://asciinema.org/a/rNjivM0dhFkDBGUtEg09400oK)

## Dev workflow

- TBD 

```
autopep8 --in-place --aggressive --aggressive glitchtipcli.py 

```

Please review the glitchtip contribution guideline for [Getting-started.md](https://gitlab.cee.redhat.com/cssre/cssre-docs/-/blob/main/development/howto/glitchtip/getting-started.md)
