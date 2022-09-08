# zeit-on-tolino
Service to auto-upload the ZEIT 🗞 e-paper to your tolino cloud library 📚

## Why yet another zeit-on-tolino service?
I know there are a bunch of similar repos out there, but as far as I know they all depend on some additional resources
which takes care of triggering and executing the syncing mechanism. `zeit-on-tolino` solves this by using github actions.
This service uses a scheduled github actions workflow for automating the down- and upload of the e-paper, so you don't
have to worry about the runtime environment of the scripts. See usage instructions below for more details

## Usage
1. [Fork this repo](https://github.com/fgebhart/zeit-on-tolino/fork) to your own github space
2. Go to your repos settings and navigate to Actions > General > Actions permissions and enable
   "Allow all actions and reusable workflows".
3. Now navigate to the Secrets page: Settings > Security > Secrets > Actions.
4. Add the following secrets by clicking on the "New repository secret" button:
   1. `TOLINO_PARTNER_SHOP`: The name of the shop you purchased your device from (see [supported shops](https://github.com/fgebhart/zeit-on-tolino#supported-tolino-partner-shops)).
   2. `TOLINO_USER`: The username (usually an email address) you use for logging into the tolino cloud.
   3. `TOLINO_PASSWORD`: The associated password.
   4. `ZEIT_PREMIUM_USER`: Your ZEIT premium username.
   5. `ZEIT_PREMIUM_PASSWORD`: The associated password.
5. Observe that your forked repo automatically triggers the sync,
   [given the configuration of the scheduled trigger](https://github.com/fgebhart/zeit-on-tolino/blob/main/.github/workflows/sync_to_tolino_cloud.yml#L5-L7).

## Supported Tolino Partner Shops
Currently not all tolino partner shops are supported. The following shops are supported and should work out of the box:
* `thalia`
* `hugendubel`

Make sure to set the `TOLINO_PARTNER_SHOP` environment variable to one of the supported values. In case the shop
you want to use is missing, feel free to either [open an issue](https://github.com/fgebhart/zeit-on-tolino/issues/new) or
raise a PR which adds the additional shop. Check out [Contributing](https://github.com/fgebhart/zeit-on-tolino#contributing)
for more details.

## Manually Sync the Zeit E-Paper to your Tolino Cloud
In case you want to manually sync the latest zeit e-paper to your tolino cloud, follow these steps:
1. Clone the repo to your local machine via `git clone git@github.com:fgebhart/zeit-on-tolino.git` and `cd zeit-on-tolino`
2. Install the requirements via `pip install poetry` and `poetry install`
3. Export the above mentioned environment variables to your local environment
4. Run the python sync script via `python sync.py`

This script can of course also be executed in a cron-scheduled fashion on a raspberry by or similar.

## Update your fork
To benefit from recent changes in the [upstream zeit-on-tolino repo](https://github.com/fgebhart/zeit-on-tolino) use the
`Update Fork` github actions workflow. Navigate to your github actions and dispatch the workflow by manually clicking via
the github ui.

## Contributing
All kinds of contributions are welcome! 

In case you want to add a new partner shop to the list of supported shops, I recommend checking the [tolino_partner.py](https://github.com/fgebhart/zeit-on-tolino/blob/main/zeit_on_tolino/tolino_partner.py) file. This file contains the minimal required configuration
values needed for a successful login. It specifies how selenium should find the user and password fields and also the
string `shop_image_keyword`, which needs to be part of the style attribute of the image `<div>` of your shop to be
clicked on. If that does not make too much sense to you, don't worry - feel free to reach out and  I will be happy to
provide support 🙂
