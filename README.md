# zeit-on-tolino
Service to auto-upload the ZEIT 🗞 e-paper to your tolino cloud library 📚

## Why yet another zeit-on-tolino service?
I know there are a bunch of similar repos out there, but as far as I know they all depend on some additional resources
which takes care of triggering and executing the syncing mechanism. `zeit-on-tolino` solves this by using github actions.
This service uses a scheduled Github actions workflow for automating the down- and upload of the e-paper, so you don't
have to worry about the runtime environment of the scripts. See usage instructions below for more details

## Usage
1. [Fork this repo](https://github.com/fgebhart/zeit-on-tolino/fork) to your own github space
2. Go to your repos settings and navigate to the secrets page (Settings > Security > Secrets > Actions)
3. Add the following secrets by clicking on the "New repository secret" button:
   1. `TOLINO_PARTNER_SHOP`: The name of the shop you purchased your device from.
   2. `TOLINO_USER`: The username (usually an email address) you use for logging into the tolino cloud.
   3. `TOLINO_PASSWORD`: The associated password.
   4. `ZEIT_PREMIUM_USER`: Your ZEIT premium username.
   5. `ZEIT_PREMIUM_PASSWORD`: The associated password.
4. Observe that your forked repo automatically triggers the sync,
   [given the configuration of the scheduled trigger](https://github.com/fgebhart/zeit-on-tolino/blob/main/.github/workflows/sync_to_tolino_cloud.yml#L5-L7),
